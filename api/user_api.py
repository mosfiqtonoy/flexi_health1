from flask import Blueprint, request, jsonify, session
from utils.security import api_login_required, api_admin_required
from services.user_service import (
    get_user_profile,
    update_user_profile,
    add_recharge,
    get_recharge_history,
    get_all_users
)

user_api_bp = Blueprint("user_api", __name__)


# =========================
# GET PROFILE
# =========================
@user_api_bp.route("/profile", methods=["GET"])
@api_login_required
def api_get_profile():

    user_id = session.get("user_id")
    user = get_user_profile(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    return jsonify({
        "success": True,
        "user": user.to_dict()
    }), 200


# =========================
# UPDATE PROFILE
# =========================
@user_api_bp.route("/profile", methods=["PUT"])
@api_login_required
def api_update_profile():

    data = request.get_json(silent=True) or {}

    full_name = data.get("full_name", "").strip()
    phone = data.get("phone", "").strip()

    if not full_name or not phone:
        return jsonify({
            "success": False,
            "message": "Name and phone required."
        }), 400

    user_id = session.get("user_id")

    success, message = update_user_profile(
        user_id,
        full_name,
        phone
    )

    if success:
        session["full_name"] = full_name
        return jsonify({
            "success": True,
            "message": message
        }), 200

    return jsonify({
        "success": False,
        "message": message
    }), 409


# =========================
# RECHARGE
# =========================
@user_api_bp.route("/recharge", methods=["POST"])
@api_login_required
def api_recharge():

    data = request.get_json(silent=True) or {}

    try:
        amount = float(data.get("amount") or 0)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid amount."
        }), 400

    if amount <= 0:
        return jsonify({
            "success": False,
            "message": "Amount must be greater than 0."
        }), 400

    operator = data.get("operator", "Unknown")

    user_id = session.get("user_id")

    saved = add_recharge(user_id, amount, operator)

    return jsonify({
        "success": True,
        "saved_amount": saved,
        "message": f"{saved:.2f} BDT saved."
    }), 200


# =========================
# RECHARGE HISTORY
# =========================
@user_api_bp.route("/recharge-history", methods=["GET"])
@api_login_required
def api_recharge_history():

    user_id = session.get("user_id")

    history = get_recharge_history(user_id)

    return jsonify({
        "success": True,
        "history": history
    }), 200


# =========================
# ADMIN - ALL USERS
# =========================
@user_api_bp.route("/all", methods=["GET"])
@api_admin_required
def api_all_users():

    users = get_all_users()

    return jsonify({
        "success": True,
        "users": users   # ✅ FIXED (no .to_dict())
    }), 200
