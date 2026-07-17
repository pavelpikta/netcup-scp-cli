"""Configuration and constants for SCP API."""

import os
from pathlib import Path

# API endpoints (netcup SCP)
BASE_URL = "https://www.servercontrolpanel.de"
AUTH_URL = f"{BASE_URL}/realms/scp/protocol/openid-connect"
API_ROOT = f"{BASE_URL}/scp-core/api"
API_BASE_URL = f"{API_ROOT}/v1"

# OAuth2 device flow
CLIENT_ID = "scp"
SCOPE = "offline_access openid"

CONFIG_DIR_NAME = "netcup-scp-cli"


def _config_dir() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return Path(xdg) / CONFIG_DIR_NAME


def credentials_path() -> Path:
    """Path to stored credentials (refresh token)."""
    return _config_dir() / "credentials"


def ensure_config_dir() -> Path:
    """Ensure config directory exists; return its path."""
    d = _config_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d
