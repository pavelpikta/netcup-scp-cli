"""Server rescue system CLI."""

import click

from ..api.servers_rescue import rescuesystem_activate, rescuesystem_deactivate, rescuesystem_get
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("rescue", help="Server rescue system.")
def rescue_group():
    pass


@rescue_group.command("get", help="Get rescue system status.")
@click.argument("server_id", type=int)
def get_cmd(server_id: int) -> None:
    try:
        data = rescuesystem_get(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@rescue_group.command("activate", help="Activate rescue system.")
@click.argument("server_id", type=int)
def activate(server_id: int) -> None:
    try:
        result = rescuesystem_activate(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@rescue_group.command("deactivate", help="Deactivate rescue system.")
@click.argument("server_id", type=int)
def deactivate(server_id: int) -> None:
    try:
        result = rescuesystem_deactivate(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")
