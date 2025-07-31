from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.maintenance import MaintenanceRequest, MaintenanceUpdate
from datetime import datetime
from decimal import Decimal

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/maintenance', methods=['GET'])
def get_maintenance_requests():
    """Get all maintenance requests"""
    requests = MaintenanceRequest.query.all()
    return jsonify([req.to_dict() for req in requests])

@maintenance_bp.route('/maintenance', methods=['POST'])
def create_maintenance_request():
    """Submit a new maintenance request"""
    data = request.json
    
    # Validate required fields
    if not data.get('resident_id') or not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Resident ID, title, and description are required'}), 400
    
    # Parse dates if provided
    scheduled_date = None
    if data.get('scheduled_date'):
        try:
            scheduled_date = datetime.fromisoformat(data['scheduled_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid scheduled_date format'}), 400
    
    completed_date = None
    if data.get('completed_date'):
        try:
            completed_date = datetime.fromisoformat(data['completed_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid completed_date format'}), 400
    
    # Parse costs if provided
    estimated_cost = None
    if data.get('estimated_cost'):
        try:
            estimated_cost = Decimal(str(data['estimated_cost']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid estimated_cost format'}), 400
    
    actual_cost = None
    if data.get('actual_cost'):
        try:
            actual_cost = Decimal(str(data['actual_cost']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid actual_cost format'}), 400
    
    maintenance_request = MaintenanceRequest(
        resident_id=data['resident_id'],
        vendor_id=data.get('vendor_id'),
        title=data['title'],
        description=data['description'],
        location=data.get('location'),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'open'),
        category=data.get('category'),
        estimated_cost=estimated_cost,
        actual_cost=actual_cost,
        scheduled_date=scheduled_date,
        completed_date=completed_date
    )
    db.session.add(maintenance_request)
    db.session.commit()
    return jsonify(maintenance_request.to_dict()), 201

@maintenance_bp.route('/maintenance/<int:request_id>', methods=['GET'])
def get_maintenance_request(request_id):
    """Get a specific maintenance request"""
    maintenance_request = MaintenanceRequest.query.get_or_404(request_id)
    return jsonify(maintenance_request.to_dict())

@maintenance_bp.route('/maintenance/<int:request_id>', methods=['PUT'])
def update_maintenance_request(request_id):
    """Update a maintenance request"""
    maintenance_request = MaintenanceRequest.query.get_or_404(request_id)
    data = request.json
    
    maintenance_request.vendor_id = data.get('vendor_id', maintenance_request.vendor_id)
    maintenance_request.title = data.get('title', maintenance_request.title)
    maintenance_request.description = data.get('description', maintenance_request.description)
    maintenance_request.location = data.get('location', maintenance_request.location)
    maintenance_request.priority = data.get('priority', maintenance_request.priority)
    maintenance_request.status = data.get('status', maintenance_request.status)
    maintenance_request.category = data.get('category', maintenance_request.category)
    
    # Update costs if provided
    if data.get('estimated_cost'):
        try:
            maintenance_request.estimated_cost = Decimal(str(data['estimated_cost']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid estimated_cost format'}), 400
    
    if data.get('actual_cost'):
        try:
            maintenance_request.actual_cost = Decimal(str(data['actual_cost']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid actual_cost format'}), 400
    
    # Update dates if provided
    if data.get('scheduled_date'):
        try:
            maintenance_request.scheduled_date = datetime.fromisoformat(data['scheduled_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid scheduled_date format'}), 400
    
    if data.get('completed_date'):
        try:
            maintenance_request.completed_date = datetime.fromisoformat(data['completed_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid completed_date format'}), 400
    
    db.session.commit()
    return jsonify(maintenance_request.to_dict())

@maintenance_bp.route('/maintenance/<int:request_id>', methods=['DELETE'])
def delete_maintenance_request(request_id):
    """Delete a maintenance request"""
    maintenance_request = MaintenanceRequest.query.get_or_404(request_id)
    db.session.delete(maintenance_request)
    db.session.commit()
    return '', 204

@maintenance_bp.route('/maintenance/<int:request_id>/updates', methods=['POST'])
def add_maintenance_update(request_id):
    """Add an update to a maintenance request"""
    maintenance_request = MaintenanceRequest.query.get_or_404(request_id)
    data = request.json
    
    # Validate required fields
    if not data.get('update_text'):
        return jsonify({'error': 'Update text is required'}), 400
    
    # Parse cost update if provided
    cost_update = None
    if data.get('cost_update'):
        try:
            cost_update = Decimal(str(data['cost_update']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid cost_update format'}), 400
    
    update = MaintenanceUpdate(
        maintenance_request_id=request_id,
        update_text=data['update_text'],
        status_change=data.get('status_change'),
        cost_update=cost_update,
        created_by=data.get('created_by')
    )
    
    # If status change is provided, update the main request status
    if data.get('status_change'):
        maintenance_request.status = data['status_change']
    
    # If cost update is provided, update the actual cost
    if cost_update:
        maintenance_request.actual_cost = cost_update
    
    db.session.add(update)
    db.session.commit()
    return jsonify(update.to_dict()), 201

@maintenance_bp.route('/maintenance/<int:request_id>/updates', methods=['GET'])
def get_maintenance_updates(request_id):
    """Get all updates for a maintenance request"""
    maintenance_request = MaintenanceRequest.query.get_or_404(request_id)
    updates = MaintenanceUpdate.query.filter_by(maintenance_request_id=request_id).all()
    return jsonify([update.to_dict() for update in updates])

