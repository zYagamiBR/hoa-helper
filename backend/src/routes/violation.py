from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.violation import Violation, ViolationAction
from datetime import datetime
from decimal import Decimal

violation_bp = Blueprint('violation', __name__)

@violation_bp.route('/violations', methods=['GET'])
def get_violations():
    """Get all violations"""
    violations = Violation.query.all()
    return jsonify([violation.to_dict() for violation in violations])

@violation_bp.route('/violations', methods=['POST'])
def create_violation():
    """Report a new violation"""
    data = request.json
    
    # Validate required fields
    if not data.get('resident_id') or not data.get('violation_type') or not data.get('description'):
        return jsonify({'error': 'Resident ID, violation type, and description are required'}), 400
    
    # Parse dates if provided
    reported_date = datetime.utcnow()
    if data.get('reported_date'):
        try:
            reported_date = datetime.fromisoformat(data['reported_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid reported_date format'}), 400
    
    resolved_date = None
    if data.get('resolved_date'):
        try:
            resolved_date = datetime.fromisoformat(data['resolved_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid resolved_date format'}), 400
    
    # Parse fine amount if provided
    fine_amount = None
    if data.get('fine_amount'):
        try:
            fine_amount = Decimal(str(data['fine_amount']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid fine_amount format'}), 400
    
    violation = Violation(
        resident_id=data['resident_id'],
        violation_type=data['violation_type'],
        description=data['description'],
        location=data.get('location'),
        severity=data.get('severity', 'medium'),
        status=data.get('status', 'open'),
        reported_by=data.get('reported_by'),
        reported_date=reported_date,
        resolved_date=resolved_date,
        fine_amount=fine_amount,
        fine_paid=data.get('fine_paid', False),
        notes=data.get('notes')
    )
    db.session.add(violation)
    db.session.commit()
    return jsonify(violation.to_dict()), 201

@violation_bp.route('/violations/<int:violation_id>', methods=['GET'])
def get_violation(violation_id):
    """Get a specific violation"""
    violation = Violation.query.get_or_404(violation_id)
    return jsonify(violation.to_dict())

@violation_bp.route('/violations/<int:violation_id>', methods=['PUT'])
def update_violation(violation_id):
    """Update a violation"""
    violation = Violation.query.get_or_404(violation_id)
    data = request.json
    
    violation.violation_type = data.get('violation_type', violation.violation_type)
    violation.description = data.get('description', violation.description)
    violation.location = data.get('location', violation.location)
    violation.severity = data.get('severity', violation.severity)
    violation.status = data.get('status', violation.status)
    violation.reported_by = data.get('reported_by', violation.reported_by)
    violation.fine_paid = data.get('fine_paid', violation.fine_paid)
    violation.notes = data.get('notes', violation.notes)
    
    # Update fine amount if provided
    if data.get('fine_amount'):
        try:
            violation.fine_amount = Decimal(str(data['fine_amount']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid fine_amount format'}), 400
    
    # Update dates if provided
    if data.get('reported_date'):
        try:
            violation.reported_date = datetime.fromisoformat(data['reported_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid reported_date format'}), 400
    
    if data.get('resolved_date'):
        try:
            violation.resolved_date = datetime.fromisoformat(data['resolved_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid resolved_date format'}), 400
    
    db.session.commit()
    return jsonify(violation.to_dict())

@violation_bp.route('/violations/<int:violation_id>', methods=['DELETE'])
def delete_violation(violation_id):
    """Delete a violation"""
    violation = Violation.query.get_or_404(violation_id)
    db.session.delete(violation)
    db.session.commit()
    return '', 204

@violation_bp.route('/violations/<int:violation_id>/actions', methods=['POST'])
def add_violation_action(violation_id):
    """Add an action to a violation (fine, warning, communication)"""
    violation = Violation.query.get_or_404(violation_id)
    data = request.json
    
    # Validate required fields
    if not data.get('action_type') or not data.get('description'):
        return jsonify({'error': 'Action type and description are required'}), 400
    
    # Parse fine amount if provided
    fine_amount = None
    if data.get('fine_amount'):
        try:
            fine_amount = Decimal(str(data['fine_amount']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid fine_amount format'}), 400
    
    # Parse due date if provided
    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400
    
    action = ViolationAction(
        violation_id=violation_id,
        action_type=data['action_type'],
        description=data['description'],
        fine_amount=fine_amount,
        due_date=due_date,
        completed=data.get('completed', False),
        taken_by=data.get('taken_by')
    )
    
    # If this is a fine action, update the violation's fine amount
    if data['action_type'] == 'fine' and fine_amount:
        violation.fine_amount = fine_amount
    
    db.session.add(action)
    db.session.commit()
    return jsonify(action.to_dict()), 201

@violation_bp.route('/violations/<int:violation_id>/actions', methods=['GET'])
def get_violation_actions(violation_id):
    """Get all actions for a violation"""
    violation = Violation.query.get_or_404(violation_id)
    actions = ViolationAction.query.filter_by(violation_id=violation_id).all()
    return jsonify([action.to_dict() for action in actions])

@violation_bp.route('/violations/<int:violation_id>/actions/<int:action_id>', methods=['PUT'])
def update_violation_action(violation_id, action_id):
    """Update a violation action"""
    action = ViolationAction.query.filter_by(
        id=action_id, 
        violation_id=violation_id
    ).first_or_404()
    data = request.json
    
    action.action_type = data.get('action_type', action.action_type)
    action.description = data.get('description', action.description)
    action.completed = data.get('completed', action.completed)
    action.taken_by = data.get('taken_by', action.taken_by)
    
    # Update fine amount if provided
    if data.get('fine_amount'):
        try:
            action.fine_amount = Decimal(str(data['fine_amount']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid fine_amount format'}), 400
    
    # Update due date if provided
    if data.get('due_date'):
        try:
            action.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400
    
    db.session.commit()
    return jsonify(action.to_dict())

