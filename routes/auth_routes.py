"""Authentication routes."""

from functools import wraps
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models.user_model import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# --- RBAC Decorators ---
def admin_required(f):
    """Decorator to enforce SuperAdmin clearance."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_superadmin:
            flash("Clearance Denied: SuperAdmin authorization required.", "danger")
            return redirect(url_for('dashboard.home'))
        return f(*args, **kwargs)
    return decorated_function

def operator_required(f):
    """Decorator to enforce at least Operator clearance."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_operator_or_higher:
            flash("Clearance Denied: Operator authorization required to execute actions.", "warning")
            return redirect(url_for('dashboard.home'))
        return f(*args, **kwargs)
    return decorated_function
# -----------------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate enterprise users."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f"Authentication verified. Logged in as {user.role}.", "success")
            return redirect(url_for("dashboard.home"))

        flash("Invalid operator credentials.", "danger")

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
@login_required
@admin_required
def register():
    """Provision a new user account (SuperAdmin Only)."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "Auditor") 

        if not username or not password:
            flash("Operator ID and Passphrase are required.", "danger")
            return redirect(url_for("auth.register"))

        if role not in ["SuperAdmin", "Operator", "Auditor"]:
            flash("Invalid clearance level selected.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Operator ID already provisioned in the system.", "warning")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()

        flash(f"Successfully provisioned {role} account for {username}.", "success")
        return redirect(url_for("auth.register")) 

    return render_template("register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    """Terminate current user session."""
    logout_user()
    flash("Secure session terminated successfully.", "info")
    return redirect(url_for("auth.login"))