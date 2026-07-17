"""User and userinfo CLI commands."""

import click

from ..api.users import user_get, user_info, user_update
from ..exceptions import APIError, ConfigError
from ..output import print_json
from .users_resources_cmd import (
    failoverips_group,
    firewall_policies_group,
    ssh_keys_group,
    user_images_group,
    user_isos_group,
    user_logs_group,
)
from .users_resources_cmd import (
    vlans_group as user_vlans_group,
)


@click.group("users", help="User info and user resources.")
def users_group():
    pass


@users_group.command("info", help="Show current user (from token / userinfo).")
def info() -> None:
    try:
        data = user_info()
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@users_group.command("get", help="Get user by ID (API user resource).")
@click.argument("user_id", type=int)
def get_user(user_id: int) -> None:
    try:
        data = user_get(user_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@users_group.command("update", help="Update user (--body JSON, UserSave schema).")
@click.argument("user_id", type=int)
@click.option("--body", type=str, required=True, help="JSON body (language, timeZone required).")
def update_user(user_id: int, body: str) -> None:
    import json

    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        click.echo(click.style(f"Invalid JSON: {e}", fg="red"), err=True)
        raise SystemExit(1) from e
    try:
        result = user_update(user_id, data)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(result)


# Register user resource groups
users_group.add_command(failoverips_group, "failoverips")
users_group.add_command(firewall_policies_group, "firewall-policies")
users_group.add_command(ssh_keys_group, "ssh-keys")
users_group.add_command(user_vlans_group, "vlans")
users_group.add_command(user_images_group, "images")
users_group.add_command(user_isos_group, "isos")
users_group.add_command(user_logs_group, "logs")
