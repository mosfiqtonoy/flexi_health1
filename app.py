from flask import Flask, render_template
from config import Config
from utils.db import init_db


# =========================
# APP FACTORY
# =========================
def create_app():
    app = Flask(__name__)

    # =========================
    # CONFIG LOAD
    # =========================
    app.config.from_object(Config)

    # =========================
    # SAFE DB INIT
    # =========================
    init_database(app)

    # =========================
    # REGISTER BLUEPRINTS
    # =========================
    register_blueprints(app)

    # =========================
    # ERROR HANDLERS
    # =========================
    register_error_handlers(app)

    return app


# =========================
# DATABASE INIT WRAPPER
# =========================
def init_database(app):
    try:
        init_db(app)
        print("[DB] Initialized successfully")
    except Exception as e:
        print(f"[DB WARNING] {e}")


# =========================
# BLUEPRINT REGISTRATION
# =========================
def register_blueprints(app):
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.admin import admin_bp

    from api.auth_api import auth_api_bp
    from api.user_api import user_api_bp
    from api.dashboard_api import dashboard_api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)

    app.register_blueprint(auth_api_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_api_bp, url_prefix='/api/v1/user')
    app.register_blueprint(dashboard_api_bp, url_prefix='/api/v1/dashboard')


# =========================
# ERROR HANDLERS
# =========================
def register_error_handlers(app):

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500


# =========================
# APP INSTANCE
# =========================
app = create_app()


# =========================
# LOCAL DEV
