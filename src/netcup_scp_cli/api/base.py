"""Base helpers for API modules."""

from ..client import APIClient
from ..config import API_BASE_URL

_default_client: APIClient | None = None


def get_client(base_url: str | None = None) -> APIClient:
    """Return shared API client (or one with optional base_url override)."""
    if base_url is not None:
        return APIClient(base_url=base_url)
    global _default_client
    if _default_client is None:
        _default_client = APIClient(base_url=API_BASE_URL)
    return _default_client
