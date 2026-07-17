"""Server interfaces and firewall CLI."""

import click

from ..api.servers_interfaces import (
    firewall_get,
    firewall_put,
    firewall_reapply,
    firewall_restore_copied_policies,
    interface_create,
    interface_delete,
    interface_get,
    interface_update,
    interfaces_list,
)
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("interfaces", help="Server network interfaces.")
def interfaces_group():
    pass


@interfaces_group.command("list", help="List interfaces of a server.")
@click.argument("server_id", type=int)
@click.option("--no-rdns", is_flag=True, help="Do not load rDNS.")
def list_cmd(server_id: int, no_rdns: bool) -> None:
    try:
        data = interfaces_list(server_id, load_rdns=not no_rdns)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@interfaces_group.command("get", help="Get one interface by MAC.")
@click.argument("server_id", type=int)
@click.argument("mac", type=str)
@click.option("--no-rdns", is_flag=True, help="Do not load rDNS.")
def get_cmd(server_id: int, mac: str, no_rdns: bool) -> None:
    try:
        data = interface_get(server_id, mac, load_rdns=not no_rdns)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@interfaces_group.command("create", help="Create interface (attach VLAN).")
@click.argument("server_id", type=int)
@click.option("--vlan-id", type=int, required=True, help="VLAN ID.")
@click.option(
    "--driver",
    type=click.Choice(["VIRTIO", "E1000", "E1000E", "RTL8139", "VMXNET3"]),
    required=True,
    help="Network driver.",
)
def create_cmd(server_id: int, vlan_id: int, driver: str) -> None:
    try:
        result = interface_create(server_id, vlan_id, driver)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@interfaces_group.command("update", help="Update interface (--body JSON with driver etc.).")
@click.argument("server_id", type=int)
@click.argument("mac", type=str)
@click.option("--body", type=str, required=True, help='JSON body e.g. {"driver":"VIRTIO"}.')
def update_cmd(server_id: int, mac: str, body: str) -> None:
    import json

    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        click.echo(click.style(f"Invalid JSON: {e}", fg="red"), err=True)
        raise SystemExit(1) from e
    try:
        result = interface_update(server_id, mac, data)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@interfaces_group.command("delete", help="Delete interface.")
@click.argument("server_id", type=int)
@click.argument("mac", type=str)
def delete_cmd(server_id: int, mac: str) -> None:
    try:
        result = interface_delete(server_id, mac)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@click.group("firewall", help="Interface firewall (server + MAC).")
def firewall_group():
    pass


@firewall_group.command("get", help="Get firewall config for interface.")
@click.argument("server_id", type=int)
@click.argument("mac", type=str)
@click.option("--consistency-check", is_flag=True, help="Check rules applied.")
def get_fw(server_id: int, mac: str, consistency_check: bool) -> None:
    try:
        data = firewall_get(server_id, mac, consistency_check=consistency_check)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@firewall_group.command(
    "put", help="Set firewall (--body JSON: copiedPolicies, userPolicies, active)."
)
@click.argument("server_id", type=int)
@click.argument("mac", type=str)
@click.option("--body", type=str, required=True, help="JSON body.")
def put_fw(server_id: int, mac: str, body: str) -> None:
    import json

    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        click.echo(click.style(f"Invalid JSON: {e}", fg="red"), err=True)
        raise SystemExit(1) from e
    try:
        result = firewall_put(server_id, mac, data)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@firewall_group.command("reapply", help="Reapply firewall.")
@click.argument("server_id", type=int)
@click.argument("mac", type=str)
def reapply(server_id: int, mac: str) -> None:
    try:
        result = firewall_reapply(server_id, mac)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@firewall_group.command("restore-copied-policies", help="Restore copied firewall policies.")
@click.argument("server_id", type=int)
@click.argument("mac", type=str)
def restore(server_id: int, mac: str) -> None:
    try:
        result = firewall_restore_copied_policies(server_id, mac)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")
