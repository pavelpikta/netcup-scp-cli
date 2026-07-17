"""Server ISO attach/detach and ISO images list API."""

from .base import get_client


def iso_get(server_id: int) -> dict:
    """GET /api/v1/servers/{serverId}/iso - Get attached ISO."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/iso")
    return resp.json()


def iso_attach(server_id: int, body: dict) -> dict | None:
    """POST /api/v1/servers/{serverId}/iso - Attach ISO
    (isoId or userIsoName, optional changeBootDeviceToCdrom)."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/iso", json=body)
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def iso_detach(server_id: int) -> None:
    """DELETE /api/v1/servers/{serverId}/iso."""
    client = get_client()
    client.delete(f"/servers/{server_id}/iso")


def isoimages_list(server_id: int) -> list[dict]:
    """GET /api/v1/servers/{serverId}/isoimages - Available ISO images for server."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/isoimages")
    return resp.json()
