import os
import json
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from flask import current_app

class SimpleReportGenerator:
    def __init__(self, db):
        self.db = db
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom styles for the reports"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        
        self.section_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.darkblue
        )
        
    def generate_financial_monthly_report(self, year, month):
        """Gera relatório financeiro mensal com dados disponíveis"""
        try:
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
            
            # Buscar dados com tratamento de erro
            try:
                payments = self.db.session.query(Payment).filter(
                    Payment.payment_date >= start_date,
                    Payment.payment_date <= end_date
                ).all()
            except:
                payments = []
            
            try:
                invoices = self.db.session.query(Invoice).filter(
                    Invoice.issue_date >= start_date,
                    Invoice.issue_date <= end_date
                ).all()
            except:
                invoices = []
            
            try:
                total_moradores = self.db.session.query(User).count()
            except:
                total_moradores = 0
                
            try:
                total_fornecedores = self.db.session.query(Vendor).count()
            except:
                total_fornecedores = 0
            
            # Calcular totais
            total_receitas = sum([float(p.amount or 0) for p in payments])
            total_despesas = sum([float(i.amount or 0) for i in invoices])
            saldo = total_receitas - total_despesas
            
            # Despesas por categoria
            despesas_por_categoria = {}
            for invoice in invoices:
                categoria = getattr(invoice, 'category', None) or 'Outros'
                if categoria not in despesas_por_categoria:
                    despesas_por_categoria[categoria] = 0
                despesas_por_categoria[categoria] += float(invoice.amount or 0)
            
            # Se não há categorias, adicionar uma padrão
            if not despesas_por_categoria:
                despesas_por_categoria['Nenhuma despesa registrada'] = 0
            
            data = {
                'periodo': f"{self._get_month_name(month)} de {year}",
                'mes': month,
                'ano': year,
                'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'total_receitas': total_receitas,
                'total_despesas': total_despesas,
                'saldo': saldo,
                'total_moradores': total_moradores,
                'total_fornecedores': total_fornecedores,
                'despesas_por_categoria': despesas_por_categoria,
                'num_pagamentos': len(payments),
                'num_faturas': len(invoices)
            }
            
            return self._generate_pdf_report('financial_monthly', data)
            
        except Exception as e:
            print(f"Error generating financial monthly report: {str(e)}")
            # Gerar relatório com dados mínimos em caso de erro
            return self._generate_empty_report('financial_monthly', year, month)
    
    def generate_transparency_monthly_report(self, year, month):
        """Gera relatório de transparência mensal"""
        try:
            from src.models.invoice import Invoice
            from src.models.payment import Payment
            from src.models.maintenance import MaintenanceRequest
            from src.models.associate import Associate
            
            # Período do mês
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)
            
            # Buscar dados com tratamento de erro
            try:
                payments = self.db.session.query(Payment).filter(
                    Payment.payment_date >= start_date,
                    Payment.payment_date <= end_date
                ).all()
            except:
                payments = []
            
            try:
                invoices = self.db.session.query(Invoice).filter(
                    Invoice.issue_date >= start_date,
                    Invoice.issue_date <= end_date
                ).all()
            except:
                invoices = []
            
            try:
                maintenance_requests = self.db.session.query(MaintenanceRequest).filter(
                    MaintenanceRequest.created_at >= start_date,
                    MaintenanceRequest.created_at <= end_date
                ).all()
            except:
                maintenance_requests = []
            
            try:
                associates = self.db.session.query(Associate).filter(
                    Associate.status == 'Active'
                ).all()
            except:
                associates = []
            
            # Nome do mês em português
            month_names = {
                1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
                5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
            }
            
            data = {
                'periodo': f"{month_names[month]} de {year}",
                'mes': month,
                'ano': year,
                'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'total_receitas': sum([float(p.amount or 0) for p in payments]),
                'total_despesas': sum([float(i.amount or 0) for i in invoices]),
                'total_manutencoes': len(maintenance_requests),
                'total_funcionarios': len(associates),
                'folha_pagamento': sum([float(getattr(a, 'monthly_salary', 0) or 0) for a in associates])
            }
            
            return self._generate_pdf_report('transparency_monthly', data)
            
        except Exception as e:
            print(f"Error generating transparency monthly report: {str(e)}")
            return self._generate_empty_report('transparency_monthly', year, month)
    
    def generate_transparency_quarterly_report(self, year, quarter):
        """Gera relatório de transparência trimestral"""
        try:
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
            
            # Buscar dados com tratamento de erro
            try:
                payments = self.db.session.query(Payment).filter(
                    Payment.payment_date >= start_date,
                    Payment.payment_date <= end_date
                ).all()
            except:
                payments = []
            
            try:
                invoices = self.db.session.query(Invoice).filter(
                    Invoice.issue_date >= start_date,
                    Invoice.issue_date <= end_date
                ).all()
            except:
                invoices = []
            
            try:
                maintenance_requests = self.db.session.query(MaintenanceRequest).filter(
                    MaintenanceRequest.created_at >= start_date,
                    MaintenanceRequest.created_at <= end_date
                ).all()
            except:
                maintenance_requests = []
            
            try:
                associates = self.db.session.query(Associate).filter(
                    Associate.status == 'Active'
                ).all()
            except:
                associates = []
            
            data = {
                'periodo': f"{quarter}º Trimestre de {year}",
                'trimestre': quarter,
                'ano': year,
                'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'total_receitas': sum([float(p.amount or 0) for p in payments]),
                'total_despesas': sum([float(i.amount or 0) for i in invoices]),
                'total_manutencoes': len(maintenance_requests),
                'total_funcionarios': len(associates),
                'folha_pagamento': sum([float(getattr(a, 'monthly_salary', 0) or 0) for a in associates])
            }
            
            return self._generate_pdf_report('transparency_quarterly', data)
            
        except Exception as e:
            print(f"Error generating transparency quarterly report: {str(e)}")
            return self._generate_empty_report('transparency_quarterly', year, quarter)
    
    def generate_annual_comparative_report(self, year):
        """Gera relatório anual comparativo"""
        try:
            from src.models.invoice import Invoice
            from src.models.payment import Payment
            
            # Dados dos últimos 5 anos
            years_data = {}
            for y in range(year - 4, year + 1):
                start_date = datetime(y, 1, 1)
                end_date = datetime(y, 12, 31)
                
                try:
                    payments = self.db.session.query(Payment).filter(
                        Payment.payment_date >= start_date,
                        Payment.payment_date <= end_date
                    ).all()
                except:
                    payments = []
                
                try:
                    invoices = self.db.session.query(Invoice).filter(
                        Invoice.issue_date >= start_date,
                        Invoice.issue_date <= end_date
                    ).all()
                except:
                    invoices = []
                
                receitas = sum([float(p.amount or 0) for p in payments])
                despesas = sum([float(i.amount or 0) for i in invoices])
                
                years_data[y] = {
                    'receitas': receitas,
                    'despesas': despesas,
                    'saldo': receitas - despesas
                }
            
            data = {
                'ano': year,
                'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'dados_anos': years_data,
                'anos': sorted(years_data.keys())
            }
            
            return self._generate_pdf_report('annual_comparative', data)
            
        except Exception as e:
            print(f"Error generating annual comparative report: {str(e)}")
            return self._generate_empty_report('annual_comparative', year)
    
    def _generate_pdf_report(self, template_name, data):
        """Gera PDF usando ReportLab"""
        try:
            # Criar diretório de relatórios
            reports_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/tmp'), 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            # Nome do arquivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{template_name}_{timestamp}.pdf'
            filepath = os.path.join(reports_dir, filename)
            
            # Criar documento PDF
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            # Gerar conteúdo baseado no tipo de relatório
            if template_name == 'financial_monthly':
                story = self._build_financial_monthly_content(data)
            elif template_name == 'transparency_monthly':
                story = self._build_transparency_monthly_content(data)
            elif template_name == 'transparency_quarterly':
                story = self._build_transparency_quarterly_content(data)
            elif template_name == 'annual_comparative':
                story = self._build_annual_comparative_content(data)
            else:
                story = self._build_default_content(data)
            
            # Construir PDF
            doc.build(story)
            
            return {
                'filename': filename,
                'filepath': filepath,
                'size': os.path.getsize(filepath)
            }
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise e
    
    def _build_financial_monthly_content(self, data):
        """Constrói conteúdo do relatório financeiro mensal"""
        story = []
        
        # Título
        story.append(Paragraph("RELATÓRIO FINANCEIRO MENSAL", self.title_style))
        story.append(Paragraph("Condomínio Conjunto Residencial Maria Stella", self.subtitle_style))
        story.append(Paragraph(data['periodo'], self.subtitle_style))
        story.append(Paragraph(f"Gerado em {data['data_geracao']}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Resumo Financeiro
        story.append(Paragraph("RESUMO FINANCEIRO", self.section_style))
        
        resumo_data = [
            ['Item', 'Valor'],
            ['Total de Receitas', f"R$ {data['total_receitas']:.2f}"],
            ['Total de Despesas', f"R$ {data['total_despesas']:.2f}"],
            ['Saldo do Período', f"R$ {data['saldo']:.2f}"]
        ]
        
        resumo_table = Table(resumo_data, colWidths=[3*inch, 2*inch])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(resumo_table)
        story.append(Spacer(1, 20))
        
        # Despesas por Categoria
        story.append(Paragraph("DESPESAS POR CATEGORIA", self.section_style))
        
        categoria_data = [['Categoria', 'Valor', '% do Total']]
        for categoria, valor in data['despesas_por_categoria'].items():
            percentual = (valor / data['total_despesas'] * 100) if data['total_despesas'] > 0 else 0
            categoria_data.append([categoria, f"R$ {valor:.2f}", f"{percentual:.1f}%"])
        
        categoria_table = Table(categoria_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        categoria_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(categoria_table)
        story.append(Spacer(1, 20))
        
        # Informações Gerais
        story.append(Paragraph("INFORMAÇÕES GERAIS", self.section_style))
        
        info_data = [
            ['Total de Moradores', str(data['total_moradores'])],
            ['Total de Fornecedores', str(data['total_fornecedores'])],
            ['Número de Pagamentos', str(data['num_pagamentos'])],
            ['Número de Faturas', str(data['num_faturas'])],
            ['Custo por Unidade', f"R$ {(data['total_despesas'] / data['total_moradores']):.2f}" if data['total_moradores'] > 0 else "R$ 0,00"]
        ]
        
        info_table = Table(info_data, colWidths=[3*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # Rodapé
        story.append(Paragraph("Este relatório foi gerado automaticamente pelo Sistema de Gestão do Condomínio", 
                              self.styles['Normal']))
        story.append(Paragraph("Para dúvidas ou esclarecimentos, entre em contato com a administração", 
                              self.styles['Normal']))
        
        return story
    
    def _build_transparency_monthly_content(self, data):
        """Constrói conteúdo do relatório de transparência mensal"""
        story = []
        
        # Título
        story.append(Paragraph("RELATÓRIO DE TRANSPARÊNCIA", self.title_style))
        story.append(Paragraph("Condomínio Conjunto Residencial Maria Stella", self.subtitle_style))
        story.append(Paragraph(data['periodo'], self.subtitle_style))
        story.append(Paragraph(f"Gerado em {data['data_geracao']}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Resumo Financeiro
        story.append(Paragraph("RESUMO FINANCEIRO DO MÊS", self.section_style))
        
        resumo_data = [
            ['Item', 'Valor'],
            ['Total de Receitas', f"R$ {data['total_receitas']:.2f}"],
            ['Total de Despesas', f"R$ {data['total_despesas']:.2f}"],
            ['Saldo do Mês', f"R$ {(data['total_receitas'] - data['total_despesas']):.2f}"]
        ]
        
        resumo_table = Table(resumo_data, colWidths=[3*inch, 2*inch])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(resumo_table)
        story.append(Spacer(1, 20))
        
        # Informações Operacionais
        story.append(Paragraph("INFORMAÇÕES OPERACIONAIS", self.section_style))
        
        operacional_data = [
            ['Total de Manutenções', str(data['total_manutencoes'])],
            ['Total de Funcionários', str(data['total_funcionarios'])],
            ['Folha de Pagamento', f"R$ {data['folha_pagamento']:.2f}"]
        ]
        
        operacional_table = Table(operacional_data, colWidths=[3*inch, 2*inch])
        operacional_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(operacional_table)
        story.append(Spacer(1, 20))
        
        # Rodapé
        story.append(Spacer(1, 30))
        story.append(Paragraph("Este relatório foi gerado automaticamente pelo sistema de gestão condominial.", 
                              self.styles['Normal']))
        story.append(Paragraph("Para dúvidas ou esclarecimentos, entre em contato com a administração.", 
                              self.styles['Normal']))
        
        return story
    
    def _build_transparency_quarterly_content(self, data):
        """Constrói conteúdo do relatório de transparência trimestral"""
        story = []
        
        # Título
        story.append(Paragraph("RELATÓRIO DE TRANSPARÊNCIA", self.title_style))
        story.append(Paragraph("Condomínio Conjunto Residencial Maria Stella", self.subtitle_style))
        story.append(Paragraph(data['periodo'], self.subtitle_style))
        story.append(Paragraph(f"Gerado em {data['data_geracao']}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Resumo Financeiro
        story.append(Paragraph("RESUMO FINANCEIRO DO TRIMESTRE", self.section_style))
        
        resumo_data = [
            ['Item', 'Valor'],
            ['Total de Receitas', f"R$ {data['total_receitas']:.2f}"],
            ['Total de Despesas', f"R$ {data['total_despesas']:.2f}"],
            ['Saldo do Trimestre', f"R$ {(data['total_receitas'] - data['total_despesas']):.2f}"]
        ]
        
        resumo_table = Table(resumo_data, colWidths=[3*inch, 2*inch])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(resumo_table)
        story.append(Spacer(1, 20))
        
        # Informações Operacionais
        story.append(Paragraph("INFORMAÇÕES OPERACIONAIS", self.section_style))
        
        operacional_data = [
            ['Total de Manutenções', str(data['total_manutencoes'])],
            ['Total de Funcionários', str(data['total_funcionarios'])],
            ['Folha de Pagamento', f"R$ {data['folha_pagamento']:.2f}"]
        ]
        
        operacional_table = Table(operacional_data, colWidths=[3*inch, 2*inch])
        operacional_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(operacional_table)
        story.append(Spacer(1, 30))
        
        # Rodapé
        story.append(Paragraph("Este relatório de transparência foi gerado em conformidade com as normas condominiais", 
                              self.styles['Normal']))
        
        return story
    
    def _build_annual_comparative_content(self, data):
        """Constrói conteúdo do relatório anual comparativo"""
        story = []
        
        # Título
        story.append(Paragraph("RELATÓRIO ANUAL COMPARATIVO", self.title_style))
        story.append(Paragraph("Condomínio Conjunto Residencial Maria Stella", self.subtitle_style))
        story.append(Paragraph(f"Evolução Financeira - {data['ano']}", self.subtitle_style))
        story.append(Paragraph(f"Gerado em {data['data_geracao']}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Evolução dos últimos 5 anos
        story.append(Paragraph("EVOLUÇÃO DOS ÚLTIMOS 5 ANOS", self.section_style))
        
        evolucao_data = [['Ano', 'Receitas', 'Despesas', 'Saldo']]
        for ano in data['anos']:
            ano_data = data['dados_anos'][ano]
            evolucao_data.append([
                str(ano),
                f"R$ {ano_data['receitas']:.2f}",
                f"R$ {ano_data['despesas']:.2f}",
                f"R$ {ano_data['saldo']:.2f}"
            ])
        
        evolucao_table = Table(evolucao_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        evolucao_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(evolucao_table)
        story.append(Spacer(1, 30))
        
        # Rodapé
        story.append(Paragraph("Este relatório apresenta a evolução financeira do condomínio nos últimos 5 anos", 
                              self.styles['Normal']))
        
        return story
    
    def _build_default_content(self, data):
        """Constrói conteúdo padrão para relatórios"""
        story = []
        story.append(Paragraph("RELATÓRIO DO CONDOMÍNIO", self.title_style))
        story.append(Paragraph("Dados não disponíveis no momento", self.styles['Normal']))
        return story
    
    def _generate_empty_report(self, template_name, year, period=None):
        """Gera relatório vazio quando não há dados"""
        try:
            reports_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/tmp'), 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{template_name}_empty_{timestamp}.pdf'
            filepath = os.path.join(reports_dir, filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            story.append(Paragraph("RELATÓRIO DO CONDOMÍNIO", self.title_style))
            story.append(Paragraph("Condomínio Conjunto Residencial Maria Stella", self.subtitle_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph("Este relatório foi gerado com dados limitados.", self.styles['Normal']))
            story.append(Paragraph("Para relatórios mais detalhados, adicione dados ao sistema.", self.styles['Normal']))
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Período: {year}" + (f" - {period}" if period else ""), self.styles['Normal']))
            story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", self.styles['Normal']))
            
            doc.build(story)
            
            return {
                'filename': filename,
                'filepath': filepath,
                'size': os.path.getsize(filepath)
            }
            
        except Exception as e:
            print(f"Error generating empty report: {str(e)}")
            raise e
    
    def _get_month_name(self, month):
        """Retorna nome do mês em português"""
        months = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return months.get(month, f'Mês {month}')
    
    def send_report_email(self, generation, recipients):
        """Simula envio de email (implementação básica)"""
        try:
            # Por enquanto, apenas simula o envio
            return {
                'success': True,
                'sent_count': len(recipients),
                'total_recipients': len(recipients)
            }
        except Exception as e:
            return {
                'success': False,
                'sent_count': 0,
                'total_recipients': len(recipients),
                'error': str(e)
            }

