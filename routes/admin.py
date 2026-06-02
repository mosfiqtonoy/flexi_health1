from flask import Blueprint, render_template, redirect, url_for, request, flash

from utils.security import admin_required
from services.user_service import get_all_users, toggle_user_status
from services.dashboard_service import (
    get_all_service_requests,
    update_service_request_status
)
from utils.db import get_db


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========================
# ADMIN DASHBOARD PANEL
# =========================
@admin_bp.route("/")
@admin_required
def panel():
    try:
        users = get_all_users()
        requests = get_all_service_requests()

        db = get_db()

        total_balance = db.execute(
            "SELECT COALESCE(SUM(balance), 0) FROM users"
        ).fetchone()[0]

        total_recharge = db.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM recharge_history"
        ).fetchone()[0]

        stats = {
            "total_users": len(users),
            "active_users": sum(1 for u in users if u.is_active),
            "total_requests": len(requests),
            "pending_requests": sum(
                1 for r in requests if r["status"] == "pending"
            ),
            "total_balance": total_balance,
            "total_recharge": total_recharge
        }

        return render_template(
            "admin/admin.html",
            users=users,
            requests=requests,
            stats=stats
        )

    except Exception as e:
        return render_template(
            "errors/500.html",
            error=str(e)
        ), 500


# =========================
# TOGGLE USER STATUS
# =========================
@admin_bp.route("/user/<int:user_id>/toggle", methods=["POST"])
@admin_required
def toggle_user(user_id):
    try:
        success, message = toggle_user_status(user_id)
        flash(message, "success" if success else "danger")
    except Exception:
        flash("Something went wrong while updating user.", "danger")

    return redirect(url_for("admin.panel"))


# =========================
# UPDATE SERVICE REQUEST
# =========================
@admin_bp.route("/request/<int:req_id>/status", methods=["POST"])
@admin_required
def update_request(req_id):
    try:
        status = request.form.get("status", "pending")

        allowed_status = {
            "pending",
            "in_progress",
            "completed",
            "rejected"
        }

        if status not in allowed_status:
            flash("Invalid status.", "danger")
            return redirect(url_for("admin.panel"))

        update_service_request_status(req_id, status)
        flash("Request status updated.", "success")

    except Exception:
        flash("Failed to update request.", "danger")

    return redirect(url_for("admin.panel"))
