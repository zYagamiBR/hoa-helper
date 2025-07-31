from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.event import Event, EventRSVP
from datetime import datetime
from decimal import Decimal

event_bp = Blueprint('event', __name__)

@event_bp.route('/events', methods=['GET'])
def get_events():
    """Get all events"""
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@event_bp.route('/events', methods=['POST'])
def create_event():
    """Create a new event"""
    data = request.json
    
    # Validate required fields
    if not data.get('title') or not data.get('event_date'):
        return jsonify({'error': 'Title and event_date are required'}), 400
    
    # Parse dates
    try:
        event_date = datetime.fromisoformat(data['event_date'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Invalid event_date format'}), 400
    
    end_date = None
    if data.get('end_date'):
        try:
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid end_date format'}), 400
    
    # Parse cost if provided
    cost_per_person = Decimal('0.00')
    if data.get('cost_per_person'):
        try:
            cost_per_person = Decimal(str(data['cost_per_person']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid cost_per_person format'}), 400
    
    event = Event(
        title=data['title'],
        description=data.get('description'),
        location=data.get('location'),
        event_date=event_date,
        end_date=end_date,
        max_attendees=data.get('max_attendees'),
        cost_per_person=cost_per_person,
        event_type=data.get('event_type'),
        status=data.get('status', 'scheduled'),
        created_by=data.get('created_by')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

@event_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get a specific event"""
    event = Event.query.get_or_404(event_id)
    return jsonify(event.to_dict())

@event_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an event"""
    event = Event.query.get_or_404(event_id)
    data = request.json
    
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.location = data.get('location', event.location)
    event.max_attendees = data.get('max_attendees', event.max_attendees)
    event.event_type = data.get('event_type', event.event_type)
    event.status = data.get('status', event.status)
    event.created_by = data.get('created_by', event.created_by)
    
    # Update cost if provided
    if data.get('cost_per_person'):
        try:
            event.cost_per_person = Decimal(str(data['cost_per_person']))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid cost_per_person format'}), 400
    
    # Update dates if provided
    if data.get('event_date'):
        try:
            event.event_date = datetime.fromisoformat(data['event_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid event_date format'}), 400
    
    if data.get('end_date'):
        try:
            event.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid end_date format'}), 400
    
    db.session.commit()
    return jsonify(event.to_dict())

@event_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event"""
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return '', 204

@event_bp.route('/events/<int:event_id>/rsvp', methods=['POST'])
def create_rsvp(event_id):
    """RSVP to an event"""
    event = Event.query.get_or_404(event_id)
    data = request.json
    
    # Validate required fields
    if not data.get('resident_id') or not data.get('response'):
        return jsonify({'error': 'Resident ID and response are required'}), 400
    
    if data['response'] not in ['yes', 'no', 'maybe']:
        return jsonify({'error': 'Response must be yes, no, or maybe'}), 400
    
    # Check if RSVP already exists
    existing_rsvp = EventRSVP.query.filter_by(
        event_id=event_id, 
        resident_id=data['resident_id']
    ).first()
    
    if existing_rsvp:
        # Update existing RSVP
        existing_rsvp.response = data['response']
        existing_rsvp.guests_count = data.get('guests_count', existing_rsvp.guests_count)
        existing_rsvp.notes = data.get('notes', existing_rsvp.notes)
        db.session.commit()
        return jsonify(existing_rsvp.to_dict())
    else:
        # Create new RSVP
        rsvp = EventRSVP(
            event_id=event_id,
            resident_id=data['resident_id'],
            response=data['response'],
            guests_count=data.get('guests_count', 0),
            notes=data.get('notes')
        )
        db.session.add(rsvp)
        db.session.commit()
        return jsonify(rsvp.to_dict()), 201

@event_bp.route('/events/<int:event_id>/rsvp', methods=['GET'])
def get_event_rsvps(event_id):
    """Get all RSVPs for an event"""
    event = Event.query.get_or_404(event_id)
    rsvps = EventRSVP.query.filter_by(event_id=event_id).all()
    return jsonify([rsvp.to_dict() for rsvp in rsvps])

@event_bp.route('/events/<int:event_id>/rsvp/<int:resident_id>', methods=['DELETE'])
def delete_rsvp(event_id, resident_id):
    """Delete an RSVP"""
    rsvp = EventRSVP.query.filter_by(event_id=event_id, resident_id=resident_id).first_or_404()
    db.session.delete(rsvp)
    db.session.commit()
    return '', 204

