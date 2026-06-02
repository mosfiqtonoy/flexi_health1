import sqlite3
import os
from flask import g, current_app


# =========================
# DATABASE CONNECTION
# =========================
def get_db():
    if "db" not in g:
        try:
            g.db = sqlite3.connect(
                current_app.config["DATABASE"],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        except Exception as e:
            raise Exception(f"Database connection failed: {e}")

    return g.db


# =========================
# CLOSE CONNECTION
# =========================
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# =========================
# INIT DATABASE
# =========================
def init_db(app):
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()

        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "schema.sql"
        )

        if not os.path.exists(schema_path):
            raise FileNotFoundError("schema.sql not found")

        with open(schema_path, "r", encoding="utf-8") as f:
            db.executescript(f.read())

        db.commit()
