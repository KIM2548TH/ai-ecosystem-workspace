"""Legacy shim for security module."""

from backend.app.core.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    oauth2_scheme,
    verify_password,
)

__all__ = [
    "create_access_token",
    "get_current_user",
    "get_password_hash",
    "oauth2_scheme",
    "verify_password",
]
