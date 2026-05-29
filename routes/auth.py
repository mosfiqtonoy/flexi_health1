# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles secure secure session generation and role-based authentication matrix."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Input Parameter Assertion Guard
        if not email or not password:
            flash("All authorization credentials must be provided.", "danger")
            return render_template("auth/login.html")

        user = User.find_by_email(email)

        # Secure cryptographic validation link
        if user and check_password_hash(user['password'], password):
            session.clear()  # Session Fixation Countermeasure
            session.permanent = True  # Triggers expiration timeouts
            
            # Formulating context authentication claims
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            
            flash(f"Welcome back, {user['name']}!", "success")
            
            # Strict Context Redirection based on roles
            if user['role'] == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('dashboard.user_dashboard'))
        
        flash("Invalid authentication credentials. Try again.", "danger")
        
    return render_template("auth/login.html")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Validates user entry parameters and injects safe data profiles into system memory."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Server-Side Robust Validation Rules
        if not name or not email or len(password) < 8:
            flash("Registration failure. Password structure must contain at least 8 elements.", "danger")
            return render_template("auth/register.html")

        if User.create(name, email, password):
            flash("Profile instantiation successful! Log in below.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Conflict occurred! An identification schema already maps to that email.", "warning")

    return render_template("auth/register.html")

@auth_bp.route('/logout')
def logout():
    """Destroys current active tracking sessions and context cookies safely."""
    session.clear()
    flash("Session terminated cleanly.", "info")
    return redirect(url_for('auth.login'))
