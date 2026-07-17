"""Server ISO CLI."""

import click

from ..api.servers_iso import iso_attach, iso_detach, iso_get, isoimages_list
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("iso", help="Server ISO attach/detach.")
def iso_group():
    pass


@iso_group.command("get", help="Get attached ISO of a server.")
@click.argument("server_id", type=int)
def get_cmd(server_id: int) -> None:
    try:
        data = iso_get(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@iso_group.command("attach", help="Attach ISO (by isoId or userIsoName).")
@click.argument("server_id", type=int)
@click.option("--iso-id", type=int, help="ISO image ID.")
@click.option("--user-iso", "user_iso_name", help="User ISO name (key).")
@click.option("--boot-cdrom", is_flag=True, help="Change boot device to CDROM.")
def attach(server_id: int, iso_id: int | None, user_iso_name: str | None, boot_cdrom: bool) -> None:
    if not iso_id and not user_iso_name:
        click.echo(click.style("Provide --iso-id or --user-iso", fg="red"), err=True)
        raise SystemExit(1)
    body = {}
    if iso_id:
        body["isoId"] = iso_id
    if user_iso_name:
        body["userIsoName"] = user_iso_name
    body["changeBootDeviceToCdrom"] = boot_cdrom
    try:
        result = iso_attach(server_id, body)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@iso_group.command("detach", help="Detach ISO from server.")
@click.argument("server_id", type=int)
def detach(server_id: int) -> None:
    try:
        iso_detach(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


@iso_group.command("images", help="List available ISO images for server.")
@click.argument("server_id", type=int)
def images(server_id: int) -> None:
    try:
        data = isoimages_list(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)
