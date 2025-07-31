from flask import Blueprint, jsonify, request, send_file, current_app
from src.models.user import db
from src.models.invoice import Invoice
from src.models.vendor import Vendor
from datetime import datetime
from decimal import Decimal
import os
import uuid
from werkzeug.utils import secure_filename

invoice_bp = Blueprint('invoice', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folder():
    """Get the upload folder for invoices"""
    return os.path.join(current_app.config['UPLOAD_FOLDER'], 'invoices')

@invoice_bp.route('/invoices', methods=['GET'])
def get_invoices():
    """Get all invoices with optional filtering"""
    status = request.args.get('status')
    vendor_id = request.args.get('vendor_id')
    
    query = Invoice.query
    
    if status:
        query = query.filter(Invoice.status == status)
    if vendor_id:
        query = query.filter(Invoice.vendor_id == vendor_id)
    
    invoices = query.order_by(Invoice.created_at.desc()).all()
    return jsonify([invoice.to_dict() for invoice in invoices])

@invoice_bp.route('/invoices', methods=['POST'])
def create_invoice():
    """Create a new invoice with comprehensive data"""
    data = request.json
    
    # Validate required fields
    required_fields = ['invoice_number', 'vendor_id', 'amount', 'reason', 'authorized_by', 'invoice_date']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if invoice number already exists
    existing_invoice = Invoice.query.filter_by(invoice_number=data['invoice_number']).first()
    if existing_invoice:
        return jsonify({'error': 'Invoice number already exists'}), 400
    
    # Validate vendor exists
    vendor = Vendor.query.get(data['vendor_id'])
    if not vendor:
        return jsonify({'error': 'Vendor not found'}), 400
    
    # Validate amount
    try:
        amount = Decimal(str(data['amount']))
        if amount <= 0:
            return jsonify({'error': 'Amount must be greater than 0'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount format'}), 400
    
    # Parse dates
    try:
        invoice_date = datetime.fromisoformat(data['invoice_date'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Invalid invoice_date format. Use ISO format.'}), 400
    
    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format. Use ISO format.'}), 400
    
    # Create invoice
    invoice = Invoice(
        invoice_number=data['invoice_number'],
        vendor_id=data['vendor_id'],
        amount=amount,
        reason=data['reason'],
        description=data.get('description'),
        category=data.get('category'),
        authorized_by=data['authorized_by'],
        authorized_at=datetime.utcnow(),
        invoice_date=invoice_date,
        due_date=due_date,
        status=data.get('status', 'pending'),
        payment_method=data.get('payment_method'),
        payment_reference=data.get('payment_reference'),
        notes=data.get('notes'),
        priority=data.get('priority', 'normal'),
        created_by=data.get('created_by', 'System')
    )
    
    db.session.add(invoice)
    db.session.commit()
    return jsonify(invoice.to_dict()), 201

@invoice_bp.route('/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """Get a specific invoice"""
    invoice = Invoice.query.get_or_404(invoice_id)
    return jsonify(invoice.to_dict())

@invoice_bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    """Update an invoice"""
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.json
    
    # Update basic fields
    if data.get('amount'):
        try:
            amount = Decimal(str(data['amount']))
            if amount <= 0:
                return jsonify({'error': 'Amount must be greater than 0'}), 400
            invoice.amount = amount
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400
    
    # Update vendor if provided
    if data.get('vendor_id'):
        vendor = Vendor.query.get(data['vendor_id'])
        if not vendor:
            return jsonify({'error': 'Vendor not found'}), 400
        invoice.vendor_id = data['vendor_id']
    
    # Update other fields
    invoice.reason = data.get('reason', invoice.reason)
    invoice.description = data.get('description', invoice.description)
    invoice.category = data.get('category', invoice.category)
    invoice.status = data.get('status', invoice.status)
    invoice.payment_method = data.get('payment_method', invoice.payment_method)
    invoice.payment_reference = data.get('payment_reference', invoice.payment_reference)
    invoice.notes = data.get('notes', invoice.notes)
    invoice.priority = data.get('priority', invoice.priority)
    
    # Update authorization if provided
    if data.get('authorized_by'):
        invoice.authorized_by = data['authorized_by']
        invoice.authorized_at = datetime.utcnow()
    
    # Update signature if provided
    if data.get('signature_data'):
        invoice.signature_data = data['signature_data']
        invoice.signature_timestamp = datetime.utcnow()
    
    # Update dates if provided
    if data.get('invoice_date'):
        try:
            invoice.invoice_date = datetime.fromisoformat(data['invoice_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid invoice_date format'}), 400
    
    if data.get('due_date'):
        try:
            invoice.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format'}), 400
    
    if data.get('paid_date'):
        try:
            invoice.paid_date = datetime.fromisoformat(data['paid_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid paid_date format'}), 400
    
    db.session.commit()
    return jsonify(invoice.to_dict())

@invoice_bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    """Delete an invoice and its associated files"""
    invoice = Invoice.query.get_or_404(invoice_id)
    
    # Delete associated file if exists
    if invoice.document_filename:
        file_path = os.path.join(UPLOAD_FOLDER, invoice.document_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(invoice)
    db.session.commit()
    return '', 204

@invoice_bp.route('/invoices/<int:invoice_id>/upload', methods=['POST'])
def upload_invoice_document(invoice_id):
    """Upload a document for an invoice"""
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Allowed types: PDF, JPG, PNG, DOC, DOCX, XLS, XLSX'}), 400
    
    upload_folder = get_upload_folder()
    
    # Generate unique filename
    original_filename = secure_filename(file.filename)
    file_extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    
    # Delete old file if exists
    if invoice.document_filename:
        old_file_path = os.path.join(upload_folder, invoice.document_filename)
        if os.path.exists(old_file_path):
            try:
                os.remove(old_file_path)
            except OSError:
                pass  # File might be in use or already deleted
    
    # Save new file
    file_path = os.path.join(upload_folder, unique_filename)
    try:
        file.save(file_path)
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
    
    # Update invoice record
    invoice.document_filename = unique_filename
    invoice.document_original_name = original_filename
    db.session.commit()
    
    return jsonify({
        'message': 'File uploaded successfully',
        'filename': unique_filename,
        'original_name': original_filename,
        'file_size': os.path.getsize(file_path)
    })

@invoice_bp.route('/invoices/<int:invoice_id>/download', methods=['GET'])
def download_invoice_document(invoice_id):
    """Download the document associated with an invoice"""
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if not invoice.document_filename:
        return jsonify({'error': 'No document found for this invoice'}), 404
    
    upload_folder = get_upload_folder()
    file_path = os.path.join(upload_folder, invoice.document_filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'Document file not found on server'}), 404
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=invoice.document_original_name or invoice.document_filename
    )

@invoice_bp.route('/invoices/extract-pdf', methods=['POST'])
def extract_pdf_data():
    """Extract data from uploaded PDF invoice"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported for extraction'}), 400
    
    try:
        # Save temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
            
            # Extract text from PDF
            extracted_data = extract_invoice_data_from_pdf(temp_file.name)
            
            # Clean up temp file
            os.unlink(temp_file.name)
            
            return jsonify(extracted_data)
            
    except Exception as e:
        return jsonify({'error': f'Failed to extract PDF data: {str(e)}'}), 500

def extract_invoice_data_from_pdf(pdf_path):
    """Extract invoice data from PDF using text analysis"""
    try:
        import PyPDF2
        import re
        from datetime import datetime
        
        # Extract text from PDF
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        # Initialize extracted data
        extracted_data = {
            'invoice_number': None,
            'amount': None,
            'vendor_name': None,
            'invoice_date': None,
            'due_date': None,
            'description': None,
            'raw_text': text[:1000]  # First 1000 chars for debugging
        }
        
        # Extract invoice number (common patterns)
        invoice_patterns = [
            r'invoice\s*#?\s*:?\s*([A-Z0-9\-]+)',
            r'inv\s*#?\s*:?\s*([A-Z0-9\-]+)',
            r'number\s*:?\s*([A-Z0-9\-]+)',
            r'#\s*([A-Z0-9\-]+)'
        ]
        
        for pattern in invoice_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted_data['invoice_number'] = match.group(1)
                break
        
        # Extract amounts (currency patterns)
        amount_patterns = [
            r'total\s*:?\s*\$?\s*([0-9,]+\.?\d*)',
            r'amount\s*:?\s*\$?\s*([0-9,]+\.?\d*)',
            r'due\s*:?\s*\$?\s*([0-9,]+\.?\d*)',
            r'\$\s*([0-9,]+\.?\d*)',
            r'R\$\s*([0-9,]+\.?\d*)'
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    extracted_data['amount'] = float(amount_str)
                    break
                except ValueError:
                    continue
        
        # Extract dates
        date_patterns = [
            r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'(\d{2,4}[\/\-]\d{1,2}[\/\-]\d{1,2})',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{2,4}'
        ]
        
        dates_found = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates_found.extend(matches)
        
        if dates_found:
            # Try to parse the first date found
            try:
                date_str = dates_found[0]
                # Simple date parsing - you might want to improve this
                extracted_data['invoice_date'] = date_str
            except:
                pass
        
        # Extract vendor/company name (look for common patterns)
        vendor_patterns = [
            r'from\s*:?\s*([A-Za-z\s&]+(?:LLC|Inc|Corp|Ltd|Co\.)?)',
            r'bill\s+to\s*:?\s*([A-Za-z\s&]+(?:LLC|Inc|Corp|Ltd|Co\.)?)',
            r'^([A-Za-z\s&]+(?:LLC|Inc|Corp|Ltd|Co\.)?)$'
        ]
        
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if len(line) > 3 and len(line) < 50:  # Reasonable company name length
                # Skip common invoice terms
                skip_terms = ['invoice', 'bill', 'total', 'amount', 'date', 'number', 'due']
                if not any(term in line.lower() for term in skip_terms):
                    if re.match(r'^[A-Za-z\s&\.,\-]+$', line):  # Only letters, spaces, common punctuation
                        extracted_data['vendor_name'] = line
                        break
        
        # Extract description/items (look for line items)
        description_lines = []
        for line in lines:
            line = line.strip()
            # Look for lines that might be item descriptions
            if len(line) > 10 and len(line) < 100:
                # Skip lines with only numbers or dates
                if not re.match(r'^[\d\s\$\.,\-\/]+$', line):
                    description_lines.append(line)
        
        if description_lines:
            extracted_data['description'] = ' | '.join(description_lines[:3])  # First 3 items
        
        return extracted_data
        
    except ImportError:
        # PyPDF2 not available, return basic structure
        return {
            'error': 'PDF extraction library not available',
            'invoice_number': None,
            'amount': None,
            'vendor_name': None,
            'invoice_date': None,
            'due_date': None,
            'description': None
        }
    except Exception as e:
        return {
            'error': f'PDF extraction failed: {str(e)}',
            'invoice_number': None,
            'amount': None,
            'vendor_name': None,
            'invoice_date': None,
            'due_date': None,
            'description': None
        }

@invoice_bp.route('/invoices/<int:invoice_id>/sign', methods=['POST'])
def sign_invoice(invoice_id):
    """Add digital signature to an invoice"""
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.json
    
    if not data.get('signature_data'):
        return jsonify({'error': 'Signature data is required'}), 400
    
    invoice.signature_data = data['signature_data']
    invoice.signature_timestamp = datetime.utcnow()
    
    # Update status to approved if it was pending
    if invoice.status == 'pending':
        invoice.status = 'approved'
    
    db.session.commit()
    return jsonify({
        'message': 'Invoice signed successfully',
        'signature_timestamp': invoice.signature_timestamp.isoformat()
    })

@invoice_bp.route('/invoices/categories', methods=['GET'])
def get_invoice_categories():
    """Get available invoice categories"""
    categories = [
        'maintenance',
        'utilities',
        'insurance',
        'security',
        'cleaning',
        'landscaping',
        'administrative',
        'legal',
        'equipment',
        'supplies',
        'other'
    ]
    return jsonify(categories)

@invoice_bp.route('/invoices/stats', methods=['GET'])
def get_invoice_stats():
    """Get invoice statistics"""
    total_invoices = Invoice.query.count()
    pending_invoices = Invoice.query.filter_by(status='pending').count()
    approved_invoices = Invoice.query.filter_by(status='approved').count()
    paid_invoices = Invoice.query.filter_by(status='paid').count()
    
    # Calculate total amounts
    total_amount = db.session.query(db.func.sum(Invoice.amount)).scalar() or 0
    pending_amount = db.session.query(db.func.sum(Invoice.amount)).filter_by(status='pending').scalar() or 0
    paid_amount = db.session.query(db.func.sum(Invoice.amount)).filter_by(status='paid').scalar() or 0
    
    return jsonify({
        'total_invoices': total_invoices,
        'pending_invoices': pending_invoices,
        'approved_invoices': approved_invoices,
        'paid_invoices': paid_invoices,
        'total_amount': float(total_amount),
        'pending_amount': float(pending_amount),
        'paid_amount': float(paid_amount)
    })

