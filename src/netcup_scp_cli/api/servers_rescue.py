"""Server rescue system API."""

from .base import get_client


def rescuesystem_get(server_id: int) -> dict:
    """GET /api/v1/servers/{serverId}/rescuesystem."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/rescuesystem")
    return resp.json()


def rescuesystem_activate(server_id: int) -> dict | None:
    """POST /api/v1/servers/{serverId}/rescuesystem."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/rescuesystem")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def rescuesystem_deactivate(server_id: int) -> dict | None:
    """DELETE /api/v1/servers/{serverId}/rescuesystem."""
    client = get_client()
    resp = client.delete(f"/servers/{server_id}/rescuesystem")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None
