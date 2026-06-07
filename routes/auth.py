from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, current_app
)
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from utils.db import get_db
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identity = request.form.get("identity", "").strip().lower()
        password = request.form.get("password", "")

        if not identity or not password:
            flash("Please provide all credentials.", "danger")
            return render_template("auth/login.html")

        user = (
            User.find_by_email(identity)
            if "@" in identity
            else User.find_by_phone(identity)
        )

        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session.permanent = True
            session["user_id"] = user.id
            session["full_name"] = user.full_name
            session["role"] = user.role

            flash(f"Welcome {user.full_name}!", "success")

            if user.role == "admin":
                return redirect(url_for("admin.panel"))
            return redirect(url_for("dashboard.home"))

        flash("Invalid credentials.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("name", "").strip()
        identifier = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "")
        blood_group = request.form.get("blood_group", "")
        dob = request.form.get("dob", "")
        address = request.form.get("address", "").strip()
        latitude = request.form.get("latitude", "")
        longitude = request.form.get("longitude", "")

        email = identifier if "@" in identifier else ""
        phone = identifier if "@" not in identifier else ""

        if not full_name or not identifier or len(password) < 8:
            flash("Invalid input data.", "danger")
            return render_template("auth/register.html")

        try:
            if (email and User.find_by_email(email)) or (phone and User.find_by_phone(phone)):
                flash("User already exists.", "warning")
                return render_template("auth/register.html")

            db = get_db()
            hashed = generate_password_hash(password)
            db.execute(
                """
                INSERT INTO users (full_name, email, phone, password_hash, role, blood_group, date_of_birth, address, latitude, longitude)
                VALUES (?, ?, ?, ?, 'user', ?, ?, ?, ?, ?)
                """,
                (full_name, email, phone, hashed, blood_group, dob, address, latitude, longitude)
            )
            db.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            current_app.logger.error(f"REGISTER ERROR: {e}")
            flash("Server error during registration.", "danger")

    return render_template("auth/register.html")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if not email:
            flash("Please provide your email.", "danger")
            return render_template("auth/forgot_password.html")

        try:
            user = User.find_by_email(email)

            if not user:
                flash("No account found.", "danger")
                return render_template("auth/forgot_password.html")

            token = secrets.token_urlsafe(32)
            expires_at = int((datetime.utcnow() + timedelta(minutes=30)).timestamp())

            db = get_db()
            db.execute(
                "UPDATE users SET reset_token = ?, reset_token_expiry = ? WHERE id = ?",
                (token, expires_at, user.id)
            )
            db.commit()

            reset_url = url_for("auth.reset_password", token=token, _external=True)
            mail = Mail(current_app)
            msg = Message(
                subject="Flexi Health - Password Reset",
                recipients=[email],
                body=f"Reset your password: {reset_url}"
            )
            mail.send(msg)

            flash("Reset link sent to email.", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            current_app.logger.error(f"FORGOT ERROR: {e}")
            flash("Failed to send email.", "danger")

    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    db = get_db()
    import time

    reset = db.execute(
        "SELECT * FROM users WHERE reset_token = ? AND reset_token_expiry > ?",
        (token, int(time.time()))
    ).fetchone()

    if not reset:
        flash("Invalid or expired link.", "danger")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if len(password) < 8:
            flash("Password too short.", "danger")
            return render_template("auth/reset_password.html", token=token)

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("auth/reset_password.html", token=token)

        hashed = generate_password_hash(password)
        db.execute(
            "UPDATE users SET password_hash = ?, reset_token = NULL, reset_token_expiry = NULL WHERE id = ?",
            (hashed, reset["id"])
        )
        db.commit()

        flash("Password reset successful.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", token=token)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))
