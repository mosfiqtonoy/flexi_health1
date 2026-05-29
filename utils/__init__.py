# utils/__init__.py
"""
Utils Package Initializer.
Exposes database utilities and security decorators globally for cleaner import paths.
"""

from .db import get_db, init_db, close_db
from .security import login_required, admin_required

# Defines the public interface of the package when using 'from utils import *'
__all__ = [
    'get_db',
    'init_db',
    'close_db',
    'login_required',
    'admin_required'
]
