"""User failover IPs API."""

from typing import Any

from .base import get_client


def failoverips_v4_list(
    user_id: int,
    ip: str | None = None,
    server_id: int | None = None,
) -> list[dict]:
    """GET /api/v1/users/{userId}/failoverips/v4."""
    client = get_client()
    params: dict[str, Any] = {}
    if ip:
        params["ip"] = ip
    if server_id is not None:
        params["serverId"] = server_id
    resp = client.get(f"/users/{user_id}/failoverips/v4", params=params or None)
    return resp.json()


def failoverips_v4_route(user_id: int, id: int, server_id: int) -> dict | None:
    """PATCH /api/v1/users/{userId}/failoverips/v4/{id} - Route failover IPv4 to server."""
    client = get_client()
    resp = client.patch(
        f"/users/{user_id}/failoverips/v4/{id}",
        json={"serverId": server_id},
        content_type="application/json",
    )
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def failoverips_v6_list(
    user_id: int,
    ip: str | None = None,
    server_id: int | None = None,
) -> list[dict]:
    """GET /api/v1/users/{userId}/failoverips/v6."""
    client = get_client()
    params = {}
    if ip:
        params["ip"] = ip
    if server_id is not None:
        params["serverId"] = server_id
    resp = client.get(f"/users/{user_id}/failoverips/v6", params=params or None)
    return resp.json()


def failoverips_v6_route(user_id: int, id: int, server_id: int) -> dict | None:
    """PATCH /api/v1/users/{userId}/failoverips/v6/{id}."""
    client = get_client()
    resp = client.patch(
        f"/users/{user_id}/failoverips/v6/{id}",
        json={"serverId": server_id},
        content_type="application/json",
    )
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None
