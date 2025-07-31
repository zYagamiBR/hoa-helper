from flask import Blueprint, jsonify, request
from src.models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Get all residents"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new resident"""
    data = request.json

    if not data.get('name') or not data.get('email') or not data.get('building') or not data.get('apartment'):
        return jsonify({'error': 'Name, email, building, and apartment are required'}), 400

    try:
        building = int(data.get('building'))
        if building < 1 or building > 50:
            return jsonify({'error': 'Building must be between 1 and 50'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Building must be a valid number'}), 400

    apartment = data.get('apartment')
    if not User.validate_apartment(apartment):
        return jsonify({'error': 'Apartment must be in format 101-104, 201-204, 301-304, or 401-404'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    if User.query.filter_by(building=building, apartment=apartment).first():
        return jsonify({'error': f'Apartment {apartment} in building {building} is already occupied'}), 400

    user = User(
        name=data['name'],
        email=data['email'],
        building=building,
        apartment=apartment,
        phone=data.get('phone')
    )

    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)

    building = data.get('building')
    apartment = data.get('apartment')

    if building is not None or apartment is not None:
        new_building = int(building) if building is not None else user.building
        new_apartment = apartment if apartment is not None else user.apartment

        try:
            if new_building < 1 or new_building > 50:
                return jsonify({'error': 'Building must be between 1 and 50'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Building must be a valid number'}), 400

        if not User.validate_apartment(new_apartment):
            return jsonify({'error': 'Apartment must be in format 101-104, 201-204, 301-304, or 401-404'}), 400

        existing_unit = User.query.filter_by(building=new_building, apartment=new_apartment).filter(User.id != user_id).first()
        if existing_unit:
            return jsonify({'error': f'Apartment {new_apartment} in building {new_building} is already occupied'}), 400

        user.building = new_building
        user.apartment = new_apartment

    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@user_bp.route('/buildings', methods=['GET'])
def get_buildings():
    return jsonify([{'number': i, 'label': f'BL{i:02d}'} for i in range(1, 51)])

@user_bp.route('/apartments', methods=['GET'])
def get_apartments():
    apartments = []
    for floor in [1, 2, 3, 4]:
        for unit in [1, 2, 3, 4]:
            apartments.append(f'{floor}0{unit}')
    return jsonify(apartments)