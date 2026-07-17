"""User firewall policies API."""

from typing import Any

from .base import get_client


def firewall_policies_list(
    user_id: int,
    limit: int | None = None,
    offset: int | None = None,
    q: str | None = None,
) -> list[dict]:
    """GET /api/v1/users/{userId}/firewall-policies."""
    client = get_client()
    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if q:
        params["q"] = q
    resp = client.get(f"/users/{user_id}/firewall-policies", params=params or None)
    return resp.json()


def firewall_policy_get(
    user_id: int,
    policy_id: int,
    with_count_of_affected_servers: bool = False,
) -> dict:
    """GET /api/v1/users/{userId}/firewall-policies/{id}."""
    client = get_client()
    resp = client.get(
        f"/users/{user_id}/firewall-policies/{policy_id}",
        params={"withCountOfAffectedServers": with_count_of_affected_servers},
    )
    return resp.json()


def firewall_policy_create(user_id: int, body: dict) -> dict:
    """POST /api/v1/users/{userId}/firewall-policies."""
    client = get_client()
    resp = client.post(f"/users/{user_id}/firewall-policies", json=body)
    return resp.json()


def firewall_policy_update(user_id: int, policy_id: int, body: dict) -> dict | None:
    """PUT /api/v1/users/{userId}/firewall-policies/{id}."""
    client = get_client()
    resp = client.put(f"/users/{user_id}/firewall-policies/{policy_id}", json=body)
    if resp.status_code == 204:
        return None
    return resp.json() if resp.text else None


def firewall_policy_delete(user_id: int, policy_id: int) -> None:
    """DELETE /api/v1/users/{userId}/firewall-policies/{id}."""
    client = get_client()
    client.delete(f"/users/{user_id}/firewall-policies/{policy_id}")
