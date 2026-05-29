# routes/admin.py
from flask import Blueprint, render_template, flash, redirect, url_for
from utils.security import admin_required
from utils.db import get_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@admin_required  # Restricts execution solely to users with validated 'admin' credentials
def admin_dashboard():
    """Serves the core administrative metrics command console."""
    try:
        db = get_db()
        # Fetching user metrics for administrative observation matrix
        users = db.execute("SELECT id, name, email, role, created_at FROM users").fetchall()
        return render_template("admin/dashboard.html", users=users)
    except Exception as e:
        flash("Failed to retrieve system user metrics matrix.", "danger")
        return redirect(url_for('dashboard.user_dashboard'))
