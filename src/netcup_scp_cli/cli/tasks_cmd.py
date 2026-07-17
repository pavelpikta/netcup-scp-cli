"""Tasks CLI commands."""

import click

from ..api.tasks import task_cancel, task_get, task_list
from ..exceptions import APIError, ConfigError
from ..output import print_json


@click.group("tasks", help="List and manage async tasks.")
def tasks_group():
    pass


@tasks_group.command("list", help="List tasks.")
@click.option("--limit", type=int, help="Max number of results.")
@click.option("--offset", type=int, help="Offset for pagination.")
@click.option("-q", "query", help="Search in name, uuid, server name/nickname/uuid.")
@click.option("--server-id", type=int, help="Filter by server ID.")
@click.option("--state", type=str, help="Filter by state (e.g. RUNNING, FINISHED).")
def list_tasks(
    limit: int | None,
    offset: int | None,
    query: str | None,
    server_id: int | None,
    state: str | None,
) -> None:
    try:
        data = task_list(limit=limit, offset=offset, q=query, server_id=server_id, state=state)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@tasks_group.command("get", help="Get one task by UUID.")
@click.argument("uuid", type=str)
def get_task(uuid: str) -> None:
    try:
        data = task_get(uuid)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    print_json(data)


@tasks_group.command("cancel", help="Cancel a task.")
@click.argument("uuid", type=str)
def cancel_task(uuid: str) -> None:
    try:
        result = task_cancel(uuid)
    except (APIError, ConfigError) as e:
        click.echo(click.style(str(e), fg="red"), err=True)
        raise SystemExit(1) from e
    if result is not None:
        print_json(result)
    else:
        click.echo("OK")
