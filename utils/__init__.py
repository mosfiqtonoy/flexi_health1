"""
Flexi Health - Utils Package

This package contains core utilities for:
- Database connection handling
- Security & authentication helpers

Designed to be:
- Production-ready
- Modular
- Easy to scale (web + API + mobile backend)
"""

# =========================
# DATABASE UTILITIES
# =========================
from .db import get_db, init_db, close_db

# =========================
# SECURITY UTILITIES
# =========================
from .security import (
    hash_password,
    check_password,
    generate_token,
    token_expiry,
    is_token_valid,
    login_required,
    admin_required,
    api_login_required,
    api_admin_required
)

# =========================
# PUBLIC API OF PACKAGE
# =========================
__all__ = [
    # DB
    "get_db",
    "init_db",
    "close_db",

    # Security
    "hash_password",
    "check_password",

    "generate_token",
    "token_expiry",
    "is_token_valid",

    # Web Auth
    "login_required",
    "admin_required",

    # API Auth
    "api_login_required",
    "api_admin_required",
]
