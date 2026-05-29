
            # models/user.py
import sqlite3
import logging
from werkzeug.security import generate_password_hash
from utils.db import get_db

# Initialize logger for tracking data tier exceptions
logger = logging.getLogger(__name__)

class User:
    """
    Hero-Level User Model Data Gateway.
    Encapsulates all database operations, encryption logic, and schema mappings for Users.
    """
    
    # MODIFIED: __init__ updated to include phone
    def __init__(self, id, name, email, phone, password, role, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.role = role
        self.created_at = created_at

    @staticmethod
    def create(name, email, phone, password, role='user'):
        """
        Applies secure PBKDF2 cryptographic hashing and injects a new user record into storage.
        """
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        
        try:
            db = get_db()
            # MODIFIED: Added phone field to the insertion schema
            cursor = db.execute(
                "INSERT INTO users (name, email, phone, password, role) VALUES (?, ?, ?, ?, ?)",
                (name, email, phone, hashed_password, role)
            )
            db.commit()
            logger.info(f"Successfully instantiated a new user account profile for: {phone}")
            return cursor.lastrowid # Returns new ID for savings account initiation
        except sqlite3.IntegrityError:
            logger.warning(f"Registration conflict: Identity verification failure for duplicate identity.")
            return False
        except Exception as e:
            logger.error(f"Critical operational database fault during registration: {e}")
            raise e

    @staticmethod
    def find_by_email(email):
        """Maps database rows for email-based identity retrieval."""
        try:
            db = get_db()
            return db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        except Exception as e:
            logger.error(f"Failed to query database user matrix for email {email}: {e}")
            return None

    # NEW: Added for SIM-centric business model
    @staticmethod
    def find_by_phone(phone):
        """Scans system for unique phone identifier."""
        try:
            db = get_db()
            return db.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
        except Exception as e:
            logger.error(f"Failed to query database user matrix for phone {phone}: {e}")
            return None

    @staticmethod
    def find_by_id(user_id):
        """Fetches user data by the distinct primary key ID."""
        try:
            db = get_db()
            return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        except Exception as e:
            logger.error(f"Failed to query database user matrix for ID {user_id}: {e}")
            return None
