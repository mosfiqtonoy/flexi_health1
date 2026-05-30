import logging
from flask import Flask, redirect, url_for, session, render_template

from config import Config
from utils.db import init_db

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp
from routes.payment import payment_bp


# ---------------- LOGGING ----------------
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )


# ---------------- APP FACTORY ----------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    configure_logging()

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(payment_bp, url_prefix="/payment")

    # Home route
    @app.route("/")
    def home():
        if "user_id" in session:
            if session.get("user_role") == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            return redirect(url_for("dashboard.user_dashboard"))
        return redirect(url_for("auth.login"))

    # Error handlers (debug friendly)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden_access(e):
        return render_template("errors/403.html"), 403

    return app


# ---------------- CREATE APP ----------------
app = create_app()

# ---------------- DB INIT (IMPORTANT FIX) ----------------
with app.app_context():
    init_db(app)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
