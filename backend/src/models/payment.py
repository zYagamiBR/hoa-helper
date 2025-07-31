from src.models.user import db
from datetime import datetime

class Payment(db.Model):
    """Represents payments made by residents (HOA dues, fines, etc.)"""
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_type = db.Column(db.String(50), nullable=False)  # 'dues', 'fine', 'special_assessment', etc.
    payment_method = db.Column(db.String(50), nullable=True)  # 'credit_card', 'bank_transfer', 'check', etc.
    description = db.Column(db.Text, nullable=True)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='completed')  # 'pending', 'completed', 'failed', 'refunded'
    reference_number = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Payment {self.amount} from {self.resident.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'resident_id': self.resident_id,
            'resident_name': self.resident.name if self.resident else None,
            'resident_building': self.resident.building if self.resident else None,
            'resident_apartment': self.resident.apartment if self.resident else None,
            'amount': float(self.amount),
            'payment_type': self.payment_type,
            'payment_method': self.payment_method,
            'description': self.description,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'reference_number': self.reference_number,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

