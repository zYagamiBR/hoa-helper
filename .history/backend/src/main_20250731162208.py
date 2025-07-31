import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.vendor import Vendor
from src.models.payment import Payment
from src.models.invoice import Invoice
from src.models.maintenance import MaintenanceRequest, MaintenanceUpdate
from src.models.event import Event, EventRSVP
from src.models.violation import Violation, ViolationAction
from src.models.associate import Associate
from src.models.bill import Bill
from src.models.report import Report, ReportGeneration, ReportTemplate
from src.routes.user import user_bp
from src.routes.vendor import vendor_bp
from src.routes.payment import payment_bp
from src.routes.invoice import invoice_bp
from src.routes.maintenance import maintenance_bp
from src.routes.event import event_bp
from src.routes.violation import violation_bp
from src.routes.associate import associate_bp
from src.routes.bill import bill_bp
from src.routes.import_export import import_export_bp
from src.routes.report_simple import report_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# File upload configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# Ensure upload directories exist
upload_dirs = [
    os.path.join(app.config['UPLOAD_FOLDER'], 'invoices'),
    os.path.join(app.config['UPLOAD_FOLDER'], 'maintenance'),
    os.path.join(app.config['UPLOAD_FOLDER'], 'associates')
]
for upload_dir in upload_dirs:
    os.makedirs(upload_dir, exist_ok=True)

# Enable CORS for all routes and origins
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


# Register all API blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(vendor_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')
app.register_blueprint(invoice_bp, url_prefix='/api')
app.register_blueprint(maintenance_bp, url_prefix='/api')
app.register_blueprint(event_bp, url_prefix='/api')
app.register_blueprint(violation_bp, url_prefix='/api')
app.register_blueprint(associate_bp, url_prefix='/api')
app.register_blueprint(bill_bp, url_prefix='/api')
app.register_blueprint(import_export_bp, url_prefix='/api/import-export')
app.register_blueprint(report_bp)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    if not os.path.exists(db_path):
        db.create_all()
        # Create sample data if database is empty
        from src.models.user import User
        if User.query.count() == 0:
            sample_vendor = Vendor(
                name='ABC Plumbing',
                email='contact@abcplumbing.com',
                phone='555-9876',
                services='Plumbing repairs and maintenance'
            )
            db.session.add(sample_vendor)
            db.session.commit()
        # Add sample vendor
        sample_vendor = Vendor(
            name='ABC Plumbing',
            email='contact@abcplumbing.com',
            phone='555-9876',
            services='Plumbing repairs and maintenance'
        )
        db.session.add(sample_vendor)
        db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
