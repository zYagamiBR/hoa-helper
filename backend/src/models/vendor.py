from src.models.user import db
from datetime import datetime

class Vendor(db.Model):
    """Represents a vendor/contractor that provides services to the HOA"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    services = db.Column(db.Text, nullable=True)  # Description of services provided
    contact_person = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    maintenance_requests = db.relationship('MaintenanceRequest', backref='assigned_vendor', lazy=True)

    def __repr__(self):
        return f'<Vendor {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'services': self.services,
            'contact_person': self.contact_person,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

