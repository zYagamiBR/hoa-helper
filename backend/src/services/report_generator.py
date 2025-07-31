import os
import json
from datetime import datetime, timedelta
from jinja2 import Template
import pdfkit
from flask import current_app
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from sqlalchemy import func, extract
from decimal import Decimal

class ReportGenerator:
    def __init__(self, db):
        self.db = db
        
    def generate_financial_monthly_report(self, year, month):
        """Gera relatório financeiro mensal"""
        from src.models.invoice import Invoice
        from src.models.payment import Payment
        from src.models.user import User
        from src.models.vendor import Vendor
        
        # Período do relatório
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # Dados de receitas
        payments = self.db.session.query(Payment).filter(
            Payment.payment_date >= start_date,
            Payment.payment_date <= end_date
        ).all()
        
        total_receitas = sum([p.amount for p in payments])
        
        # Dados de despesas
        invoices = self.db.session.query(Invoice).filter(
            Invoice.issue_date >= start_date,
            Invoice.issue_date <= end_date
        ).all()
        
        total_despesas = sum([i.amount for i in invoices])
        
        # Despesas por categoria
        despesas_por_categoria = {}
        for invoice in invoices:
            categoria = invoice.category or 'Outros'
            if categoria not in despesas_por_categoria:
                despesas_por_categoria[categoria] = 0
            despesas_por_categoria[categoria] += float(invoice.amount)
        
        # Dados de moradores
        total_moradores = self.db.session.query(User).count()
        
        # Dados de fornecedores
        total_fornecedores = self.db.session.query(Vendor).count()
        
        # Saldo
        saldo = total_receitas - total_despesas
        
        data = {
            'periodo': f"{self._get_month_name(month)} de {year}",
            'mes': month,
            'ano': year,
            'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
            'total_receitas': float(total_receitas),
            'total_despesas': float(total_despesas),
            'saldo': float(saldo),
            'total_moradores': total_moradores,
            'total_fornecedores': total_fornecedores,
            'despesas_por_categoria': despesas_por_categoria,
            'receitas_detalhadas': [p.to_dict() for p in payments],
            'despesas_detalhadas': [i.to_dict() for i in invoices]
        }
        
        return self._generate_pdf_report('financial_monthly', data)
    
    def generate_transparency_quarterly_report(self, year, quarter):
        """Gera relatório de transparência trimestral"""
        from src.models.invoice import Invoice
        from src.models.payment import Payment
        from src.models.maintenance import MaintenanceRequest
        from src.models.associate import Associate
        
        # Período do trimestre
        start_month = (quarter - 1) * 3 + 1
        start_date = datetime(year, start_month, 1)
        
        if quarter == 4:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_month = quarter * 3
            end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
        
        # Dados financeiros
        payments = self.db.session.query(Payment).filter(
            Payment.payment_date >= start_date,
            Payment.payment_date <= end_date
        ).all()
        
        invoices = self.db.session.query(Invoice).filter(
            Invoice.issue_date >= start_date,
            Invoice.issue_date <= end_date
        ).all()
        
        # Manutenções
        maintenance_requests = self.db.session.query(MaintenanceRequest).filter(
            MaintenanceRequest.created_at >= start_date,
            MaintenanceRequest.created_at <= end_date
        ).all()
        
        # Funcionários
        associates = self.db.session.query(Associate).filter(
            Associate.status == 'Active'
        ).all()
        
        # Análise de despesas por grupo
        grupos_despesas = {
            'Pessoal': ['Salários', 'INSS', 'FGTS', 'Vale Transporte', 'Ticket Refeição', 'Cesta Básica'],
            'Utilidades': ['Energia Elétrica', 'Água e Esgoto', 'Internet', 'Telefonia', 'Gás'],
            'Manutenção': ['Limpeza', 'Jardinagem', 'Manutenção Predial', 'Reparos'],
            'Segurança': ['Portaria', 'Vigilância', 'Monitoramento'],
            'Área de Lazer': ['Piscina', 'Eventos', 'Material Esportivo', 'Socorrista'],
            'Administrativo': ['Material de Escritório', 'Contabilidade', 'Jurídico', 'Taxas']
        }
        
        despesas_por_grupo = {}
        for grupo, categorias in grupos_despesas.items():
            total_grupo = 0
            for invoice in invoices:
                if invoice.category in categorias:
                    total_grupo += float(invoice.amount)
            despesas_por_grupo[grupo] = total_grupo
        
        data = {
            'periodo': f"{quarter}º Trimestre de {year}",
            'trimestre': quarter,
            'ano': year,
            'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
            'total_receitas': sum([float(p.amount) for p in payments]),
            'total_despesas': sum([float(i.amount) for i in invoices]),
            'despesas_por_grupo': despesas_por_grupo,
            'total_manutencoes': len(maintenance_requests),
            'manutencoes_concluidas': len([m for m in maintenance_requests if m.status == 'Completed']),
            'total_funcionarios': len(associates),
            'folha_pagamento': sum([float(a.monthly_salary or 0) for a in associates])
        }
        
        return self._generate_pdf_report('transparency_quarterly', data)
    
    def generate_annual_comparative_report(self, year):
        """Gera relatório anual comparativo"""
        from src.models.invoice import Invoice
        from src.models.payment import Payment
        
        # Dados dos últimos 5 anos
        years_data = {}
        for y in range(year - 4, year + 1):
            start_date = datetime(y, 1, 1)
            end_date = datetime(y, 12, 31)
            
            payments = self.db.session.query(Payment).filter(
                Payment.payment_date >= start_date,
                Payment.payment_date <= end_date
            ).all()
            
            invoices = self.db.session.query(Invoice).filter(
                Invoice.issue_date >= start_date,
                Invoice.issue_date <= end_date
            ).all()
            
            years_data[y] = {
                'receitas': sum([float(p.amount) for p in payments]),
                'despesas': sum([float(i.amount) for i in invoices]),
                'saldo': sum([float(p.amount) for p in payments]) - sum([float(i.amount) for i in invoices])
            }
        
        data = {
            'ano': year,
            'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
            'dados_anos': years_data,
            'evolucao_receitas': [years_data[y]['receitas'] for y in sorted(years_data.keys())],
            'evolucao_despesas': [years_data[y]['despesas'] for y in sorted(years_data.keys())],
            'anos': sorted(years_data.keys())
        }
        
        return self._generate_pdf_report('annual_comparative', data)
    
    def _generate_pdf_report(self, template_name, data):
        """Gera PDF a partir do template"""
        template_path = os.path.join(current_app.root_path, 'templates', 'reports', f'{template_name}.html')
        
        if not os.path.exists(template_path):
            # Criar template padrão se não existir
            self._create_default_template(template_name, template_path)
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        html_content = template.render(**data)
        
        # Configurações do PDF
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        # Gerar PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{template_name}_{timestamp}.pdf'
        filepath = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/tmp'), 'reports', filename)
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        pdfkit.from_string(html_content, filepath, options=options)
        
        return {
            'filename': filename,
            'filepath': filepath,
            'size': os.path.getsize(filepath)
        }
    
    def _create_default_template(self, template_name, template_path):
        """Cria template padrão baseado no tipo de relatório"""
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        
        if template_name == 'financial_monthly':
            template_content = self._get_financial_monthly_template()
        elif template_name == 'transparency_quarterly':
            template_content = self._get_transparency_quarterly_template()
        elif template_name == 'annual_comparative':
            template_content = self._get_annual_comparative_template()
        else:
            template_content = self._get_default_template()
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
    
    def _get_financial_monthly_template(self):
        return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatório Financeiro Mensal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
        .title { font-size: 24px; font-weight: bold; color: #333; }
        .subtitle { font-size: 16px; color: #666; margin-top: 10px; }
        .section { margin-bottom: 30px; }
        .section-title { font-size: 18px; font-weight: bold; color: #333; border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 15px; }
        .summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px; }
        .summary-card { background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; }
        .summary-value { font-size: 24px; font-weight: bold; color: #007bff; }
        .summary-label { font-size: 14px; color: #666; margin-top: 5px; }
        .table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .table th { background-color: #f8f9fa; font-weight: bold; }
        .positive { color: #28a745; }
        .negative { color: #dc3545; }
        .footer { margin-top: 50px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">RELATÓRIO FINANCEIRO MENSAL</div>
        <div class="subtitle">Condomínio Conjunto Residencial Maria Stella</div>
        <div class="subtitle">{{ periodo }}</div>
        <div style="font-size: 12px; margin-top: 10px;">Gerado em {{ data_geracao }}</div>
    </div>
    
    <div class="section">
        <div class="section-title">Resumo Financeiro</div>
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-value positive">R$ {{ "%.2f"|format(total_receitas) }}</div>
                <div class="summary-label">Total de Receitas</div>
            </div>
            <div class="summary-card">
                <div class="summary-value negative">R$ {{ "%.2f"|format(total_despesas) }}</div>
                <div class="summary-label">Total de Despesas</div>
            </div>
            <div class="summary-card">
                <div class="summary-value {% if saldo >= 0 %}positive{% else %}negative{% endif %}">R$ {{ "%.2f"|format(saldo) }}</div>
                <div class="summary-label">Saldo do Período</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">Despesas por Categoria</div>
        <table class="table">
            <thead>
                <tr>
                    <th>Categoria</th>
                    <th>Valor</th>
                    <th>% do Total</th>
                </tr>
            </thead>
            <tbody>
                {% for categoria, valor in despesas_por_categoria.items() %}
                <tr>
                    <td>{{ categoria }}</td>
                    <td>R$ {{ "%.2f"|format(valor) }}</td>
                    <td>{{ "%.1f"|format((valor / total_despesas * 100) if total_despesas > 0 else 0) }}%</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <div class="section-title">Informações Gerais</div>
        <p><strong>Total de Moradores:</strong> {{ total_moradores }}</p>
        <p><strong>Total de Fornecedores:</strong> {{ total_fornecedores }}</p>
        <p><strong>Custo por Unidade:</strong> R$ {{ "%.2f"|format(total_despesas / total_moradores if total_moradores > 0 else 0) }}</p>
    </div>
    
    <div class="footer">
        <p>Este relatório foi gerado automaticamente pelo Sistema de Gestão do Condomínio</p>
        <p>Para dúvidas ou esclarecimentos, entre em contato com a administração</p>
    </div>
</body>
</html>
        '''
    
    def _get_transparency_quarterly_template(self):
        return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatório de Transparência Trimestral</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
        .title { font-size: 24px; font-weight: bold; color: #333; }
        .subtitle { font-size: 16px; color: #666; margin-top: 10px; }
        .section { margin-bottom: 30px; }
        .section-title { font-size: 18px; font-weight: bold; color: #333; border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 15px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: #f8f9fa; padding: 15px; border-radius: 5px; }
        .table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .table th { background-color: #f8f9fa; font-weight: bold; }
        .footer { margin-top: 50px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">RELATÓRIO DE TRANSPARÊNCIA</div>
        <div class="subtitle">Condomínio Conjunto Residencial Maria Stella</div>
        <div class="subtitle">{{ periodo }}</div>
        <div style="font-size: 12px; margin-top: 10px;">Gerado em {{ data_geracao }}</div>
    </div>
    
    <div class="section">
        <div class="section-title">Resumo Financeiro do Trimestre</div>
        <div class="grid-2">
            <div class="card">
                <h4>Receitas</h4>
                <p style="font-size: 20px; color: #28a745; font-weight: bold;">R$ {{ "%.2f"|format(total_receitas) }}</p>
            </div>
            <div class="card">
                <h4>Despesas</h4>
                <p style="font-size: 20px; color: #dc3545; font-weight: bold;">R$ {{ "%.2f"|format(total_despesas) }}</p>
            </div>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">Despesas por Grupo</div>
        <table class="table">
            <thead>
                <tr>
                    <th>Grupo de Despesa</th>
                    <th>Valor</th>
                    <th>% do Total</th>
                </tr>
            </thead>
            <tbody>
                {% for grupo, valor in despesas_por_grupo.items() %}
                <tr>
                    <td>{{ grupo }}</td>
                    <td>R$ {{ "%.2f"|format(valor) }}</td>
                    <td>{{ "%.1f"|format((valor / total_despesas * 100) if total_despesas > 0 else 0) }}%</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <div class="section-title">Manutenções e Serviços</div>
        <div class="grid-2">
            <div class="card">
                <h4>Total de Solicitações</h4>
                <p style="font-size: 20px; font-weight: bold;">{{ total_manutencoes }}</p>
            </div>
            <div class="card">
                <h4>Solicitações Concluídas</h4>
                <p style="font-size: 20px; font-weight: bold;">{{ manutencoes_concluidas }}</p>
            </div>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">Recursos Humanos</div>
        <div class="grid-2">
            <div class="card">
                <h4>Total de Funcionários</h4>
                <p style="font-size: 20px; font-weight: bold;">{{ total_funcionarios }}</p>
            </div>
            <div class="card">
                <h4>Folha de Pagamento Mensal</h4>
                <p style="font-size: 20px; font-weight: bold;">R$ {{ "%.2f"|format(folha_pagamento) }}</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Este relatório foi gerado automaticamente pelo Sistema de Gestão do Condomínio</p>
        <p>Para dúvidas ou esclarecimentos, entre em contato com a administração</p>
    </div>
</body>
</html>
        '''
    
    def _get_annual_comparative_template(self):
        return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatório Anual Comparativo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
        .title { font-size: 24px; font-weight: bold; color: #333; }
        .subtitle { font-size: 16px; color: #666; margin-top: 10px; }
        .section { margin-bottom: 30px; }
        .section-title { font-size: 18px; font-weight: bold; color: #333; border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 15px; }
        .table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        .table th { background-color: #f8f9fa; font-weight: bold; }
        .footer { margin-top: 50px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">RELATÓRIO ANUAL COMPARATIVO</div>
        <div class="subtitle">Condomínio Conjunto Residencial Maria Stella</div>
        <div class="subtitle">Evolução Financeira - Últimos 5 Anos</div>
        <div style="font-size: 12px; margin-top: 10px;">Gerado em {{ data_geracao }}</div>
    </div>
    
    <div class="section">
        <div class="section-title">Evolução Financeira por Ano</div>
        <table class="table">
            <thead>
                <tr>
                    <th>Ano</th>
                    <th>Receitas</th>
                    <th>Despesas</th>
                    <th>Saldo</th>
                    <th>Variação Receitas</th>
                    <th>Variação Despesas</th>
                </tr>
            </thead>
            <tbody>
                {% for ano in anos %}
                <tr>
                    <td><strong>{{ ano }}</strong></td>
                    <td>R$ {{ "%.2f"|format(dados_anos[ano]['receitas']) }}</td>
                    <td>R$ {{ "%.2f"|format(dados_anos[ano]['despesas']) }}</td>
                    <td style="color: {% if dados_anos[ano]['saldo'] >= 0 %}#28a745{% else %}#dc3545{% endif %};">
                        R$ {{ "%.2f"|format(dados_anos[ano]['saldo']) }}
                    </td>
                    <td>
                        {% if loop.index > 1 %}
                            {% set prev_year = anos[loop.index0 - 1] %}
                            {% set variacao = ((dados_anos[ano]['receitas'] - dados_anos[prev_year]['receitas']) / dados_anos[prev_year]['receitas'] * 100) if dados_anos[prev_year]['receitas'] > 0 else 0 %}
                            <span style="color: {% if variacao >= 0 %}#28a745{% else %}#dc3545{% endif %};">
                                {{ "%.1f"|format(variacao) }}%
                            </span>
                        {% else %}
                            -
                        {% endif %}
                    </td>
                    <td>
                        {% if loop.index > 1 %}
                            {% set prev_year = anos[loop.index0 - 1] %}
                            {% set variacao = ((dados_anos[ano]['despesas'] - dados_anos[prev_year]['despesas']) / dados_anos[prev_year]['despesas'] * 100) if dados_anos[prev_year]['despesas'] > 0 else 0 %}
                            <span style="color: {% if variacao <= 0 %}#28a745{% else %}#dc3545{% endif %};">
                                {{ "%.1f"|format(variacao) }}%
                            </span>
                        {% else %}
                            -
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    
    <div class="footer">
        <p>Este relatório foi gerado automaticamente pelo Sistema de Gestão do Condomínio</p>
        <p>Para dúvidas ou esclarecimentos, entre em contato com a administração</p>
    </div>
</body>
</html>
        '''
    
    def _get_default_template(self):
        return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatório</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório Personalizado</h1>
        <p>Condomínio Conjunto Residencial Maria Stella</p>
    </div>
    <p>Template padrão - Configure o template específico para este tipo de relatório.</p>
</body>
</html>
        '''
    
    def _get_month_name(self, month):
        months = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return months.get(month, 'Mês Inválido')
    
    def send_report_email(self, report_generation, recipients):
        """Envia relatório por email"""
        try:
            # Configurações de email (devem ser configuradas no ambiente)
            smtp_server = current_app.config.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = current_app.config.get('SMTP_PORT', 587)
            smtp_username = current_app.config.get('SMTP_USERNAME')
            smtp_password = current_app.config.get('SMTP_PASSWORD')
            
            if not smtp_username or not smtp_password:
                raise Exception("Configurações de email não encontradas")
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['Subject'] = f"Relatório Condomínio Maria Stella - {datetime.now().strftime('%B %Y')}"
            
            # Corpo do email
            body = f"""
            Prezado(a) Morador(a),
            
            Segue em anexo o relatório de transparência do Condomínio Conjunto Residencial Maria Stella.
            
            Este relatório foi gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}.
            
            Para dúvidas ou esclarecimentos, entre em contato com a administração.
            
            Atenciosamente,
            Administração do Condomínio
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Anexar arquivo
            if os.path.exists(report_generation.file_path):
                with open(report_generation.file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {report_generation.file_name}'
                )
                msg.attach(part)
            
            # Enviar email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            
            sent_count = 0
            for recipient in recipients:
                try:
                    msg['To'] = recipient
                    server.send_message(msg)
                    sent_count += 1
                    del msg['To']
                except Exception as e:
                    print(f"Erro ao enviar para {recipient}: {str(e)}")
            
            server.quit()
            
            return {
                'success': True,
                'sent_count': sent_count,
                'total_recipients': len(recipients)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'sent_count': 0,
                'total_recipients': len(recipients)
            }

