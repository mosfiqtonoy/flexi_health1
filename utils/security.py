# utils/security.py
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Hero-Level Auth Guard:
    Prevents unauthenticated users from accessing protected routes.
    If the 'user_id' is missing from the session, it redirects to the login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # Flash a warning message for the user
            flash("Unauthorized access! Please login to your account first.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Role-Based Access Control (RBAC) Guard:
    Restricts access solely to users with the 'admin' role.
    If a regular user tries to access admin-only routes, they are pushed back to the dashboard.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if logged in AND if the role is 'admin'
        if 'user_id' not in session or session.get('user_role') != 'admin':
            flash("Access Denied! You do not have administrative privileges.", "danger")
            return redirect(url_for('dashboard.user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function
