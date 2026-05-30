# config.py

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "hero_default_77x_shield")
    DATABASE = os.environ.get("DATABASE_URL", "/tmp/flexi_health.db")
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SSLCOMMERZ_STORE_ID = os.environ.get("SSLCOMMERZ_STORE_ID", "teststore")
    SSLCOMMERZ_STORE_PASSWORD = os.environ.get("SSLCOMMERZ_STORE_PASSWORD", "testpass")

    # Gmail SMTP
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    TESTING = True
    DATABASE = ":memory:"

config_dict = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig,
    'default': DevelopmentConfig
}
