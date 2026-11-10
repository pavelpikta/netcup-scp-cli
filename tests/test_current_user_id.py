"""Tests for get_current_user_id error handling."""

from unittest.mock import patch

import pytest

from netcup_scp_cli.api.users import get_current_user_id
from netcup_scp_cli.exceptions import AuthError


def test_current_user_id_missing_id_raises_auth_error() -> None:
    with patch("netcup_scp_cli.api.users.user_info", return_value={}):
        with pytest.raises(AuthError):
            get_current_user_id()


def test_current_user_id_returns_id() -> None:
    with patch("netcup_scp_cli.api.users.user_info", return_value={"id": "42"}):
        assert get_current_user_id() == 42
