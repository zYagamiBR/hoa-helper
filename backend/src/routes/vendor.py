from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.vendor import Vendor

vendor_bp = Blueprint('vendor', __name__)

@vendor_bp.route('/vendors', methods=['GET'])
def get_vendors():
    """Get all vendors"""
    vendors = Vendor.query.all()
    return jsonify([vendor.to_dict() for vendor in vendors])

@vendor_bp.route('/vendors', methods=['POST'])
def create_vendor():
    """Create a new vendor"""
    data = request.json
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    vendor = Vendor(
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        services=data.get('services'),
        contact_person=data.get('contact_person')
    )
    db.session.add(vendor)
    db.session.commit()
    return jsonify(vendor.to_dict()), 201

@vendor_bp.route('/vendors/<int:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    """Get a specific vendor"""
    vendor = Vendor.query.get_or_404(vendor_id)
    return jsonify(vendor.to_dict())

@vendor_bp.route('/vendors/<int:vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    """Update a vendor"""
    vendor = Vendor.query.get_or_404(vendor_id)
    data = request.json
    
    vendor.name = data.get('name', vendor.name)
    vendor.email = data.get('email', vendor.email)
    vendor.phone = data.get('phone', vendor.phone)
    vendor.address = data.get('address', vendor.address)
    vendor.services = data.get('services', vendor.services)
    vendor.contact_person = data.get('contact_person', vendor.contact_person)
    
    db.session.commit()
    return jsonify(vendor.to_dict())

@vendor_bp.route('/vendors/<int:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    """Delete a vendor"""
    vendor = Vendor.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    return '', 204

