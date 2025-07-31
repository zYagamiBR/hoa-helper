from src.models.user import db
from datetime import datetime

class Event(db.Model):
    """Represents community events organized by the HOA"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    event_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    max_attendees = db.Column(db.Integer, nullable=True)
    cost_per_person = db.Column(db.Numeric(10, 2), default=0.00)
    event_type = db.Column(db.String(50), nullable=True)  # 'meeting', 'social', 'maintenance', etc.
    status = db.Column(db.String(20), default='scheduled')  # 'scheduled', 'cancelled', 'completed'
    created_by = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rsvps = db.relationship('EventRSVP', backref='event', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.title} on {self.event_date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'max_attendees': self.max_attendees,
            'cost_per_person': float(self.cost_per_person) if self.cost_per_person else 0.00,
            'event_type': self.event_type,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'rsvp_count': len(self.rsvps),
            'rsvps': [rsvp.to_dict() for rsvp in self.rsvps]
        }

class EventRSVP(db.Model):
    """Represents RSVP responses from residents for events"""
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    response = db.Column(db.String(20), nullable=False)  # 'yes', 'no', 'maybe'
    guests_count = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Ensure one RSVP per resident per event
    __table_args__ = (db.UniqueConstraint('event_id', 'resident_id', name='unique_event_resident_rsvp'),)

    def __repr__(self):
        return f'<EventRSVP {self.response} for Event {self.event_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'resident_id': self.resident_id,
            'resident_name': self.resident.name if self.resident else None,
            'resident_building': self.resident.building if self.resident else None,
            'resident_apartment': self.resident.apartment if self.resident else None,
            'response': self.response,
            'guests_count': self.guests_count,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

