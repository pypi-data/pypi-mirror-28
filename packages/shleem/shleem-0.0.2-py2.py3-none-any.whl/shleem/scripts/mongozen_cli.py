"""A command-line interface for shleem."""

import click

from .util_cli import util


@click.group(help="A command-line interface for shleem.")
def cli():
    """A command-line interface for shleem."""
    pass


cli.add_command(util)
