# -*- coding: utf-8 -*-
import json

from chaoslib.discovery import discover as disco
from chaostoolkit.cli import discover as chtk_discover
from chaostoolkit.cli import init as chtk_init
import click
from logzero import logger
import requests

from chaosiq.config import initialize_config, load_config, \
    CHAOISQ_CONFIG_PATH, DEFAULT_TOKEN

__all__ = ["cli"]

CHAOSIQ_API_URL = "https://api.chaosiq.io"


###############################################################################
# chaosiq CLI
###############################################################################
@click.group()
def cli():
    pass


@cli.command()
@click.option('--config-file', default=CHAOISQ_CONFIG_PATH, show_default=True,
              help='chaosiq configuration file path.')
@click.option('--force', is_flag=True, help='Force the operation.')
@click.argument('operation', type=click.Choice(["init"]))
def config(operation: str, config_file: str = CHAOISQ_CONFIG_PATH,
           force: bool = False):
    """
    Manage your chaosiq configuration
    """
    if operation == "init":
        initialize_config(config_file, force)


###############################################################################
# chaostoolkit CLI overloading
###############################################################################
@click.command(help=chtk_discover.__doc__)
@click.option('--no-system-info', is_flag=True,
              help='Do not discover system information.')
@click.option('--no-install', is_flag=True,
              help='Assume package already in PYTHONPATH.')
@click.option('--discovery-report-path', default="./discovery.json",
              help='Path where to save the report from the discovery.',
              show_default=True)
@click.argument('package')
@click.pass_context
def discover(ctx: click.Context, package: str,
             discovery_report_path: str = "./discovery.json",
             no_system_info: bool = False, no_install: bool = False,
             config_file: str = CHAOISQ_CONFIG_PATH):
    config = load_config(click.format_filename(config_file))
    if not config:
        raise click.ClickException("Your chaosiq configuration looks empty. "
                                   "Run `chaosiq config init` to initialize a "
                                   "default one.")

    token = config.get("auth", {}).get("token")
    if not token:
        raise click.ClickException("Missing chaosiq token, please ensure you "
                                   "have it in your configuration file "
                                   "({c}).".format(c=config_file))

    if token == DEFAULT_TOKEN:
        raise click.ClickException("It seems you have not set your token yet "
                                   "in the configuration. Please set one "
                                   "before continuing.")

    # invoking actual chaostoolkit parent discovery function
    discovery = disco(
        package_name=package, discover_system=not no_system_info,
        download_and_install=not no_install)

    logger.info("Calling chaosiq to fetch potential experiments")
    url = "{u}/v1/suggest".format(u=CHAOSIQ_API_URL)
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {t}".format(t=token),
        "Connection": "close"
    }

    try:
        r = requests.post(
            url, json=discovery, headers=headers, timeout=(2, 30))
    except requests.ConnectTimeout as c:
        logger.warn(
            "Failed to contact the ChaosIQ API service. Try again soon!")
    except requests.ConnectionError as e:
        logger.warn(
            "The ChaosIQ API service looks busy. Try again soon!")
    except requests.ReadTimeout as t:
        logger.warn(
            "The ChaosIQ API service took long to respond. Try again soon!")
    except requests.HTTPError as x:
        logger.debug(str(x))
        logger.error(
            "Something went wrong. Please contact ChaosIQ.")
    else:
        if r.status_code != 200:
            logger.warn("failed to fetch experiment suggestions from chaosiq.")
            logger.debug(r.text)
        else:
            discovery = r.json()
            logger.info(
                "{d} experiment suggestions were found".format(
                    d=len(discovery.get("experiments", []))))

    with open(discovery_report_path, "w") as d:
        d.write(json.dumps(discovery, indent=2))

    logger.info("Discovery report saved in {p}".format(
        p=discovery_report_path))

    return discovery


@click.command(help=chtk_init.__doc__)
@click.option('--discovery-report-path', default="./discovery.json",
              help='Path where to save the report from the discovery.',
              show_default=True, type=click.Path(exists=True))
@click.option('--experiment-path', default="./experiment.json",
              help='Path where to save the experiment.',
              show_default=True)
@click.pass_context
def init(ctx, discovery_report_path: str = "./discovery.json",
         experiment_path: str = "./experiment.json"):
    choice = click.prompt(
        click.style(
            "Use 'chaosiq' init feature or the chaostoolkit 'default'",
            fg='green'),
        default="chaosiq", show_default=True,
        type=click.Choice(['default', 'chaosiq']))

    if choice == "default":
        ctx.forward(chtk_init)
        return

    discovery = None
    with open(discovery_report_path) as d:
        discovery = json.loads(d.read())

    if not discovery or not discovery.get("experiments"):
        click.ClickException("No experiments found in this discovery report")

    experiments = []
    for experiment in discovery["experiments"]:
        experiments.append((
            experiment["title"],
            experiment
        ))

    echo = click.echo
    if len(experiments) > 10:
        echo = click.echo_via_pager
    echo("\n".join([
        "{i}) {t}".format(i=idx, t=title) for (idx, (title, exp)) in enumerate(
            experiments)]))
    index = click.prompt(
        click.style('Please select an experiment', fg='green'), type=int)
    logger.info("You have selected experiment: '{t}'".format(
        t=experiments[index][0]))

    logger.info("Saving to '{e}'".format(e=experiment_path))
    with open(experiment_path, "w") as e:
        e.write(json.dumps(experiments[index][1], indent=4))

    logger.info("You may now run this experiment with `chaos run {e}`".format(
        e=experiment_path))
