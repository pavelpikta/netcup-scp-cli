"""Server metrics API."""

from typing import Any

from .base import get_client


def metrics_cpu(server_id: int, hours: int | None = None) -> dict:
    """GET /api/v1/servers/{serverId}/metrics/cpu."""
    client = get_client()
    params: dict[str, Any] = {}
    if hours is not None:
        params["hours"] = hours
    resp = client.get(f"/servers/{server_id}/metrics/cpu", params=params or None)
    return resp.json()


def metrics_disk(server_id: int, hours: int | None = None) -> dict:
    """GET /api/v1/servers/{serverId}/metrics/disk."""
    client = get_client()
    params = {}
    if hours is not None:
        params["hours"] = hours
    resp = client.get(f"/servers/{server_id}/metrics/disk", params=params or None)
    return resp.json()


def metrics_network(server_id: int, hours: int | None = None) -> dict:
    """GET /api/v1/servers/{serverId}/metrics/network."""
    client = get_client()
    params = {}
    if hours is not None:
        params["hours"] = hours
    resp = client.get(f"/servers/{server_id}/metrics/network", params=params or None)
    return resp.json()


def metrics_network_packet(server_id: int, hours: int | None = None) -> dict:
    """GET /api/v1/servers/{serverId}/metrics/network/packet."""
    client = get_client()
    params = {}
    if hours is not None:
        params["hours"] = hours
    resp = client.get(f"/servers/{server_id}/metrics/network/packet", params=params or None)
    return resp.json()
