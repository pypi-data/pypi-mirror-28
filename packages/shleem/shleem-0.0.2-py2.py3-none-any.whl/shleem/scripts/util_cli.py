"""A simple command-line tool for shleem."""

import pprint

import click

from shleem.param_inference_maps import rebuild_all_maps
from shleem.collection_cfg import rebuild_collection_cfg_files
from shleem.shared import _shleem_cfg


@click.group(help="Utility shleem operations.")
def util():
    """Utility shleem operations."""
    pass


@util.command(help="Rebuild parameter inference maps.")
def rebuildmaps():
    """Rebuild parameter inference maps."""
    rebuild_all_maps()


@util.command(help="Rebuild collection attributes.")
def rebuildattr():
    """Rebuild collection attributes."""
    rebuild_collection_cfg_files()


@util.command(help="Print shleem's current configuration.")
def printcfg():
    """Print shleem's current configuration."""
    pprint.pprint(_shleem_cfg(), indent=1, width=10)
