# app.py
import logging
from flask import Flask, redirect, url_for, session, render_template
from config import Config
from utils.db import init_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp

def configure_logging():
    """Configures system logs for monitoring incoming requests and runtime errors."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

def create_app():
    """
    Application Factory Pattern.
    Initializes configuration, registers blueprints, and hooks global middlewares.
    """
    app = Flask(__name__)
    
    # 1. Load Environment & System Configuration
    app.config.from_object(Config)

    # 2. Configure System Logger
    configure_logging()

    # 3. Initialize Database Lifecycle Hooks
    init_db(app)

    # 4. Register Industrial Blueprints with Isolated Namespaces
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)

    # 5. Root Entry Point Routing
    @app.route('/')
    def home():
        """Gatekeeper route to evaluate session state and route accordingly."""
        if 'user_id' in session:
            if session.get('user_role') == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('dashboard.user_dashboard'))
        return redirect(url_for('auth.login'))

    # 6. Global Error Handling Interceptors (Production Standard)
    @app.errorhandler(404)
    def page_not_found(e):
        """Gracefully handles missing endpoints."""
        app.logger.warning(f"404 Error encountered: {e}")
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        """Intercepts critical unhandled code execution failures."""
        app.logger.error(f"500 Internal Server Failure: {e}")
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden_access(e):
        """Intercepts unauthorized cross-role access breaches."""
        app.logger.warning(f"403 Forbidden Access Triggered: {e}")
        return render_template("errors/403.html"), 403

    # 7. Enterprise Security Protocols Middleware
    @app.after_request
    def inject_security_headers(response):
        """Appends strict HTTP security headers to fortify against XSS and Clickjacking."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    return app

# Generate the Production App instance
app = create_app()

if __name__ == "__main__":
    # Standard deployment runtime config for localized verification
    app.run(host='0.0.0.0', port=5000, debug=True)
