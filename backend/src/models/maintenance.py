from src.models.user import db
from datetime import datetime

class MaintenanceRequest(db.Model):
    """Represents maintenance requests submitted by residents"""
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=True)  # Where the issue is located
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high', 'urgent'
    status = db.Column(db.String(20), default='open')  # 'open', 'in_progress', 'completed', 'cancelled'
    category = db.Column(db.String(50), nullable=True)  # 'plumbing', 'electrical', 'hvac', etc.
    estimated_cost = db.Column(db.Numeric(10, 2), nullable=True)
    actual_cost = db.Column(db.Numeric(10, 2), nullable=True)
    scheduled_date = db.Column(db.DateTime, nullable=True)
    completed_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    updates = db.relationship('MaintenanceUpdate', backref='maintenance_request', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<MaintenanceRequest {self.title} - {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'resident_id': self.resident_id,
            'resident_name': self.resident.name if self.resident else None,
            'resident_building': self.resident.building if self.resident else None,
            'resident_apartment': self.resident.apartment if self.resident else None,
            'vendor_id': self.vendor_id,
            'vendor_name': self.assigned_vendor.name if self.assigned_vendor else None,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'priority': self.priority,
            'status': self.status,
            'category': self.category,
            'estimated_cost': float(self.estimated_cost) if self.estimated_cost else None,
            'actual_cost': float(self.actual_cost) if self.actual_cost else None,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updates': [update.to_dict() for update in self.updates]
        }

class MaintenanceUpdate(db.Model):
    """Represents updates/progress notes on maintenance requests"""
    id = db.Column(db.Integer, primary_key=True)
    maintenance_request_id = db.Column(db.Integer, db.ForeignKey('maintenance_request.id'), nullable=False)
    update_text = db.Column(db.Text, nullable=False)
    status_change = db.Column(db.String(20), nullable=True)  # New status if this update changes status
    cost_update = db.Column(db.Numeric(10, 2), nullable=True)  # Cost update if applicable
    created_by = db.Column(db.String(100), nullable=True)  # Who created this update
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MaintenanceUpdate for Request {self.maintenance_request_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'maintenance_request_id': self.maintenance_request_id,
            'update_text': self.update_text,
            'status_change': self.status_change,
            'cost_update': float(self.cost_update) if self.cost_update else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

