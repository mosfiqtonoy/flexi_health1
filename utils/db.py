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
# INITIALIZE DATABASE (FIXED)
# -------------------------------
def init_db(app):
    app.teardown_appcontext(close_db)

    schema_path = os.path.join(app.root_path, "schema.sql")

    try:
        # check schema file
        if not os.path.exists(schema_path):
            print("❌ DB INIT ERROR: schema.sql not found at", schema_path)
            return

        # connect database
        db_path = app.config.get("DATABASE", "flexi_health.db")
        db = sqlite3.connect(db_path)

        # execute schema
        with open(schema_path, "r", encoding="utf-8") as f:
            db.executescript(f.read())

        db.commit()
        db.close()

        print("✅ Database initialized successfully")

    except Exception as e:
        print("❌ DB INIT ERROR:", str(e))
