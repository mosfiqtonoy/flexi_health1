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
    
    def __init__(self, id, name, email, password, role, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at

    @staticmethod
    def create(name, email, password, role='user'):
        """
        Applies secure PBKDF2 cryptographic hashing and injects a new user record into storage.
        Returns True if successful, False if the email is a duplicate.
        """
        # Enterprise-grade hashing parameters (PBKDF2 with strong 16-byte salt)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        
        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, hashed_password, role)
            )
            db.commit()
            logger.info(f"Successfully instantiated a new user account profile for: {email}")
            return True
        except sqlite3.IntegrityError:
            # Handles UNIQUE constraint failure for the email column gracefully
            logger.warning(f"Registration conflict: Identity verification failure for duplicate email: {email}")
            return False
        except Exception as e:
            logger.error(f"Critical operational database fault during registration: {e}")
            raise e

    @staticmethod
    def find_by_email(email):
        """
        Scans the system storage repository and maps database rows to a clean dictionary object.
        Returns a sqlite3.Row object if found, else None.
        """
        try:
            db = get_db()
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return user
        except Exception as e:
            logger.error(f"Failed to query database user matrix for email {email}: {e}")
            return None

    @staticmethod
    def find_by_id(user_id):
        """
        Fetches user data by the distinct primary key ID. Useful for secure session validation.
        """
        try:
            db = get_db()
            return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        except Exception as e:
            logger.error(f"Failed to query database user matrix for ID {user_id}: {e}")
            return None
