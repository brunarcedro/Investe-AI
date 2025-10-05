from typing import Dict, List
import yfinance as yf

class PortfolioAllocator:
    def __init__(self):
        self.allocation_rules = {
            'conservador': {
                'renda_fixa': 0.70,
                'acoes': 0.20,
                'fundos_imobiliarios': 0.05,
                'reserva': 0.05
            },
            'moderado': {
                'renda_fixa': 0.40,
                'acoes': 0.45,
                'fundos_imobiliarios': 0.10,
                'reserva': 0.05
            },
            'agressivo': {
                'renda_fixa': 0.15,
                'acoes': 0.65,
                'fundos_imobiliarios': 0.15,
                'reserva': 0.05
            }
        }
        
        self.asset_recommendations = {
            'renda_fixa': [
                {'code': 'TESOURO_SELIC', 'name': 'Tesouro Selic', 'percentage': 0.6},
                {'code': 'CDB_BANCO', 'name': 'CDB Banco', 'percentage': 0.4}
            ],
            'acoes': [
                {'code': 'BOVA11.SA', 'name': 'ETF Bovespa', 'percentage': 0.6},
                {'code': 'IVVB11.SA', 'name': 'ETF S&P500', 'percentage': 0.4}
            ],
            'fundos_imobiliarios': [
                {'code': 'HGLG11.SA', 'name': 'FII Diversificado', 'percentage': 1.0}
            ]
        }
    
    def adjust_allocation_for_user(self, base_allocation: Dict, user_context: Dict) -> Dict:
        """Ajusta alocação baseada no contexto do usuário"""
        allocation = base_allocation.copy()
        
        # Ajuste por idade
        if user_context['idade'] < 23:
            allocation['acoes'] += 0.05
            allocation['renda_fixa'] -= 0.05
        
        # Ajuste por experiência
        if user_context['experiencia'] == 0:
            allocation['acoes'] -= 0.10
            allocation['renda_fixa'] += 0.10
        
        # Ajuste por reserva de emergência
        if user_context['reserva_emergencia'] == 0:
            allocation['reserva'] += 0.10
            allocation['acoes'] -= 0.05
            allocation['fundos_imobiliarios'] -= 0.05
        
        # Normalizar para somar 100%
        total = sum(allocation.values())
        for key in allocation:
            allocation[key] = allocation[key] / total
        
        return allocation
    
    def get_current_prices(self, assets: List[str]) -> Dict:
        """Busca preços atuais dos ativos"""
        prices = {}
        for asset in assets:
            try:
                ticker = yf.Ticker(asset)
                hist = ticker.history(period="1d")
                if not hist.empty:
                    prices[asset] = hist['Close'].iloc[-1]
                else:
                    prices[asset] = None
            except:
                prices[asset] = None
        return prices
    
    def generate_portfolio(self, risk_profile: str, monthly_amount: float, user_context: Dict) -> Dict:
        """Gera recomendação completa de portfolio"""
        
        # Obter alocação base
        base_allocation = self.allocation_rules[risk_profile]
        
        # Ajustar para contexto do usuário
        final_allocation = self.adjust_allocation_for_user(base_allocation, user_context)
        
        # Calcular valores específicos
        specific_assets = {}
        
        for category, percentage in final_allocation.items():
            if category in self.asset_recommendations:
                category_value = monthly_amount * percentage
                specific_assets[category] = {
                    'total_value': category_value,
                    'assets': []
                }
                
                for asset in self.asset_recommendations[category]:
                    asset_value = category_value * asset['percentage']
                    specific_assets[category]['assets'].append({
                        'code': asset['code'],
                        'name': asset['name'],
                        'value': round(asset_value, 2),
                        'percentage': asset['percentage']
                    })
        
        # Calcular retorno esperado
        expected_return = self.calculate_expected_return(risk_profile)
        
        return {
            'alocacao': {k: round(v, 3) for k, v in final_allocation.items()},
            'ativos_especificos': specific_assets,
            'retorno_esperado': expected_return
        }
    
    def calculate_expected_return(self, risk_profile: str) -> str:
        """Calcula retorno esperado baseado no perfil"""
        returns = {
            'conservador': "6-9% ao ano",
            'moderado': "8-12% ao ano", 
            'agressivo': "10-15% ao ano"
        }
        return returns[risk_profile]