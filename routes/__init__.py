"""
Routes Package Mapping Specification.
Consolidates scattered feature components to secure optimal modular control.
"""
from .auth import auth_bp
from .dashboard import dashboard_bp
from .admin import admin_bp

# Structural mapping loop for app.py processing pipeline
# Empty strings '' mean the blueprint mounts directly to the root URL context
all_blueprints = [
    (auth_bp, '/auth'),
    (dashboard_bp, ''),
    (admin_bp, '')
]
