"""Server metrics CLI."""

import click

from ..api.servers_metrics import metrics_cpu, metrics_disk, metrics_network, metrics_network_packet
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("metrics", help="Server metrics.")
def metrics_group():
    pass


@metrics_group.command("cpu", help="Get CPU metrics.")
@click.argument("server_id", type=int)
@click.option("--hours", type=int, help="Time range in hours.")
def cpu(server_id: int, hours: int | None) -> None:
    try:
        data = metrics_cpu(server_id, hours=hours)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@metrics_group.command("disk", help="Get disk metrics.")
@click.argument("server_id", type=int)
@click.option("--hours", type=int, help="Time range in hours.")
def disk(server_id: int, hours: int | None) -> None:
    try:
        data = metrics_disk(server_id, hours=hours)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@metrics_group.command("network", help="Get network metrics.")
@click.argument("server_id", type=int)
@click.option("--hours", type=int, help="Time range in hours.")
def network(server_id: int, hours: int | None) -> None:
    try:
        data = metrics_network(server_id, hours=hours)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@metrics_group.command("packet", help="Get network packet metrics.")
@click.argument("server_id", type=int)
@click.option("--hours", type=int, help="Time range in hours.")
def packet(server_id: int, hours: int | None) -> None:
    try:
        data = metrics_network_packet(server_id, hours=hours)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)
