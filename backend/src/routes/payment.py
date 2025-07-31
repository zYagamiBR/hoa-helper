from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.payment import Payment
from datetime import datetime
from decimal import Decimal

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payments', methods=['GET'])
def get_payments():
    """Get all payments"""
    payments = Payment.query.all()
    return jsonify([payment.to_dict() for payment in payments])

@payment_bp.route('/payments', methods=['POST'])
def create_payment():
    """Record a new payment"""
    data = request.json
    
    # Validate required fields
    if not data.get('resident_id') or not data.get('amount') or not data.get('payment_type'):
        return jsonify({'error': 'Resident ID, amount, and payment type are required'}), 400
    
    try:
        amount = Decimal(str(data['amount']))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount format'}), 400
    
    # Parse dates if provided
    payment_date = datetime.utcnow()
    if data.get('payment_date'):
        try:
            payment_date = datetime.fromisoformat(data['payment_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid payment_date format'}), 400
    
    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400
    
    payment = Payment(
        resident_id=data['resident_id'],
        amount=amount,
        payment_type=data['payment_type'],
        payment_method=data.get('payment_method'),
        description=data.get('description'),
        payment_date=payment_date,
        due_date=due_date,
        status=data.get('status', 'completed'),
        reference_number=data.get('reference_number')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify(payment.to_dict()), 201

@payment_bp.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Get a specific payment"""
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.to_dict())

@payment_bp.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    """Update a payment"""
    payment = Payment.query.get_or_404(payment_id)
    data = request.json
    
    if data.get('amount'):
        try:
            payment.amount = Decimal(str(data['amount']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400
    
    payment.payment_type = data.get('payment_type', payment.payment_type)
    payment.payment_method = data.get('payment_method', payment.payment_method)
    payment.description = data.get('description', payment.description)
    payment.status = data.get('status', payment.status)
    payment.reference_number = data.get('reference_number', payment.reference_number)
    
    # Update dates if provided
    if data.get('payment_date'):
        try:
            payment.payment_date = datetime.fromisoformat(data['payment_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid payment_date format'}), 400
    
    if data.get('due_date'):
        try:
            payment.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400
    
    db.session.commit()
    return jsonify(payment.to_dict())

@payment_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    """Delete a payment"""
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return '', 204

