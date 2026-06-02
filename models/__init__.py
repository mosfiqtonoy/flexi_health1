"""
Flexi Health - Models Package

This package contains all database models used in:
- Web application (Flask UI)
- REST API (mobile/future apps)

Design goals:
- Clean imports
- Scalable architecture
- Easy extension for new models
"""

# =========================
# CORE MODELS
# =========================
from .user import User

# Future models can be added like:
# from .health import HealthRecord
# from .payment import Payment
# from .request import ServiceRequest

# =========================
# PUBLIC EXPORTS
# =========================
__all__ = [
    "User",
]
