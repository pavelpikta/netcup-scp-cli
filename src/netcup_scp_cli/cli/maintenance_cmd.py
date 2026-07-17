"""Maintenance and ping CLI commands."""

import click

from ..api.maintenance import get_maintenance, ping
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("maintenance", help="Maintenance info and API ping.")
def maintenance_group():
    pass


@maintenance_group.command("ping", help="Check if SCP API is available.")
def ping_cmd() -> None:
    try:
        result = ping()
    except Exception as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo(result)


@maintenance_group.command("info", help="Get maintenance window information.")
def info() -> None:
    try:
        data = get_maintenance()
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)
