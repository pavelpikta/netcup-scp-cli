"""Shared CLI helpers."""

import click

from ..api.users import get_current_user_id


def user_id_option(f):
    """Click option that adds --user-id; default is current user from token."""
    return click.option(
        "--user-id",
        type=int,
        default=None,
        help="User ID (default: current user from token).",
    )(f)


def resolve_user_id(user_id: int | None) -> int:
    """Return user_id or current user ID from token."""
    if user_id is not None:
        return user_id
    return get_current_user_id()
