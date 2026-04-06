"""Backup management routes."""

from routes.auth_routes import admin_required, operator_required
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required

from extensions import db
from models.backup_model import Backup
from services.backup_service import (
    ARCHIVED_PREFIX,
    archive_backup_file,
    restore_backup_file,
    save_backup_file,
    soft_delete_backup,
)


backup_bp = Blueprint("backup", __name__, url_prefix="/backups")


@backup_bp.route("/", methods=["GET", "POST"])
@login_required
def manage_backups():
    """Upload backup files and list all backups."""
    if request.method == "POST":
        backup_file = request.files.get("backup_file")
        metadata, error = save_backup_file(
            backup_file,
            current_app.config["UPLOAD_FOLDER"],
            current_app.config["ALLOWED_EXTENSIONS"],
        )

        if error:
            flash(error, "danger")
            return redirect(url_for("backup.manage_backups"))

        backup_record = Backup(
            filename=metadata["filename"],
            file_size=metadata["file_size"],
        )
        db.session.add(backup_record)
        db.session.commit()
        flash("Backup uploaded successfully.", "success")
        return redirect(url_for("backup.manage_backups"))

    active_backups = (
        Backup.query.filter(
            ~Backup.filename.like(f"{ARCHIVED_PREFIX}%"),
            Backup.deleted_at.is_(None)
        )
        .order_by(Backup.upload_date.desc())
        .all()
    )
    archived_backups = (
        Backup.query.filter(
            Backup.filename.like(f"{ARCHIVED_PREFIX}%"),
            Backup.deleted_at.is_(None)
        )
        .order_by(Backup.upload_date.desc())
        .all()
    )
    return render_template(
        "backups.html",
        backups=active_backups,
        archived_backups=archived_backups,
    )


@backup_bp.route("/delete/<int:backup_id>", methods=["POST"])
@login_required
def delete_backup(backup_id):
    """Archive selected backup file and metadata for possible restoration."""
    backup_record = Backup.query.get_or_404(backup_id)

    archived_name, archived = archive_backup_file(
        backup_record.filename,
        current_app.config["UPLOAD_FOLDER"],
    )
    if not archived:
        flash("Backup file was not found on disk. Metadata kept unchanged.", "warning")
        return redirect(url_for("backup.manage_backups"))

    backup_record.filename = archived_name
    db.session.commit()

    flash("Backup archived. You can restore it anytime.", "info")
    return redirect(url_for("backup.manage_backups"))


@backup_bp.route("/restore/<int:backup_id>", methods=["POST"])
@login_required
def restore_backup(backup_id):
    """Restore an archived backup back to active backups list."""
    backup_record = Backup.query.get_or_404(backup_id)

    restored_name, restored = restore_backup_file(
        backup_record.filename,
        current_app.config["UPLOAD_FOLDER"],
    )
    if not restored:
        flash("Archived backup file is missing and cannot be restored.", "danger")
        return redirect(url_for("backup.manage_backups"))

    backup_record.filename = restored_name
    db.session.commit()

    flash("Backup restored successfully.", "success")
    return redirect(url_for("backup.manage_backups"))


@backup_bp.route("/purge/<int:backup_id>", methods=["POST"])
@login_required
def purge_backup(backup_id):
    """Move backup to trash (soft delete) for recovery window."""
    backup_record = Backup.query.get_or_404(backup_id)

    soft_delete_backup(db.session, backup_record)
    flash("Backup moved to trash. Recover from Recovery tab within 30 days.", "warning")
    return redirect(url_for("backup.manage_backups"))
