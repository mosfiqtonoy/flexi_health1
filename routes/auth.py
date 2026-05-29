# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import check_password_hash
from models.user import User
from utils.db import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles secure session generation and dual-identifier role-based authentication matrix."""
    if request.method == 'POST':
        # MODIFIED: Accepts either Email or Phone as a unified identifier payload
        identity = request.form.get('identity', '').strip().lower()
        password = request.form.get('password', '')

        if not identity or not password:
            flash("All authorization credentials must be provided.", "danger")
            return render_template("auth/login.html")

        # MODIFIED: Dynamically queries user based on identity format (Email or SIM phone number)
        if '@' in identity:
            user = User.find_by_email(identity)
        else:
            user = User.find_by_phone(identity)

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
    """Validates multidimensional user parameters and injects safe profiles into memory."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')

        # Server-Side Robust Validation Rules for all core identities
        if not name or not email or not phone or len(password) < 8:
            flash("Registration failure. Comprehensive payload structure required.", "danger")
            return render_template("auth/register.html")

        try:
            db = get_db()
            
            # MODIFIED: Check for duplication on both unique channels to avoid conflicts
            if User.find_by_email(email) or User.find_by_phone(phone):
                flash("Conflict occurred! Email or Phone number already mapped to an existing account.", "warning")
                return render_template("auth/register.html")

            # MODIFIED: Passes both email and phone into the storage instantiation engine
            new_user_id = User.create(name, email, phone, password)
            
            if new_user_id:
                # AUTOMATION: Instantiate the 10% auto-savings container with a 500 BDT unlock boundary
                db.execute(
                    "INSERT INTO savings_accounts (user_id, balance, min_threshold) VALUES (?, 0.0, 500.0)",
                    (new_user_id,)
                )
                db.commit()  # Flush transaction matrix securely to persistent memory
                
                flash("Profile instantiation successful! Log in below.", "success")
                return redirect(url_for('auth.login'))
        
        except Exception as e:
            current_app.logger.error(f"Critical onboarding transaction failure: {str(e)}")
            flash("System fault during automated profile initialization. Please try again.", "danger")

    return render_template("auth/register.html")

@auth_bp.route('/logout')
def logout():
    """Destroys current active tracking sessions and context cookies safely."""
    session.clear()
    flash("Session terminated cleanly.", "info")
    return redirect(url_for('auth.login'))
