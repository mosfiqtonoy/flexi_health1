from flask import Blueprint, render_template, redirect, url_for

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========================
# ADMIN DASHBOARD
# =========================
@admin_bp.route("/")
def dashboard():
    return "Admin Dashboard"


# =========================
# USERS PAGE (example)
# =========================
@admin_bp.route("/users")
def users():
    return "Users List Page"


# =========================
# SETTINGS PAGE (example)
# =========================
@admin_bp.route("/settings")
def settings():
    return "Admin Settings Page"
