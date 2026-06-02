# config.py

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ---------------- CORE ----------------
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "change-this-in-production")

    # ---------------- DATABASE ----------------
    # Render + production friendly fix
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "flexi_health.db")
    )

    # ---------------- SESSION ----------------
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # production এ True করতে হবে (HTTPS)
    SESSION_COOKIE_SAMESITE = "Lax"

    # ---------------- PAYMENT (optional) ----------------
    SSLCOMMERZ_STORE_ID = os.environ.get("SSLCOMMERZ_STORE_ID")
    SSLCOMMERZ_STORE_PASSWORD = os.environ.get("SSLCOMMERZ_STORE_PASSWORD")

    # ---------------- MAIL ----------------
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # IMPORTANT FIX
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # HTTPS required


class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"


config_dict = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
    "test": TestingConfig,
    "default": DevelopmentConfig,
}
