"""User VLANs and standalone VLAN API."""

from .base import get_client


def vlans_list(user_id: int, server_id: int | None = None) -> list[dict]:
    """GET /api/v1/users/{userId}/vlans."""
    client = get_client()
    params = {}
    if server_id is not None:
        params["serverId"] = server_id
    resp = client.get(f"/users/{user_id}/vlans", params=params or None)
    return resp.json()


def vlan_get(user_id: int, vlan_id: int) -> dict:
    """GET /api/v1/users/{userId}/vlans/{vlanId}."""
    client = get_client()
    resp = client.get(f"/users/{user_id}/vlans/{vlan_id}")
    return resp.json()


def vlan_update(user_id: int, vlan_id: int, name: str) -> None:
    """PUT /api/v1/users/{userId}/vlans/{vlanId} - body: VLanSave (name)."""
    client = get_client()
    client.put(f"/users/{user_id}/vlans/{vlan_id}", json={"name": name})


def vlan_get_by_id(vlan_id: int) -> dict:
    """GET /api/v1/vlans/{vlanId} - Get VLAN by ID (no user scope)."""
    client = get_client()
    resp = client.get(f"/vlans/{vlan_id}")
    return resp.json()
