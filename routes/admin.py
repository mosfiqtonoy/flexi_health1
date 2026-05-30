from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from utils.security import admin_required
from utils.db import get_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    try:
        db = get_db()
        query = """
            SELECT u.id, u.name, u.email, u.phone, u.role, u.created_at, s.balance 
            FROM users u
            LEFT JOIN savings_accounts s ON u.id = s.user_id
            ORDER BY u.created_at DESC
        """
        users = db.execute(query).fetchall()
        total_savings = db.execute("SELECT SUM(balance) FROM savings_accounts").fetchone()[0] or 0
        total_users = len(users)
        return render_template(
            "admin/dashboard.html",
            users=users,
            total_savings=total_savings,
            total_users=total_users
        )
    except Exception as e:
        current_app.logger.error(f"Admin Dashboard Failure: {str(e)}")
        flash("System failed to retrieve administrative metrics.", "danger")
        return redirect(url_for('dashboard.user_dashboard'))

@admin_bp.route('/admin/requests')
@admin_required
def manage_service_requests():
    try:
        db = get_db()
        requests = db.execute("SELECT * FROM service_requests ORDER BY status DESC, created_at ASC").fetchall()
        return render_template("admin/requests.html", requests=requests)
    except Exception as e:
        current_app.logger.error(f"Service Request Fetch Failure: {str(e)}")
        flash("Failed to load service requests.", "danger")
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/requests/update/<int:request_id>', methods=['POST'])
@admin_required
def update_request_status(request_id):
    new_status = request.form.get('status')
    try:
        db = get_db()
        db.execute("UPDATE service_requests SET status = ? WHERE id = ?", (new_status, request_id))
        db.commit()
        flash(f"Request #{request_id} status updated to {new_status}.", "success")
    except Exception as e:
        current_app.logger.error(f"Request Status Update Failure: {str(e)}")
        flash("Failed to update request status.", "danger")
    return redirect(url_for('admin.manage_service_requests'))

@admin_bp.route('/admin/user/update/<int:user_id>', methods=['POST'])
@admin_required
def update_user_status(user_id):
    new_role = request.form.get('role')
    try:
        db = get_db()
        db.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
        db.commit()
        flash(f"Role updated successfully for User ID {user_id}.", "success")
    except Exception as e:
        current_app.logger.error(f"Role Update Failure for User ID {user_id}: {str(e)}")
        flash("Failed to update user role.", "danger")
    return redirect(url_for('admin.admin_dashboard'))
