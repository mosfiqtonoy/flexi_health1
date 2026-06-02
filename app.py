from flask import Flask, render_template
from config import Config
from db import init_db   # adjust if needed

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # DB INIT (safe)
    with app.app_context():
        init_db(app)

    # Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.admin import admin_bp

    from api.auth_api import auth_api_bp
    from api.user_api import user_api_bp
    from api.dashboard_api import dashboard_api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)

    app.register_blueprint(auth_api_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_api_bp, url_prefix="/api/v1/user")
    app.register_blueprint(dashboard_api_bp, url_prefix="/api/v1/dashboard")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
