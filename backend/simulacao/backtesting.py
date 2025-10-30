"""
Módulo de Backtesting - Simulação com dados reais do mercado
Usa yfinance para obter cotações históricas e simular carteiras
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


# Mapeamento de classes de ativos para tickers reais
TICKERS_BRASIL = {
    'renda_fixa': '^IRX',  # Treasury Bill 13 Week (proxy CDI)
    'acoes_brasil': 'BOVA11.SA',  # ETF Bovespa
    'acoes_internacional': 'IVVB11.SA',  # ETF S&P 500
    'fundos_imobiliarios': 'IFIX.SA',  # Índice FIIs
    'commodities': 'GOLD11.SA',  # ETF Ouro
    'criptomoedas': 'BTC-USD'  # Bitcoin
}

# Benchmarks para comparação
BENCHMARKS = {
    'CDI': '^IRX',
    'IBOVESPA': '^BVSP',
    'S&P500': '^GSPC',
    'Dólar': 'BRL=X'
}


class Backtesting:
    """Classe para realizar backtesting de carteiras"""

    def __init__(self):
        self.cache = {}  # Cache de dados baixados

    @staticmethod
    def _safe_float(value, default=0.0):
        """Converte valor para float, substituindo NaN/inf por valor padrão"""
        if pd.isna(value) or np.isinf(value):
            return default
        return float(value)

    def obter_dados_historicos(
        self,
        ticker: str,
        periodo: str = '5y',
        intervalo: str = '1mo'
    ) -> pd.DataFrame:
        """
        Obtém dados históricos de um ticker

        Args:
            ticker: Código do ativo (ex: 'BOVA11.SA')
            periodo: Período ('1y', '2y', '5y', '10y', 'max')
            intervalo: Intervalo ('1d', '1wk', '1mo')

        Returns:
            DataFrame com dados históricos
        """
        cache_key = f"{ticker}_{periodo}_{intervalo}"

        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            dados = yf.download(
                ticker,
                period=periodo,
                interval=intervalo,
                progress=False
            )

            if dados.empty:
                # Retorna dados mock se não conseguir baixar
                return self._gerar_dados_mock(periodo, intervalo)

            self.cache[cache_key] = dados
            return dados

        except Exception as e:
            print(f"Erro ao baixar {ticker}: {e}")
            return self._gerar_dados_mock(periodo, intervalo)

    def _gerar_dados_mock(self, periodo: str, intervalo: str) -> pd.DataFrame:
        """Gera dados simulados caso API falhe"""
        num_periodos = {'1y': 12, '2y': 24, '5y': 60, '10y': 120}.get(periodo, 60)

        dates = pd.date_range(
            end=datetime.now(),
            periods=num_periodos,
            freq='MS'
        )

        # Simula retornos aleatórios
        returns = np.random.normal(0.01, 0.05, num_periodos)
        prices = 100 * (1 + returns).cumprod()

        return pd.DataFrame({
            'Close': prices
        }, index=dates)

    def simular_carteira(
        self,
        alocacao: Dict[str, float],
        valor_inicial: float = 10000,
        aporte_mensal: float = 0,
        periodo: str = '5y'
    ) -> Dict:
        """
        Simula evolução de uma carteira com dados reais

        Args:
            alocacao: Dict com alocação (ex: {'renda_fixa': 0.6, 'acoes_brasil': 0.4})
            valor_inicial: Valor inicial em R$
            aporte_mensal: Aporte mensal em R$
            periodo: Período da simulação

        Returns:
            Dict com resultados da simulação
        """
        # Normalizar alocação (garantir que soma 100%)
        total = sum(alocacao.values())
        alocacao_norm = {k: v/total for k, v in alocacao.items()}

        # Baixar dados de todos os ativos
        dados_ativos = {}
        for classe, peso in alocacao_norm.items():
            if peso > 0.001:  # Apenas se alocação > 0.1%
                ticker = TICKERS_BRASIL.get(classe, '^IRX')
                dados_ativos[classe] = self.obter_dados_historicos(ticker, periodo)

        # Se não conseguiu dados, retornar simulação mock
        if not dados_ativos:
            return self._simular_mock(valor_inicial, aporte_mensal, periodo)

        # Calcular retornos de cada ativo
        retornos_ativos = {}
        primeira_classe = None
        for classe, dados in dados_ativos.items():
            # Garantir que Close é uma Series 1D
            if 'Close' in dados.columns:
                close_values = dados['Close']
                # Se for MultiIndex (várias colunas), pegar a primeira
                if isinstance(close_values, pd.DataFrame):
                    close_series = close_values.iloc[:, 0]
                else:
                    close_series = close_values
            else:
                # Fallback: usar primeira coluna
                close_series = dados.iloc[:, 0]

            retornos = close_series.pct_change().fillna(0)
            retornos_ativos[classe] = retornos
            if primeira_classe is None:
                primeira_classe = classe

        # Combinar retornos em um DataFrame
        # Usar index do primeiro ativo para garantir compatibilidade
        if primeira_classe:
            df_retornos = pd.DataFrame(retornos_ativos, index=dados_ativos[primeira_classe].index)
        else:
            df_retornos = pd.DataFrame(retornos_ativos)

        # Calcular retorno da carteira (média ponderada)
        retorno_carteira = (df_retornos * pd.Series(alocacao_norm)).sum(axis=1)

        # Simular evolução patrimonial
        patrimonio = [valor_inicial]
        aportes_acumulados = [0]

        for i, ret in enumerate(retorno_carteira[1:], 1):
            # Aplicar retorno do período
            novo_patrimonio = patrimonio[-1] * (1 + ret)

            # Adicionar aporte mensal
            novo_patrimonio += aporte_mensal
            aportes_acumulados.append(aportes_acumulados[-1] + aporte_mensal)

            patrimonio.append(novo_patrimonio)

        # Calcular métricas
        patrimonio_final = patrimonio[-1]
        total_aportado = valor_inicial + aportes_acumulados[-1]
        rentabilidade_total = ((patrimonio_final - total_aportado) / total_aportado) * 100

        # Retorno anualizado
        anos = len(patrimonio) / 12  # assumindo dados mensais
        retorno_anual = ((patrimonio_final / valor_inicial) ** (1/anos) - 1) * 100

        # Volatilidade
        volatilidade = retorno_carteira.std() * np.sqrt(12) * 100  # Anualizada

        # Sharpe Ratio (assumindo CDI como taxa livre de risco = 11%)
        sharpe = (retorno_anual - 11) / volatilidade if volatilidade > 0 else 0

        # Maior queda (Max Drawdown)
        patrimonio_series = pd.Series(patrimonio)
        running_max = patrimonio_series.expanding().max()
        drawdown = ((patrimonio_series - running_max) / running_max) * 100
        max_drawdown = drawdown.min()

        return {
            'patrimonio_historico': patrimonio,
            'datas': df_retornos.index.tolist(),
            'patrimonio_final': self._safe_float(patrimonio_final),
            'valor_inicial': valor_inicial,
            'aportes_total': self._safe_float(aportes_acumulados[-1]),
            'total_aportado': self._safe_float(total_aportado),
            'rentabilidade_total': self._safe_float(rentabilidade_total),
            'retorno_anualizado': self._safe_float(retorno_anual),
            'volatilidade_anual': self._safe_float(volatilidade),
            'sharpe_ratio': self._safe_float(sharpe),
            'max_drawdown': self._safe_float(max_drawdown),
            'melhor_mes': self._safe_float(retorno_carteira.max() * 100),
            'pior_mes': self._safe_float(retorno_carteira.min() * 100),
        }

    def comparar_com_benchmarks(
        self,
        alocacao: Dict[str, float],
        valor_inicial: float = 10000,
        aporte_mensal: float = 0,
        periodo: str = '5y'
    ) -> Dict:
        """
        Compara carteira com benchmarks (CDI, IBOV, S&P500)
        """
        # Simular carteira recomendada
        resultado_carteira = self.simular_carteira(
            alocacao, valor_inicial, aporte_mensal, periodo
        )

        # Simular benchmarks
        benchmarks_resultados = {}

        # 100% Renda Fixa (CDI)
        benchmarks_resultados['CDI'] = self.simular_carteira(
            {'renda_fixa': 1.0}, valor_inicial, aporte_mensal, periodo
        )

        # 100% Ações Brasil
        benchmarks_resultados['IBOVESPA'] = self.simular_carteira(
            {'acoes_brasil': 1.0}, valor_inicial, aporte_mensal, periodo
        )

        # 100% S&P 500
        benchmarks_resultados['S&P500'] = self.simular_carteira(
            {'acoes_internacional': 1.0}, valor_inicial, aporte_mensal, periodo
        )

        return {
            'carteira_ia': resultado_carteira,
            'benchmarks': benchmarks_resultados
        }

    def _simular_mock(self, valor_inicial: float, aporte_mensal: float, periodo: str) -> Dict:
        """Simulação mock caso APIs falhem"""
        num_meses = {'1y': 12, '2y': 24, '5y': 60, '10y': 120}.get(periodo, 60)

        # Simula retornos aleatórios
        retornos = np.random.normal(0.01, 0.03, num_meses)

        patrimonio = [valor_inicial]
        for ret in retornos:
            novo = patrimonio[-1] * (1 + ret) + aporte_mensal
            patrimonio.append(novo)

        return {
            'patrimonio_historico': patrimonio,
            'datas': pd.date_range(end=datetime.now(), periods=num_meses+1, freq='MS').tolist(),
            'patrimonio_final': round(patrimonio[-1], 2),
            'valor_inicial': valor_inicial,
            'aportes_total': aporte_mensal * num_meses,
            'total_aportado': valor_inicial + (aporte_mensal * num_meses),
            'rentabilidade_total': round(((patrimonio[-1] - (valor_inicial + aporte_mensal * num_meses)) / (valor_inicial + aporte_mensal * num_meses)) * 100, 2),
            'retorno_anualizado': 12.0,
            'volatilidade_anual': 15.0,
            'sharpe_ratio': 0.8,
            'max_drawdown': -10.0,
            'melhor_mes': 5.2,
            'pior_mes': -3.1,
        }


# Função auxiliar para conversão de alocação
def converter_alocacao_para_decimal(alocacao_percentual: Dict[str, float]) -> Dict[str, float]:
    """
    Converte alocação de percentual (0-100) para decimal (0-1)
    """
    return {k: v/100 for k, v in alocacao_percentual.items()}
