from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from src.models.associate import Associate
from src.models.user import db

associate_bp = Blueprint('associate', __name__)

# File upload configuration
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'}
UPLOAD_FOLDER = 'uploads/associates'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    """Ensure upload folder exists"""
    upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
    os.makedirs(upload_path, exist_ok=True)
    return upload_path

@associate_bp.route('/associates', methods=['GET'])
def get_associates():
    """Get all associates"""
    try:
        associates = Associate.query.all()
        return jsonify([associate.to_dict() for associate in associates])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@associate_bp.route('/associates', methods=['POST'])
def create_associate():
    """Create a new associate"""
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('name') or not data.get('department') or not data.get('work_area'):
            return jsonify({'error': 'Name, department, and work area are required'}), 400
        
        # Validate department and work area
        if not Associate.validate_department(data['department']):
            return jsonify({'error': f'Invalid department. Must be one of: {", ".join(Associate.get_departments())}'}), 400
        
        if not Associate.validate_work_area(data['work_area']):
            return jsonify({'error': f'Invalid work area. Must be one of: {", ".join(Associate.get_work_areas())}'}), 400
        
        # Validate CPF if provided
        if data.get('cpf') and not Associate.validate_cpf(data['cpf']):
            return jsonify({'error': 'Invalid CPF format'}), 400
        
        # Check if email already exists
        if data.get('email'):
            existing_email = Associate.query.filter_by(email=data['email']).first()
            if existing_email:
                return jsonify({'error': 'Email already exists'}), 400
        
        # Check if employee_id already exists
        if data.get('employee_id'):
            existing_id = Associate.query.filter_by(employee_id=data['employee_id']).first()
            if existing_id:
                return jsonify({'error': 'Employee ID already exists'}), 400
        
        # Check if CPF already exists
        if data.get('cpf'):
            existing_cpf = Associate.query.filter_by(cpf=data['cpf']).first()
            if existing_cpf:
                return jsonify({'error': 'CPF already exists'}), 400
        
        # Parse dates
        hire_date = None
        if data.get('hire_date'):
            try:
                hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid hire date format (use YYYY-MM-DD)'}), 400
        
        birth_date = None
        if data.get('birth_date'):
            try:
                birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid birth date format (use YYYY-MM-DD)'}), 400
        
        last_evaluation_date = None
        if data.get('last_evaluation_date'):
            try:
                last_evaluation_date = datetime.strptime(data['last_evaluation_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid evaluation date format (use YYYY-MM-DD)'}), 400
        
        # Create new associate
        associate = Associate(
            # Personal Information
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            mobile=data.get('mobile'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            birth_date=birth_date,
            cpf=data.get('cpf'),
            rg=data.get('rg'),
            nationality=data.get('nationality'),
            marital_status=data.get('marital_status'),
            
            # Employment Information
            employee_id=data.get('employee_id'),
            department=data['department'],
            work_area=data['work_area'],
            position=data.get('position'),
            hire_date=hire_date,
            contract_type=data.get('contract_type'),
            work_schedule=data.get('work_schedule'),
            status=data.get('status', 'Active'),
            
            # Financial Information
            monthly_salary=data.get('monthly_salary'),
            payment_method=data.get('payment_method'),
            bank_name=data.get('bank_name'),
            bank_account=data.get('bank_account'),
            bank_agency=data.get('bank_agency'),
            pix_key=data.get('pix_key'),
            
            # Emergency Contact
            emergency_contact_name=data.get('emergency_contact_name'),
            emergency_contact_relationship=data.get('emergency_contact_relationship'),
            emergency_contact_phone=data.get('emergency_contact_phone'),
            emergency_contact_address=data.get('emergency_contact_address'),
            
            # Additional Information
            education_level=data.get('education_level'),
            certifications=data.get('certifications'),
            skills=data.get('skills'),
            languages=data.get('languages'),
            notes=data.get('notes'),
            
            # Performance
            last_evaluation_date=last_evaluation_date,
            performance_rating=data.get('performance_rating'),
            
            # System fields
            created_by=data.get('created_by', 'System')
        )
        
        db.session.add(associate)
        db.session.commit()
        return jsonify(associate.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@associate_bp.route('/associates/<int:associate_id>', methods=['GET'])
def get_associate(associate_id):
    """Get a specific associate"""
    try:
        associate = Associate.query.get_or_404(associate_id)
        return jsonify(associate.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@associate_bp.route('/associates/<int:associate_id>', methods=['PUT'])
def update_associate(associate_id):
    """Update an associate"""
    try:
        associate = Associate.query.get_or_404(associate_id)
        data = request.json
        
        # Validate department and work area if provided
        if data.get('department') and not Associate.validate_department(data['department']):
            return jsonify({'error': f'Invalid department. Must be one of: {", ".join(Associate.get_departments())}'}), 400
        
        if data.get('work_area') and not Associate.validate_work_area(data['work_area']):
            return jsonify({'error': f'Invalid work area. Must be one of: {", ".join(Associate.get_work_areas())}'}), 400
        
        # Validate CPF if provided
        if data.get('cpf') and not Associate.validate_cpf(data['cpf']):
            return jsonify({'error': 'Invalid CPF format'}), 400
        
        # Check if email already exists (excluding current associate)
        if data.get('email') and data['email'] != associate.email:
            existing_email = Associate.query.filter_by(email=data['email']).filter(Associate.id != associate_id).first()
            if existing_email:
                return jsonify({'error': 'Email already exists'}), 400
        
        # Check if employee_id already exists (excluding current associate)
        if data.get('employee_id') and data['employee_id'] != associate.employee_id:
            existing_id = Associate.query.filter_by(employee_id=data['employee_id']).filter(Associate.id != associate_id).first()
            if existing_id:
                return jsonify({'error': 'Employee ID already exists'}), 400
        
        # Check if CPF already exists (excluding current associate)
        if data.get('cpf') and data['cpf'] != associate.cpf:
            existing_cpf = Associate.query.filter_by(cpf=data['cpf']).filter(Associate.id != associate_id).first()
            if existing_cpf:
                return jsonify({'error': 'CPF already exists'}), 400
        
        # Update fields
        for field in ['name', 'email', 'phone', 'mobile', 'address', 'city', 'state', 'zip_code',
                      'cpf', 'rg', 'nationality', 'marital_status', 'employee_id', 'department',
                      'work_area', 'position', 'contract_type', 'work_schedule', 'status',
                      'monthly_salary', 'payment_method', 'bank_name', 'bank_account', 'bank_agency',
                      'pix_key', 'emergency_contact_name', 'emergency_contact_relationship',
                      'emergency_contact_phone', 'emergency_contact_address', 'education_level',
                      'certifications', 'skills', 'languages', 'notes', 'performance_rating']:
            if field in data:
                setattr(associate, field, data[field])
        
        # Handle date fields
        for date_field in ['hire_date', 'birth_date', 'last_evaluation_date']:
            if date_field in data and data[date_field]:
                try:
                    setattr(associate, date_field, datetime.strptime(data[date_field], '%Y-%m-%d').date())
                except ValueError:
                    return jsonify({'error': f'Invalid {date_field} format (use YYYY-MM-DD)'}), 400
            elif date_field in data and data[date_field] is None:
                setattr(associate, date_field, None)
        
        associate.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(associate.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@associate_bp.route('/associates/<int:associate_id>', methods=['DELETE'])
def delete_associate(associate_id):
    """Delete an associate"""
    try:
        associate = Associate.query.get_or_404(associate_id)
        db.session.delete(associate)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Utility endpoints for dropdown options
@associate_bp.route('/associates/departments', methods=['GET'])
def get_departments():
    """Get list of all departments"""
    return jsonify(Associate.get_departments())

@associate_bp.route('/associates/work-areas', methods=['GET'])
def get_work_areas():
    """Get list of all work areas"""
    return jsonify(Associate.get_work_areas())

@associate_bp.route('/associates/contract-types', methods=['GET'])
def get_contract_types():
    """Get list of all contract types"""
    return jsonify(Associate.get_contract_types())

@associate_bp.route('/associates/marital-statuses', methods=['GET'])
def get_marital_statuses():
    """Get list of all marital statuses"""
    return jsonify(Associate.get_marital_statuses())

@associate_bp.route('/associates/education-levels', methods=['GET'])
def get_education_levels():
    """Get list of all education levels"""
    return jsonify(Associate.get_education_levels())

@associate_bp.route('/associates/payment-methods', methods=['GET'])
def get_payment_methods():
    """Get list of all payment methods"""
    return jsonify(Associate.get_payment_methods())

@associate_bp.route('/associates/performance-ratings', methods=['GET'])
def get_performance_ratings():
    """Get list of all performance ratings"""
    return jsonify(Associate.get_performance_ratings())

@associate_bp.route('/associates/statuses', methods=['GET'])
def get_statuses():
    """Get list of all employee statuses"""
    return jsonify(Associate.get_statuses())

# File upload endpoints
@associate_bp.route('/associates/<int:associate_id>/upload/<file_type>', methods=['POST'])
def upload_file(associate_id, file_type):
    """Upload a file for an associate"""
    try:
        associate = Associate.query.get_or_404(associate_id)
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        if file_type not in ['curriculum', 'contract', 'photo']:
            return jsonify({'error': 'Invalid file type. Must be curriculum, contract, or photo'}), 400
        
        # Create upload directory
        upload_path = ensure_upload_folder()
        
        # Generate secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{associate_id}_{file_type}_{timestamp}_{filename}"
        
        # Save file
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        # Update associate record
        if file_type == 'curriculum':
            associate.curriculum_filename = filename
        elif file_type == 'contract':
            associate.contract_filename = filename
        elif file_type == 'photo':
            associate.photo_filename = filename
        
        associate.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': f'{file_type.title()} uploaded successfully',
            'filename': filename
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@associate_bp.route('/associates/<int:associate_id>/files/<file_type>', methods=['DELETE'])
def delete_file(associate_id, file_type):
    """Delete a file for an associate"""
    try:
        associate = Associate.query.get_or_404(associate_id)
        
        if file_type not in ['curriculum', 'contract', 'photo']:
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Get filename
        filename = None
        if file_type == 'curriculum':
            filename = associate.curriculum_filename
            associate.curriculum_filename = None
        elif file_type == 'contract':
            filename = associate.contract_filename
            associate.contract_filename = None
        elif file_type == 'photo':
            filename = associate.photo_filename
            associate.photo_filename = None
        
        if filename:
            # Delete physical file
            upload_path = ensure_upload_folder()
            file_path = os.path.join(upload_path, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        associate.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': f'{file_type.title()} deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

