# ==========================================================
# AUTH ROUTES MODULE (LOGIN + REGISTER + LOGOUT)
# ==========================================================

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, current_app
)

from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User
from utils.db import get_db


# ==========================================================
# BLUEPRINT INITIALIZATION
# ==========================================================
auth_bp = Blueprint('auth', __name__)


# ==========================================================
# LOGIN ROUTE
# ==========================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        # ---------------- INPUT DATA ----------------
        identity = request.form.get('identity', '').strip().lower()
        password = request.form.get('password', '')

        # ---------------- VALIDATION ----------------
        if not identity or not password:
            flash("Please provide all credentials.", "danger")
            return render_template("auth/login.html")

        # ---------------- USER FETCH ----------------
        if '@' in identity:
            user = User.find_by_email(identity)
        else:
            user = User.find_by_phone(identity)

        # ---------------- PASSWORD CHECK ----------------
        if user and check_password_hash(user['password'], password):

            session.clear()
            session.permanent = True

            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']

            flash(f"Welcome {user['name']}!", "success")

            # ---------------- ROLE REDIRECT ----------------
            if user['role'] == 'admin':
                return redirect(url_for('admin.admin_dashboard'))

            return redirect(url_for('dashboard.user_dashboard'))

        flash("Invalid credentials.", "danger")

    return render_template("auth/login.html")


# ==========================================================
# REGISTER ROUTE
# ==========================================================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        # ---------------- INPUT DATA ----------------
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')

        # ---------------- VALIDATION ----------------
        if not name or not email or not phone or len(password) < 8:
            flash("Invalid input data.", "danger")
            return render_template("auth/register.html")

        try:
            # ---------------- DUPLICATE CHECK ----------------
            if User.find_by_email(email) or User.find_by_phone(phone):
                flash("User already exists.", "warning")
                return render_template("auth/register.html")

            # ---------------- CREATE USER ----------------
            hashed_password = generate_password_hash(password)
            new_user_id = User.create(name, email, phone, hashed_password)

            if not new_user_id:
                flash("User creation failed.", "danger")
                return render_template("auth/register.html")

            # ---------------- CREATE SAVINGS ACCOUNT ----------------
            db = get_db()

            db.execute(
                """
                INSERT INTO savings_accounts (user_id, balance, min_threshold)
                VALUES (?, 0.0, 500.0)
                """,
                (new_user_id,)
            )

            db.commit()

            flash("Account created successfully!", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            current_app.logger.error(f"REGISTER ERROR: {str(e)}")
            flash("Server error during registration.", "danger")

    return render_template("auth/register.html")


# ==========================================================
# LOGOUT ROUTE
# ==========================================================
@auth_bp.route('/logout')
def logout():

    session.clear()
    flash("Logged out successfully.", "info")

    return redirect(url_for('auth.login'))
