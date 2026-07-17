"""Server image setup and image flavours API."""

from .base import get_client


def imageflavours_list(server_id: int) -> list[dict]:
    """GET /api/v1/servers/{serverId}/imageflavours."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/imageflavours")
    return resp.json()


def image_setup(server_id: int, body: dict) -> dict | None:
    """POST /api/v1/servers/{serverId}/image - Setup image (ServerImageSetup schema)."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/image", json=body)
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def user_image_setup(server_id: int, body: dict) -> dict | None:
    """POST /api/v1/servers/{serverId}/user-image - Setup user image
    (userImageName, optional diskName, emailNotification)."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/user-image", json=body)
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None
