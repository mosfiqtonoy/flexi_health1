import sqlite3
import os
from flask import g, current_app


# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def get_db():
    if "db" not in g:
        db_path = current_app.config.get("DATABASE", "flexi_health.db")

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")

        g.db = conn

    return g.db


# -------------------------------
# CLOSE DATABASE CONNECTION
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

    if not os.path.exists(schema_path):
        print("❌ schema.sql not found at:", schema_path)
        return

    try:
        db_path = app.config.get("DATABASE", "flexi_health.db")

        # safe initialization
        with sqlite3.connect(db_path) as db:
            with open(schema_path, "r", encoding="utf-8") as f:
                db.executescript(f.read())

        print("✅ Database initialized successfully")

    except Exception as e:
        print("❌ DB INIT ERROR:", str(e))
