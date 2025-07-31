from datetime import datetime
from src.models.user import db

class Associate(db.Model):
    __tablename__ = 'associate'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Information
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    mobile = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    cpf = db.Column(db.String(14), unique=True, nullable=True)  # Brazilian CPF
    rg = db.Column(db.String(20), nullable=True)  # Brazilian RG
    nationality = db.Column(db.String(50), nullable=True)
    marital_status = db.Column(db.String(20), nullable=True)  # Single, Married, Divorced, Widowed
    
    # Employment Information
    employee_id = db.Column(db.String(20), unique=True, nullable=True)
    department = db.Column(db.String(50), nullable=False)  # Cleaning, HOA, Gardening, Maintenance, Doorman
    work_area = db.Column(db.String(50), nullable=False)   # HOA, Club, Buildings, Mixed
    position = db.Column(db.String(100), nullable=True)
    hire_date = db.Column(db.Date, nullable=True)
    contract_type = db.Column(db.String(50), nullable=True)  # Full-time, Part-time, Contract, Temporary
    work_schedule = db.Column(db.String(100), nullable=True)  # e.g., "Monday-Friday 8AM-5PM"
    status = db.Column(db.String(20), default='Active')    # Active, Inactive, On Leave, Terminated
    
    # Financial Information
    monthly_salary = db.Column(db.Numeric(10, 2), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)  # Bank Transfer, Cash, Check
    bank_name = db.Column(db.String(100), nullable=True)
    bank_account = db.Column(db.String(50), nullable=True)
    bank_agency = db.Column(db.String(20), nullable=True)
    pix_key = db.Column(db.String(100), nullable=True)
    
    # Emergency Contact
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_relationship = db.Column(db.String(50), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    emergency_contact_address = db.Column(db.Text, nullable=True)
    
    # Documents and Files
    curriculum_filename = db.Column(db.String(255), nullable=True)
    contract_filename = db.Column(db.String(255), nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    documents_notes = db.Column(db.Text, nullable=True)
    
    # Additional Information
    education_level = db.Column(db.String(50), nullable=True)  # Elementary, High School, College, Graduate
    certifications = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    languages = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Performance and Evaluation
    last_evaluation_date = db.Column(db.Date, nullable=True)
    performance_rating = db.Column(db.String(20), nullable=True)  # Excellent, Good, Average, Needs Improvement
    
    # System fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            # Personal Information
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'mobile': self.mobile,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'cpf': self.cpf,
            'rg': self.rg,
            'nationality': self.nationality,
            'marital_status': self.marital_status,
            
            # Employment Information
            'employee_id': self.employee_id,
            'department': self.department,
            'work_area': self.work_area,
            'position': self.position,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'contract_type': self.contract_type,
            'work_schedule': self.work_schedule,
            'status': self.status,
            
            # Financial Information
            'monthly_salary': float(self.monthly_salary) if self.monthly_salary else None,
            'payment_method': self.payment_method,
            'bank_name': self.bank_name,
            'bank_account': self.bank_account,
            'bank_agency': self.bank_agency,
            'pix_key': self.pix_key,
            
            # Emergency Contact
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_relationship': self.emergency_contact_relationship,
            'emergency_contact_phone': self.emergency_contact_phone,
            'emergency_contact_address': self.emergency_contact_address,
            
            # Documents
            'curriculum_filename': self.curriculum_filename,
            'contract_filename': self.contract_filename,
            'photo_filename': self.photo_filename,
            'documents_notes': self.documents_notes,
            
            # Additional Information
            'education_level': self.education_level,
            'certifications': self.certifications,
            'skills': self.skills,
            'languages': self.languages,
            'notes': self.notes,
            
            # Performance
            'last_evaluation_date': self.last_evaluation_date.isoformat() if self.last_evaluation_date else None,
            'performance_rating': self.performance_rating,
            
            # System fields
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by
        }
    
    @staticmethod
    def get_departments():
        """Get list of valid departments"""
        return ['Cleaning', 'HOA', 'Gardening', 'Maintenance', 'Doorman']
    
    @staticmethod
    def get_work_areas():
        """Get list of valid work areas"""
        return ['HOA', 'Club', 'Buildings', 'Mixed']
    
    @staticmethod
    def get_contract_types():
        """Get list of valid contract types"""
        return ['Full-time', 'Part-time', 'Contract', 'Temporary']
    
    @staticmethod
    def get_marital_statuses():
        """Get list of valid marital statuses"""
        return ['Single', 'Married', 'Divorced', 'Widowed', 'Other']
    
    @staticmethod
    def get_education_levels():
        """Get list of valid education levels"""
        return ['Elementary', 'High School', 'Technical', 'College', 'Graduate', 'Post-Graduate']
    
    @staticmethod
    def get_payment_methods():
        """Get list of valid payment methods"""
        return ['Bank Transfer', 'PIX', 'Cash', 'Check']
    
    @staticmethod
    def get_performance_ratings():
        """Get list of valid performance ratings"""
        return ['Excellent', 'Good', 'Average', 'Needs Improvement', 'Unsatisfactory']
    
    @staticmethod
    def get_statuses():
        """Get list of valid employee statuses"""
        return ['Active', 'Inactive', 'On Leave', 'Terminated', 'Suspended']
    
    @staticmethod
    def validate_department(department):
        """Validate if department is valid"""
        return department in Associate.get_departments()
    
    @staticmethod
    def validate_work_area(work_area):
        """Validate if work area is valid"""
        return work_area in Associate.get_work_areas()
    
    @staticmethod
    def validate_cpf(cpf):
        """Basic CPF format validation"""
        if not cpf:
            return True  # CPF is optional
        # Remove non-digits
        cpf = ''.join(filter(str.isdigit, cpf))
        return len(cpf) == 11

