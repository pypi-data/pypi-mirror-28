from os import system

from tox import hookimpl


@hookimpl
def tox_configure(config):
    for env in config.envlist:
        for cmd in config.envconfigs[env]._reader.getlist("run_before"):
            system(cmd)
