from src.models.user import db
from datetime import datetime
import os

class Invoice(db.Model):
    """Represents invoices from vendors and other HOA expenses with comprehensive tracking"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Invoice Information
    invoice_number = db.Column(db.String(100), nullable=False, unique=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Description and Justification
    reason = db.Column(db.Text, nullable=False)  # Why was this needed
    description = db.Column(db.Text, nullable=True)  # Additional details
    category = db.Column(db.String(50), nullable=True)  # 'maintenance', 'utilities', 'insurance', etc.
    
    # Document Management
    document_filename = db.Column(db.String(255), nullable=True)  # Uploaded invoice document
    document_original_name = db.Column(db.String(255), nullable=True)  # Original filename
    
    # Authorization and Approval
    authorized_by = db.Column(db.String(100), nullable=False)  # Who authorized this invoice
    authorized_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # When authorized
    signature_data = db.Column(db.Text, nullable=True)  # Digital signature (base64 encoded)
    signature_timestamp = db.Column(db.DateTime, nullable=True)  # When signed
    
    # Dates and Status
    invoice_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    paid_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'paid', 'overdue', 'cancelled'
    
    # Payment Information
    payment_method = db.Column(db.String(50), nullable=True)
    payment_reference = db.Column(db.String(100), nullable=True)
    
    # Additional Information
    notes = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='normal')  # 'low', 'normal', 'high', 'urgent'
    
    # Audit Trail
    created_by = db.Column(db.String(100), default='System')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    vendor = db.relationship('Vendor', backref='invoices')

    def __repr__(self):
        return f'<Invoice {self.invoice_number} - ${self.amount}>'

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'vendor_id': self.vendor_id,
            'vendor_name': self.vendor.name if self.vendor else None,
            'amount': float(self.amount),
            'reason': self.reason,
            'description': self.description,
            'category': self.category,
            'document_filename': self.document_filename,
            'document_original_name': self.document_original_name,
            'authorized_by': self.authorized_by,
            'authorized_at': self.authorized_at.isoformat() if self.authorized_at else None,
            'signature_data': self.signature_data,
            'signature_timestamp': self.signature_timestamp.isoformat() if self.signature_timestamp else None,
            'invoice_date': self.invoice_date.isoformat() if self.invoice_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'paid_date': self.paid_date.isoformat() if self.paid_date else None,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'notes': self.notes,
            'priority': self.priority,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def get_document_path(self):
        """Get the full path to the uploaded document"""
        if self.document_filename:
            return os.path.join('uploads', 'invoices', self.document_filename)
        return None

