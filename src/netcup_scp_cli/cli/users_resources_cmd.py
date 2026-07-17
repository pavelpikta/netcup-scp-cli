"""User resources CLI: failoverips, firewall-policies, ssh-keys, vlans, images, isos, logs."""

import click

from ..api.s3_upload import DEFAULT_PART_SIZE
from ..api.user_failoverips import (
    failoverips_v4_list,
    failoverips_v4_route,
    failoverips_v6_list,
    failoverips_v6_route,
)
from ..api.user_firewall_policies import (
    firewall_policies_list,
    firewall_policy_create,
    firewall_policy_delete,
    firewall_policy_get,
    firewall_policy_update,
)
from ..api.user_images import (
    user_image_delete,
    user_image_download_url,
    user_image_upload,
    user_images_list,
)
from ..api.user_isos import (
    user_iso_delete,
    user_iso_download_url,
    user_iso_upload,
    user_isos_list,
)
from ..api.user_logs import user_logs_list
from ..api.user_ssh_keys import ssh_key_create, ssh_key_delete, ssh_keys_list
from ..api.user_vlans import vlan_get, vlan_update, vlans_list
from ..exceptions import APIError, ConfigError
from ..output import print_json
from .helpers import resolve_user_id, user_id_option


# ---- Failover IPs ----
@click.group("failoverips", help="Failover IPv4/IPv6.")
def failoverips_group():
    pass


@failoverips_group.group("v4", help="Failover IPv4.")
def v4_group():
    pass


@v4_group.command("list", help="List failover IPv4s.")
@user_id_option
@click.option("--ip", help="Filter by IP.")
@click.option("--server-id", type=int, help="Filter by server.")
def v4_list(user_id: int | None, ip: str | None, server_id: int | None) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = failoverips_v4_list(uid, ip=ip, server_id=server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@v4_group.command("route", help="Route failover IPv4 to server.")
@user_id_option
@click.argument("id", type=int)
@click.argument("server_id", type=int)
def v4_route(user_id: int | None, id: int, server_id: int) -> None:
    uid = resolve_user_id(user_id)
    try:
        result = failoverips_v4_route(uid, id, server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@failoverips_group.group("v6", help="Failover IPv6.")
def v6_group():
    pass


@v6_group.command("list", help="List failover IPv6s.")
@user_id_option
@click.option("--ip", help="Filter by IP.")
@click.option("--server-id", type=int, help="Filter by server.")
def v6_list(user_id: int | None, ip: str | None, server_id: int | None) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = failoverips_v6_list(uid, ip=ip, server_id=server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@v6_group.command("route", help="Route failover IPv6 to server.")
@user_id_option
@click.argument("id", type=int)
@click.argument("server_id", type=int)
def v6_route(user_id: int | None, id: int, server_id: int) -> None:
    uid = resolve_user_id(user_id)
    try:
        result = failoverips_v6_route(uid, id, server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


# ---- Firewall policies ----
@click.group("firewall-policies", help="User firewall policies.")
def firewall_policies_group():
    pass


@firewall_policies_group.command("list", help="List firewall policies.")
@user_id_option
@click.option("--limit", type=int)
@click.option("--offset", type=int)
@click.option("-q", "query", help="Search by name or description.")
def fp_list(user_id: int | None, limit: int | None, offset: int | None, query: str | None) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = firewall_policies_list(uid, limit=limit, offset=offset, q=query)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@firewall_policies_group.command("get", help="Get firewall policy.")
@user_id_option
@click.argument("policy_id", type=int)
@click.option("--with-servers-count", is_flag=True, help="Include count of affected servers.")
def fp_get(user_id: int | None, policy_id: int, with_servers_count: bool) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = firewall_policy_get(
            uid, policy_id, with_count_of_affected_servers=with_servers_count
        )
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@firewall_policies_group.command("create", help="Create firewall policy (--body JSON).")
@user_id_option
@click.option("--body", type=str, required=True, help="JSON: name, description?, rules[].")
def fp_create(user_id: int | None, body: str) -> None:
    import json

    uid = resolve_user_id(user_id)
    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        click.echo(click.style(f"Invalid JSON: {e}", fg="red"), err=True)
        raise SystemExit(1) from e
    try:
        result = firewall_policy_create(uid, data)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(result)


@firewall_policies_group.command("update", help="Update firewall policy (--body JSON).")
@user_id_option
@click.argument("policy_id", type=int)
@click.option("--body", type=str, required=True)
def fp_update(user_id: int | None, policy_id: int, body: str) -> None:
    import json

    uid = resolve_user_id(user_id)
    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        click.echo(click.style(f"Invalid JSON: {e}", fg="red"), err=True)
        raise SystemExit(1) from e
    try:
        result = firewall_policy_update(uid, policy_id, data)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@firewall_policies_group.command("delete", help="Delete firewall policy.")
@user_id_option
@click.argument("policy_id", type=int)
def fp_delete(user_id: int | None, policy_id: int) -> None:
    uid = resolve_user_id(user_id)
    try:
        firewall_policy_delete(uid, policy_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


# ---- SSH keys ----
@click.group("ssh-keys", help="SSH keys.")
def ssh_keys_group():
    pass


@ssh_keys_group.command("list", help="List SSH keys.")
@user_id_option
def sk_list(user_id: int | None) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = ssh_keys_list(uid)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@ssh_keys_group.command("add", help="Add SSH key.")
@user_id_option
@click.option("--name", required=True)
@click.option("--key", required=True, help="Public key content.")
def sk_add(user_id: int | None, name: str, key: str) -> None:
    uid = resolve_user_id(user_id)
    try:
        result = ssh_key_create(uid, name, key)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(result)


@ssh_keys_group.command("delete", help="Delete SSH key.")
@user_id_option
@click.argument("key_id", type=int)
def sk_delete(user_id: int | None, key_id: int) -> None:
    uid = resolve_user_id(user_id)
    try:
        ssh_key_delete(uid, key_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


# ---- VLANs ----
@click.group("vlans", help="User VLANs.")
def vlans_group():
    pass


@vlans_group.command("list", help="List VLANs.")
@user_id_option
@click.option("--server-id", type=int, help="Filter by server.")
def vlans_list_cmd(user_id: int | None, server_id: int | None) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = vlans_list(uid, server_id=server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@vlans_group.command("get", help="Get VLAN.")
@user_id_option
@click.argument("vlan_id", type=int)
def vlans_get_cmd(user_id: int | None, vlan_id: int) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = vlan_get(uid, vlan_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@vlans_group.command("update", help="Update VLAN name.")
@user_id_option
@click.argument("vlan_id", type=int)
@click.argument("name", type=str)
def vlans_update_cmd(user_id: int | None, vlan_id: int, name: str) -> None:
    uid = resolve_user_id(user_id)
    try:
        vlan_update(uid, vlan_id, name)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


# ---- User images ----
@click.group("images", help="User images (S3).")
def user_images_group():
    pass


@user_images_group.command("list", help="List user images.")
@user_id_option
def ui_list(user_id: int | None) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = user_images_list(uid)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@user_images_group.command("delete", help="Delete user image.")
@user_id_option
@click.argument("key", type=str)
def ui_delete(user_id: int | None, key: str) -> None:
    uid = resolve_user_id(user_id)
    try:
        user_image_delete(uid, key)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


@user_images_group.command("download-url", help="Get presigned download URL.")
@user_id_option
@click.argument("key", type=str)
def ui_download_url(user_id: int | None, key: str) -> None:
    uid = resolve_user_id(user_id)
    try:
        url = user_image_download_url(uid, key)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if isinstance(url, str):
        click.echo(url)
    else:
        print_json(url)


@user_images_group.command("upload", help="Upload a local file as a user image.")
@user_id_option
@click.argument("key", type=str)
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=str))
@click.option(
    "--part-size",
    type=int,
    default=DEFAULT_PART_SIZE,
    show_default=True,
    help="Multipart chunk size in bytes.",
)
@click.option(
    "--multipart/--no-multipart",
    default=None,
    help="Force S3 multipart or single-shot; default auto (multipart if file > part-size).",
)
def ui_upload(
    user_id: int | None,
    key: str,
    path: str,
    part_size: int,
    multipart: bool | None,
) -> None:
    uid = resolve_user_id(user_id)

    def on_progress(done: int, total: int) -> None:
        if total:
            click.echo(f"\rUploaded {done}/{total} bytes", nl=False, err=True)
        else:
            click.echo("\rUploaded empty file", nl=False, err=True)

    try:
        user_image_upload(
            uid,
            key,
            path,
            part_size=part_size,
            use_multipart=multipart,
            on_progress=on_progress,
        )
    except (APIError, ConfigError, FileNotFoundError, ValueError, OSError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("", err=True)
    click.echo("OK")


# ---- User ISOs ----
@click.group("isos", help="User ISOs (S3).")
def user_isos_group():
    pass


@user_isos_group.command("list", help="List user ISOs.")
@user_id_option
def uiso_list(user_id: int | None) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = user_isos_list(uid)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@user_isos_group.command("delete", help="Delete user ISO.")
@user_id_option
@click.argument("key", type=str)
def uiso_delete(user_id: int | None, key: str) -> None:
    uid = resolve_user_id(user_id)
    try:
        user_iso_delete(uid, key)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("OK")


@user_isos_group.command("download-url", help="Get presigned download URL.")
@user_id_option
@click.argument("key", type=str)
def uiso_download_url(user_id: int | None, key: str) -> None:
    uid = resolve_user_id(user_id)
    try:
        url = user_iso_download_url(uid, key)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if isinstance(url, str):
        click.echo(url)
    else:
        print_json(url)


@user_isos_group.command("upload", help="Upload a local file as a user ISO.")
@user_id_option
@click.argument("key", type=str)
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=str))
@click.option(
    "--part-size",
    type=int,
    default=DEFAULT_PART_SIZE,
    show_default=True,
    help="Multipart chunk size in bytes.",
)
@click.option(
    "--multipart/--no-multipart",
    default=None,
    help="Force S3 multipart or single-shot; default auto (multipart if file > part-size).",
)
def uiso_upload(
    user_id: int | None,
    key: str,
    path: str,
    part_size: int,
    multipart: bool | None,
) -> None:
    uid = resolve_user_id(user_id)

    def on_progress(done: int, total: int) -> None:
        if total:
            click.echo(f"\rUploaded {done}/{total} bytes", nl=False, err=True)
        else:
            click.echo("\rUploaded empty file", nl=False, err=True)

    try:
        user_iso_upload(
            uid,
            key,
            path,
            part_size=part_size,
            use_multipart=multipart,
            on_progress=on_progress,
        )
    except (APIError, ConfigError, FileNotFoundError, ValueError, OSError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    click.echo("", err=True)
    click.echo("OK")


# ---- User logs ----
@click.group("logs", help="User logs.")
def user_logs_group():
    pass


@user_logs_group.command("list", help="List user logs.")
@user_id_option
@click.option("--limit", type=int)
@click.option("--offset", type=int)
def ul_list(user_id: int | None, limit: int | None, offset: int | None) -> None:
    uid = resolve_user_id(user_id)
    try:
        data = user_logs_list(uid, limit=limit, offset=offset)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)
