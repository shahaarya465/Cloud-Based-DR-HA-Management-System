"""Dashboard routes."""

from flask import Blueprint, render_template
from flask_login import login_required

from models.backup_model import Backup
from models.recovery_model import RecoveryLog


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def home():
    """Render portal dashboard with high-level stats."""
    total_backups = Backup.query.count()
    total_recoveries = RecoveryLog.query.count()
    recent_backups = Backup.query.order_by(Backup.upload_date.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_backups=total_backups,
        total_recoveries=total_recoveries,
        recent_backups=recent_backups,
    )
