"""Server GPU driver download API."""

from .base import get_client


def gpu_driver_get(server_id: int) -> dict:
    """GET /api/v1/servers/{serverId}/gpu-driver - Presigned GPU driver URL if available."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/gpu-driver")
    return resp.json()
