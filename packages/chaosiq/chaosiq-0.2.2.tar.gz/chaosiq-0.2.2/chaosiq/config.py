# -*- coding: utf-8 -*-
import os
import os.path

import yaml

from chaosiq.types import Configuration

__all__ = ["initialize_config", "load_config", "CHAOISQ_CONFIG_PATH",
           "DEFAULT_TOKEN"]

CHAOISQ_CONFIG_PATH = os.path.abspath(os.path.expanduser("~/.chaosiq/config"))
DEFAULT_TOKEN = "<YOUR TOKEN>"
DEFAULT_CONFIG = {
    "auth": {
        "token": DEFAULT_TOKEN
    }
}


def load_config(config_path: str = CHAOISQ_CONFIG_PATH) -> Configuration:
    """
    Load the chaosiq configuration into memory. Returns `None` when the config
    file doesn't exist.
    """
    if not os.path.exists(config_path):
        return

    with open(config_path) as f:
        return yaml.load(f.read())


def initialize_config(config_path: str = CHAOISQ_CONFIG_PATH,
                      force: bool = False):
    """
    Initialize a default configuration on disk. If the cconfiguration already
    exists, it is left untouched, unless the `force` parameter is set to
    `True`.

    The configuration is set to be read and written only by the current user.
    """
    if os.path.exists(config_path) and not force:
        return

    try:
        os.mkdir(os.path.dirname(config_path))
    except FileExistsError:
        pass

    with open(config_path, "w") as f:
        os.chmod(config_path, 0o600)
        f.write(yaml.dump(DEFAULT_CONFIG, default_flow_style=False))
