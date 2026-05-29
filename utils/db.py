# utils/db.py
import sqlite3
from flask import g, current_app

def get_db():
    """Establishes and returns a unique, thread-safe database instance per request lifecycle."""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Enables access via key-mappings instead of array indexes
    return g.db

def close_db(e=None):
    """Automatically safely unhooks and disposes of database links on context termination."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """Attaches context teardown hooks and safely executes core table schema declarations."""
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()
