"""Server interfaces and firewall API."""

from .base import get_client


def interfaces_list(server_id: int, load_rdns: bool = True) -> list[dict]:
    """GET /api/v1/servers/{serverId}/interfaces."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/interfaces", params={"loadRdns": load_rdns})
    return resp.json()


def interface_get(server_id: int, mac: str, load_rdns: bool = True) -> dict:
    """GET /api/v1/servers/{serverId}/interfaces/{mac}."""
    client = get_client()
    resp = client.get(f"/servers/{server_id}/interfaces/{mac}", params={"loadRdns": load_rdns})
    return resp.json()


def interface_create(server_id: int, vlan_id: int, network_driver: str) -> dict | None:
    """POST /api/v1/servers/{serverId}/interfaces - Create NIC with VLAN."""
    client = get_client()
    resp = client.post(
        f"/servers/{server_id}/interfaces",
        json={"vlanId": vlan_id, "networkDriver": network_driver},
        content_type="application/merge-patch+json",
    )
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def interface_update(server_id: int, mac: str, body: dict) -> dict | None:
    """PUT /api/v1/servers/{serverId}/interfaces/{mac}."""
    client = get_client()
    resp = client.put(f"/servers/{server_id}/interfaces/{mac}", json=body)
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def interface_delete(server_id: int, mac: str) -> dict | None:
    """DELETE /api/v1/servers/{serverId}/interfaces/{mac}."""
    client = get_client()
    resp = client.delete(f"/servers/{server_id}/interfaces/{mac}")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def firewall_get(server_id: int, mac: str, consistency_check: bool = False) -> dict:
    """GET /api/v1/servers/{serverId}/interfaces/{mac}/firewall."""
    client = get_client()
    resp = client.get(
        f"/servers/{server_id}/interfaces/{mac}/firewall",
        params={"consistencyCheck": consistency_check},
    )
    return resp.json()


def firewall_put(server_id: int, mac: str, body: dict) -> dict | None:
    """PUT /api/v1/servers/{serverId}/interfaces/{mac}/firewall."""
    client = get_client()
    resp = client.put(f"/servers/{server_id}/interfaces/{mac}/firewall", json=body)
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def firewall_reapply(server_id: int, mac: str) -> dict | None:
    """POST /api/v1/servers/{serverId}/interfaces/{mac}/firewall:reapply."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/interfaces/{mac}/firewall:reapply")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def firewall_restore_copied_policies(server_id: int, mac: str) -> dict | None:
    """POST /api/v1/servers/{serverId}/interfaces/{mac}/firewall:restore-copied-policies."""
    client = get_client()
    resp = client.post(f"/servers/{server_id}/interfaces/{mac}/firewall:restore-copied-policies")
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None
