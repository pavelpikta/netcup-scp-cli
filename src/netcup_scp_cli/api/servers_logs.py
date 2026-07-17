"""Server logs API."""

from typing import Any

from .base import get_client


def server_logs_list(
    server_id: int, limit: int | None = None, offset: int | None = None
) -> list[dict]:
    """GET /api/v1/servers/{serverId}/logs."""
    client = get_client()
    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    resp = client.get(f"/servers/{server_id}/logs", params=params or None)
    return resp.json()
