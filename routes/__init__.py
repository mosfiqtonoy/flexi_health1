"""
Routes Package Mapping Specification.
Consolidates scattered feature components to secure optimal modular control.
"""
from .auth import auth_bp
from .dashboard import dashboard_bp
from .admin import admin_bp
from .payment import payment_bp

all_blueprints = [
    (auth_bp, '/auth'),
    (dashboard_bp, ''),
    (admin_bp, ''),
    (payment_bp, '/payment')
]
