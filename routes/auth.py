# routes/auth.py

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, current_app
)

from werkzeug.security import check_password_hash

from models.user import User
from utils.db import get_db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        identity = request.form.get('identity', '').strip().lower()
        password = request.form.get('password', '')

        if not identity or not password:
            flash("Please provide all credentials.", "danger")
            return render_template("auth/login.html")

        if '@' in identity:
            user = User.find_by_email(identity)
        else:
            user = User.find_by_phone(identity)

        if user and check_password_hash(user['password'], password):

            session.clear()
            session.permanent = True

            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']

            flash(f"Welcome {user['name']}!", "success")

            if user['role'] == 'admin':
                return redirect(url_for('admin.admin_dashboard'))

            return redirect(url_for('dashboard.user_dashboard'))

        flash("Invalid credentials.", "danger")

    return render_template("auth/login.html")


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')

        if not name or not email or not phone or len(password) < 8:
            flash("Invalid input data.", "danger")
            return render_template("auth/register.html")

        try:
            if User.find_by_email(email) or User.find_by_phone(phone):
                flash("User already exists.", "warning")
                return render_template("auth/register.html")

            new_user_id = User.create(name, email, phone, password)

            if not new_user_id:
                flash("User creation failed.", "danger")
                return render_template("auth/register.html")

            db = get_db()
            db.execute(
                "INSERT INTO savings_accounts (user_id, balance, min_threshold) VALUES (?, 0.0, 500.0)",
                (new_user_id,)
            )
            db.commit()

            flash("Account created successfully!", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            current_app.logger.error(f"REGISTER ERROR: {str(e)}")
            flash("Server error during registration.", "danger")

    return render_template("auth/register.html")


@auth_bp.route('/logout')
def logout():

    session.clear()
    flash("Logged out successfully.", "info")

    return redirect(url_for('auth.login'))


@auth_bp.route('/create-admin')
def create_admin():
    from werkzeug.security import generate_password_hash
    db = get_db()
    hashed = generate_password_hash('admin123')
    try:
        db.execute(
            "INSERT INTO users (name, email, phone, password, role) VALUES (?, ?, ?, ?, ?)",
            ('Admin', 'admin@flexihealth.com', '01700000000', hashed, 'admin')
        )
        db.commit()
        return "Admin created! Email: admin@flexihealth.com, Password: admin123"
    except Exception as e:
        return f"Error: {str(e)}"
    
