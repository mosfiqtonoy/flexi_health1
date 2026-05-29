from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from utils.security import admin_required
from utils.db import get_db

# Initialize Admin Blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@admin_required  # Role-Based Access Control (RBAC) enforcement
def admin_dashboard():
    """
    Serves the core administrative metrics command console.
    Tracks total registered system users, micro-savings balance matrices, 
    and verifies the 500 BDT service eligibility threshold.
    """
    try:
        db = get_db()

        # Fetching user metrics joined with their respective 10% savings account state
        query = """
            SELECT u.id, u.name, u.phone, u.role, u.created_at, s.balance 
            FROM users u
            LEFT JOIN savings_accounts s ON u.id = s.user_id
            ORDER BY u.created_at DESC
        """
        users = db.execute(query).fetchall()

        # Aggregating platform-wide financial liquidity metrics for cost/sales analysis
        total_savings = db.execute("SELECT SUM(balance) FROM savings_accounts").fetchone()[0] or 0
        total_users = len(users)

        return render_template(
            "admin/dashboard.html", 
            users=users, 
            total_savings=total_savings,
            total_users=total_users
        )

    except Exception as e:
        # Strict server-side error logging for infrastructure diagnostics
        current_app.logger.error(f"Administrative Dashboard Execution Failure: {str(e)}")
        flash("System failed to retrieve administrative metrics matrix.", "danger")
        return redirect(url_for('dashboard.user_dashboard'))

@admin_bp.route('/admin/requests')
@admin_required
def manage_service_requests():
    """
    Monitors and dispatches urgent medical emergency requests.
    Handles allocations for Telemedicine, Ambulances, Blood Banks, and Medicine Delivery.
    """
    try:
        db = get_db()
        # Fetching active service tickers sorted by urgency and timestamps
        requests = db.execute("SELECT * FROM service_requests ORDER BY status DESC, created_at ASC").fetchall()
        return render_template("admin/requests.html", requests=requests)
    except Exception as e:
        current_app.logger.error(f"Service Request Fetch Failure: {str(e)}")
        flash("Failed to load active emergency dispatch payloads.", "danger")
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/user/update/<int:user_id>', methods=['POST'])
@admin_required
def update_user_status(user_id):
    """
    Mutates system authorization layers for specific users.
    Enables upgrading profiles to Doctors, Part-time Delivery Agents, or Admins.
    """
    new_role = request.form.get('role')
    try:
        db = get_db()
        db.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
        db.commit()
        flash(f"Privilege escalation successful for User ID {user_id}.", "success")
    except Exception as e:
        current_app.logger.error(f"RBAC Mutation Failure for User ID {user_id}: {str(e)}")
        flash("Failed to update target user authorization level.", "danger")
    
    return redirect(url_for('admin.admin_dashboard'))
