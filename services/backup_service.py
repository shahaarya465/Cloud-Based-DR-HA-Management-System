"""Service helpers for backup file operations."""

import os
from datetime import datetime

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


ARCHIVED_PREFIX = "archived/"


def is_allowed_file(filename, allowed_extensions):
    """Return True when file extension is within allowed types."""
    if not filename or "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in allowed_extensions


def save_backup_file(uploaded_file: FileStorage, upload_folder: str, allowed_extensions):
    """Validate and save an uploaded backup file.

    Returns:
        tuple[dict | None, str | None]:
            - metadata dict on success, else None
            - error message on failure, else None
    """
    if uploaded_file is None or uploaded_file.filename == "":
        return None, "Please choose a backup file to upload."

    if not is_allowed_file(uploaded_file.filename, allowed_extensions):
        allowed = ", ".join(sorted(allowed_extensions))
        return None, f"Invalid file type. Allowed extensions: {allowed}."

    safe_name = secure_filename(uploaded_file.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    final_name = f"{timestamp}_{safe_name}"
    destination_path = os.path.join(upload_folder, final_name)

    uploaded_file.save(destination_path)
    file_size = os.path.getsize(destination_path)

    return {"filename": final_name, "file_size": file_size}, None


def is_archived_filename(filename: str):
    """Return True when a backup filename is marked as archived."""
    return bool(filename and filename.startswith(ARCHIVED_PREFIX))


def archive_backup_file(filename: str, upload_folder: str):
    """Move an active backup file into an archive subfolder and return new filename."""
    if is_archived_filename(filename):
        return filename, True

    source_path = os.path.join(upload_folder, filename)
    if not os.path.exists(source_path):
        return filename, False

    archive_folder = os.path.join(upload_folder, "archived")
    os.makedirs(archive_folder, exist_ok=True)

    archived_name = f"{ARCHIVED_PREFIX}{os.path.basename(filename)}"
    destination_path = os.path.join(upload_folder, archived_name)
    os.rename(source_path, destination_path)
    return archived_name, True


def restore_backup_file(filename: str, upload_folder: str):
    """Restore an archived backup file to active location and return restored filename."""
    if not is_archived_filename(filename):
        return filename, True

    source_path = os.path.join(upload_folder, filename)
    if not os.path.exists(source_path):
        return filename, False

    base_name = os.path.basename(filename)
    destination_path = os.path.join(upload_folder, base_name)
    if os.path.exists(destination_path):
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        base_name = f"{timestamp}_{base_name}"
        destination_path = os.path.join(upload_folder, base_name)

    os.rename(source_path, destination_path)
    return base_name, True


def delete_backup_file(filename: str, upload_folder: str):
    """Delete a backup file from the storage directory if it exists."""
    file_path = os.path.join(upload_folder, filename)
    if not os.path.exists(file_path):
        return False

    os.remove(file_path)
    return True


def soft_delete_backup(db_session, backup):
    """Mark a backup as deleted (soft delete) without removing the file."""
    backup.deleted_at = datetime.utcnow()
    db_session.commit()
    return True


def restore_from_trash(db_session, backup):
    """Restore a soft-deleted backup back to active state."""
    backup.deleted_at = None
    db_session.commit()
    return True


def hard_delete_backup(db_session, backup, upload_folder):
    """Permanently delete a backup file and metadata (used after trash retention)."""
    if backup.filename and os.path.exists(os.path.join(upload_folder, backup.filename)):
        delete_backup_file(backup.filename, upload_folder)
    db_session.delete(backup)
    db_session.commit()
    return True
