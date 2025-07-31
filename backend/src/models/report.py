from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json

Base = declarative_base()

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    type = Column(String(100), nullable=False)  # monthly, quarterly, annual, custom
    category = Column(String(100), nullable=False)  # financial, transparency, maintenance, etc.
    description = Column(Text)
    
    # Report configuration
    template_name = Column(String(200), nullable=False)
    parameters = Column(Text)  # JSON string with report parameters
    
    # Scheduling
    is_scheduled = Column(Boolean, default=False)
    schedule_frequency = Column(String(50))  # monthly, quarterly, annually
    schedule_day = Column(Integer)  # Day of month/quarter/year to generate
    last_generated = Column(DateTime)
    next_generation = Column(DateTime)
    
    # Email settings
    email_enabled = Column(Boolean, default=True)
    email_recipients = Column(Text)  # JSON array of email addresses
    email_subject_template = Column(String(500))
    email_body_template = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'category': self.category,
            'description': self.description,
            'template_name': self.template_name,
            'parameters': json.loads(self.parameters) if self.parameters else {},
            'is_scheduled': self.is_scheduled,
            'schedule_frequency': self.schedule_frequency,
            'schedule_day': self.schedule_day,
            'last_generated': self.last_generated.isoformat() if self.last_generated else None,
            'next_generation': self.next_generation.isoformat() if self.next_generation else None,
            'email_enabled': self.email_enabled,
            'email_recipients': json.loads(self.email_recipients) if self.email_recipients else [],
            'email_subject_template': self.email_subject_template,
            'email_body_template': self.email_body_template,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ReportGeneration(Base):
    __tablename__ = 'report_generations'
    
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, nullable=False)
    
    # Generation details
    generated_at = Column(DateTime, default=datetime.utcnow)
    generated_by = Column(String(200))  # User who generated or 'system' for automatic
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    
    # File details
    file_name = Column(String(500))
    file_path = Column(String(1000))
    file_size = Column(Integer)
    
    # Email details
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime)
    email_recipients_count = Column(Integer, default=0)
    email_error = Column(Text)
    
    # Status
    status = Column(String(50), default='generated')  # generated, sent, failed
    error_message = Column(Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'report_id': self.report_id,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'generated_by': self.generated_by,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'email_sent': self.email_sent,
            'email_sent_at': self.email_sent_at.isoformat() if self.email_sent_at else None,
            'email_recipients_count': self.email_recipients_count,
            'email_error': self.email_error,
            'status': self.status,
            'error_message': self.error_message
        }

class ReportTemplate(Base):
    __tablename__ = 'report_templates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)
    
    # Template configuration
    template_type = Column(String(50), default='pdf')  # pdf, excel, csv
    template_content = Column(Text)  # HTML template or configuration
    
    # Data requirements
    required_data_sources = Column(Text)  # JSON array of required data sources
    default_parameters = Column(Text)  # JSON object with default parameters
    
    # Styling
    header_template = Column(Text)
    footer_template = Column(Text)
    css_styles = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'template_type': self.template_type,
            'template_content': self.template_content,
            'required_data_sources': json.loads(self.required_data_sources) if self.required_data_sources else [],
            'default_parameters': json.loads(self.default_parameters) if self.default_parameters else {},
            'header_template': self.header_template,
            'footer_template': self.footer_template,
            'css_styles': self.css_styles,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

