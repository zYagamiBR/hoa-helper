from flask import Blueprint, request, jsonify, send_file, current_app
import csv
import io
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from ..models.user import User
from ..models.vendor import Vendor
from ..models.associate import Associate
from ..models.invoice import Invoice
from ..models.maintenance import MaintenanceRequest
from ..models.event import Event
from ..models.payment import Payment
from ..models.violation import Violation

import_export_bp = Blueprint('import_export', __name__)

def get_db():
    """Get database instance from current app"""
    from .. import db
    return db

# Helper function to convert model to dict
def model_to_dict(model):
    """Convert SQLAlchemy model to dictionary"""
    result = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        if isinstance(value, datetime):
            result[column.name] = value.isoformat()
        else:
            result[column.name] = value
    return result

# RESIDENTS IMPORT/EXPORT
@import_export_bp.route('/residents/export', methods=['GET'])
def export_residents():
    """Export all residents to CSV"""
    try:
        residents = User.query.all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        headers = ['id', 'name', 'email', 'phone', 'building', 'apartment', 'unit', 'created_at']
        writer.writerow(headers)
        
        # Write data
        for resident in residents:
            writer.writerow([
                resident.id,
                resident.name,
                resident.email,
                resident.phone,
                resident.building,
                resident.apartment,
                resident.unit,
                resident.created_at.isoformat() if resident.created_at else ''
            ])
        
        # Create file-like object
        output.seek(0)
        file_data = io.BytesIO(output.getvalue().encode('utf-8'))
        
        return send_file(
            file_data,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'residents_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@import_export_bp.route('/residents/import', methods=['POST'])
def import_residents():
    """Import residents from CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400
        
        # Read CSV
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        imported_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_input, start=2):
            try:
                # Validate required fields
                if not row.get('name') or not row.get('email'):
                    errors.append(f"Row {row_num}: Name and email are required")
                    continue
                
                # Check if resident already exists
                existing = User.query.filter_by(email=row['email']).first()
                if existing:
                    errors.append(f"Row {row_num}: Resident with email {row['email']} already exists")
                    continue
                
                # Create new resident
                resident = User(
                    name=row['name'],
                    email=row['email'],
                    phone=row.get('phone', ''),
                    building=int(row['building']) if row.get('building') else None,
                    apartment=int(row['apartment']) if row.get('apartment') else None,
                    unit=row.get('unit', '')
                )
                
                db = get_db()
                db.session.add(resident)
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        if imported_count > 0:
            db = get_db()
            db.session.commit()
        
        return jsonify({
            'success': True,
            'imported_count': imported_count,
            'errors': errors
        })
        
    except Exception as e:
        db = get_db()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# VENDORS IMPORT/EXPORT
@import_export_bp.route('/vendors/export', methods=['GET'])
def export_vendors():
    """Export all vendors to CSV"""
    try:
        vendors = Vendor.query.all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        headers = ['id', 'name', 'service', 'email', 'phone', 'address', 'created_at']
        writer.writerow(headers)
        
        for vendor in vendors:
            writer.writerow([
                vendor.id,
                vendor.name,
                vendor.service,
                vendor.email,
                vendor.phone,
                vendor.address,
                vendor.created_at.isoformat() if vendor.created_at else ''
            ])
        
        output.seek(0)
        file_data = io.BytesIO(output.getvalue().encode('utf-8'))
        
        return send_file(
            file_data,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'vendors_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@import_export_bp.route('/vendors/import', methods=['POST'])
def import_vendors():
    """Import vendors from CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400
        
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        imported_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_input, start=2):
            try:
                if not row.get('name'):
                    errors.append(f"Row {row_num}: Name is required")
                    continue
                
                existing = Vendor.query.filter_by(name=row['name']).first()
                if existing:
                    errors.append(f"Row {row_num}: Vendor {row['name']} already exists")
                    continue
                
                vendor = Vendor(
                    name=row['name'],
                    service=row.get('service', ''),
                    email=row.get('email', ''),
                    phone=row.get('phone', ''),
                    address=row.get('address', '')
                )
                
                db = get_db()
                db.session.add(vendor)
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        if imported_count > 0:
            db = get_db()
            db.session.commit()
        
        return jsonify({
            'success': True,
            'imported_count': imported_count,
            'errors': errors
        })
        
    except Exception as e:
        db = get_db()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ASSOCIATES IMPORT/EXPORT
@import_export_bp.route('/associates/export', methods=['GET'])
def export_associates():
    """Export all associates to CSV"""
    try:
        associates = Associate.query.all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        headers = ['id', 'name', 'email', 'phone', 'department', 'work_area', 'position', 
                  'monthly_salary', 'hire_date', 'status', 'created_at']
        writer.writerow(headers)
        
        for associate in associates:
            writer.writerow([
                associate.id,
                associate.name,
                associate.email,
                associate.phone,
                associate.department,
                associate.work_area,
                associate.position,
                float(associate.monthly_salary) if associate.monthly_salary else '',
                associate.hire_date.isoformat() if associate.hire_date else '',
                associate.status,
                associate.created_at.isoformat() if associate.created_at else ''
            ])
        
        output.seek(0)
        file_data = io.BytesIO(output.getvalue().encode('utf-8'))
        
        return send_file(
            file_data,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'associates_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@import_export_bp.route('/associates/import', methods=['POST'])
def import_associates():
    """Import associates from CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400
        
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        imported_count = 0
        errors = []
        
        for row_num, row in enumerate(csv_input, start=2):
            try:
                if not row.get('name'):
                    errors.append(f"Row {row_num}: Name is required")
                    continue
                
                existing = Associate.query.filter_by(email=row.get('email')).first() if row.get('email') else None
                if existing:
                    errors.append(f"Row {row_num}: Associate with email {row['email']} already exists")
                    continue
                
                associate = Associate(
                    name=row['name'],
                    email=row.get('email', ''),
                    phone=row.get('phone', ''),
                    department=row.get('department', ''),
                    work_area=row.get('work_area', ''),
                    position=row.get('position', ''),
                    monthly_salary=float(row['monthly_salary']) if row.get('monthly_salary') else None,
                    hire_date=datetime.fromisoformat(row['hire_date']) if row.get('hire_date') else None,
                    status=row.get('status', 'Active')
                )
                
                db = get_db()
                db.session.add(associate)
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        if imported_count > 0:
            db = get_db()
            db.session.commit()
        
        return jsonify({
            'success': True,
            'imported_count': imported_count,
            'errors': errors
        })
        
    except Exception as e:
        db = get_db()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Generic export template endpoint
@import_export_bp.route('/<entity>/template', methods=['GET'])
def download_template(entity):
    """Download CSV template for importing data"""
    templates = {
        'residents': ['name', 'email', 'phone', 'building', 'apartment'],
        'vendors': ['name', 'service', 'email', 'phone', 'address'],
        'associates': ['name', 'email', 'phone', 'department', 'work_area', 'position', 'monthly_salary', 'hire_date', 'status'],
        'invoices': ['invoice_number', 'vendor_name', 'amount', 'reason', 'status', 'authorized_by'],
        'maintenance': ['title', 'description', 'category', 'priority', 'status', 'estimated_cost']
    }
    
    if entity not in templates:
        return jsonify({'error': 'Invalid entity'}), 400
    
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(templates[entity])
        
        output.seek(0)
        file_data = io.BytesIO(output.getvalue().encode('utf-8'))
        
        return send_file(
            file_data,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{entity}_import_template.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

