"""Standalone VLAN get (by vlanId, no user scope)."""

import click

from ..api.user_vlans import vlan_get_by_id
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("vlans", help="VLAN by ID (standalone).")
def vlans_standalone_group():
    pass


@vlans_standalone_group.command("get", help="Get VLAN by ID.")
@click.argument("vlan_id", type=int)
def get_cmd(vlan_id: int) -> None:
    try:
        data = vlan_get_by_id(vlan_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)
