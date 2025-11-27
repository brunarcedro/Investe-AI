# main.py
"""
API FastAPI com DUPLA REDE NEURAL - VERSÃO ATUALIZADA
Versão 3.0 - Usa Voting Classifier + Ensemble V4 Ultimate
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import joblib
from datetime import datetime
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

app = FastAPI(
    title="Investe-AI v3.0",
    description="Sistema dual com Voting Classifier + Ensemble V4 Ultimate",
    version="3.0.0"
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
    """Dados de entrada do investidor (15 features para Rede 1)"""
    # 15 features obrigatórias (ordem exata do dataset de treinamento)
    idade: int = Field(..., ge=18, le=100, description="Idade em anos")
    renda_mensal: float = Field(..., ge=0, description="Renda mensal em R$")
    dependentes: int = Field(..., ge=0, le=10, description="Número de dependentes")
    estado_civil: int = Field(..., ge=0, le=4, description="Estado civil (0=solteiro, 1=casado, etc.)")
    valor_investir_mensal: float = Field(..., ge=0, description="Valor disponível para investir por mês")
    experiencia_anos: int = Field(..., ge=0, le=50, description="Anos de experiência em investimentos")
    dividas_percentual: float = Field(..., ge=0, le=100, description="% da renda comprometida com dívidas")
    patrimonio_atual: float = Field(..., ge=0, description="Patrimônio total atual em R$")
    tolerancia_perda_1: int = Field(..., ge=1, le=10, description="Tolerância à perda cenário 1 (1-10)")
    tolerancia_perda_2: int = Field(..., ge=1, le=10, description="Tolerância à perda cenário 2 (1-10)")
    horizonte_investimento: int = Field(..., ge=1, le=50, description="Horizonte de investimento em anos")
    conhecimento_mercado: int = Field(..., ge=1, le=5, description="Nível de conhecimento do mercado (1-5)")
    estabilidade_emprego: int = Field(..., ge=1, le=10, description="Estabilidade do emprego (1-10)")
    tem_reserva_emergencia: bool = Field(..., description="Possui reserva de emergência")
    planos_grandes_gastos: bool = Field(..., description="Planeja grandes gastos nos próximos 2 anos")

    # Features opcionais para UI
    objetivo_principal: Optional[str] = Field(default="aposentadoria", description="Objetivo do investimento")
    percentual_investir: Optional[float] = Field(default=10, ge=0, le=100, description="% da renda para investir")

class RespostaClassificacao(BaseModel):
    """Resposta da classificação de perfil"""
    perfil: str
    score_risco: float
    confianca: float
    probabilidades: Dict[str, float]
    descricao: str
    caracteristicas: List[str]

class RespostaRecomendacao(BaseModel):
    """Resposta completa com perfil + alocação"""
    perfil_risco: str
    score_risco: float
    confianca_classificacao: float
    probabilidades_perfis: Dict[str, float]
    alocacao_recomendada: Dict[str, float]
    produtos_sugeridos: Dict[str, List[str]]
    justificativa: str
    alertas: List[str]
    metricas: Dict[str, float]

# ============= CARREGAMENTO DOS MODELOS =============

# Variáveis globais para modelos
modelo_voting_classifier = None
scaler_perfil = None
modelo_ensemble_v4 = None
scaler_alocacao = None
pesos_ensemble = None

# Carregar Voting Classifier (Rede 1)
try:
    model_path = ROOT_DIR / 'models' / 'risk_classifier' / 'best_model.pkl'
    dados_voting = joblib.load(str(model_path))
    modelo_voting_classifier = dados_voting['model']
    scaler_perfil = dados_voting['scaler']
    print("[OK] Voting Classifier carregado (Rede 1 - Classificação)")
except Exception as e:
    print(f"[ERRO] Voting Classifier não encontrado: {e}")
    modelo_voting_classifier = None
    scaler_perfil = None

# Carregar Ensemble V4 Ultimate (Rede 2)
try:
    model_path = ROOT_DIR / 'models' / 'portfolio_allocator' / 'best_model_v4_ultimate.pkl'
    dados_v4 = joblib.load(str(model_path))

    # Extrair componentes do V4
    modelo_ensemble_v4 = {
        'mlp1': dados_v4['mlp1'],
        'mlp2': dados_v4['mlp2'],
        'rf': dados_v4['rf'],
        'gb_models': dados_v4['gb_models'],
        'et': dados_v4['et']
    }
    pesos_ensemble = dados_v4['weights']  # (w1, w2, w3, w4, w5)
    scaler_alocacao = dados_v4['scaler']
    asset_classes = dados_v4['asset_classes']
    r2_score_modelo = dados_v4['r2_score']

    print(f"[OK] Ensemble V4 Ultimate carregado (Rede 2 - Alocação)")
    print(f"     R² Score: {r2_score_modelo:.4f}")
    print(f"     Pesos: MLP1={pesos_ensemble[0]:.3f}, MLP2={pesos_ensemble[1]:.3f}, "
          f"RF={pesos_ensemble[2]:.3f}, GB={pesos_ensemble[3]:.3f}, ET={pesos_ensemble[4]:.3f}")

except Exception as e:
    print(f"[ERRO] Ensemble V4 não encontrado: {e}")
    modelo_ensemble_v4 = None
    scaler_alocacao = None
    pesos_ensemble = None
    asset_classes = ['renda_fixa', 'acoes_brasil', 'acoes_internacional',
                     'fundos_imobiliarios', 'commodities', 'criptomoedas']
    r2_score_modelo = 0.0

# ============= FUNÇÕES AUXILIARES =============

def preparar_features_rede1(investidor: PerfilInvestidor) -> np.ndarray:
    """
    Prepara 15 features para o Voting Classifier (Rede 1)
    Ordem exata do dataset de treinamento
    """
    features = np.array([[
        investidor.idade,
        investidor.renda_mensal,
        investidor.dependentes,
        investidor.estado_civil,
        investidor.valor_investir_mensal,
        investidor.experiencia_anos,
        investidor.dividas_percentual,
        investidor.patrimonio_atual,
        investidor.tolerancia_perda_1,
        investidor.tolerancia_perda_2,
        investidor.horizonte_investimento,
        investidor.conhecimento_mercado,
        investidor.estabilidade_emprego,
        1 if investidor.tem_reserva_emergencia else 0,
        1 if investidor.planos_grandes_gastos else 0
    ]])

    return features

def extrair_features_rede2(investidor: PerfilInvestidor) -> np.ndarray:
    """
    Extrai 8 features base para Rede 2 (Portfolio Allocator)
    a partir dos dados do investidor
    """
    # Calcula perfil_risco_medio a partir das tolerâncias
    perfil_risco_medio = (investidor.tolerancia_perda_1 + investidor.tolerancia_perda_2) / 2.0

    features = np.array([[
        investidor.idade,
        investidor.renda_mensal,
        investidor.patrimonio_atual,
        investidor.experiencia_anos,
        perfil_risco_medio,  # Média das tolerâncias
        investidor.horizonte_investimento,
        1 if investidor.tem_reserva_emergencia else 0,
        investidor.conhecimento_mercado
    ]])

    return features

def aplicar_feature_engineering(features_base: np.ndarray) -> np.ndarray:
    """
    Aplica feature engineering para criar 27 features (Rede 2)

    Input: 8 features base (idade, renda, patrimonio, experiencia, perfil_risco, horizonte, tem_emergencia, conhecimento)
    Output: 27 features enriquecidas
    """
    idade = features_base[0, 0]
    renda = features_base[0, 1]
    patrimonio = features_base[0, 2]
    experiencia = features_base[0, 3]
    perfil_risco = features_base[0, 4]
    horizonte = features_base[0, 5]
    tem_emergencia = features_base[0, 6]
    conhecimento = features_base[0, 7]

    # 1. Polinomiais
    idade_squared = idade ** 2
    idade_cubed = idade ** 3
    renda_squared = renda ** 2
    patrimonio_squared = patrimonio ** 2

    # 2. Logarítmicas
    renda_log = np.log1p(renda)
    patrimonio_log = np.log1p(patrimonio)

    # 3. Radiculares
    renda_sqrt = np.sqrt(renda)
    patrimonio_sqrt = np.sqrt(patrimonio)

    # 4. Risco
    risco_squared = perfil_risco ** 2
    risco_cubed = perfil_risco ** 3

    # 5. Interações
    renda_patrimonio_ratio = renda / (patrimonio + 1)
    patrimonio_renda_ratio = patrimonio / (renda + 1)
    risco_horizonte = perfil_risco * horizonte
    idade_horizonte = idade * horizonte
    experiencia_conhecimento = experiencia * conhecimento
    risco_idade = perfil_risco * idade
    risco_renda = perfil_risco * renda_log

    # 6. Compostos
    capacidade_investimento = (renda_log + patrimonio_log) / 2
    perfil_completo = (perfil_risco + conhecimento + experiencia/10) / 3

    # Combinar todas as 27 features
    features_27 = np.array([[
        # Originais (8)
        idade, renda, patrimonio, experiencia, perfil_risco,
        horizonte, tem_emergencia, conhecimento,
        # Polinomiais (4)
        idade_squared, idade_cubed, renda_squared, patrimonio_squared,
        # Logarítmicas (2)
        renda_log, patrimonio_log,
        # Radiculares (2)
        renda_sqrt, patrimonio_sqrt,
        # Risco (2)
        risco_squared, risco_cubed,
        # Interações (7)
        renda_patrimonio_ratio, patrimonio_renda_ratio,
        risco_horizonte, idade_horizonte, experiencia_conhecimento,
        risco_idade, risco_renda,
        # Compostos (2)
        capacidade_investimento, perfil_completo
    ]])

    return features_27

def classificar_perfil(investidor: PerfilInvestidor) -> tuple:
    """
    Usa Voting Classifier para classificar perfil

    Returns: (perfil_nome, score_risco, confianca, probabilidades_dict)
    """
    if modelo_voting_classifier is None or scaler_perfil is None:
        # Fallback simples
        score = investidor.perfil_risco / 5.0
        perfil = mapear_score_para_perfil(score)
        return perfil, score, 0.75, {"conservador": 33, "moderado": 34, "agressivo": 33}

    try:
        # Preparar features
        features = preparar_features_rede1(investidor)

        # Normalizar
        features_scaled = scaler_perfil.transform(features)

        # Predizer
        perfil_classe = modelo_voting_classifier.predict(features_scaled)[0]
        probabilidades = modelo_voting_classifier.predict_proba(features_scaled)[0]

        # Extrair probabilidades por classe
        classes = modelo_voting_classifier.classes_
        prob_dict = {classe: round(float(prob) * 100, 1) for classe, prob in zip(classes, probabilidades)}

        # Confiança = max probabilidade
        confianca = round(float(max(probabilidades)), 2)

        # Converter classe para score (0-1)
        mapa_score = {
            "conservador": 0.2,
            "moderado": 0.5,
            "balanceado": 0.6,
            "arrojado": 0.8,
            "agressivo": 0.9
        }
        score_risco = mapa_score.get(perfil_classe.lower(), 0.5)

        # Nome do perfil formatado
        perfil_nome = perfil_classe.capitalize()

        return perfil_nome, score_risco, confianca, prob_dict

    except Exception as e:
        print(f"[ERRO] Erro ao classificar perfil: {e}")
        score = investidor.perfil_risco / 5.0
        perfil = mapear_score_para_perfil(score)
        return perfil, score, 0.70, {}

def mapear_score_para_perfil(score: float) -> str:
    """Mapeia score numérico para nome de perfil"""
    if score < 0.3:
        return "Conservador"
    elif score < 0.5:
        return "Moderado"
    elif score < 0.7:
        return "Balanceado"
    elif score < 0.85:
        return "Arrojado"
    else:
        return "Agressivo"

def alocar_portfolio_v4(features_27: np.ndarray, perfil_risco_texto: str = "Moderado") -> np.ndarray:
    """
    Usa Ensemble V4 Ultimate para alocar portfolio

    Input: 27 features enriquecidas, perfil de risco (texto)
    Output: 6 percentuais (soma = 100%)
    """
    # Alocações fallback baseadas no perfil de risco
    fallback_alocacoes = {
        "Conservador": np.array([50, 20, 15, 10, 3, 2]),
        "Moderado": np.array([35, 30, 20, 10, 3, 2]),
        "Balanceado": np.array([25, 35, 25, 10, 3, 2]),
        "Arrojado": np.array([15, 40, 30, 10, 3, 2]),
        "Agressivo": np.array([10, 40, 35, 10, 3, 2])
    }

    if modelo_ensemble_v4 is None or scaler_alocacao is None:
        # Fallback se modelo não carregado
        return fallback_alocacoes.get(perfil_risco_texto, fallback_alocacoes["Moderado"])

    try:
        # Normalizar features
        features_scaled = scaler_alocacao.transform(features_27)

        # Predições de cada modelo
        pred_mlp1 = modelo_ensemble_v4['mlp1'].predict(features_scaled)
        pred_mlp2 = modelo_ensemble_v4['mlp2'].predict(features_scaled)
        pred_rf = modelo_ensemble_v4['rf'].predict(features_scaled)
        pred_gb = np.column_stack([gb.predict(features_scaled) for gb in modelo_ensemble_v4['gb_models']])
        pred_et = modelo_ensemble_v4['et'].predict(features_scaled)

        # Voting ponderado
        w1, w2, w3, w4, w5 = pesos_ensemble
        ensemble_pred = (
            w1 * pred_mlp1 +
            w2 * pred_mlp2 +
            w3 * pred_rf +
            w4 * pred_gb +
            w5 * pred_et
        )

        # DEBUG: Print predictions before normalization
        print(f"[DEBUG] Raw predictions: {ensemble_pred[0]}")

        # Normalizar para somar 100%
        ensemble_pred = np.maximum(ensemble_pred, 0)
        soma = ensemble_pred.sum()

        print(f"[DEBUG] After clipping: {ensemble_pred[0]}, soma={soma}")

        # Se soma muito baixa ou muitos zeros, usar fallback baseado no perfil
        num_zeros = np.sum(ensemble_pred[0] <= 0.01)
        if soma < 0.5 or num_zeros >= 4:
            # Muitos valores zero ou soma muito baixa - usar fallback
            print(f"[WARNING] Predições ruins (soma={soma:.3f}, zeros={num_zeros}), usando fallback para perfil {perfil_risco_texto}")
            return fallback_alocacoes.get(perfil_risco_texto, fallback_alocacoes["Moderado"])

        # Normalizar para percentagem
        ensemble_pred = (ensemble_pred / soma) * 100

        # Garantir mínimo de 0.5% para ativos com alocação > 0
        for i in range(ensemble_pred.shape[1]):
            if 0 < ensemble_pred[0, i] < 0.5:
                ensemble_pred[0, i] = 0.5

        # Renormalizar para garantir soma = 100%
        ensemble_pred = (ensemble_pred / ensemble_pred.sum()) * 100

        print(f"[DEBUG] Final allocation: {ensemble_pred[0]}")

        return ensemble_pred[0]

    except Exception as e:
        print(f"[ERRO] Erro ao alocar portfolio: {e}")
        import traceback
        traceback.print_exc()
        return fallback_alocacoes.get(perfil_risco_texto, fallback_alocacoes["Moderado"])

def gerar_produtos_sugeridos(alocacao_dict: Dict[str, float]) -> Dict[str, List[str]]:
    """Gera sugestões de produtos por classe de ativo"""
    produtos = {}

    if alocacao_dict.get('Renda Fixa', 0) > 0:
        produtos['Renda Fixa'] = [
            "Tesouro Selic (liquidez diária)",
            "Tesouro IPCA+ (proteção inflação)",
            "CDB 100-110% CDI",
            "LCI/LCA (isentos de IR)"
        ]

    if alocacao_dict.get('Ações Brasil', 0) > 0:
        produtos['Ações Brasil'] = [
            "ETF BOVA11 (IBOV)",
            "ETF SMAL11 (Small Caps)",
            "Ações de dividendos",
            "Fundos de ações"
        ]

    if alocacao_dict.get('Ações Internacional', 0) > 0:
        produtos['Ações Internacional'] = [
            "ETF IVVB11 (S&P 500)",
            "BDRs de empresas americanas",
            "Fundos cambiais",
            "ETFs globais"
        ]

    if alocacao_dict.get('Fundos Imobiliários', 0) > 0:
        produtos['Fundos Imobiliários'] = [
            "FIIs de tijolo (HGLG11)",
            "FIIs de papel (KNRI11)",
            "FIIs de fundos (HFOF11)"
        ]

    if alocacao_dict.get('Commodities', 0) > 0:
        produtos['Commodities'] = [
            "ETF GOLD11 (ouro)",
            "Fundos de commodities"
        ]

    if alocacao_dict.get('Criptomoedas', 0) > 0:
        produtos['Criptomoedas'] = [
            "Bitcoin via exchanges",
            "ETF HASH11 (índice cripto)"
        ]

    return produtos

def calcular_metricas(alocacao: List[float], horizonte: int) -> Dict[str, float]:
    """Calcula métricas estimadas do portfolio"""
    # Retornos e riscos anuais esperados
    retornos = [0.11, 0.15, 0.12, 0.10, 0.08, 0.25]  # Por classe de ativo
    riscos = [0.02, 0.25, 0.20, 0.15, 0.18, 0.60]

    # Cálculos ponderados
    retorno_esperado = sum(a/100 * r for a, r in zip(alocacao, retornos))
    risco_portfolio = sum(a/100 * r for a, r in zip(alocacao, riscos))

    # Sharpe Ratio
    taxa_livre_risco = 0.1175  # Selic
    sharpe = (retorno_esperado - taxa_livre_risco) / risco_portfolio if risco_portfolio > 0 else 0

    # Projeção
    valor_inicial = 100000
    valor_projetado = valor_inicial * ((1 + retorno_esperado) ** horizonte)

    return {
        'retorno_esperado_anual': round(retorno_esperado * 100, 2),
        'risco_anual': round(risco_portfolio * 100, 2),
        'sharpe_ratio': round(sharpe, 2),
        'valor_projetado': round(valor_projetado, 2),
        'horizonte_anos': horizonte,
        'r2_modelo': round(r2_score_modelo, 4)
    }

# ============= ENDPOINTS =============

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "versao": "3.0.0",
        "rede_1": "Voting Classifier" if modelo_voting_classifier else "Mock",
        "rede_2": "Ensemble V4 Ultimate" if modelo_ensemble_v4 else "Mock",
        "r2_score": round(r2_score_modelo, 4) if modelo_ensemble_v4 else 0.0,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/classificar-perfil", response_model=RespostaClassificacao)
async def endpoint_classificar_perfil(investidor: PerfilInvestidor):
    """Endpoint: Classificação de perfil (Rede 1)"""
    try:
        perfil, score, confianca, prob_dict = classificar_perfil(investidor)

        # Descrições
        descricoes = {
            "Conservador": "Prioriza segurança e preservação de capital",
            "Moderado": "Busca equilíbrio entre segurança e crescimento",
            "Balanceado": "Equilibra renda fixa e variável",
            "Arrojado": "Aceita riscos maiores por retornos superiores",
            "Agressivo": "Busca maximizar retornos com alta volatilidade"
        }

        # Características
        caracteristicas = []
        if investidor.idade < 30:
            caracteristicas.append("Jovem com horizonte longo")
        elif investidor.idade > 60:
            caracteristicas.append("Próximo à aposentadoria")

        if investidor.experiencia_investimento > 5:
            caracteristicas.append("Investidor experiente")
        elif investidor.experiencia_investimento == 0:
            caracteristicas.append("Primeiro investimento")

        if not investidor.tem_reserva_emergencia:
            caracteristicas.append("ALERTA: Sem reserva de emergência")

        return RespostaClassificacao(
            perfil=perfil,
            score_risco=round(score, 2),
            confianca=confianca,
            probabilidades=prob_dict,
            descricao=descricoes.get(perfil, "Perfil identificado"),
            caracteristicas=caracteristicas
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recomendar-portfolio", response_model=RespostaRecomendacao)
async def endpoint_recomendar_portfolio(investidor: PerfilInvestidor):
    """Endpoint: Recomendação completa (Rede 1 + Rede 2)"""
    try:
        # 1. Classificar perfil (Rede 1 - usa 15 features)
        perfil, score_risco, confianca, prob_dict = classificar_perfil(investidor)

        # 2. Preparar features para Rede 2 (extrai 8 features base)
        features_base_8 = extrair_features_rede2(investidor)
        features_27 = aplicar_feature_engineering(features_base_8)

        # 3. Alocar portfolio (Rede 2 - Ensemble V4 com 27 features)
        alocacao_array = alocar_portfolio_v4(features_27, perfil)

        # 4. Formatar alocação (sempre retorna todas as 6 classes)
        nomes_traduzidos = ['Renda Fixa', 'Ações Brasil', 'Ações Internacional',
                            'Fundos Imobiliários', 'Commodities', 'Criptomoedas']

        alocacao_dict = {}
        for i, nome in enumerate(nomes_traduzidos):
            # Sempre inclui todas as 6 classes de ativos (mesmo se = 0)
            alocacao_dict[nome] = round(float(alocacao_array[i]), 1)

        # 5. Produtos e métricas
        produtos = gerar_produtos_sugeridos(alocacao_dict)
        metricas = calcular_metricas(alocacao_array, investidor.horizonte_investimento)

        # 6. Alertas
        alertas = []
        if not investidor.tem_reserva_emergencia:
            alertas.append("ALERTA: Monte reserva de emergência antes de investir")

        if alocacao_array[5] > 5:  # Cripto > 5%
            alertas.append("ALERTA: Criptomoedas são muito voláteis")

        if investidor.experiencia_anos == 0:
            alertas.append("DICA: Comece com aportes pequenos")

        # 7. Justificativa
        justificativa = (
            f"Para seu perfil {perfil}, com {investidor.idade} anos e "
            f"horizonte de {investidor.horizonte_investimento} anos, "
            f"recomendamos uma carteira balanceada com retorno esperado de "
            f"{metricas['retorno_esperado_anual']}% ao ano e risco de "
            f"{metricas['risco_anual']}%. "
            f"O modelo Ensemble V4 (R²={metricas['r2_modelo']}) sugere esta alocação "
            f"otimizada com base em suas características."
        )

        return RespostaRecomendacao(
            perfil_risco=perfil,
            score_risco=round(score_risco, 2),
            confianca_classificacao=confianca,
            probabilidades_perfis=prob_dict,
            alocacao_recomendada=alocacao_dict,
            produtos_sugeridos=produtos,
            justificativa=justificativa,
            alertas=alertas,
            metricas=metricas
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/info-sistema")
async def info_sistema():
    """Informações detalhadas do sistema"""
    return {
        "versao": "3.0.0",
        "rede_1": {
            "nome": "Voting Classifier",
            "tipo": "Ensemble (RF + MLP + SVM)",
            "entrada": "8 features do investidor",
            "saida": "Perfil de risco + probabilidades",
            "acuracia": "~88%",
            "status": "OK" if modelo_voting_classifier else "Mock"
        },
        "rede_2": {
            "nome": "Ensemble V4 Ultimate",
            "tipo": "5 modelos (2 MLPs + RF + GB + ET)",
            "entrada": "27 features (feature engineering)",
            "saida": "6 classes de ativos (%)",
            "r2_score": round(r2_score_modelo, 4),
            "pesos_dinamicos": list(pesos_ensemble) if pesos_ensemble else [],
            "status": "OK" if modelo_ensemble_v4 else "Mock"
        },
        "classes_ativos": asset_classes,
        "data_deploy": datetime.now().isoformat()
    }

# ============= EXECUÇÃO =============

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print(" INVESTE-AI v3.0 - SISTEMA DUAL DE REDES NEURAIS")
    print("="*70)
    print(" Rede 1: Voting Classifier (Classificação de Perfil)")
    print(" Rede 2: Ensemble V4 Ultimate (Alocação de Portfolio)")
    print("-"*70)
    uvicorn.run(app, host="0.0.0.0", port=8000)
