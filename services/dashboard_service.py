from utils.db import get_db
from models.user import User


# =========================
# HEALTH RECORDS
# =========================
def add_health_record(user_id, weight, height, bp_sys, bp_dia, blood_type, notes):
    try:
        db = get_db()
        db.execute(
            """
            INSERT INTO health_records
            (user_id, weight, height,
             blood_pressure_systolic,
             blood_pressure_diastolic,
             blood_type, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                weight or None,
                height or None,
                bp_sys or None,
                bp_dia or None,
                blood_type or None,
                notes or None
            )
        )
        db.commit()
        return True
    except Exception:
        return False


def get_health_records(user_id, limit=20):
    try:
        db = get_db()
        rows = db.execute(
            """
            SELECT * FROM health_records
            WHERE user_id = ?
            ORDER BY recorded_at DESC
            LIMIT ?
            """,
            (user_id, limit)
        ).fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []


def get_latest_health_record(user_id):
    try:
        db = get_db()
        row = db.execute(
            """
            SELECT * FROM health_records
            WHERE user_id = ?
            ORDER BY recorded_at DESC
            LIMIT 1
            """,
            (user_id,)
        ).fetchone()
        return dict(row) if row else None
    except Exception:
        return None


# =========================
# SERVICE REQUEST
# =========================
def submit_service_request(user_id, service_type, description, amount_used=0.0):
    try:
        user = User.find_by_id(user_id)  # FIXED: was get_by_id

        if not user:
            return False, "User not found."

        try:
            amount_used = float(amount_used or 0)
        except (TypeError, ValueError):
            amount_used = 0.0

        if amount_used > 0 and user.balance < amount_used:
            return False, "Insufficient balance."

        db = get_db()
        db.execute(
            """
            INSERT INTO service_requests
            (user_id, service_type, description, amount_used)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, service_type, description, amount_used)
        )

        if amount_used > 0:
            db.execute(
                "UPDATE users SET balance = balance - ? WHERE id = ?",
                (amount_used, user_id)
            )

        db.commit()
        return True, "Service request submitted."

    except Exception:
        return False, "Failed to submit request."


def get_service_requests(user_id):
    try:
        db = get_db()
        rows = db.execute(
            """
            SELECT * FROM service_requests
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []


def get_all_service_requests():
    try:
        db = get_db()
        rows = db.execute(
            """
            SELECT sr.*, u.full_name, u.email
            FROM service_requests sr
            JOIN users u ON sr.user_id = u.id
            ORDER BY sr.created_at DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []


# =========================
# STATUS UPDATE
# =========================
def update_service_request_status(request_id, status):
    try:
        allowed_status = {"pending", "in_progress", "completed", "rejected"}

        if status not in allowed_status:
            return False

        db = get_db()
        db.execute(
            """
            UPDATE service_requests
            SET status = ?,
                updated_at = strftime('%s','now')
            WHERE id = ?
            """,
            (status, request_id)
        )
        db.commit()
        return True
    except Exception:
        return False


# =========================
# DASHBOARD SUMMARY
# =========================
def get_dashboard_summary(user_id):
    try:
        db = get_db()

        health_count = db.execute(
            "SELECT COUNT(*) FROM health_records WHERE user_id = ?",
            (user_id,)
        ).fetchone()[0]

        request_count = db.execute(
            "SELECT COUNT(*) FROM service_requests WHERE user_id = ?",
            (user_id,)
        ).fetchone()[0]

        recharge_total = db.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM recharge_history WHERE user_id = ?",
            (user_id,)
        ).fetchone()[0]

        user = User.find_by_id(user_id)  # FIXED: was get_by_id

        return {
            "health_records": health_count,
            "service_requests": request_count,
            "total_recharged": recharge_total,
            "balance": user.balance if user else 0
        }

    except Exception:
        return {
            "health_records": 0,
            "service_requests": 0,
            "total_recharged": 0,
            "balance": 0
        }
