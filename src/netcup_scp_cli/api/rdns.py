"""rDNS API (IPv4 and IPv6)."""

from .base import get_client


def rdns_get_ipv4(ip: str) -> dict:
    """GET /api/v1/rdns/ipv4/{ip}."""
    client = get_client()
    resp = client.get(f"/rdns/ipv4/{ip}")
    return resp.json()


def rdns_set_ipv4(ip: str, rdns: str) -> None:
    """POST /api/v1/rdns/ipv4 - Set rDNS for IPv4."""
    client = get_client()
    client.post("/rdns/ipv4", json={"ip": ip, "rdns": rdns})


def rdns_delete_ipv4(ip: str) -> None:
    """DELETE /api/v1/rdns/ipv4/{ip}."""
    client = get_client()
    client.delete(f"/rdns/ipv4/{ip}")


def rdns_get_ipv6(ip: str) -> dict:
    """GET /api/v1/rdns/ipv6/{ip}."""
    client = get_client()
    resp = client.get(f"/rdns/ipv6/{ip}")
    return resp.json()


def rdns_set_ipv6(ip: str, rdns: str) -> None:
    """POST /api/v1/rdns/ipv6 - Set rDNS for IPv6."""
    client = get_client()
    client.post("/rdns/ipv6", json={"ip": ip, "rdns": rdns})


def rdns_delete_ipv6(ip: str) -> None:
    """DELETE /api/v1/rdns/ipv6/{ip}."""
    client = get_client()
    client.delete(f"/rdns/ipv6/{ip}")
