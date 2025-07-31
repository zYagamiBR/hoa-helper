from flask import Blueprint, request, jsonify, send_file, current_app
from src.models.user import db
from src.services.basic_report_generator import BasicReportGenerator
import os
from datetime import datetime

report_bp = Blueprint('report', __name__)

@report_bp.route('/api/reports/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Retorna estatísticas do dashboard de relatórios"""
    try:
        # Estatísticas básicas (simuladas para funcionar com dados vazios)
        stats = {
            'total_reports': 0,
            'emails_sent': 0,
            'scheduled_reports': 2,  # Simulado
            'next_scheduled': '06/08/2025'
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/quick-generate', methods=['POST'])
def quick_generate_report():
    """Geração rápida de relatório sem configuração prévia"""
    try:
        data = request.get_json() or {}
        
        # Parâmetros padrão
        report_type = data.get('report_type', 'financial_monthly')
        year = data.get('year', datetime.now().year)
        month = data.get('month', datetime.now().month)
        quarter = data.get('quarter', ((datetime.now().month - 1) // 3) + 1)
        
        generator = BasicReportGenerator(db)
        
        # Gerar relatório baseado no tipo
        if report_type == 'financial_monthly':
            result = generator.generate_financial_monthly_report(year, month)
        elif report_type == 'transparency_monthly':
            result = generator.generate_transparency_monthly_report(year, month)
        elif report_type == 'annual_comparative':
            result = generator.generate_annual_comparative_report(year)
        else:
            return jsonify({'error': 'Tipo de relatório não suportado'}), 400
        
        return jsonify({
            'success': True,
            'message': 'Relatório gerado com sucesso',
            'filename': result['filename'],
            'size': result['size'],
            'download_url': f'/api/reports/download/{result["filename"]}'
        })
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro ao gerar relatório: {str(e)}'
        }), 500

@report_bp.route('/api/reports/download/<filename>', methods=['GET'])
def download_report(filename):
    """Download de relatório gerado"""
    try:
        reports_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/tmp'), 'reports')
        filepath = os.path.join(reports_dir, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/api/reports/send-email', methods=['POST'])
def send_report_email():
    """Simula envio de relatório por email"""
    try:
        data = request.get_json() or {}
        
        # Simular envio de email
        return jsonify({
            'success': True,
            'message': 'Email enviado com sucesso (simulado)',
            'sent_count': 1,
            'total_recipients': 1
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@report_bp.route('/api/reports/templates', methods=['GET'])
def get_report_templates():
    """Lista templates de relatórios disponíveis"""
    try:
        templates = [
            {
                'id': 'financial_monthly',
                'name': 'Relatório Financeiro Mensal',
                'description': 'Receitas vs Despesas com análise detalhada por categoria',
                'frequency': 'Mensal'
            },
            {
                'id': 'transparency_quarterly',
                'name': 'Prestação de Contas Trimestral',
                'description': 'Relatório de transparência com despesas por grupo',
                'frequency': 'Trimestral'
            },
            {
                'id': 'annual_comparative',
                'name': 'Relatório Comparativo Anual',
                'description': 'Evolução financeira dos últimos 5 anos',
                'frequency': 'Anual'
            }
        ]
        
        return jsonify(templates)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

