import hashlib
import hmac
import secrets
import time
import binascii
from functools import wraps
from flask import session, redirect, url_for, jsonify


# =========================
# CONFIG CONSTANTS
# =========================
PBKDF2_ITERATIONS = 260000


# =========================
# PASSWORD HASHING
# =========================
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        PBKDF2_ITERATIONS
    )

    return f"pbkdf2:sha256:{PBKDF2_ITERATIONS}${binascii.hexlify(salt).decode()}${binascii.hexlify(dk).decode()}"


def check_password(password: str, password_hash: str) -> bool:
    try:
        parts = password_hash.split("$")
        if len(parts) != 3:
            return False

        algo_info, salt_hex, dk_hex = parts

        iterations = int(algo_info.split(":")[2])
        salt = binascii.unhexlify(salt_hex)

        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            iterations
        )

        return hmac.compare_digest(
            binascii.hexlify(dk).decode(),
            dk_hex
        )

    except Exception:
        return False


# =========================
# TOKEN SYSTEM
# =========================
def generate_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def token_expiry(minutes: int = 60) -> int:
    return int(time.time()) + minutes * 60


def is_token_valid(expiry: int) -> bool:
    return expiry and int(time.time()) < expiry


# =========================
# WEB AUTH DECORATORS
# =========================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        if session.get("role") != "admin":
            return redirect(url_for("errors.forbidden"))

        return f(*args, **kwargs)

    return wrapper


# =========================
# API AUTH DECORATORS
# =========================
def api_login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Authentication required"
            }), 401
        return f(*args, **kwargs)

    return wrapper


def api_admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Authentication required"
            }), 401

        if session.get("role") != "admin":
            return jsonify({
                "success": False,
                "message": "Admin access required"
            }), 403

        return f(*args, **kwargs)

    return wrapper
