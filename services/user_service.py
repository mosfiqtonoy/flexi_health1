
   from utils.db import get_db
from models.user import User


# =========================
# GET USER PROFILE
# =========================
def get_user_profile(user_id):
    db = get_db()

    row = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    return User(row) if row else None


# =========================
# UPDATE USER PROFILE
# =========================
def update_user_profile(user_id, full_name, phone):
    db = get_db()

    # check duplicate phone
    existing = db.execute(
        "SELECT id FROM users WHERE phone = ? AND id != ?",
        (phone, user_id)
    ).fetchone()

    if existing:
        return False, "Phone number already in use."

    db.execute(
        """
        UPDATE users
        SET full_name = ?, phone = ?
        WHERE id = ?
        """,
        (full_name, phone, user_id)
    )

    db.commit()
    return True, "Profile updated successfully."


# =========================
# GET ALL USERS  (🔥 FIX FOR YOUR ERROR)
# =========================
def get_all_users():
    db = get_db()

    rows = db.execute(
        "SELECT * FROM users ORDER BY id DESC"
    ).fetchall()

    return [dict(row) for row in rows]


# =========================
# RECHARGE SYSTEM
# =========================
def add_recharge(user_id, amount, operator):
    SAVINGS_RATE = 0.05
    saved_amount = round(amount * SAVINGS_RATE, 2)

    db = get_db()

    db.execute(
        """
        INSERT INTO recharge_history
        (user_id, amount, saved_amount, operator, status)
        VALUES (?, ?, ?, ?, 'completed')
        """,
        (user_id, amount, saved_amount, operator)
    )

    db.execute(
        """
        UPDATE users
        SET balance = balance + ?
        WHERE id = ?
        """,
        (saved_amount, user_id)
    )

    db.commit()
    return saved_amount


# =========================
# RECHARGE HISTORY
# =========================
def get_recharge_history(user_id, limit=20):
    db = get_db()

    rows = db.execute(
        """
        SELECT * FROM recharge_history
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, limit)
    ).fetchall()

    return [dict(row) for row in rows]
