"""Recovery log model for disaster recovery simulation."""

from datetime import datetime

from extensions import db


class RecoveryLog(db.Model):
    """Log entry for a simulated recovery operation."""

    __tablename__ = "recovery_log"

    id = db.Column(db.Integer, primary_key=True)
    backup_id = db.Column(db.Integer, db.ForeignKey("backup.id"), nullable=False)
    recovery_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    backup = db.relationship("Backup", back_populates="recovery_logs")
