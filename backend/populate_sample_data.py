#!/usr/bin/env python3
"""
Script to populate the HOA management system with sample data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
import random
from src.models.user import db, User
from src.models.vendor import Vendor
from src.models.payment import Payment
from src.models.invoice import Invoice
from src.models.maintenance import MaintenanceRequest, MaintenanceUpdate
from src.models.event import Event, EventRSVP
from src.models.violation import Violation, ViolationAction
from src.models.associate import Associate
from src.main import app

def clear_existing_data():
    """Clear existing sample data"""
    print("Clearing existing data...")
    with app.app_context():
        # Clear in reverse order of dependencies
        db.session.query(EventRSVP).delete()
        db.session.query(ViolationAction).delete()
        db.session.query(MaintenanceUpdate).delete()
        db.session.query(Payment).delete()
        db.session.query(Invoice).delete()
        db.session.query(MaintenanceRequest).delete()
        db.session.query(Event).delete()
        db.session.query(Violation).delete()
        db.session.query(Associate).delete()
        db.session.query(Vendor).delete()
        db.session.query(User).delete()
        db.session.commit()
        print("Existing data cleared.")

def create_sample_residents():
    """Create sample residents"""
    print("Creating sample residents...")
    residents = [
        {"name": "Maria Silva Santos", "email": "maria.silva@email.com", "building": 1, "apartment": "101", "phone": "(11) 99999-1001"},
        {"name": "João Carlos Oliveira", "email": "joao.oliveira@email.com", "building": 1, "apartment": "102", "phone": "(11) 99999-1002"},
        {"name": "Ana Paula Costa", "email": "ana.costa@email.com", "building": 2, "apartment": "201", "phone": "(11) 99999-1003"},
        {"name": "Carlos Eduardo Lima", "email": "carlos.lima@email.com", "building": 2, "apartment": "202", "phone": "(11) 99999-1004"},
        {"name": "Fernanda Rodrigues", "email": "fernanda.rodrigues@email.com", "building": 3, "apartment": "301", "phone": "(11) 99999-1005"},
        {"name": "Roberto Almeida", "email": "roberto.almeida@email.com", "building": 3, "apartment": "302", "phone": "(11) 99999-1006"},
        {"name": "Juliana Pereira", "email": "juliana.pereira@email.com", "building": 4, "apartment": "401", "phone": "(11) 99999-1007"},
        {"name": "Marcos Antonio", "email": "marcos.antonio@email.com", "building": 5, "apartment": "101", "phone": "(11) 99999-1008"},
    ]
    
    for resident_data in residents:
        resident = User(
            name=resident_data["name"],
            email=resident_data["email"],
            building=resident_data["building"],
            apartment=resident_data["apartment"],
            phone=resident_data["phone"]
        )
        db.session.add(resident)
    
    db.session.commit()
    print(f"Created {len(residents)} residents.")

def create_sample_vendors():
    """Create sample vendors"""
    print("Creating sample vendors...")
    vendors = [
        {"name": "Empresa de Limpeza Clean Master", "email": "contato@cleanmaster.com", "phone": "(11) 3333-1001", "services": "Limpeza e conservação predial"},
        {"name": "Segurança Total Ltda", "email": "comercial@segurancatotal.com", "phone": "(11) 3333-1002", "services": "Serviços de segurança e portaria"},
        {"name": "Jardinagem Verde Vida", "email": "atendimento@verdevida.com", "phone": "(11) 3333-1003", "services": "Jardinagem e paisagismo"},
        {"name": "Manutenção Predial Pro", "email": "servicos@predialPro.com", "phone": "(11) 3333-1004", "services": "Manutenção predial e reparos"},
        {"name": "Elevadores Express", "email": "manutencao@elevadoresexpress.com", "phone": "(11) 3333-1005", "services": "Manutenção de elevadores"},
        {"name": "Piscinas Cristal", "email": "contato@piscinascristal.com", "phone": "(11) 3333-1006", "services": "Tratamento e manutenção de piscinas"},
        {"name": "Elétrica São Paulo", "email": "eletrica@eletricasp.com", "phone": "(11) 3333-1007", "services": "Serviços elétricos e instalações"},
    ]
    
    for vendor_data in vendors:
        vendor = Vendor(
            name=vendor_data["name"],
            email=vendor_data["email"],
            phone=vendor_data["phone"],
            services=vendor_data["services"]
        )
        db.session.add(vendor)
    
    db.session.commit()
    print(f"Created {len(vendors)} vendors.")

def create_sample_associates():
    """Create sample associates (employees)"""
    print("Creating sample associates...")
    associates = [
        {"name": "José da Silva", "position": "Porteiro", "department": "Doorman", "work_area": "Buildings", "monthly_salary": 2500.00, "hire_date": "2023-01-15", "status": "Active"},
        {"name": "Maria das Graças", "position": "Faxineira", "department": "Cleaning", "work_area": "Buildings", "monthly_salary": 2200.00, "hire_date": "2023-02-01", "status": "Active"},
        {"name": "Carlos Santos", "position": "Zelador", "department": "Maintenance", "work_area": "Mixed", "monthly_salary": 2800.00, "hire_date": "2023-03-10", "status": "Active"},
        {"name": "Ana Lucia", "position": "Administradora", "department": "HOA", "work_area": "HOA", "monthly_salary": 4500.00, "hire_date": "2022-11-20", "status": "Active"},
        {"name": "Pedro Oliveira", "position": "Segurança", "department": "Security", "work_area": "Buildings", "monthly_salary": 2600.00, "hire_date": "2023-04-05", "status": "Active"},
    ]
    
    for associate_data in associates:
        associate = Associate(
            name=associate_data["name"],
            position=associate_data["position"],
            department=associate_data["department"],
            work_area=associate_data["work_area"],
            monthly_salary=associate_data["monthly_salary"],
            hire_date=datetime.strptime(associate_data["hire_date"], "%Y-%m-%d").date(),
            status=associate_data["status"]
        )
        db.session.add(associate)
    
    db.session.commit()
    print(f"Created {len(associates)} associates.")

def create_sample_payments():
    """Create sample payments"""
    print("Creating sample payments...")
    residents = db.session.query(User).all()
    
    payments = []
    for i in range(15):  # Create 15 payments over the last 3 months
        resident = random.choice(residents)
        payment_date = datetime.now() - timedelta(days=random.randint(1, 90))
        amount = random.choice([850.00, 950.00, 1050.00, 1150.00])  # Different condo fees
        
        payment = Payment(
            resident_id=resident.id,
            amount=amount,
            payment_type="dues",
            payment_date=payment_date,
            description=f"Taxa de condomínio - {payment_date.strftime('%m/%Y')}",
            payment_method=random.choice(["PIX", "Transferência", "Boleto"])
        )
        payments.append(payment)
        db.session.add(payment)
    
    db.session.commit()
    print(f"Created {len(payments)} payments.")

def create_sample_invoices():
    """Create sample invoices"""
    print("Creating sample invoices...")
    vendors = db.session.query(Vendor).all()
    
    invoices = []
    categories = ["Limpeza", "Segurança", "Manutenção", "Jardinagem", "Elevadores", "Utilidades", "Administração"]
    
    for i in range(12):  # Create 12 invoices over the last 3 months
        vendor = random.choice(vendors)
        invoice_date = datetime.now() - timedelta(days=random.randint(1, 90))
        amount = random.uniform(500.00, 5000.00)
        category = random.choice(categories)
        
        invoice = Invoice(
            invoice_number=f"INV-{2025}-{i+1:04d}",
            vendor_id=vendor.id,
            amount=round(amount, 2),
            reason=f"Serviços de {category.lower()} conforme contrato",
            description=f"Serviços de {category.lower()} - {invoice_date.strftime('%m/%Y')}",
            category=category,
            authorized_by="Ana Lucia - Administradora",
            invoice_date=invoice_date,
            due_date=invoice_date + timedelta(days=30),
            status=random.choice(["pending", "approved", "paid"])
        )
        invoices.append(invoice)
        db.session.add(invoice)
    
    db.session.commit()
    print(f"Created {len(invoices)} invoices.")

def create_sample_maintenance():
    """Create sample maintenance requests"""
    print("Creating sample maintenance requests...")
    residents = db.session.query(User).all()
    
    requests = []
    issues = [
        "Vazamento no banheiro",
        "Problema na fechadura da porta",
        "Lâmpada queimada no corredor",
        "Elevador fazendo ruído estranho",
        "Infiltração na parede",
        "Problema na torneira da cozinha",
        "Porta do interfone não abre",
        "Problema no ar condicionado"
    ]
    
    for i in range(10):
        resident = random.choice(residents)
        created_date = datetime.now() - timedelta(days=random.randint(1, 60))
        issue = random.choice(issues)
        
        request = MaintenanceRequest(
            resident_id=resident.id,
            title=issue,
            description=f"Solicitação de reparo: {issue}. Problema identificado no prédio {resident.building}, apartamento {resident.apartment}.",
            priority=random.choice(["low", "medium", "high"]),
            status=random.choice(["open", "in_progress", "completed"]),
            created_at=created_date
        )
        requests.append(request)
        db.session.add(request)
    
    db.session.commit()
    
    # Add some updates to maintenance requests
    for request in requests[:5]:  # Add updates to first 5 requests
        update = MaintenanceUpdate(
            maintenance_request_id=request.id,
            update_text=f"Técnico designado para verificar o problema. Agendado para próxima semana.",
            created_at=request.created_at + timedelta(days=2)
        )
        db.session.add(update)
    
    db.session.commit()
    print(f"Created {len(requests)} maintenance requests with updates.")

def create_sample_events():
    """Create sample events"""
    print("Creating sample events...")
    
    events = [
        {
            "title": "Assembleia Geral Ordinária",
            "description": "Assembleia anual para aprovação do orçamento e prestação de contas",
            "date": datetime.now() + timedelta(days=30),
            "location": "Salão de Festas",
            "max_attendees": 100
        },
        {
            "title": "Festa Junina do Condomínio",
            "description": "Festa tradicional com comidas típicas e quadrilha",
            "date": datetime.now() + timedelta(days=15),
            "location": "Área de Lazer",
            "max_attendees": 150
        },
        {
            "title": "Reunião do Conselho",
            "description": "Reunião mensal do conselho consultivo",
            "date": datetime.now() + timedelta(days=7),
            "location": "Sala de Reuniões",
            "max_attendees": 20
        },
        {
            "title": "Curso de Primeiros Socorros",
            "description": "Treinamento básico de primeiros socorros para moradores",
            "date": datetime.now() + timedelta(days=45),
            "location": "Salão de Festas",
            "max_attendees": 30
        },
        {
            "title": "Campanha de Vacinação Pet",
            "description": "Vacinação gratuita para cães e gatos dos moradores",
            "date": datetime.now() + timedelta(days=20),
            "location": "Área Externa",
            "max_attendees": 50
        }
    ]
    
    residents = db.session.query(User).all()
    
    for event_data in events:
        event = Event(
            title=event_data["title"],
            description=event_data["description"],
            event_date=event_data["date"],
            location=event_data["location"],
            max_attendees=event_data["max_attendees"]
        )
        db.session.add(event)
        db.session.flush()  # Get the event ID
        
        # Add some RSVPs
        num_rsvps = random.randint(5, min(15, len(residents)))
        selected_residents = random.sample(residents, num_rsvps)
        
        for resident in selected_residents:
            rsvp = EventRSVP(
                event_id=event.id,
                resident_id=resident.id,
                response=random.choice(["yes", "no", "maybe"])
            )
            db.session.add(rsvp)
    
    db.session.commit()
    print(f"Created {len(events)} events with RSVPs.")

def create_sample_violations():
    """Create sample violations"""
    print("Creating sample violations...")
    residents = db.session.query(User).all()
    
    violations = [
        {
            "type": "Ruído excessivo",
            "description": "Música alta após 22h em dia de semana",
            "severity": "Medium"
        },
        {
            "type": "Uso inadequado da área comum",
            "description": "Deixou objetos pessoais na área da piscina",
            "severity": "Low"
        },
        {
            "type": "Descumprimento de regras de pets",
            "description": "Cachorro solto na área comum sem coleira",
            "severity": "Medium"
        },
        {
            "type": "Estacionamento irregular",
            "description": "Veículo estacionado em vaga de visitante por mais de 24h",
            "severity": "Low"
        },
        {
            "type": "Alteração não autorizada",
            "description": "Instalação de ar condicionado sem aprovação do condomínio",
            "severity": "High"
        },
        {
            "type": "Descarte irregular de lixo",
            "description": "Lixo colocado fora do horário estabelecido",
            "severity": "Low"
        }
    ]
    
    for i in range(8):
        resident = random.choice(residents)
        violation_data = random.choice(violations)
        reported_date = datetime.now() - timedelta(days=random.randint(1, 45))
        
        violation = Violation(
            resident_id=resident.id,
            violation_type=violation_data["type"],
            description=violation_data["description"],
            severity=violation_data["severity"],
            status=random.choice(["open", "resolved", "dismissed"]),
            reported_date=reported_date
        )
        db.session.add(violation)
        db.session.flush()  # Get the violation ID
        
        # Add some actions
        if random.choice([True, False]):
            action = ViolationAction(
                violation_id=violation.id,
                action_type=random.choice(["warning", "fine", "communication"]),
                description=f"Notificação enviada ao morador sobre {violation_data['type'].lower()}",
                created_at=reported_date + timedelta(days=random.randint(1, 7))
            )
            db.session.add(action)
    
    db.session.commit()
    print(f"Created violations with actions.")

def main():
    """Main function to populate all sample data"""
    print("Starting to populate HOA management system with sample data...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Clear existing data first
        clear_existing_data()
        
        # Create sample data
        create_sample_residents()
        create_sample_vendors()
        create_sample_associates()
        create_sample_payments()
        create_sample_invoices()
        create_sample_maintenance()
        create_sample_events()
        create_sample_violations()
        
        print("\n✅ Sample data population completed successfully!")
        print("\nSummary:")
        print(f"- Residents: {db.session.query(User).count()}")
        print(f"- Vendors: {db.session.query(Vendor).count()}")
        print(f"- Associates: {db.session.query(Associate).count()}")
        print(f"- Payments: {db.session.query(Payment).count()}")
        print(f"- Invoices: {db.session.query(Invoice).count()}")
        print(f"- Maintenance Requests: {db.session.query(MaintenanceRequest).count()}")
        print(f"- Events: {db.session.query(Event).count()}")
        print(f"- Violations: {db.session.query(Violation).count()}")

if __name__ == "__main__":
    main()

