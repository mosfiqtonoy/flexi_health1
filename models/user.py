
   from utils.db import get_db


class User:
    def __init__(self, row):
        if not row:
            raise ValueError("User row cannot be None")

        self.id = row["id"]
        self.full_name = row["full_name"]
        self.email = row["email"]
        self.phone = row["phone"]
        self.password_hash = row["password_hash"]
        self.role = row["role"]
        self.balance = row["balance"]
        self.is_active = row["is_active"]

        self.date_of_birth = row["date_of_birth"]
        self.blood_group = row["blood_group"]
        self.address = row["address"]
        self.latitude = row["latitude"]
        self.longitude = row["longitude"]

        self.created_at = row["created_at"]

    # =========================
    # FIXED FIND METHODS (IMPORTANT)
    # =========================
    @staticmethod
    def find_by_email(email):
        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        return User(row) if row else None

    @staticmethod
    def find_by_phone(phone):
        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE phone = ?",
            (phone,)
        ).fetchone()
        return User(row) if row else None

    @staticmethod
    def find_by_id(user_id):
        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        return User(row) if row else None
