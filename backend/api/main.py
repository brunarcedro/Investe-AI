# main_v2.py
"""
API FastAPI com DUPLA REDE NEURAL
Versão 2.0 - Integra as duas redes neurais
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import joblib
from datetime import datetime

# Importa a segunda rede neural
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para imports funcionarem
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.models.portfolio_allocator.portfolio_network import SegundaRedeNeural

app = FastAPI(
    title="Sistema Inteligente de Investimentos v2.0",
    description="API com dupla rede neural para recomendação de carteiras",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= MODELOS DE DADOS =============

class PerfilInvestidor(BaseModel):
    """Dados de entrada do investidor"""
    idade: int = Field(..., ge=18, le=100, description="Idade em anos")
    renda_mensal: float = Field(..., ge=0, description="Renda mensal em R$")
    patrimonio_total: float = Field(..., ge=0, description="Patrimônio total em R$")
    experiencia_investimento: int = Field(..., ge=0, le=50, description="Anos de experiência")
    objetivo_principal: str = Field(..., description="Objetivo do investimento")
    horizonte_investimento: int = Field(..., ge=1, le=50, description="Horizonte em anos")
    tolerancia_risco: str = Field(..., description="Tolerância ao risco")
    conhecimento_mercado: str = Field(..., description="Nível de conhecimento")
    tem_reserva_emergencia: bool = Field(..., description="Possui reserva de emergência")
    percentual_investir: float = Field(..., ge=0, le=100, description="% da renda para investir")

class RespostaClassificacao(BaseModel):
    """Resposta da classificação de perfil"""
    perfil: str
    score_risco: float
    descricao: str
    caracteristicas: List[str]

class RespostaRecomendacao(BaseModel):
    """Resposta da recomendação de portfolio"""
    perfil_risco: str
    alocacao_recomendada: Dict[str, float]
    produtos_sugeridos: Dict[str, List[str]]
    justificativa: str
    alertas: List[str]
    metricas: Dict[str, float]

# ============= CARREGAMENTO DOS MODELOS =============

# Primeira rede neural (classificação de perfil) - BEST MODEL
try:
    # Using BEST model: neural_network.pkl (91% accuracy)
    model_path = Path(__file__).parent.parent / 'models' / 'risk_classifier' / 'best_model.pkl'
    dados_primeira_rede = joblib.load(str(model_path))
    # O modelo salva um dicionário com 'model', 'scaler', 'is_trained'
    modelo_perfil = dados_primeira_rede['model']
    scaler_perfil = dados_primeira_rede['scaler']
    print("Network 1 (Risk Classifier) loaded - BEST MODEL (91% accuracy)")
except Exception as e:
    print(f"Primeira rede neural nao encontrada - usando mock: {e}")
    modelo_perfil = None
    scaler_perfil = None

# Segunda rede neural (alocação de portfolio) - BEST MODEL
try:
    # Using BEST model: segunda_rede_neural.pkl (R² > 0.85)
    model_path = Path(__file__).parent.parent / 'models' / 'portfolio_allocator' / 'best_model.pkl'
    dados_segunda_rede = joblib.load(str(model_path))
    segunda_rede = SegundaRedeNeural()
    segunda_rede.model = dados_segunda_rede['model']
    segunda_rede.scaler = dados_segunda_rede['scaler']
    segunda_rede.asset_classes = dados_segunda_rede['asset_classes']
    segunda_rede.trained = True
    print("Network 2 (Portfolio Allocator) loaded - BEST MODEL (R² > 0.85)")
except Exception as e:
    print(f"Segunda rede neural nao encontrada - treinando nova: {e}")
    segunda_rede = SegundaRedeNeural()
    # Treina com dados sintéticos
    df = segunda_rede.gerar_dados_teste(500)
    X = segunda_rede.preparar_features(df)
    y = segunda_rede.preparar_targets(df)
    segunda_rede.treinar(X, y)

# ============= FUNÇÕES AUXILIARES =============

def classificar_perfil_risco(investidor: PerfilInvestidor) -> tuple:
    """
    Usa a PRIMEIRA rede neural para classificar o perfil
    Retorna: (perfil_nome, score_risco)
    """

    # Se tiver o modelo treinado, usa ele
    if modelo_perfil and scaler_perfil:
        # Prepara features para o modelo original (15 features)
        features = [
            investidor.idade,
            investidor.renda_mensal,
            0,  # dependentes (não temos no novo modelo)
            0,  # estado_civil (não temos no novo modelo)
            investidor.renda_mensal * (investidor.percentual_investir / 100),  # valor_investir_mensal
            investidor.experiencia_investimento,
            investidor.patrimonio_total,
            0,  # dividas_percentual (não temos)
            5,  # tolerancia_perda_1 (estimativa)
            5,  # tolerancia_perda_2 (estimativa)
            investidor.horizonte_investimento,
            {"nenhum": 2, "basico": 4, "intermediario": 6, "avancado": 8}.get(investidor.conhecimento_mercado, 5),
            7,  # estabilidade_emprego (estimativa)
            1 if investidor.tem_reserva_emergencia else 0,
            0   # planos_grandes_gastos (estimativa)
        ]

        try:
            # Normaliza e prediz
            features_scaled = scaler_perfil.transform([features])
            predicao_class = modelo_perfil.predict(features_scaled)[0]
            predicao_proba = modelo_perfil.predict_proba(features_scaled)[0]

            # Mapeia classe para score numérico
            mapa_score = {"conservador": 0.2, "moderado": 0.5, "agressivo": 0.8}
            score = mapa_score.get(predicao_class, max(predicao_proba))
        except Exception as e:
            print(f"Erro ao usar modelo: {e}")
            score = 0.5  # fallback
    else:
        # Lógica simplificada baseada na tolerância declarada
        mapa_risco = {
            "muito_conservador": 0.1,
            "conservador": 0.3,
            "moderado": 0.5,
            "arrojado": 0.7,
            "muito_arrojado": 0.9
        }
        score = mapa_risco.get(investidor.tolerancia_risco, 0.5)
    
    # Determina o perfil baseado no score
    if score < 0.2:
        perfil = "Muito Conservador"
    elif score < 0.4:
        perfil = "Conservador"
    elif score < 0.6:
        perfil = "Moderado"
    elif score < 0.8:
        perfil = "Arrojado"
    else:
        perfil = "Muito Arrojado"
    
    return perfil, score

def preparar_features_segunda_rede(investidor: PerfilInvestidor, score_risco: float) -> np.ndarray:
    """
    Prepara features para a SEGUNDA rede neural
    """
    # Mapeia conhecimento para número
    conhecimento_map = {
        "nenhum": 0.0,
        "basico": 0.33,
        "intermediario": 0.67,
        "avancado": 1.0
    }
    
    features = np.array([[
        investidor.idade / 100,
        investidor.renda_mensal / 50000,
        investidor.patrimonio_total / 1000000,
        investidor.experiencia_investimento / 30,
        score_risco,  # Usa o score da primeira rede
        investidor.horizonte_investimento / 30,
        1 if investidor.tem_reserva_emergencia else 0,
        conhecimento_map.get(investidor.conhecimento_mercado, 0.5)
    ]])
    
    return features

def gerar_produtos_sugeridos(alocacao: Dict[str, float]) -> Dict[str, List[str]]:
    """
    Sugere produtos específicos baseado na alocação
    """
    produtos = {}
    
    if alocacao.get('renda_fixa', 0) > 0:
        produtos['renda_fixa'] = [
            "Tesouro Selic (liquidez diária)",
            "Tesouro IPCA+ (proteção inflação)",
            "CDB de bancos grandes (100-110% CDI)",
            "LCI/LCA (isentos de IR)"
        ]
    
    if alocacao.get('acoes_brasil', 0) > 0:
        produtos['acoes_brasil'] = [
            "ETF BOVA11 (índice Bovespa)",
            "ETF SMAL11 (small caps)",
            "Ações de dividendos (BBAS3, ITUB4, VALE3)",
            "Fundos de ações gestão ativa"
        ]
    
    if alocacao.get('acoes_internacional', 0) > 0:
        produtos['acoes_internacional'] = [
            "ETF IVVB11 (S&P 500 em reais)",
            "BDRs de empresas americanas",
            "Fundos cambiais de ações",
            "ETFs globais via Avenue/Interactive Brokers"
        ]
    
    if alocacao.get('fundos_imobiliarios', 0) > 0:
        produtos['fundos_imobiliarios'] = [
            "FIIs de tijolo (HGLG11, VISC11)",
            "FIIs de papel (KNRI11, HGCR11)",
            "FIIs de fundos (HFOF11)",
            "FIIs de logística (VILG11)"
        ]
    
    if alocacao.get('commodities', 0) > 0:
        produtos['commodities'] = [
            "ETF GOLD11 (ouro)",
            "Fundos de commodities",
            "BDRs de mineradoras"
        ]
    
    if alocacao.get('criptomoedas', 0) > 0:
        produtos['criptomoedas'] = [
            "Bitcoin via exchanges brasileiras",
            "Ethereum",
            "ETF HASH11 (índice de criptos)",
            "Stablecoins para menor volatilidade"
        ]
    
    return produtos

def calcular_metricas(alocacao: Dict[str, float], horizonte: int) -> Dict[str, float]:
    """
    Calcula métricas estimadas do portfolio
    """
    # Retornos esperados anuais (estimativas)
    retornos = {
        'renda_fixa': 0.11,  # CDI + spread
        'acoes_brasil': 0.15,  # Histórico IBOV
        'acoes_internacional': 0.12,  # S&P 500 em reais
        'fundos_imobiliarios': 0.10,  # Yield médio
        'commodities': 0.08,  # Conservador
        'criptomoedas': 0.25  # Alta volatilidade
    }
    
    # Riscos (desvio padrão anual)
    riscos = {
        'renda_fixa': 0.02,
        'acoes_brasil': 0.25,
        'acoes_internacional': 0.20,
        'fundos_imobiliarios': 0.15,
        'commodities': 0.18,
        'criptomoedas': 0.60
    }
    
    # Calcula retorno esperado ponderado
    retorno_esperado = sum(
        alocacao.get(asset, 0) * retornos.get(asset, 0)
        for asset in retornos
    )
    
    # Calcula risco (simplificado - sem correlação)
    risco_portfolio = sum(
        alocacao.get(asset, 0) * riscos.get(asset, 0)
        for asset in riscos
    )
    
    # Sharpe Ratio (usando Selic como taxa livre de risco)
    taxa_livre_risco = 0.1175  # Selic atual
    sharpe_ratio = (retorno_esperado - taxa_livre_risco) / risco_portfolio if risco_portfolio > 0 else 0
    
    # Projeção de crescimento
    valor_inicial = 100000  # Base 100k
    valor_projetado = valor_inicial * ((1 + retorno_esperado) ** horizonte)
    
    return {
        'retorno_esperado_anual': round(retorno_esperado * 100, 2),
        'risco_anual': round(risco_portfolio * 100, 2),
        'sharpe_ratio': round(sharpe_ratio, 2),
        'valor_projetado': round(valor_projetado, 2),
        'horizonte_anos': horizonte
    }

# ============= ENDPOINTS =============

@app.get("/")
async def root():
    """Health check e informações do sistema"""
    return {
        "status": "online",
        "versao": "2.0.0",
        "modelo_perfil": "Carregado" if modelo_perfil else "Mock",
        "modelo_alocacao": "Carregado" if segunda_rede.trained else "Sintetico",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/classificar-perfil", response_model=RespostaClassificacao)
async def endpoint_classificar_perfil(investidor: PerfilInvestidor):
    """
    PRIMEIRA REDE NEURAL: Classifica o perfil de risco do investidor
    """
    try:
        # Classifica usando a primeira rede
        perfil, score = classificar_perfil_risco(investidor)
        
        # Descrição baseada no perfil
        descricoes = {
            "Muito Conservador": "Prioriza segurança absoluta e preservação de capital",
            "Conservador": "Busca segurança com pequena exposição a risco",
            "Moderado": "Equilibra segurança e crescimento",
            "Arrojado": "Aceita riscos maiores buscando retornos superiores",
            "Muito Arrojado": "Busca maximizar retornos aceitando alta volatilidade"
        }
        
        # Características do investidor
        caracteristicas = []
        if investidor.idade < 30:
            caracteristicas.append("Jovem com horizonte longo")
        elif investidor.idade > 60:
            caracteristicas.append("Próximo ou na aposentadoria")
        
        if investidor.patrimonio_total > 500000:
            caracteristicas.append("Patrimônio substancial")
        
        if investidor.experiencia_investimento > 5:
            caracteristicas.append("Investidor experiente")
        elif investidor.experiencia_investimento == 0:
            caracteristicas.append("Primeiro investimento")
        
        if investidor.tem_reserva_emergencia:
            caracteristicas.append("Possui reserva de emergencia")
        else:
            caracteristicas.append("ALERTA: Sem reserva de emergencia")
        
        return RespostaClassificacao(
            perfil=perfil,
            score_risco=round(score, 2),
            descricao=descricoes.get(perfil, "Perfil identificado"),
            caracteristicas=caracteristicas
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recomendar-portfolio", response_model=RespostaRecomendacao)
async def endpoint_recomendar_portfolio(investidor: PerfilInvestidor):
    """
    SEGUNDA REDE NEURAL: Recomenda alocação de portfolio personalizada
    """
    try:
        # Primeiro classifica o perfil
        perfil, score_risco = classificar_perfil_risco(investidor)
        
        # Prepara features para segunda rede
        features = preparar_features_segunda_rede(investidor, score_risco)
        
        # Gera recomendação usando a SEGUNDA rede neural
        alocacao_array = segunda_rede.prever(features)[0]
        
        # Converte para dicionário
        alocacao = {}
        for i, asset in enumerate(segunda_rede.asset_classes):
            if alocacao_array[i] > 0.01:  # Só mostra se > 1%
                # Traduz nomes para português
                nome_traduzido = {
                    'renda_fixa': 'Renda Fixa',
                    'acoes_brasil': 'Ações Brasil',
                    'acoes_internacional': 'Ações Internacional',
                    'fundos_imobiliarios': 'Fundos Imobiliários',
                    'commodities': 'Commodities',
                    'criptomoedas': 'Criptomoedas'
                }.get(asset, asset)
                
                alocacao[nome_traduzido] = round(float(alocacao_array[i]) * 100, 1)
        
        # Produtos sugeridos
        alocacao_interna = {
            segunda_rede.asset_classes[i]: alocacao_array[i]
            for i in range(len(segunda_rede.asset_classes))
        }
        produtos = gerar_produtos_sugeridos(alocacao_interna)
        
        # Métricas
        metricas = calcular_metricas(alocacao_interna, investidor.horizonte_investimento)
        
        # Alertas
        alertas = []
        if not investidor.tem_reserva_emergencia:
            alertas.append("ALERTA: Monte uma reserva de emergencia antes de investir")

        if alocacao_interna.get('criptomoedas', 0) > 0.05:
            alertas.append("ALERTA: Criptomoedas sao muito volateis - invista com cuidado")

        if investidor.experiencia_investimento == 0:
            alertas.append("DICA: Comece com aportes pequenos e va aprendendo")

        if investidor.idade > 60 and alocacao_interna.get('acoes_brasil', 0) > 0.3:
            alertas.append("ALERTA: Considere reduzir exposicao a renda variavel")
        
        # Justificativa
        justificativa = f"Para seu perfil {perfil}, com {investidor.idade} anos e "
        justificativa += f"horizonte de {investidor.horizonte_investimento} anos, "
        justificativa += f"recomendamos uma carteira {'conservadora' if score_risco < 0.4 else 'balanceada' if score_risco < 0.7 else 'arrojada'} "
        justificativa += f"com foco em {investidor.objetivo_principal.replace('_', ' ')}. "
        justificativa += f"A alocação busca equilibrar retorno esperado de {metricas['retorno_esperado_anual']}% ao ano "
        justificativa += f"com risco controlado de {metricas['risco_anual']}%."
        
        return RespostaRecomendacao(
            perfil_risco=perfil,
            alocacao_recomendada=alocacao,
            produtos_sugeridos=produtos,
            justificativa=justificativa,
            alertas=alertas,
            metricas=metricas
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/info-sistema")
async def info_sistema():
    """Informações sobre o sistema de dupla rede neural"""
    return {
        "arquitetura": {
            "primeira_rede": {
                "funcao": "Classificação de perfil de risco",
                "entrada": "15 features do investidor",
                "saida": "Score de risco (0-1)",
                "status": "Operacional" if modelo_perfil else "Modo mock"
            },
            "segunda_rede": {
                "funcao": "Recomendação de alocação",
                "entrada": "8 features (perfil + contexto)",
                "saida": "6 percentuais de alocação",
                "arquitetura": "MLP com 2 camadas ocultas (100, 50)",
                "status": "Treinada" if segunda_rede.trained else "Dados sinteticos"
            }
        },
        "classes_ativos": segunda_rede.asset_classes,
        "versao_api": "2.0.0",
        "data_deploy": datetime.now().isoformat()
    }

# ============= SIMULAÇÃO (NOVO - DADOS REAIS) =============

# Import módulos de simulação
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from simulacao.backtesting import Backtesting, converter_alocacao_para_decimal
    from simulacao.monte_carlo import MonteCarloSimulation

    backtesting_engine = Backtesting()
    monte_carlo_engine = MonteCarloSimulation()
    print("Módulos de simulação carregados")
except Exception as e:
    print(f"Erro ao carregar módulos de simulação: {e}")
    backtesting_engine = None
    monte_carlo_engine = None

class SimulacaoRequest(BaseModel):
    """Dados para simulação"""
    alocacao: Dict[str, float]  # Alocação em percentual
    valor_inicial: float = Field(default=10000, ge=100)
    aporte_mensal: float = Field(default=0, ge=0)
    periodo: str = Field(default='5y')  # '1y', '2y', '5y', '10y'

class ProjecaoRequest(BaseModel):
    """Dados para projeção futura"""
    alocacao: Dict[str, float]
    valor_inicial: float = Field(default=10000, ge=100)
    aporte_mensal: float = Field(default=0, ge=0)
    anos: int = Field(default=10, ge=1, le=50)
    num_simulacoes: int = Field(default=1000, ge=100, le=10000)

@app.post("/api/simular-backtesting")
async def simular_backtesting(request: SimulacaoRequest):
    """
    Simula carteira com dados históricos reais do mercado
    """
    try:
        if not backtesting_engine:
            raise HTTPException(status_code=503, detail="Módulo de simulação indisponível")

        # Converter alocação de % para decimal
        alocacao_decimal = converter_alocacao_para_decimal(request.alocacao)

        # Executar simulação
        resultado = backtesting_engine.simular_carteira(
            alocacao=alocacao_decimal,
            valor_inicial=request.valor_inicial,
            aporte_mensal=request.aporte_mensal,
            periodo=request.periodo
        )

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/comparar-benchmarks")
async def comparar_benchmarks(request: SimulacaoRequest):
    """
    Compara carteira com benchmarks (CDI, IBOV, S&P500)
    """
    try:
        if not backtesting_engine:
            raise HTTPException(status_code=503, detail="Módulo de simulação indisponível")

        alocacao_decimal = converter_alocacao_para_decimal(request.alocacao)

        resultado = backtesting_engine.comparar_com_benchmarks(
            alocacao=alocacao_decimal,
            valor_inicial=request.valor_inicial,
            aporte_mensal=request.aporte_mensal,
            periodo=request.periodo
        )

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projetar-monte-carlo")
async def projetar_monte_carlo(request: ProjecaoRequest):
    """
    Projeta cenários futuros usando Monte Carlo
    """
    try:
        if not monte_carlo_engine:
            raise HTTPException(status_code=503, detail="Módulo de Monte Carlo indisponível")

        alocacao_decimal = converter_alocacao_para_decimal(request.alocacao)

        # Executar simulação de Monte Carlo
        resultado = monte_carlo_engine.simular_cenarios(
            alocacao=alocacao_decimal,
            valor_inicial=request.valor_inicial,
            aporte_mensal=request.aporte_mensal,
            anos=request.anos,
            num_simulacoes=request.num_simulacoes
        )

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cenarios-detalhados")
async def cenarios_detalhados(request: ProjecaoRequest):
    """
    Gera 3 cenários: Otimista, Realista, Pessimista
    """
    try:
        if not monte_carlo_engine:
            raise HTTPException(status_code=503, detail="Módulo de Monte Carlo indisponível")

        alocacao_decimal = converter_alocacao_para_decimal(request.alocacao)

        resultado = monte_carlo_engine.gerar_cenarios_detalhados(
            alocacao=alocacao_decimal,
            valor_inicial=request.valor_inicial,
            aporte_mensal=request.aporte_mensal,
            anos=request.anos
        )

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============= EXECUÇÃO =============

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print(" SISTEMA DE INVESTIMENTOS COM DUPLA REDE NEURAL v2.0")
    print("="*60)
    print("\nPrimeira rede: Classificacao de perfil")
    print("Segunda rede: Alocacao de portfolio")
    print("\nIniciando servidor...")
    print("-"*60)

    uvicorn.run(app, host="0.0.0.0", port=8000)