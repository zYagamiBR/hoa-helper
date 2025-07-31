import os
import json
from datetime import datetime, timedelta
from flask import current_app

class BasicReportGenerator:
    def __init__(self, db):
        self.db = db
        
    def generate_financial_monthly_report(self, year, month):
        """Gera relatório financeiro mensal em formato JSON"""
        try:
            from src.models.invoice import Invoice
            from src.models.payment import Payment
            from src.models.user import User
            from src.models.vendor import Vendor
            from src.models.bill import Bill
            
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
                bills = self.db.session.query(Bill).all()  # All active bills
            except:
                bills = []
            
            try:
                total_moradores = self.db.session.query(User).count()
            except:
                total_moradores = 0
                
            try:
                total_fornecedores = self.db.session.query(Vendor).count()
            except:
                total_fornecedores = 0
            
            # Calculate monthly bills cost
            monthly_bills_cost = 0
            bills_por_categoria = {}
            for bill in bills:
                categoria = getattr(bill, 'category', None) or 'Contas Recorrentes'
                monthly_cost = 0
                
                if bill.frequency == 'Monthly':
                    monthly_cost = float(bill.amount or 0)
                elif bill.frequency == 'Quarterly':
                    monthly_cost = float(bill.amount or 0) / 3
                elif bill.frequency == 'Yearly':
                    monthly_cost = float(bill.amount or 0) / 12
                elif bill.frequency == 'Biannual':
                    monthly_cost = float(bill.amount or 0) / 6
                
                monthly_bills_cost += monthly_cost
                if categoria not in bills_por_categoria:
                    bills_por_categoria[categoria] = 0
                bills_por_categoria[categoria] += monthly_cost
            
            # Calcular totais
            total_receitas = sum([float(p.amount or 0) for p in payments])
            total_invoices = sum([float(i.amount or 0) for i in invoices])
            total_despesas = total_invoices + monthly_bills_cost
            saldo = total_receitas - total_despesas
            
            # Despesas por categoria (invoices + bills)
            despesas_por_categoria = {}
            for invoice in invoices:
                categoria = getattr(invoice, 'category', None) or 'Outros'
                if categoria not in despesas_por_categoria:
                    despesas_por_categoria[categoria] = 0
                despesas_por_categoria[categoria] += float(invoice.amount or 0)
            
            # Add bills to categories
            for categoria, valor in bills_por_categoria.items():
                if categoria not in despesas_por_categoria:
                    despesas_por_categoria[categoria] = 0
                despesas_por_categoria[categoria] += valor
            
            # Se não há categorias, adicionar uma padrão
            if not despesas_por_categoria:
                despesas_por_categoria['Nenhuma despesa registrada'] = 0
            
            data = {
                'tipo': 'financial_monthly',
                'periodo': f"{self._get_month_name(month)} de {year}",
                'mes': month,
                'ano': year,
                'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'total_receitas': total_receitas,
                'total_despesas': total_despesas,
                'total_faturas': total_invoices,
                'total_contas_recorrentes': monthly_bills_cost,
                'saldo': saldo,
                'total_moradores': total_moradores,
                'total_fornecedores': total_fornecedores,
                'despesas_por_categoria': despesas_por_categoria,
                'num_pagamentos': len(payments),
                'num_faturas': len(invoices),
                'num_contas_recorrentes': len(bills)
            }
            
            return self._generate_json_report('financial_monthly', data)
            
        except Exception as e:
            print(f"Error generating financial monthly report: {str(e)}")
            # Gerar relatório com dados mínimos em caso de erro
            return self._generate_empty_report('financial_monthly', year, month)
    
    def generate_transparency_monthly_report(self, year, month):
        """Gera relatório de transparência mensal em formato JSON"""
        try:
            from src.models.invoice import Invoice
            from src.models.payment import Payment
            from src.models.maintenance import MaintenanceRequest
            from src.models.associate import Associate
            from src.models.bill import Bill
            
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
                bills = self.db.session.query(Bill).all()  # All active bills
            except:
                bills = []
            
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
            
            # Calculate monthly bills cost
            monthly_bills_cost = 0
            for bill in bills:
                if bill.frequency == 'Monthly':
                    monthly_bills_cost += float(bill.amount or 0)
                elif bill.frequency == 'Quarterly':
                    monthly_bills_cost += float(bill.amount or 0) / 3
                elif bill.frequency == 'Yearly':
                    monthly_bills_cost += float(bill.amount or 0) / 12
                elif bill.frequency == 'Biannual':
                    monthly_bills_cost += float(bill.amount or 0) / 6
            
            total_invoices_cost = sum([float(i.amount or 0) for i in invoices])
            total_expenses = total_invoices_cost + monthly_bills_cost
            
            data = {
                'tipo': 'transparency_monthly',
                'periodo': f"{self._get_month_name(month)} de {year}",
                'mes': month,
                'ano': year,
                'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'total_receitas': sum([float(p.amount or 0) for p in payments]),
                'total_despesas': total_expenses,
                'total_faturas': total_invoices_cost,
                'total_contas_recorrentes': monthly_bills_cost,
                'total_manutencoes': len(maintenance_requests),
                'total_funcionarios': len(associates),
                'folha_pagamento': sum([float(getattr(a, 'monthly_salary', 0) or 0) for a in associates])
            }
            
            return self._generate_json_report('transparency_monthly', data)
            
        except Exception as e:
            print(f"Error generating transparency monthly report: {str(e)}")
            return self._generate_empty_report('transparency_monthly', year, month)
    
    def generate_annual_comparative_report(self, year):
        """Gera relatório anual comparativo em formato JSON"""
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
                'tipo': 'annual_comparative',
                'ano': year,
                'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'dados_anos': years_data,
                'anos': sorted(years_data.keys())
            }
            
            return self._generate_json_report('annual_comparative', data)
            
        except Exception as e:
            print(f"Error generating annual comparative report: {str(e)}")
            return self._generate_empty_report('annual_comparative', year)
    
    def _generate_json_report(self, template_name, data):
        """Gera relatório em formato JSON"""
        try:
            # Criar diretório de relatórios
            reports_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/tmp'), 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            # Nome do arquivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{template_name}_{timestamp}.json'
            filepath = os.path.join(reports_dir, filename)
            
            # Salvar dados em JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return {
                'filename': filename,
                'filepath': filepath,
                'size': os.path.getsize(filepath),
                'format': 'json',
                'data': data
            }
            
        except Exception as e:
            print(f"Error generating JSON report: {str(e)}")
            raise e
    
    def _generate_empty_report(self, template_name, year, period=None):
        """Gera relatório vazio quando não há dados"""
        try:
            reports_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', '/tmp'), 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{template_name}_empty_{timestamp}.json'
            filepath = os.path.join(reports_dir, filename)
            
            data = {
                'tipo': template_name,
                'status': 'empty',
                'message': 'Relatório gerado com dados limitados',
                'periodo': f"{year}" + (f" - {period}" if period else ""),
                'data_geracao': datetime.now().strftime('%d/%m/%Y às %H:%M'),
                'total_receitas': 0,
                'total_despesas': 0,
                'saldo': 0,
                'observacao': 'Para relatórios mais detalhados, adicione dados ao sistema.'
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return {
                'filename': filename,
                'filepath': filepath,
                'size': os.path.getsize(filepath),
                'format': 'json',
                'data': data
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

