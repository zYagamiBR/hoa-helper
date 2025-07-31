from flask import Blueprint, request, jsonify, send_file, current_app
from src.models.report import Report
from src.services.simple_report_generator import SimpleReportGenerator
from src.models.user import db
import os
from datetime import datetime
from src.models.user import User

report_bp = Blueprint('report', __name__)

@report_bp.route('/api/reports', methods=['GET'])
def get_reports():
    """Lista todos os relatórios configurados"""
    try:
        reports = db.session.query(Report).filter(Report.is_active == True).all()
        return jsonify([report.to_dict() for report in reports])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports', methods=['POST'])
def create_report():
    """Cria uma nova configuração de relatório"""
    try:
        data = request.get_json()
        
        report = Report(
            name=data['name'],
            type=data['type'],
            category=data['category'],
            description=data.get('description'),
            template_name=data['template_name'],
            parameters=json.dumps(data.get('parameters', {})),
            is_scheduled=data.get('is_scheduled', False),
            schedule_frequency=data.get('schedule_frequency'),
            schedule_day=data.get('schedule_day'),
            email_enabled=data.get('email_enabled', True),
            email_recipients=json.dumps(data.get('email_recipients', [])),
            email_subject_template=data.get('email_subject_template'),
            email_body_template=data.get('email_body_template')
        )
        
        db.session.add(report)
        db.session.commit()
        
        return jsonify(report.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    """Atualiza configuração de relatório"""
    try:
report = db.session.query(Report).get(report_id)
        if not report:
            return jsonify({'error': 'Relatório não encontrado'}), 404
        
        data = request.get_json()
        
        report.name = data.get('name', report.name)
        report.type = data.get('type', report.type)
        report.category = data.get('category', report.category)
        report.description = data.get('description', report.description)
        report.template_name = data.get('template_name', report.template_name)
        report.parameters = json.dumps(data.get('parameters', json.loads(report.parameters or '{}')))
        report.is_scheduled = data.get('is_scheduled', report.is_scheduled)
        report.schedule_frequency = data.get('schedule_frequency', report.schedule_frequency)
        report.schedule_day = data.get('schedule_day', report.schedule_day)
        report.email_enabled = data.get('email_enabled', report.email_enabled)
        report.email_recipients = json.dumps(data.get('email_recipients', json.loads(report.email_recipients or '[]')))
        report.email_subject_template = data.get('email_subject_template', report.email_subject_template)
        report.email_body_template = data.get('email_body_template', report.email_body_template)
        report.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(report.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """Remove configuração de relatório"""
    try:
report = db.session.query(Report).get(report_id)
        if not report:
            return jsonify({'error': 'Relatório não encontrado'}), 404
        
        report.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Relatório removido com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/<int:report_id>/generate', methods=['POST'])
def generate_report(report_id):
    """Gera um relatório específico"""
    try:
report = db.session.query(Report).get(report_id)
        if not report:
            return jsonify({'error': 'Relatório não encontrado'}), 404
        
        data = request.get_json() or {}
        generator = SimpleReportGenerator(db)
        
        # Parâmetros do relatório
        year = data.get('year', datetime.now().year)
        month = data.get('month', datetime.now().month)
        quarter = data.get('quarter', ((datetime.now().month - 1) // 3) + 1)
        
        # Gerar relatório baseado no tipo
        if report.template_name == 'financial_monthly':
            result = generator.generate_financial_monthly_report(year, month)
            period_start = datetime(year, month, 1)
            if month == 12:
                period_end = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                period_end = datetime(year, month + 1, 1) - timedelta(days=1)
        elif report.template_name == 'transparency_monthly':
            result = generator.generate_transparency_monthly_report(year, month)
            period_start = datetime(year, month, 1)
            if month == 12:
                period_end = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                period_end = datetime(year, month + 1, 1) - timedelta(days=1)
        elif report.template_name == 'annual_comparative':
            result = generator.generate_annual_comparative_report(year)
            period_start = datetime(year, 1, 1)
            period_end = datetime(year, 12, 31)
        else:
            return jsonify({'error': 'Tipo de relatório não suportado'}), 400
        
        # Salvar registro de geração
        generation = ReportGeneration(
            report_id=report.id,
            generated_by=data.get('generated_by', 'system'),
            period_start=period_start,
            period_end=period_end,
            file_name=result['filename'],
            file_path=result['filepath'],
            file_size=result['size'],
            status='generated'
        )
        
        db.session.add(generation)
        
        # Enviar por email se configurado
        if report.email_enabled and report.email_recipients:
            recipients = json.loads(report.email_recipients)
            if not recipients:
                # Se não há destinatários específicos, enviar para todos os moradores
                users = db.session.query(User).filter(User.email.isnot(None)).all()
                recipients = [user.email for user in users if user.email]
            
            if recipients:
                email_result = generator.send_report_email(generation, recipients)
                generation.email_sent = email_result['success']
                generation.email_sent_at = datetime.utcnow() if email_result['success'] else None
                generation.email_recipients_count = email_result['sent_count']
                generation.email_error = email_result.get('error')
                generation.status = 'sent' if email_result['success'] else 'failed'
        
        # Atualizar última geração do relatório
        report.last_generated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Relatório gerado com sucesso',
            'generation': generation.to_dict(),
            'download_url': f'/api/reports/download/{generation.id}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/download/<int:generation_id>', methods=['GET'])
def download_report(generation_id):
    """Download de relatório gerado"""
    try:
generation = db.session.query(ReportGeneration).get(generation_id)
        if not generation:
            return jsonify({'error': 'Relatório não encontrado'}), 404
        
        if not os.path.exists(generation.file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        return send_file(
            generation.file_path,
            as_attachment=True,
            download_name=generation.file_name,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/generations', methods=['GET'])
def get_report_generations():
    """Lista histórico de gerações de relatórios"""
    try:
page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        generations = db.session.query(ReportGeneration)\
            .order_by(ReportGeneration.generated_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'generations': [gen.to_dict() for gen in generations.items],
            'total': generations.total,
            'pages': generations.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/templates', methods=['GET'])
def get_report_templates():
    """Lista templates de relatórios disponíveis"""
    try:
        templates = [
            {
                'name': 'financial_monthly',
                'display_name': 'Relatório Financeiro Mensal',
                'description': 'Relatório mensal com receitas, despesas e análise financeira',
                'category': 'financial',
                'parameters': ['year', 'month']
            },
            {
                'name': 'transparency_quarterly',
                'display_name': 'Relatório de Transparência Trimestral',
                'description': 'Relatório trimestral de transparência com despesas por grupo',
                'category': 'transparency',
                'parameters': ['year', 'quarter']
            },
            {
                'name': 'annual_comparative',
                'display_name': 'Relatório Anual Comparativo',
                'description': 'Comparativo de 5 anos com evolução financeira',
                'category': 'comparative',
                'parameters': ['year']
            }
        ]
        
        return jsonify(templates)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/quick-generate', methods=['POST'])
def quick_generate_report():
    """Geração rápida de relatório sem configuração prévia"""
    try:
        data = request.get_json()
        
        template_name = data.get('template_name')
        year = data.get('year', datetime.now().year)
        month = data.get('month', datetime.now().month)
        quarter = data.get('quarter', ((datetime.now().month - 1) // 3) + 1)
        
        generator = SimpleReportGenerator(db)
        
        # Gerar relatório baseado no template
        if template_name == 'financial_monthly':
            result = generator.generate_financial_monthly_report(year, month)
            period_start = datetime(year, month, 1)
            if month == 12:
                period_end = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                period_end = datetime(year, month + 1, 1) - timedelta(days=1)
        elif template_name == 'transparency_monthly':
            result = generator.generate_transparency_monthly_report(year, month)
            period_start = datetime(year, month, 1)
            if month == 12:
                period_end = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                period_end = datetime(year, month + 1, 1) - timedelta(days=1)
        elif template_name == 'annual_comparative':
            result = generator.generate_annual_comparative_report(year)
            period_start = datetime(year, 1, 1)
            period_end = datetime(year, 12, 31)
        else:
            return jsonify({'error': 'Template não suportado'}), 400
        
        # Salvar registro de geração
        from src.models.report import ReportGeneration
        generation = ReportGeneration(
            report_id=0,  # Geração rápida sem configuração
            generated_by=data.get('generated_by', 'user'),
            period_start=period_start,
            period_end=period_end,
            file_name=result['filename'],
            file_path=result['filepath'],
            file_size=result['size'],
            status='generated'
        )
        
        db.session.add(generation)
        db.session.commit()
        
        return jsonify({
            'message': 'Relatório gerado com sucesso',
            'generation': generation.to_dict(),
            'download_url': f'/api/reports/download/{generation.id}'
        })
        
    except Exception as e:
        try:
            db.session.rollback()
        except:
            pass
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/send-email', methods=['POST'])
def send_report_email():
    """Envia relatório por email"""
    try:
data = request.get_json()
        
        generation_id = data.get('generation_id')
        recipients = data.get('recipients', [])
        
        generation = db.session.query(ReportGeneration).get(generation_id)
        if not generation:
            return jsonify({'error': 'Relatório não encontrado'}), 404
        
        if not recipients:
            # Se não há destinatários específicos, enviar para todos os moradores
            users = db.session.query(User).filter(User.email.isnot(None)).all()
            recipients = [user.email for user in users if user.email]
        
        if not recipients:
            return jsonify({'error': 'Nenhum destinatário encontrado'}), 400
        
        generator = SimpleReportGenerator(db)
        email_result = generator.send_report_email(generation, recipients)
        
        # Atualizar registro de geração
        generation.email_sent = email_result['success']
        generation.email_sent_at = datetime.utcnow() if email_result['success'] else None
        generation.email_recipients_count = email_result['sent_count']
        generation.email_error = email_result.get('error')
        generation.status = 'sent' if email_result['success'] else 'failed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Email enviado com sucesso' if email_result['success'] else 'Erro ao enviar email',
            'sent_count': email_result['sent_count'],
            'total_recipients': email_result['total_recipients'],
            'error': email_result.get('error')
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/dashboard', methods=['GET'])
def get_reports_dashboard():
    """Dashboard com estatísticas de relatórios"""
    try:

        # Estatísticas gerais
        total_reports = db.session.query(Report).filter(Report.is_active == True).count()
        scheduled_reports = db.session.query(Report).filter(
            Report.is_active == True,
            Report.is_scheduled == True
        ).count()
        
        # Gerações recentes
        recent_generations = db.session.query(ReportGeneration)\
            .order_by(ReportGeneration.generated_at.desc())\
            .limit(10).all()
        
        # Estatísticas de email
        total_emails_sent = db.session.query(ReportGeneration)\
            .filter(ReportGeneration.email_sent == True).count()
        
        return jsonify({
            'total_reports': total_reports,
            'scheduled_reports': scheduled_reports,
            'total_emails_sent': total_emails_sent,
            'recent_generations': [gen.to_dict() for gen in recent_generations]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

