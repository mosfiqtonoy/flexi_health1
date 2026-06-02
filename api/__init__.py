"""
Flexi Health API Package
Contains all REST API blueprints for mobile + frontend apps.
"""

from .auth_api import auth_api_bp
from .user_api import user_api_bp
from .dashboard_api import dashboard_api_bp

__all__ = [
    "auth_api_bp",
    "user_api_bp",
    "dashboard_api_bp"
]
