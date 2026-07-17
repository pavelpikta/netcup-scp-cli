"""Server disks API."""

from .base import get_client


def disks_list(server_id: int) -> list[dict]:
    """GET /api/v1/servers/{serverId}/disks."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/disks")
    return resp.json()


def disk_get(server_id: int, disk_name: str) -> dict:
    """GET /api/v1/servers/{serverId}/disks/{diskName}."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/disks/{disk_name}")
    return resp.json()


def disks_supported_drivers(server_id: int) -> list[dict]:
    """GET /api/v1/servers/{serverId}/disks/supported-drivers."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/disks/supported-drivers")
    return resp.json()


def disks_patch_driver(server_id: int, driver: str) -> dict | None:
    """PATCH /api/v1/servers/{serverId}/disks - Update disk driver."""
    client = get_client()
    resp = client.patch(f"/servers/{server_id}/disks", json={"driver": driver})
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def disk_format(server_id: int, disk_name: str) -> dict | None:
    """POST /api/v1/servers/{serverId}/disks/{diskName}:format."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/disks/{disk_name}:format")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None
