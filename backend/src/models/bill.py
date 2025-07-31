from datetime import datetime
from src.models.user import db

class Bill(db.Model):
    __tablename__ = 'bills'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
    vendor_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # utilities, insurance, maintenance, security, etc.
    frequency = db.Column(db.String(50), nullable=False)  # monthly, quarterly, yearly
    due_day = db.Column(db.Integer)  # Day of month when bill is due (1-31)
    status = db.Column(db.String(50), default='active')  # active, inactive, cancelled
    auto_pay = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(100))
    account_number = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'amount': self.amount,
            'vendor_name': self.vendor_name,
            'category': self.category,
            'frequency': self.frequency,
            'due_day': self.due_day,
            'status': self.status,
            'auto_pay': self.auto_pay,
            'payment_method': self.payment_method,
            'account_number': self.account_number,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Bill {self.title} - R$ {self.amount} ({self.frequency})>'

