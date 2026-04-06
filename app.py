"""Application entry point and factory."""

import os
from flask import Flask, current_app
from werkzeug.security import generate_password_hash

from config import Config
from extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID for Flask-Login session handling."""
    from models.user_model import User
    return User.query.get(int(user_id))

def initialize_database():
    """Create database tables and ensure a default admin user exists."""
    from models.user_model import User

    db.create_all()

    # Fallback to 'admin.sys' if not defined in config
    username = current_app.config.get("ADMIN_DEFAULT_USERNAME", "admin.sys")
    existing_admin = User.query.filter_by(username=username).first()
    
    if existing_admin:
        # Ensure the existing admin has the correct role if upgrading an old DB
        if existing_admin.role != "SuperAdmin":
            existing_admin.role = "SuperAdmin"
            db.session.commit()
        return

    # Fallback to a default password if not in config
    password = current_app.config.get("ADMIN_DEFAULT_PASSWORD", "SuperSecretBank123!")

    admin_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role="SuperAdmin" # Assigning the master clearance level
    )
    db.session.add(admin_user)
    db.session.commit()
    print(f"Default SuperAdmin '{username}' provisioned.")

def register_cli_commands(app):
    """Register CLI helpers for operational tasks."""
    @app.cli.command("init-db")
    def init_db_command():
        """Initialize database tables and default data."""
        with app.app_context():
            initialize_database()
        print("Database initialized successfully.")

def register_blueprints(app):
    """Register all route blueprints."""
    from routes.auth_routes import auth_bp
    from routes.backup_routes import backup_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.recovery_routes import recovery_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(backup_bp)
    app.register_blueprint(recovery_bp)

def create_app():
    """Create and configure the Flask application instance."""
    
    # BULLETPROOF FIX: Force absolute paths so Flask never loses the templates
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, 
                template_folder=os.path.join(BASE_DIR, 'templates'),
                static_folder=os.path.join(BASE_DIR, 'static'))
    
    app.config.from_object(Config)

    os.makedirs(app.config.get("UPLOAD_FOLDER", "backups"), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    register_blueprints(app)
    register_cli_commands(app)

    with app.app_context():
        initialize_database()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)