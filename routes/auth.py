# routes/auth.py

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, current_app
)
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from utils.db import get_db
import secrets
from datetime import datetime, timedelta

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


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        email = request.form.get('email', '').strip().lower()

        if not email:
            flash("Please provide your email.", "danger")
            return render_template("auth/forgot_password.html")

        try:
            user = User.find_by_email(email)

            if not user:
                flash("No account found with this email.", "danger")
                return render_template("auth/forgot_password.html")

            db = get_db()

            # Delete old tokens for this user
            db.execute(
                "DELETE FROM password_reset_tokens WHERE user_id = ?",
                (user['id'],)
            )

            # Generate new token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(minutes=30)

            db.execute(
                "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
                (user['id'], token, expires_at)
            )
            db.commit()

            # Send email
            reset_url = url_for('auth.reset_password', token=token, _external=True)

            mail = Mail(current_app)
            msg = Message(
                subject="Flexi Health - Password Reset",
                recipients=[email],
                body=f"""
Hello {user['name']},

You requested a password reset for your Flexi Health account.

Click the link below to reset your password (valid for 30 minutes):

{reset_url}

If you did not request this, please ignore this email.

Flexi Health Team
"""
            )
            mail.send(msg)

            flash("Password reset link sent to your email!", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            current_app.logger.error(f"FORGOT PASSWORD ERROR: {str(e)}")
            flash("Failed to send reset email. Try again.", "danger")

    return render_template("auth/forgot_password.html")


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    try:
        db = get_db()

        # Find valid token
        reset = db.execute(
            """
            SELECT * FROM password_reset_tokens 
            WHERE token = ? AND used = 0 AND expires_at > ?
            """,
            (token, datetime.utcnow())
        ).fetchone()

        if not reset:
            flash("Invalid or expired reset link.", "danger")
            return redirect(url_for('auth.forgot_password'))

        if request.method == 'POST':

            password = request.form.get('password', '')
            confirm = request.form.get('confirm_password', '')

            if len(password) < 8:
                flash("Password must be at least 8 characters.", "danger")
                return render_template("auth/reset_password.html", token=token)

            if password != confirm:
                flash("Passwords do not match.", "danger")
                return render_template("auth/reset_password.html", token=token)

            # Update password
            hashed = generate_password_hash(password)
            db.execute(
                "UPDATE users SET password = ? WHERE id = ?",
                (hashed, reset['user_id'])
            )

            # Mark token as used
            db.execute(
                "UPDATE password_reset_tokens SET used = 1 WHERE token = ?",
                (token,)
            )
            db.commit()

            flash("Password reset successfully! Please login.", "success")
            return redirect(url_for('auth.login'))

    except Exception as e:
        current_app.logger.error(f"RESET PASSWORD ERROR: {str(e)}")
        flash("Something went wrong. Try again.", "danger")
        return redirect(url_for('auth.forgot_password'))

    return render_template("auth/reset_password.html", token=token)


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
