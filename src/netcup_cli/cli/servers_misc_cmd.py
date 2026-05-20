"""Server logs, guest-agent, image, user-image, storage-optimization CLI."""

import click

from ..api.servers_guest import guest_agent_get, guest_agent_status_get
from ..api.servers_image import image_setup, imageflavours_list, user_image_setup
from ..api.servers_logs import server_logs_list
from ..api.servers_storage import storage_optimization_start
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("logs", help="Server logs.")
def logs_group():
    pass


@logs_group.command("list", help="List server logs.")
@click.argument("server_id", type=int)
@click.option("--limit", type=int, help="Max results.")
@click.option("--offset", type=int, help="Offset.")
def list_cmd(server_id: int, limit: int | None, offset: int | None) -> None:
    try:
        data = server_logs_list(server_id, limit=limit, offset=offset)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@click.group("guest-agent", help="Guest agent data.")
def guest_agent_group():
    pass


@guest_agent_group.command("get", help="Get guest agent data.")
@click.argument("server_id", type=int)
def get_cmd(server_id: int) -> None:
    try:
        data = guest_agent_get(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@guest_agent_group.command("status", help="Get guest agent status.")
@click.argument("server_id", type=int)
def guest_agent_status_cmd(server_id: int) -> None:
    try:
        data = guest_agent_status_get(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@click.group("image", help="Server image setup.")
def image_group():
    pass


@image_group.command("flavours", help="List image flavours for server.")
@click.argument("server_id", type=int)
def flavours(server_id: int) -> None:
    try:
        data = imageflavours_list(server_id)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@image_group.command("setup", help="Setup image (use --body JSON or key=val).")
@click.argument("server_id", type=int)
@click.option("--body", type=str, help='JSON body (e.g. {"imageFlavourId":1,"diskName":"vda"}).')
def setup(server_id: int, body: str | None) -> None:
    import json

    if not body:
        click.echo(click.style("Provide --body with JSON", fg="red"), err=True)
        raise SystemExit(1)
    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        click.echo(click.style(f"Invalid JSON: {e}", fg="red"), err=True)
        raise SystemExit(1) from e
    try:
        result = image_setup(server_id, data)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@click.group("user-image", help="Setup user image.")
def user_image_group():
    pass


@user_image_group.command("setup", help="Setup user image.")
@click.argument("server_id", type=int)
@click.option("--name", "user_image_name", required=True, help="User image name.")
@click.option("--disk-name", help="Disk name.")
@click.option("--email-notification", is_flag=True, help="Send email when done.")
def setup_cmd(
    server_id: int, user_image_name: str, disk_name: str | None, email_notification: bool
) -> None:
    body = {"userImageName": user_image_name}
    if disk_name:
        body["diskName"] = disk_name
    body["emailNotification"] = email_notification
    try:
        result = user_image_setup(server_id, body)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")


@click.group("storage-optimization", help="Storage optimization.")
def storage_opt_group():
    pass


@storage_opt_group.command("start", help="Start storage optimization.")
@click.argument("server_id", type=int)
@click.option("--disks", multiple=True, help="Disk name(s) (repeat for multiple).")
@click.option(
    "--start-after",
    "start_after_optimization",
    is_flag=True,
    help="Start server after optimization.",
)
def start(server_id: int, disks: tuple[str, ...], start_after_optimization: bool) -> None:
    disk_list = list(disks) if disks else None
    try:
        result = storage_optimization_start(
            server_id,
            disks=disk_list,
            start_after_optimization=start_after_optimization,
        )
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result:
        print_json(result)
    else:
        click.echo("OK")
