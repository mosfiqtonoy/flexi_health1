
        import sqlite3
import os
from flask import g, current_app

def get_db():
    if "db" not in g:
        db_path = current_app.config.get("DATABASE", "flexi_health.db")
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        schema_path = os.path.join(app.root_path, "schema.sql")
        with open(schema_path, "r") as f:
            db.executescript(f.read())
        db.commit()
