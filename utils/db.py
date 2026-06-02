import sqlite3
import os
from flask import g, current_app


# =========================
# DATABASE CONNECTION
# =========================
def get_db():
    if "db" not in g:
        db_path = current_app.config.get("DATABASE")

        if not db_path:
            raise Exception("DATABASE config missing")

        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

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

    schema_path = os.path.join(
        app.root_path,
        "schema.sql"
    )

    if not os.path.exists(schema_path):
        raise FileNotFoundError("schema.sql not found")

    with open(schema_path, "r", encoding="utf-8") as f:
        db = sqlite3.connect(
            app.config["DATABASE"]
        )
        db.executescript(f.read())
        db.commit()
        db.close()
