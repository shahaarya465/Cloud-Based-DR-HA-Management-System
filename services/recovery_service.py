"""Service helpers for disaster recovery simulation."""

from models.recovery_model import RecoveryLog


def simulate_restore_operation(backup):
    """Simulate a restore operation for the provided backup."""
    if backup is None:
        return "FAILED"
    return "SUCCESS"


def log_recovery_event(db_session, backup, status):
    """Create and persist a recovery log entry."""
    recovery_log = RecoveryLog(backup_id=backup.id, status=status)
    db_session.add(recovery_log)
    db_session.commit()
    return recovery_log


def execute_recovery(db_session, backup):
    """Run restore simulation and store the resulting event log."""
    status = simulate_restore_operation(backup)
    return log_recovery_event(db_session, backup, status)
