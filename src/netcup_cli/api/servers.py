"""Servers API."""

from typing import Any

from .base import get_client


def server_list(
    *,
    limit: int | None = None,
    offset: int | None = None,
    firewall_policy_id: int | None = None,
    ip: str | None = None,
    name: str | None = None,
    q: str | None = None,
    sort: list[str] | None = None,
) -> list[dict]:
    """GET /api/v1/servers - List servers with optional filters."""
    client = get_client()
    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if firewall_policy_id is not None:
        params["firewallPolicyId"] = firewall_policy_id
    if ip:
        params["ip"] = ip
    if name:
        params["name"] = name
    if q:
        params["q"] = q
    if sort:
        params["sort"] = sort
    resp = client.get("/servers", params=params or None)
    return resp.json()


def server_get(server_id: int, load_server_live_info: bool = True) -> dict:
    """GET /api/v1/servers/{serverId} - Get one server."""
    client = get_client()
    resp = client.get(
        f"/servers/{server_id}",
        params={"loadServerLiveInfo": load_server_live_info},
    )
    return resp.json()


def server_patch(
    server_id: int,
    body: dict,
    state_option: str | None = None,
) -> dict | None:
    """PATCH /api/v1/servers/{serverId} - Patch server (state, hostname, etc.).
    Returns JSON or None for 204."""
    client = get_client()
    params = {"stateOption": state_option} if state_option else None
    resp = client.patch(f"/servers/{server_id}", json=body, params=params)
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None
