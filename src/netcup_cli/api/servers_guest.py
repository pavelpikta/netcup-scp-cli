"""Server guest agent API."""

from .base import get_client


def guest_agent_get(server_id: int) -> dict:
    """GET /api/v1/servers/{serverId}/guest-agent."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/guest-agent")
    return resp.json()


def guest_agent_status_get(server_id: int) -> dict:
    """GET /api/v1/servers/{serverId}/guest-agent/status."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/guest-agent/status")
    return resp.json()
