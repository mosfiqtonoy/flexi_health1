
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

        # Extended profile fields (Flexi Health)
        self.date_of_birth = row["date_of_birth"]
        self.blood_group = row["blood_group"]
        self.address = row["address"]
        self.latitude = row["latitude"]
        self.longitude = row["longitude"]

        self.created_at = row["created_at"]

    # =========================
    # FETCH METHODS
    # =========================
    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        return User(row) if row else None

    @staticmethod
    def get_by_email(email):
        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        return User(row) if row else None

    @staticmethod
    def get_by_phone(phone):
        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE phone = ?",
            (phone,)
        ).fetchone()
        return User(row) if row else None

    @staticmethod
    def get_by_reset_token(token):
        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE reset_token = ?",
            (token,)
        ).fetchone()
        return User(row) if row else None

    @staticmethod
    def get_all():
        db = get_db()
        rows = db.execute(
            "SELECT * FROM users ORDER BY created_at DESC"
        ).fetchall()
        return [User(r) for r in rows]

    @staticmethod
    def count():
        db = get_db()
        return db.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

    # =========================
    # UPDATE METHODS (NEW)
    # =========================
    def update_balance(self, new_balance):
        db = get_db()
        db.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (new_balance, self.id)
        )
        db.commit()
        self.balance = new_balance

    def update_profile(self, **kwargs):
        allowed_fields = [
            "full_name",
            "phone",
            "date_of_birth",
            "blood_group",
            "address",
            "latitude",
            "longitude"
        ]

        fields = []
        values = []

        for key in allowed_fields:
            if key in kwargs:
                fields.append(f"{key} = ?")
                values.append(kwargs[key])

        if not fields:
            return False

        values.append(self.id)

        db = get_db()
        db.execute(
            f"UPDATE users SET {', '.join(fields)} WHERE id = ?",
            values
        )
        db.commit()

        return True

    # =========================
    # SERIALIZATION (API READY)
    # =========================
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,

            "role": self.role,
            "balance": self.balance,
            "is_active": self.is_active,

            "date_of_birth": self.date_of_birth,
            "blood_group": self.blood_group,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,

            "created_at": self.created_at
        }
