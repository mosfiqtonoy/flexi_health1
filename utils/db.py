import sqlite3
import os
from flask import g, current_app

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def get_db():
    if "db" not in g:
        db_path = current_app.config.get("DATABASE", "flexi_health.db")
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

# -------------------------------
# CLOSE DB AFTER REQUEST
# -------------------------------
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# -------------------------------
# INITIALIZE DATABASE
# -------------------------------
def init_db(app):
    app.teardown_appcontext(close_db)
    schema_path = os.path.join(app.root_path, "schema.sql")
    try:
        with app.app_context():
            db = get_db()
            if not os.path.exists(schema_path):
                print("DB INIT ERROR: schema.sql not found at", schema_path)
                return

            # ✅ Check if DB already initialized
            cursor = db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = cursor.fetchall()
            if tables:
                print("✅ Database already exists, skipping init")
                return

            with open(schema_path, "r", encoding="utf-8") as f:
                db.executescript(f.read())
            db.commit()
            print("✅ Database initialized successfully")
    except Exception as e:
        print("❌ DB INIT ERROR:", str(e))
