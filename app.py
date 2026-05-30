# app.py

import logging
from flask import Flask, redirect, url_for, session, render_template
from flask_mail import Mail
from config import Config
from utils.db import init_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp
from routes.payment import payment_bp

mail = Mail()

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    configure_logging()

    # Flask-Mail init
    mail.init_app(app)

    # database init
    init_db(app)

    # blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(payment_bp, url_prefix='/payment')

    @app.route('/')
    def home():
        if 'user_id' in session:
            if session.get('user_role') == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('dashboard.user_dashboard'))
        return redirect(url_for('auth.login'))

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.warning(f"404 Error: {e}")
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"500 Error: {e}")
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden_access(e):
        app.logger.warning(f"403 Error: {e}")
        return render_template("errors/403.html"), 403

    @app.after_request
    def inject_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
