"""Servers CLI commands."""

import click

from ..api.servers import server_get, server_list, server_patch
from ..api.servers_gpu import gpu_driver_get
from ..exceptions import APIError, ConfigError
from ..output import print_json
from .servers_disks_cmd import disks_group
from .servers_interfaces_cmd import firewall_group, interfaces_group
from .servers_iso_cmd import iso_group
from .servers_metrics_cmd import metrics_group
from .servers_misc_cmd import (
    guest_agent_group,
    image_group,
    logs_group,
    storage_opt_group,
    user_image_group,
)
from .servers_rescue_cmd import rescue_group
from .servers_snapshots_cmd import snapshots_group


@click.group("servers", help="List and manage servers.")
def servers_group():
    pass


@servers_group.command("list", help="List servers (with optional filters).")
@click.option("--limit", type=int, help="Max number of results.")
@click.option("--offset", type=int, help="Offset for pagination.")
@click.option(
    "--firewall-policy-id",
    type=int,
    help="Filter by assigned firewall policy ID.",
)
@click.option("--ip", help="Filter by IP.")
@click.option("--name", help="Filter by server name.")
@click.option("-q", "query", help="Search in name, nickname, ipv4Addresses.")
def list_servers(
    limit: int | None,
    offset: int | None,
    firewall_policy_id: int | None,
    ip: str | None,
    name: str | None,
    query: str | None,
) -> None:
    try:
        data = server_list(
            limit=limit,
            offset=offset,
            firewall_policy_id=firewall_policy_id,
            ip=ip,
            name=name,
            q=query,
        )
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@servers_group.command(
    "gpu-driver",
    help="Get presigned GPU driver download URL (if vGPU / driver available).",
)
@click.argument("server_id", type=int)
def gpu_driver(server_id: int) -> None:
    try:
        data = gpu_driver_get(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@servers_group.command("get", help="Get one server by ID.")
@click.argument("server_id", type=int)
@click.option("--no-live", is_flag=True, help="Do not load server live info.")
def get_server(server_id: int, no_live: bool) -> None:
    try:
        data = server_get(server_id, load_server_live_info=not no_live)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@servers_group.command("power", help="Power on/off or powercycle server.")
@click.argument("server_id", type=int)
@click.argument("state", type=click.Choice(["on", "off"]), metavar="STATE")
@click.option(
    "--option",
    "state_option",
    type=click.Choice(["POWERCYCLE", "RESET", "POWEROFF"]),
    help="State option: for ON use POWERCYCLE/RESET, for OFF use POWEROFF.",
)
def power(server_id: int, state: str, state_option: str | None) -> None:
    body = {"state": state.upper()}
    try:
        result = server_patch(server_id, body, state_option=state_option)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result is not None:
        print_json(result)
    else:
        click.echo("OK")


@servers_group.command("set-hostname", help="Set server hostname.")
@click.argument("server_id", type=int)
@click.argument("hostname", type=str)
def set_hostname(server_id: int, hostname: str) -> None:
    try:
        server_patch(server_id, {"hostname": hostname})
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


@servers_group.command("set-nickname", help="Set server nickname.")
@click.argument("server_id", type=int)
@click.argument("nickname", type=str)
def set_nickname(server_id: int, nickname: str) -> None:
    try:
        server_patch(server_id, {"nickname": nickname})
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


# Register server sub-resource groups
servers_group.add_command(disks_group, "disks")
servers_group.add_command(interfaces_group, "interfaces")
servers_group.add_command(firewall_group, "firewall")
servers_group.add_command(iso_group, "iso")
servers_group.add_command(snapshots_group, "snapshots")
servers_group.add_command(rescue_group, "rescue")
servers_group.add_command(metrics_group, "metrics")
servers_group.add_command(logs_group, "logs")
servers_group.add_command(guest_agent_group, "guest-agent")
servers_group.add_command(image_group, "image")
servers_group.add_command(user_image_group, "user-image")
servers_group.add_command(storage_opt_group, "storage-optimization")
