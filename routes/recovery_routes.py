"""Disaster recovery simulation routes."""

from routes.auth_routes import admin_required, operator_required
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from extensions import db
from models.backup_model import Backup
from models.recovery_model import RecoveryLog
from services.backup_service import ARCHIVED_PREFIX, restore_from_trash
from services.recovery_service import execute_recovery


recovery_bp = Blueprint("recovery", __name__, url_prefix="/recovery")


@recovery_bp.route("/", methods=["GET", "POST"])
@login_required
def recovery_page():
    """Simulate restore operations and display history logs."""
    if request.method == "POST":
        backup_id = request.form.get("backup_id", type=int)
        if not backup_id:
            flash("Please select a backup to restore.", "danger")
            return redirect(url_for("recovery.recovery_page"))

        backup_record = Backup.query.get_or_404(backup_id)
        recovery_log = execute_recovery(db.session, backup_record)
        flash(
            f"Recovery simulation completed for '{backup_record.filename}' with status: {recovery_log.status}.",
            "success" if recovery_log.status == "SUCCESS" else "warning",
        )
        return redirect(url_for("recovery.recovery_page"))

    # Active backups for recovery operations (not deleted, not archived)
    active_backups = (
        Backup.query.filter(
            ~Backup.filename.like(f"{ARCHIVED_PREFIX}%"),
            Backup.deleted_at.is_(None)
        )
        .order_by(Backup.upload_date.desc())
        .all()
    )
    # Trashed backups available for recovery
    trashed_backups = (
        Backup.query.filter(Backup.deleted_at.isnot(None))
        .order_by(Backup.deleted_at.desc())
        .all()
    )
    recovery_logs = RecoveryLog.query.order_by(RecoveryLog.recovery_time.desc()).all()

    return render_template(
        "recovery.html",
        backups=active_backups,
        trashed_backups=trashed_backups,
        recovery_logs=recovery_logs,
    )


@recovery_bp.route("/recover-from-trash/<int:backup_id>", methods=["POST"])
@login_required
def recover_from_trash(backup_id):
    """Recover a permanently deleted backup from trash."""
    backup_record = Backup.query.get_or_404(backup_id)

    restore_from_trash(db.session, backup_record)
    flash(f"Backup '{backup_record.filename}' recovered and ready for recovery operations.", "success")
    return redirect(url_for("recovery.recovery_page"))
