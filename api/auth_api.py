from flask import Blueprint, request, jsonify, session
from services.auth_service import (
    register_user,
    authenticate_user,
    reset_password,
    initiate_password_reset
)

auth_api_bp = Blueprint("auth_api", __name__)


# =========================
# REGISTER
# =========================
@auth_api_bp.route("/register", methods=["POST"])
def api_register():

    data = request.get_json(silent=True) or {}

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()
    password = data.get("password", "")

    # validation
    if not all([full_name, email, phone, password]):
        return jsonify({
            "success": False,
            "message": "All fields required."
        }), 400

    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must be at least 6 characters."
        }), 400

    success, message = register_user(
        full_name, email, phone, password
    )

    if success:
        return jsonify({
            "success": True,
            "message": message
        }), 201

    return jsonify({
        "success": False,
        "message": message
    }), 409


# =========================
# LOGIN
# =========================
@auth_api_bp.route("/login", methods=["POST"])
def api_login():

    data = request.get_json(silent=True) or {}

    identifier = data.get("identifier", "").strip()
    password = data.get("password", "")

    if not identifier or not password:
        return jsonify({
            "success": False,
            "message": "Credentials required."
        }), 400

    user, message = authenticate_user(identifier, password)

    if not user:
        return jsonify({
            "success": False,
            "message": message
        }), 401

    # session-based auth (web + mobile hybrid)
    session.permanent = True
    session["user_id"] = user.id
    session["full_name"] = user.full_name
    session["email"] = user.email
    session["role"] = user.role

    return jsonify({
        "success": True,
        "message": message,
        "user": user.to_dict()
    }), 200


# =========================
# LOGOUT
# =========================
@auth_api_bp.route("/logout", methods=["POST"])
def api_logout():
    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    }), 200


# =========================
# FORGOT PASSWORD
# =========================
@auth_api_bp.route("/forgot-password", methods=["POST"])
def api_forgot_password():

    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()

    if not email:
        return jsonify({
            "success": False,
            "message": "Email required."
        }), 400

    success, result = initiate_password_reset(email)

    if success:
        return jsonify({
            "success": True,
            "message": "Reset token generated.",
            "token": result   # ⚠️ dev only (remove in production)
        }), 200

    return jsonify({
        "success": False,
        "message": result
    }), 404


# =========================
# RESET PASSWORD
# =========================
@auth_api_bp.route("/reset-password", methods=["POST"])
def api_reset_password():

    data = request.get_json(silent=True) or {}

    token = data.get("token", "")
    password = data.get("password", "")

    if not token or not password:
        return jsonify({
            "success": False,
            "message": "Token and password required."
        }), 400

    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password too weak."
        }), 400

    success, message = reset_password(token, password)

    if success:
        return jsonify({
            "success": True,
            "message": message
        }), 200

    return jsonify({
        "success": False,
        "message": message
    }), 400
