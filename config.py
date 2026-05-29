import os
from datetime import timedelta

# Define the base directory of the project for absolute path references
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class. 
    Contains settings universal to all environments.
    """
    # Security: Use a strong secret key from environment or fallback to a safe default
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "hero_default_77x_shield")
    
    # Database: Default SQLite path
    DATABASE = os.environ.get("DATABASE_URL", os.path.join(BASE_DIR, "users.db"))
    
    # Session Security: Sessions expire in 30 minutes
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Cookie Security: Prevents JavaScript from accessing cookies (XSS protection)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in Production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Configurations for Local Development."""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Configurations for Live Production Server."""
    DEBUG = False
    ENV = 'production'
    # Strict Security for Production
    SESSION_COOKIE_SECURE = True  # Requires HTTPS
    # Use a more robust DB like PostgreSQL in production if needed
    
class TestingConfig(Config):
    """Configurations for Automated Unit Tests."""
    TESTING = True
    DATABASE = ":memory:"  # Uses fast in-memory DB for tests

# Mapping configurations to a dictionary for easy access in app.py
config_dict = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig,
    'default': DevelopmentConfig
}
