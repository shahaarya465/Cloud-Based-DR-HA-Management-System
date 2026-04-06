"""Backup model for uploaded backup metadata."""

from datetime import datetime

from extensions import db


class Backup(db.Model):
    """Uploaded backup file metadata."""

    __tablename__ = "backup"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    recovery_logs = db.relationship(
        "RecoveryLog",
        back_populates="backup",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def is_deleted(self):
        """Return True if backup is in trash (soft deleted)."""
        return self.deleted_at is not None
