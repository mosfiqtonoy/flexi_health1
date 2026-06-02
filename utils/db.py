import sqlite3
import os
from flask import g, current_app


# =========================
# DATABASE CONNECTION
# =========================
def get_db():
    if "db" not in g:
        try:
            db_path = current_app.config.get("DATABASE")

            if not db_path:
                raise Exception("DATABASE config not found")

            g.db = sqlite3.connect(
                db_path,
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
# INIT DATABASE (SAFE)
# =========================
def init_db(app):
    app.teardown_appcontext(close_db)

    schema_path = os.path.join(
        app.root_path,
        "schema.sql"
    )

    if not os.path.exists(schema_path):
        raise FileNotFoundError("schema
