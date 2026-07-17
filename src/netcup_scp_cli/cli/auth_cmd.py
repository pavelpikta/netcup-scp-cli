"""Auth-related CLI commands."""

import click

from ..auth import (
    load_credentials,
    request_device_code,
    save_credentials,
    wait_for_device_authorization,
)
from ..exceptions import AuthError, ConfigError


@click.group("auth", help="Authentication: login, logout, token.")
def auth_group():
    pass


@auth_group.command("login", help="Log in via device code (opens browser).")
@click.option("--no-save", is_flag=True, help="Do not save refresh token to disk.")
def login(no_save: bool) -> None:
    device = request_device_code()
    click.echo("")
    click.echo("======================================")
    click.echo(" Open this URL in your browser:")
    click.echo(device["verification_uri_complete"])
    click.echo(f" User code: {device['user_code']}")
    click.echo("======================================")
    click.echo("")
    click.echo("Waiting for authorization…")
    try:
        tokens = wait_for_device_authorization(
            device["device_code"],
            interval=device.get("interval", 5),
            expires_in=device.get("expires_in", 600),
        )
    except AuthError as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    refresh = tokens["refresh_token"]
    access = tokens["access_token"]
    if not no_save:
        save_credentials(refresh)
        click.echo(click.style("Logged in. Refresh token saved.", fg="green"))
    else:
        click.echo(click.style("Logged in (token not saved).", fg="yellow"))
    click.echo(
        "Access token (first 20 chars): " + (access[:20] + "…") if len(access) > 20 else access
    )


@auth_group.command("logout", help="Remove stored refresh token.")
def logout() -> None:
    from ..config import credentials_path

    p = credentials_path()
    if not p.exists():
        click.echo("No stored credentials.")
        return
    p.unlink()
    click.echo("Credentials removed.")


@auth_group.command("revoke", help="Revoke current refresh token (and remove from disk).")
def revoke() -> None:
    from ..auth import revoke_refresh_token

    try:
        creds = load_credentials()
    except ConfigError as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    revoke_refresh_token(creds["refresh_token"])
    from ..config import credentials_path

    p = credentials_path()
    if p.exists():
        p.unlink()
    click.echo("Refresh token revoked and removed from disk.")


@auth_group.command("show", help="Show path of stored credentials (and whether they exist).")
def show() -> None:
    from ..config import credentials_path

    p = credentials_path()
    click.echo(p)
    if p.exists():
        click.echo("Credentials file exists.")
    else:
        click.echo("No credentials file.")
