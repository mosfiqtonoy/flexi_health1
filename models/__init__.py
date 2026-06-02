"""
Flexi Health - Models Package
Central model registry for:
- Flask Web App
- REST API layer
- Future mobile apps
Keeps imports clean and scalable.
"""

# =========================
# CORE MODELS
# =========================
from .user import User

# -------------------------
# FUTURE MODELS (SAFE PLACEHOLDERS)
# -------------------------
# from .health import HealthRecord
# from .payment import Payment
# from .request import ServiceRequest

# =========================
# PUBLIC EXPORTS
# =========================
__all__ = [
    "User",
]
