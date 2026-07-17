"""Custom exceptions for netcup CLI."""


class SCPError(Exception):
    """Base exception for netcup CLI (SCP API)."""


class AuthError(SCPError):
    """Authentication or token error."""


class APIError(SCPError):
    """API request error."""

    def __init__(self, message: str, status_code: int | None = None, body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class ConfigError(SCPError):
    """Configuration or credentials error."""
