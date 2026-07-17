"""User SSH keys API."""

from .base import get_client


def ssh_keys_list(user_id: int) -> list[dict]:
    """GET /api/v1/users/{userId}/ssh-keys."""
    client = get_client()
    resp = client.get(f"/users/{user_id}/ssh-keys")
    return resp.json()


def ssh_key_create(user_id: int, name: str, key: str) -> dict:
    """POST /api/v1/users/{userId}/ssh-keys - body: name, key (required)."""
    client = get_client()
    resp = client.post(f"/users/{user_id}/ssh-keys", json={"name": name, "key": key})
    return resp.json()


def ssh_key_delete(user_id: int, key_id: int) -> None:
    """DELETE /api/v1/users/{userId}/ssh-keys/{id}."""
    client = get_client()
    client.delete(f"/users/{user_id}/ssh-keys/{key_id}")
