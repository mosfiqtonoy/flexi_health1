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

    @staticmethod
    def find_by_email(email):
        db = get_db()
        row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return User(row) if row else None

    @staticmethod
    def get_by_email(email):
        return User.find_by_email(email)

    @staticmethod
    def find_by_phone(phone):
        db = get_db()
        row = db.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
        return User(row) if row else None

    @staticmethod
    def get_by_phone(phone):
        return User.find_by_phone(phone)

    @staticmethod
    def find_by_id(user_id):
        db = get_db()
        row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return User(row) if row else None

    @staticmethod
    def get_by_reset_token(token):
        db = get_db()
        row = db.execute("SELECT * FROM users WHERE reset_token = ?", (token,)).fetchone()
        return User(row) if row else None
