import sqlite3
import os
from flask import g, current_app


def get_db():
    if "db" not in g:
        db_path = current_app.config.get("DATABASE")

        if not db_path:
            raise Exception("DATABASE not configured in app")

        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db(app):
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()

        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "schema.sql"
        )

        if not os.path.exists(schema_path):
            raise FileNotFoundError("schema.sql missing")

        with open(schema_path, "r", encoding="utf-8") as f:
            db.executescript(f.read())

        db.commit()
