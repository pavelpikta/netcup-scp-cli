"""Server storage optimization API."""

from typing import Any

from .base import get_client


def storage_optimization_start(
    server_id: int,
    disks: list[str] | None = None,
    start_after_optimization: bool = False,
) -> dict | None:
    """POST /api/v1/servers/{serverId}/storageoptimization."""
    client = get_client()
    params: dict[str, Any] = {}
    if disks is not None:
        params["disks"] = disks
    params["startAfterOptimization"] = start_after_optimization
    resp = client.post(f"/servers/{server_id}/storageoptimization", params=params)
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None
