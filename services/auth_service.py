import time
from utils.db import get_db
from utils.security import (
    hash_password,
    check_password,
    generate_token,
    token_expiry
)
from models.user import User

# =========================
# REGISTER USER
# =========================
def register_user(full_name, email, phone, password, blood_group="", dob="", address="", latitude="", longitude=""):
    try:
        db = get_db()

        email = email.strip().lower()
        phone = phone.strip()

        # check existing user
        if User.get_by_email(email):
            return False, "Email already registered."

        if User.get_by_phone(phone):
            return False, "Phone number already registered."

        if len(password or "") < 8:
            return False, "Password too weak."

        pw_hash = hash_password(password)

        db.execute(
            """
            INSERT INTO users
            (full_name, email, phone, password_hash, blood_group, date_of_birth, address, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (full_name.strip(), email, phone, pw_hash, blood_group, dob, address, latitude, longitude)
        )

        db.commit()

        return True, "Registration successful."

    except Exception as e:
        print(f"Error during registration: {e}")
        return False, "Registration failed. Try again."


# =========================
# AUTHENTICATION
# =========================
def authenticate_user(email_or_phone, password):
    try:
        identifier = email_or_phone.strip()

        user = User.get_by_email(identifier.lower())

        if not user:
            user = User.get_by_phone(identifier)

        if not user:
            return None, "Invalid credentials."

        if not user.is_active:
            return None, "Account is deactivated."

        if not check_password(password, user.password_hash):
            return None, "Invalid credentials."

        return user, "Login successful."

    except Exception:
        return None, "Authentication error."


# =========================
# PASSWORD RESET INIT
# =========================
def initiate_password_reset(email):
    try:
        db = get_db()

        email = email.strip().lower()

        user = User.get_by_email(email)

        if not user:
            return False, "No account found with that email."

        token = generate_token()
        expiry = token_expiry(30)  # 30 min safer default

        db.execute(
            """
            UPDATE users
            SET reset_token = ?, reset_token_expiry = ?
            WHERE id = ?
            """,
            (token, expiry, user.id)
        )

        db.commit()

        return True, token

    except Exception:
        return False, "Failed to generate reset link."


# =========================
# PASSWORD RESET
# =========================
def reset_password(token, new_password):
    try:
        if len(new_password or "") < 8:
            return False, "Password too weak."

        user = User.get_by_reset_token(token)

        if not user:
            return False, "Invalid reset link."

        db = get_db()

        row = db.execute(
            """
            SELECT reset_token_expiry
            FROM users
            WHERE id = ?
            """,
            (user.id,)
        ).fetchone()

        if not row:
            return False, "Invalid reset session."

        if int(time.time()) > row["reset_token_expiry"]:
            return False, "Reset link expired."

        pw_hash = hash_password(new_password)

        db.execute(
            """
            UPDATE users
            SET password_hash = ?,
                reset_token = NULL,
                reset_token_expiry = NULL
            WHERE id = ?
            """,
            (pw_hash, user.id)
        )

        db.commit()

        return True, "Password reset successful."

    except Exception:
        return False, "Password reset failed."
