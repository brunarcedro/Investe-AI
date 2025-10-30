"""
Simulação de Monte Carlo - Projeção Futura
Gera múltiplos cenários possíveis baseados em dados históricos
"""

import numpy as np
import pandas as pd
from typing import Dict, List
from .backtesting import Backtesting, TICKERS_BRASIL


class MonteCarloSimulation:
    """Simulação de Monte Carlo para projeção de carteiras"""

    def __init__(self):
        self.backtesting = Backtesting()

    @staticmethod
    def _safe_float(value, default=0.0):
        """Converte valor para float, substituindo NaN/inf por valor padrão"""
        if pd.isna(value) or np.isinf(value):
            return default
        return float(value)

    def calcular_parametros_historicos(
        self,
        alocacao: Dict[str, float],
        periodo_historico: str = '5y'
    ) -> Dict:
        """
        Calcula retorno médio e volatilidade baseado em dados históricos

        Returns:
            Dict com 'retorno_medio_mensal' e 'volatilidade_mensal'
        """
        # Baixar dados históricos de cada ativo
        retornos_ativos = []
        pesos = []

        for classe, peso in alocacao.items():
            if peso > 0.001:
                ticker = TICKERS_BRASIL.get(classe, '^IRX')
                dados = self.backtesting.obter_dados_historicos(ticker, periodo_historico)

                if not dados.empty:
                    retorno = dados['Close'].pct_change().dropna()
                    retornos_ativos.append(retorno)
                    pesos.append(peso)

        if not retornos_ativos:
            # Valores padrão se não conseguir dados
            return {
                'retorno_medio_mensal': 0.01,  # 1% ao mês
                'volatilidade_mensal': 0.03     # 3% de desvio padrão
            }

        # Combinar retornos
        df_retornos = pd.concat(retornos_ativos, axis=1)

        # Calcular retorno ponderado da carteira
        retorno_carteira = (df_retornos * pesos).sum(axis=1) / sum(pesos)

        return {
            'retorno_medio_mensal': self._safe_float(retorno_carteira.mean(), 0.01),
            'volatilidade_mensal': self._safe_float(retorno_carteira.std(), 0.03)
        }

    def simular_cenarios(
        self,
        alocacao: Dict[str, float],
        valor_inicial: float = 10000,
        aporte_mensal: float = 0,
        anos: int = 10,
        num_simulacoes: int = 1000
    ) -> Dict:
        """
        Executa simulação de Monte Carlo

        Args:
            alocacao: Alocação da carteira
            valor_inicial: Valor inicial
            aporte_mensal: Aporte mensal
            anos: Horizonte em anos
            num_simulacoes: Número de cenários a simular

        Returns:
            Dict com resultados das simulações
        """
        # Obter parâmetros históricos
        params = self.calcular_parametros_historicos(alocacao)
        retorno_medio = params['retorno_medio_mensal']
        volatilidade = params['volatilidade_mensal']

        meses = anos * 12
        resultados = []

        # Executar simulações
        for _ in range(num_simulacoes):
            patrimonio = valor_inicial

            # Simular mês a mês
            for mes in range(meses):
                # Gerar retorno aleatório (distribuição normal)
                retorno = np.random.normal(retorno_medio, volatilidade)

                # Aplicar retorno
                patrimonio = patrimonio * (1 + retorno)

                # Adicionar aporte
                patrimonio += aporte_mensal

            resultados.append(patrimonio)

        # Calcular estatísticas
        resultados = np.array(resultados)

        return {
            'num_simulacoes': num_simulacoes,
            'anos': anos,
            'valor_inicial': valor_inicial,
            'aporte_mensal': aporte_mensal,
            'patrimonio_medio': self._safe_float(np.mean(resultados)),
            'patrimonio_mediano': self._safe_float(np.median(resultados)),
            'patrimonio_minimo': self._safe_float(np.min(resultados)),
            'patrimonio_maximo': self._safe_float(np.max(resultados)),
            'percentil_10': self._safe_float(np.percentile(resultados, 10)),
            'percentil_25': self._safe_float(np.percentile(resultados, 25)),
            'percentil_75': self._safe_float(np.percentile(resultados, 75)),
            'percentil_90': self._safe_float(np.percentile(resultados, 90)),
            'desvio_padrao': self._safe_float(np.std(resultados)),
            'probabilidade_dobrar': self._safe_float(np.sum(resultados >= valor_inicial * 2) / num_simulacoes * 100),
            'probabilidade_perda': self._safe_float(np.sum(resultados < valor_inicial + (aporte_mensal * meses)) / num_simulacoes * 100),
        }

    def gerar_cenarios_detalhados(
        self,
        alocacao: Dict[str, float],
        valor_inicial: float = 10000,
        aporte_mensal: float = 0,
        anos: int = 10
    ) -> Dict:
        """
        Gera 3 cenários detalhados: Otimista, Realista, Pessimista

        Returns:
            Dict com evolução mensal de cada cenário
        """
        params = self.calcular_parametros_historicos(alocacao)
        retorno_medio = params['retorno_medio_mensal']
        volatilidade = params['volatilidade_mensal']

        meses = anos * 12

        # Definir parâmetros dos cenários
        cenarios = {
            'otimista': {
                'retorno': retorno_medio + volatilidade,  # +1 desvio padrão
                'patrimonio': [valor_inicial]
            },
            'realista': {
                'retorno': retorno_medio,
                'patrimonio': [valor_inicial]
            },
            'pessimista': {
                'retorno': retorno_medio - volatilidade,  # -1 desvio padrão
                'patrimonio': [valor_inicial]
            }
        }

        # Simular cada cenário
        for cenario, config in cenarios.items():
            patrimonio_atual = valor_inicial

            for mes in range(meses):
                # Aplicar retorno do cenário
                patrimonio_atual = patrimonio_atual * (1 + config['retorno'])

                # Adicionar aporte
                patrimonio_atual += aporte_mensal

                config['patrimonio'].append(patrimonio_atual)

        return {
            'meses': list(range(meses + 1)),
            'otimista': {
                'patrimonio': [self._safe_float(p) for p in cenarios['otimista']['patrimonio']],
                'final': self._safe_float(cenarios['otimista']['patrimonio'][-1])
            },
            'realista': {
                'patrimonio': [self._safe_float(p) for p in cenarios['realista']['patrimonio']],
                'final': self._safe_float(cenarios['realista']['patrimonio'][-1])
            },
            'pessimista': {
                'patrimonio': [self._safe_float(p) for p in cenarios['pessimista']['patrimonio']],
                'final': self._safe_float(cenarios['pessimista']['patrimonio'][-1])
            }
        }
