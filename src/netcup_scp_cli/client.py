"""HTTP client for SCP API with Bearer token handling."""

from typing import Any

import requests

from .auth import get_access_token
from .config import API_BASE_URL
from .exceptions import APIError


class APIClient:
    """Minimal API client for SCP REST API."""

    def __init__(self, access_token: str | None = None, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self._access_token = access_token

    def _headers(self) -> dict[str, str]:
        token = self._access_token or get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | list | None = None,
        data: dict | None = None,
        content_type: str | None = None,
        accept: str | None = None,
    ) -> requests.Response:
        url = f"{self.base_url}{path}" if path.startswith("/") else f"{self.base_url}/{path}"
        headers = self._headers()
        if content_type:
            headers["Content-Type"] = content_type
        if accept:
            headers["Accept"] = accept
        resp = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=json,
            data=data,
            timeout=60,
        )
        return resp

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict | list | None = None,
        data: dict | None = None,
        content_type: str | None = None,
        accept: str | None = None,
        raise_for_status: bool = True,
    ) -> requests.Response:
        resp = self._request(
            method,
            path,
            params=params,
            json=json,
            data=data,
            content_type=content_type,
            accept=accept,
        )
        if raise_for_status and not resp.ok:
            raise APIError(
                f"API error: {resp.status_code}",
                status_code=resp.status_code,
                body=resp.text,
            )
        return resp

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        accept: str | None = None,
    ) -> requests.Response:
        return self.request("GET", path, params=params, accept=accept)

    def post(
        self,
        path: str,
        json: dict | list | None = None,
        data: dict | None = None,
        content_type: str | None = None,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self.request(
            "POST", path, json=json, data=data, content_type=content_type, params=params
        )

    def put(self, path: str, json: dict | list | None = None) -> requests.Response:
        return self.request("PUT", path, json=json)

    def patch(
        self,
        path: str,
        json: dict | list | None = None,
        content_type: str = "application/merge-patch+json",
    ) -> requests.Response:
        return self.request("PATCH", path, json=json, content_type=content_type)

    def delete(self, path: str) -> requests.Response:
        return self.request("DELETE", path)
