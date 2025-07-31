from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Represents a resident/homeowner in the HOA"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    building = db.Column(db.Integer, nullable=False)  # Building number (1-50)
    apartment = db.Column(db.String(10), nullable=False)  # Apartment number (101-404)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='resident', lazy=True)
    maintenance_requests = db.relationship('MaintenanceRequest', backref='resident', lazy=True)
    event_rsvps = db.relationship('EventRSVP', backref='resident', lazy=True)
    violations = db.relationship('Violation', backref='resident', lazy=True)

    def __repr__(self):
        return f'<User {self.name} - Building {self.building}, Apt {self.apartment}>'

    @staticmethod
    def validate_apartment(apartment):
        """Validate apartment number format (101-104, 201-204, 301-304, 401-404)"""
        if not apartment or len(apartment) != 3:
            return False
        
        try:
            floor = int(apartment[0])
            apt_num = int(apartment[1:])
            
            # Valid floors: 1, 2, 3, 4
            # Valid apartment numbers: 01, 02, 03, 04
            return floor in [1, 2, 3, 4] and apt_num in [1, 2, 3, 4]
        except ValueError:
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'building': self.building,
            'apartment': self.apartment,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

