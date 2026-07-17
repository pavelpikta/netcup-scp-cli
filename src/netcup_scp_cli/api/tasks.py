"""Tasks API."""

from typing import Any

from .base import get_client


def task_list(
    limit: int | None = None,
    offset: int | None = None,
    q: str | None = None,
    server_id: int | None = None,
    state: str | None = None,
) -> list[dict]:
    """GET /api/v1/tasks - List tasks."""
    client = get_client()
    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if q:
        params["q"] = q
    if server_id is not None:
        params["serverId"] = server_id
    if state:
        params["state"] = state
    resp = client.get("/tasks", params=params or None)
    return resp.json()


def task_get(uuid: str) -> dict:
    """GET /api/v1/tasks/{uuid} - Get one task."""
    client = get_client()
    resp = client.get(f"/tasks/{uuid}")
    return resp.json()


def task_cancel(uuid: str) -> dict | None:
    """PUT /api/v1/tasks/{uuid}:cancel - Cancel task."""
    client = get_client()
    resp = client.put(f"/tasks/{uuid}:cancel")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None
