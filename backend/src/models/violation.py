from src.models.user import db
from datetime import datetime

class Violation(db.Model):
    """Represents rule violations reported against residents"""
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    violation_type = db.Column(db.String(100), nullable=False)  # 'noise', 'parking', 'pet', etc.
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    severity = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high'
    status = db.Column(db.String(20), default='open')  # 'open', 'resolved', 'dismissed'
    reported_by = db.Column(db.String(100), nullable=True)  # Who reported the violation
    reported_date = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_date = db.Column(db.DateTime, nullable=True)
    fine_amount = db.Column(db.Numeric(10, 2), nullable=True)
    fine_paid = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    actions = db.relationship('ViolationAction', backref='violation', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Violation {self.violation_type} - {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'resident_id': self.resident_id,
            'resident_name': self.resident.name if self.resident else None,
            'resident_building': self.resident.building if self.resident else None,
            'resident_apartment': self.resident.apartment if self.resident else None,
            'violation_type': self.violation_type,
            'description': self.description,
            'location': self.location,
            'severity': self.severity,
            'status': self.status,
            'reported_by': self.reported_by,
            'reported_date': self.reported_date.isoformat() if self.reported_date else None,
            'resolved_date': self.resolved_date.isoformat() if self.resolved_date else None,
            'fine_amount': float(self.fine_amount) if self.fine_amount else None,
            'fine_paid': self.fine_paid,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'actions': [action.to_dict() for action in self.actions]
        }

class ViolationAction(db.Model):
    """Represents actions taken in response to violations (warnings, fines, communications)"""
    id = db.Column(db.Integer, primary_key=True)
    violation_id = db.Column(db.Integer, db.ForeignKey('violation.id'), nullable=False)
    action_type = db.Column(db.String(50), nullable=False)  # 'warning', 'fine', 'communication', 'hearing'
    description = db.Column(db.Text, nullable=False)
    fine_amount = db.Column(db.Numeric(10, 2), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    taken_by = db.Column(db.String(100), nullable=True)  # Who took this action
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ViolationAction {self.action_type} for Violation {self.violation_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'violation_id': self.violation_id,
            'action_type': self.action_type,
            'description': self.description,
            'fine_amount': float(self.fine_amount) if self.fine_amount else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'taken_by': self.taken_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

