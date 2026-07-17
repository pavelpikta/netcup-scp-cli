"""Main CLI entrypoint."""

import click

from .. import __version__
from .auth_cmd import auth_group
from .maintenance_cmd import maintenance_group
from .rdns_cmd import rdns_group
from .servers_cmd import servers_group
from .tasks_cmd import tasks_group
from .users_cmd import users_group
from .vlans_cmd import vlans_standalone_group


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="netcup CLI – netcup Server Control Panel REST API client.",
)
@click.version_option(version=__version__, prog_name="netcup")
def cli() -> None:
    pass


def _register_groups() -> None:
    cli.add_command(auth_group)
    cli.add_command(servers_group)
    cli.add_command(rdns_group)
    cli.add_command(tasks_group)
    cli.add_command(users_group)
    cli.add_command(vlans_standalone_group, "vlans")
    cli.add_command(maintenance_group)


_register_groups()


def main() -> None:
    """Entry point for console script."""
    cli()


if __name__ == "__main__":
    main()
