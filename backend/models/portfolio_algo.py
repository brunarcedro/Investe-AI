from typing import Dict, List

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
    
    def generate_portfolio(self, risk_profile: str, monthly_amount: float, user_context: Dict) -> Dict:
        """Gera recomendação básica de portfolio"""
        allocation = self.allocation_rules[risk_profile].copy()
        
        # Ajustes simples baseados no contexto
        if user_context.get('idade', 25) < 23:
            allocation['acoes'] += 0.05
            allocation['renda_fixa'] -= 0.05
        
        # Calcular valores específicos
        specific_assets = {}
        for category, percentage in allocation.items():
            category_value = monthly_amount * percentage
            specific_assets[category] = {
                'total_value': round(category_value, 2),
                'assets': [{'name': f'{category.title()} recomendado', 'value': round(category_value, 2)}]
            }
        
        expected_returns = {
            'conservador': "6-9% ao ano",
            'moderado': "8-12% ao ano", 
            'agressivo': "10-15% ao ano"
        }
        
        return {
            'alocacao': {k: round(v, 3) for k, v in allocation.items()},
            'ativos_especificos': specific_assets,
            'retorno_esperado': expected_returns[risk_profile]
        }