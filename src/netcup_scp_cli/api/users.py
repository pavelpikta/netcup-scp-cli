"""User and userinfo API."""

import requests

from ..auth import get_access_token
from ..config import BASE_URL
from .base import get_client


def user_info() -> dict:
    """OpenID Connect userinfo - get current user id and profile."""
    token = get_access_token()
    resp = requests.get(
        f"{BASE_URL}/realms/scp/protocol/openid-connect/userinfo",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def user_get(user_id: int) -> dict:
    """GET /api/v1/users/{userId} - Get one user (by id)."""
    client = get_client()
    resp = client.get(f"/users/{user_id}")
    return resp.json()


def user_update(user_id: int, body: dict) -> dict:
    """PUT /api/v1/users/{userId} - Update user (UserSave schema)."""
    client = get_client()
    resp = client.put(f"/users/{user_id}", json=body)
    return resp.json()


def get_current_user_id() -> int:
    """Return current user ID from userinfo (for commands that need userId)."""
    return int(user_info()["id"])
