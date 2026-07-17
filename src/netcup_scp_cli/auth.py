"""Authentication: device code flow, refresh token, credential storage."""

import json
import time
from pathlib import Path

import requests

from .config import AUTH_URL, CLIENT_ID, SCOPE, credentials_path, ensure_config_dir
from .exceptions import AuthError, ConfigError


def request_device_code() -> dict:
    """Request device code for OAuth2 device flow. Returns dict with
    device_code, user_code, verification_uri_complete, etc."""
    resp = requests.post(
        f"{AUTH_URL}/auth/device",
        data={"client_id": CLIENT_ID, "scope": SCOPE},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def exchange_device_code(device_code: str) -> dict:
    """Exchange device code for access and refresh tokens."""
    resp = requests.post(
        f"{AUTH_URL}/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code,
            "client_id": CLIENT_ID,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def refresh_access_token(refresh_token: str) -> dict:
    """Get new access token using refresh token."""
    resp = requests.post(
        f"{AUTH_URL}/token",
        data={
            "client_id": CLIENT_ID,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise AuthError(f"Token refresh failed: {resp.status_code} - {resp.text}")
    return resp.json()


def revoke_refresh_token(refresh_token: str) -> None:
    """Revoke a refresh token."""
    resp = requests.post(
        f"{AUTH_URL}/revoke",
        data={
            "client_id": CLIENT_ID,
            "token": refresh_token,
            "token_type_hint": "refresh_token",
        },
        timeout=30,
    )
    resp.raise_for_status()


def load_credentials(path: Path | None = None) -> dict:
    """Load stored credentials (refresh_token). Raises ConfigError if missing or invalid."""
    p = path or credentials_path()
    if not p.exists():
        raise ConfigError("No stored credentials. Run: netcup auth login")
    try:
        data = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError) as e:
        raise ConfigError(f"Invalid or unreadable credentials file: {e}") from e
    if not data.get("refresh_token"):
        raise ConfigError("Credentials file missing refresh_token. Run: netcup auth login")
    return data


def save_credentials(refresh_token: str, path: Path | None = None) -> None:
    """Persist refresh token to config directory."""
    p = path or credentials_path()
    ensure_config_dir()
    p.write_text(json.dumps({"refresh_token": refresh_token}, indent=2))
    try:
        p.chmod(0o600)
    except OSError:
        pass


def get_access_token(refresh_token: str | None = None) -> str:
    """
    Return a valid access token. Uses refresh_token from argument or from stored credentials.
    """
    token = refresh_token
    if not token:
        creds = load_credentials()
        token = creds["refresh_token"]
    result = refresh_access_token(token)
    return result["access_token"]


def wait_for_device_authorization(
    device_code: str,
    interval: int = 5,
    expires_in: int = 600,
) -> dict:
    """
    Poll token endpoint until user authorizes device. Returns token response or raises.
    """
    deadline = time.monotonic() + expires_in
    while time.monotonic() < deadline:
        try:
            return exchange_device_code(device_code)
        except requests.HTTPError as e:
            if e.response.status_code == 400:
                body = (
                    e.response.json()
                    if e.response.headers.get("content-type", "").startswith("application/json")
                    else {}
                )
                error = body.get("error", "")
                if error == "authorization_pending":
                    time.sleep(interval)
                    continue
                if error == "slow_down":
                    interval = min(interval + 5, 60)
                    time.sleep(interval)
                    continue
                if error == "access_denied":
                    raise AuthError("Access denied on device authorization.")
                if error == "expired_token":
                    raise AuthError("Device code expired. Please run login again.")
            raise
    raise AuthError("Device authorization timed out.")
