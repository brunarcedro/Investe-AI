from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import sys
import os

# Adicionar path para imports locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.neural_network import RiskProfileClassifier
from models.portfolio_algo import PortfolioAllocator

app = FastAPI(title="Investment Recommendation API", version="1.0.0")

# Modelos Pydantic para validação
class UserProfile(BaseModel):
    idade: int
    renda_mensal: float
    dependentes: int
    estado_civil: int
    valor_investir_mensal: float
    experiencia_anos: int
    patrimonio_atual: float
    dividas_percentual: float
    tolerancia_perda_1: int
    tolerancia_perda_2: int
    objetivo_prazo: int
    conhecimento_mercado: int
    estabilidade_emprego: int
    reserva_emergencia: int
    planos_grandes_gastos: int

class ProfileResponse(BaseModel):
    perfil_risco: str
    confianca: float
    probabilidades: Dict[str, float]

class PortfolioResponse(BaseModel):
    alocacao: Dict[str, float]
    ativos_especificos: Dict[str, List[Dict]]
    valor_total: float
    retorno_esperado: str

# Inicializar modelos globalmente
classifier = None
allocator = None

@app.on_event("startup")
async def startup_event():
    global classifier, allocator
    # Carregar rede neural treinada
    classifier = RiskProfileClassifier()
    X, y = classifier.load_dataset()
    classifier.train(X, y)
    
    # Inicializar alocador de portfolio
    allocator = PortfolioAllocator()

@app.get("/")
async def root():
    return {"message": "Investment Recommendation API", "status": "running"}

@app.post("/classify-profile", response_model=ProfileResponse)
async def classify_profile(user_data: UserProfile):
    try:
        # Converter para lista de features
        features = [
            user_data.idade, user_data.renda_mensal, user_data.dependentes,
            user_data.estado_civil, user_data.valor_investir_mensal,
            user_data.experiencia_anos, user_data.patrimonio_atual,
            user_data.dividas_percentual, user_data.tolerancia_perda_1,
            user_data.tolerancia_perda_2, user_data.objetivo_prazo,
            user_data.conhecimento_mercado, user_data.estabilidade_emprego,
            user_data.reserva_emergencia, user_data.planos_grandes_gastos
        ]
        
        # Classificar perfil
        result = classifier.predict(features)
        
        return ProfileResponse(
            perfil_risco=result['perfil_previsto'],
            confianca=result['confianca'],
            probabilidades=result['probabilidades']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend-portfolio")
async def recommend_portfolio(user_data: UserProfile):
    if classifier is None or allocator is None:
        raise HTTPException(status_code=500, detail="Modelos não inicializados")
    
    try:
        # Classificar perfil primeiro
        features = [
            user_data.idade, user_data.renda_mensal, user_data.dependentes,
            user_data.estado_civil, user_data.valor_investir_mensal,
            user_data.experiencia_anos, user_data.patrimonio_atual,
            user_data.dividas_percentual, user_data.tolerancia_perda_1,
            user_data.tolerancia_perda_2, user_data.objetivo_prazo,
            user_data.conhecimento_mercado, user_data.estabilidade_emprego,
            user_data.reserva_emergencia, user_data.planos_grandes_gastos
        ]
        
        profile_result = classifier.predict(features)
        risk_profile = profile_result['perfil_previsto']
        
        # Gerar portfolio
        portfolio = allocator.generate_portfolio(
            risk_profile=risk_profile,
            monthly_amount=user_data.valor_investir_mensal,
            user_context={
                'idade': user_data.idade,
                'experiencia': user_data.experiencia_anos,
                'reserva_emergencia': user_data.reserva_emergencia
            }
        )
        
        # Adicionar informações do perfil à resposta
        portfolio['perfil_identificado'] = {
            'perfil': risk_profile,
            'confianca': profile_result['confianca'],
            'probabilidades': profile_result['probabilidades']
        }
        
        return portfolio
        
    except Exception as e:
        # Log do erro para debug
        print(f"Erro no recommend_portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)