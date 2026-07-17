"""Server snapshots API."""

from .base import get_client


def snapshots_list(server_id: int) -> list[dict]:
    """GET /api/v1/servers/{serverId}/snapshots."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/snapshots")
    return resp.json()


def snapshot_get(server_id: int, name: str) -> dict:
    """GET /api/v1/servers/{serverId}/snapshots/{name}."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/snapshots/{name}")
    return resp.json()


def snapshot_create(server_id: int, body: dict) -> dict | None:
    """POST /api/v1/servers/{serverId}/snapshots - body: name, optional
    description, diskName, onlineSnapshot."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/snapshots", json=body)
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def snapshot_delete(server_id: int, name: str) -> dict | None:
    """DELETE /api/v1/servers/{serverId}/snapshots/{name}."""
    client = get_client()
    resp = client.delete(f"/servers/{server_id}/snapshots/{name}")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def snapshot_export(server_id: int, name: str) -> dict | None:
    """POST /api/v1/servers/{serverId}/snapshots/{name}/export."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/snapshots/{name}/export")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def snapshot_revert(server_id: int, name: str) -> dict | None:
    """POST /api/v1/servers/{serverId}/snapshots/{name}/revert."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/snapshots/{name}/revert")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def snapshots_dryrun(server_id: int, body: dict) -> list[dict]:
    """POST /api/v1/servers/{serverId}/snapshots:dryrun - Check if snapshot creation is possible."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/snapshots:dryrun", json=body)
    return resp.json()
