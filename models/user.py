
     # ==========================================================
# USER MODEL - DATABASE LAYER (CLEAN + SAFE VERSION)
# ==========================================================

import sqlite3
import logging
from werkzeug.security import generate_password_hash
from utils.db import get_db


# ---------------- LOGGER ----------------
logger = logging.getLogger(__name__)


# ==========================================================
# USER MODEL CLASS
# ==========================================================
class User:
    """
    Handles all database operations for users:
    - Create user
    - Find by email
    - Find by phone
    - Find by ID
    """

    def __init__(self, id, name, email, phone, password, role, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.role = role
        self.created_at = created_at


    # ======================================================
    # CREATE USER
    # ======================================================
    @staticmethod
    def create(name, email, phone, password, role='user'):
        """
        Inserts new user safely into database.
        Returns: new user id OR False if failed
        """

        try:
            hashed_password = generate_password_hash(
                password,
                method='pbkdf2:sha256',
                salt_length=16
            )

            db = get_db()

            cursor = db.execute(
                """
                INSERT INTO users (name, email, phone, password, role)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, email, phone, hashed_password, role)
            )

            db.commit()

            user_id = cursor.lastrowid
            logger.info(f"User created successfully: {email}")

            return user_id

        # ---------------- DUPLICATE ERROR ----------------
        except sqlite3.IntegrityError:
            logger.warning(f"Duplicate user attempt: {email} / {phone}")
            return False

        # ---------------- GENERAL ERROR (SAFE) ----------------
        except Exception as e:
            logger.error(f"User creation failed: {str(e)}")
            return False


    # ======================================================
    # FIND BY EMAIL
    # ======================================================
    @staticmethod
    def find_by_email(email):
        try:
            db = get_db()
            return db.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()

        except Exception as e:
            logger.error(f"Email lookup failed: {str(e)}")
            return None


    # ======================================================
    # FIND BY PHONE
    # ======================================================
    @staticmethod
    def find_by_phone(phone):
        try:
            db = get_db()
            return db.execute(
                "SELECT * FROM users WHERE phone = ?",
                (phone,)
            ).fetchone()

        except Exception as e:
            logger.error(f"Phone lookup failed: {str(e)}")
            return None


    # ======================================================
    # FIND BY ID
    # ======================================================
    @staticmethod
    def find_by_id(user_id):
        try:
            db = get_db()
            return db.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()

        except Exception as e:
            logger.error(f"ID lookup failed: {str(e)}")
            return None
