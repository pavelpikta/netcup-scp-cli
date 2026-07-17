"""Server disks CLI."""

import click

from ..api.servers_disks import (
    disk_format,
    disk_get,
    disks_list,
    disks_patch_driver,
    disks_supported_drivers,
)
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("disks", help="Server disks.")
def disks_group():
    pass


@disks_group.command("list", help="List disks of a server.")
@click.argument("server_id", type=int)
def list_cmd(server_id: int) -> None:
    try:
        data = disks_list(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@disks_group.command("get", help="Get one disk.")
@click.argument("server_id", type=int)
@click.argument("disk_name", type=str)
def get_cmd(server_id: int, disk_name: str) -> None:
    try:
        data = disk_get(server_id, disk_name)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@disks_group.command("supported-drivers", help="List supported storage drivers.")
@click.argument("server_id", type=int)
def supported_drivers(server_id: int) -> None:
    try:
        data = disks_supported_drivers(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@disks_group.command("set-driver", help="Patch disk driver (VIRTIO, VIRTIO_SCSI, IDE, SATA).")
@click.argument("server_id", type=int)
@click.argument("driver", type=click.Choice(["VIRTIO", "VIRTIO_SCSI", "IDE", "SATA"]))
def set_driver(server_id: int, driver: str) -> None:
    try:
        result = disks_patch_driver(server_id, driver)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@disks_group.command("format", help="Format a disk (data loss!).")
@click.argument("server_id", type=int)
@click.argument("disk_name", type=str)
def format_cmd(server_id: int, disk_name: str) -> None:
    try:
        result = disk_format(server_id, disk_name)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")
