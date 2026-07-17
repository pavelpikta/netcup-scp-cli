"""rDNS CLI commands."""

import click

from ..api.rdns import (
    rdns_delete_ipv4,
    rdns_delete_ipv6,
    rdns_get_ipv4,
    rdns_get_ipv6,
    rdns_set_ipv4,
    rdns_set_ipv6,
)
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("rdns", help="Get/set/delete rDNS for IPv4 or IPv6.")
def rdns_group():
    pass


@rdns_group.group("ipv4", help="rDNS for IPv4.")
def rdns_ipv4():
    pass


@rdns_ipv4.command("get", help="Get rDNS for an IPv4 address.")
@click.argument("ip", type=str)
def get_ipv4(ip: str) -> None:
    try:
        data = rdns_get_ipv4(ip)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@rdns_ipv4.command("set", help="Set rDNS for an IPv4 address.")
@click.argument("ip", type=str)
@click.argument("rdns", type=str)
def set_ipv4(ip: str, rdns: str) -> None:
    try:
        rdns_set_ipv4(ip, rdns)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


@rdns_ipv4.command("delete", help="Delete rDNS for an IPv4 address.")
@click.argument("ip", type=str)
def delete_ipv4(ip: str) -> None:
    try:
        rdns_delete_ipv4(ip)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


@rdns_group.group("ipv6", help="rDNS for IPv6.")
def rdns_ipv6():
    pass


@rdns_ipv6.command("get", help="Get rDNS for an IPv6 address.")
@click.argument("ip", type=str)
def get_ipv6(ip: str) -> None:
    try:
        data = rdns_get_ipv6(ip)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@rdns_ipv6.command("set", help="Set rDNS for an IPv6 address.")
@click.argument("ip", type=str)
@click.argument("rdns", type=str)
def set_ipv6(ip: str, rdns: str) -> None:
    try:
        rdns_set_ipv6(ip, rdns)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


@rdns_ipv6.command("delete", help="Delete rDNS for an IPv6 address.")
@click.argument("ip", type=str)
def delete_ipv6(ip: str) -> None:
    try:
        rdns_delete_ipv6(ip)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")
