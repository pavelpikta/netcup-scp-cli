"""Server snapshots CLI."""

import click

from ..api.servers_snapshots import (
    snapshot_create,
    snapshot_delete,
    snapshot_export,
    snapshot_get,
    snapshot_revert,
    snapshots_dryrun,
    snapshots_list,
)
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("snapshots", help="Server snapshots.")
def snapshots_group():
    pass


@snapshots_group.command("list", help="List snapshots of a server.")
@click.argument("server_id", type=int)
def list_cmd(server_id: int) -> None:
    try:
        data = snapshots_list(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@snapshots_group.command("get", help="Get one snapshot.")
@click.argument("server_id", type=int)
@click.argument("name", type=str)
def get_cmd(server_id: int, name: str) -> None:
    try:
        data = snapshot_get(server_id, name)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@snapshots_group.command("create", help="Create snapshot.")
@click.argument("server_id", type=int)
@click.option("--name", required=True, help="Snapshot name.")
@click.option("--description", help="Description.")
@click.option("--disk-name", help="Disk name.")
@click.option("--online", "online_snapshot", is_flag=True, help="Online snapshot.")
def create_cmd(
    server_id: int,
    name: str,
    description: str | None,
    disk_name: str | None,
    online_snapshot: bool,
) -> None:
    body = {"name": name}
    if description:
        body["description"] = description
    if disk_name:
        body["diskName"] = disk_name
    body["onlineSnapshot"] = online_snapshot
    try:
        result = snapshot_create(server_id, body)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@snapshots_group.command("delete", help="Delete snapshot.")
@click.argument("server_id", type=int)
@click.argument("name", type=str)
def delete_cmd(server_id: int, name: str) -> None:
    try:
        result = snapshot_delete(server_id, name)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@snapshots_group.command("export", help="Export snapshot.")
@click.argument("server_id", type=int)
@click.argument("name", type=str)
def export_cmd(server_id: int, name: str) -> None:
    try:
        result = snapshot_export(server_id, name)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@snapshots_group.command("revert", help="Revert to snapshot.")
@click.argument("server_id", type=int)
@click.argument("name", type=str)
def revert_cmd(server_id: int, name: str) -> None:
    try:
        result = snapshot_revert(server_id, name)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@snapshots_group.command("dryrun", help="Check if snapshot creation is possible.")
@click.argument("server_id", type=int)
@click.option("--disk-name", help="Disk name.")
@click.option("--online", "online_snapshot", is_flag=True, help="Online snapshot.")
def dryrun_cmd(server_id: int, disk_name: str | None, online_snapshot: bool) -> None:
    body = {"onlineSnapshot": online_snapshot}
    if disk_name:
        body["diskName"] = disk_name
    try:
        data = snapshots_dryrun(server_id, body)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)
