"""User model for authentication."""

from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    """System user account."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # New RBAC Column. Defaulting to least-privilege (Auditor)
    role = db.Column(db.String(20), nullable=False, default="Auditor")

    @property
    def is_superadmin(self):
        return self.role == 'SuperAdmin'

    @property
    def is_operator_or_higher(self):
        return self.role in ['SuperAdmin', 'Operator']