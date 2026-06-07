from flask import Blueprint, render_template, redirect, url_for, session, flash
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Access denied.", "danger")
            return redirect(url_for("dashboard.home"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")

@admin_bp.route("/users")
@admin_required
def users():
    return render_template("admin/requests.html")

@admin_bp.route("/settings")
@admin_required
def settings():
    return render_template("admin/settings.html")
