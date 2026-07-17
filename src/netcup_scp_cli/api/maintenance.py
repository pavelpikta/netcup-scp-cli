"""Maintenance and ping API."""

from ..config import API_ROOT
from .base import get_client


def ping() -> str:
    """GET /api/ping - Check if application is available. Returns text/plain (e.g. OK)."""
    client = get_client(base_url=API_ROOT)
    resp = client.get("/ping", accept="text/plain")
    return resp.text.strip()


def get_maintenance() -> dict:
    """GET /api/v1/maintenance - Get maintenance information."""
    client = get_client()
    resp = client.get("/maintenance")
    return resp.json()
