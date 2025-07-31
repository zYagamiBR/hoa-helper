from flask import Blueprint, request, jsonify
from ..models.bill import Bill
from ..models.user import db

bill_bp = Blueprint('bills', __name__)

@bill_bp.route('/bills', methods=['GET'])
def get_bills():
    """Get all bills"""
    try:
        bills = Bill.query.all()
        return jsonify([bill.to_dict() for bill in bills])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bill_bp.route('/bills', methods=['POST'])
def create_bill():
    """Create a new bill"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'amount', 'vendor_name', 'category', 'frequency']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        bill = Bill(
            title=data['title'],
            description=data.get('description', ''),
            amount=float(data['amount']),
            vendor_name=data['vendor_name'],
            category=data['category'],
            frequency=data['frequency'],
            due_day=data.get('due_day'),
            status=data.get('status', 'active'),
            auto_pay=data.get('auto_pay', False),
            payment_method=data.get('payment_method', ''),
            account_number=data.get('account_number', ''),
            notes=data.get('notes', '')
        )
        
        db.session.add(bill)
        db.session.commit()
        
        return jsonify(bill.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': 'Invalid amount format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bill_bp.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    """Get a specific bill"""
    try:
        bill = Bill.query.get_or_404(bill_id)
        return jsonify(bill.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bill_bp.route('/bills/<int:bill_id>', methods=['PUT'])
def update_bill(bill_id):
    """Update a bill"""
    try:
        bill = Bill.query.get_or_404(bill_id)
        data = request.get_json()
        
        # Update fields if provided
        if 'title' in data:
            bill.title = data['title']
        if 'description' in data:
            bill.description = data['description']
        if 'amount' in data:
            bill.amount = float(data['amount'])
        if 'vendor_name' in data:
            bill.vendor_name = data['vendor_name']
        if 'category' in data:
            bill.category = data['category']
        if 'frequency' in data:
            bill.frequency = data['frequency']
        if 'due_day' in data:
            bill.due_day = data['due_day']
        if 'status' in data:
            bill.status = data['status']
        if 'auto_pay' in data:
            bill.auto_pay = data['auto_pay']
        if 'payment_method' in data:
            bill.payment_method = data['payment_method']
        if 'account_number' in data:
            bill.account_number = data['account_number']
        if 'notes' in data:
            bill.notes = data['notes']
        
        db.session.commit()
        return jsonify(bill.to_dict())
    except ValueError as e:
        return jsonify({'error': 'Invalid amount format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bill_bp.route('/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    """Delete a bill"""
    try:
        bill = Bill.query.get_or_404(bill_id)
        db.session.delete(bill)
        db.session.commit()
        return jsonify({'message': 'Bill deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bill_bp.route('/bills/categories', methods=['GET'])
def get_bill_categories():
    """Get available bill categories"""
    categories = [
        'utilities',
        'insurance', 
        'maintenance',
        'security',
        'cleaning',
        'landscaping',
        'elevator',
        'internet',
        'legal',
        'accounting',
        'other'
    ]
    return jsonify(categories)

@bill_bp.route('/bills/frequencies', methods=['GET'])
def get_bill_frequencies():
    """Get available bill frequencies"""
    frequencies = [
        'monthly',
        'quarterly', 
        'semi-annual',
        'yearly'
    ]
    return jsonify(frequencies)

