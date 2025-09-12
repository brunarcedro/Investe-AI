import requests
import json

# Dados de teste
test_user = {
    "idade": 23,
    "renda_mensal": 3500,
    "dependentes": 0,
    "estado_civil": 0,
    "valor_investir_mensal": 700,
    "experiencia_anos": 1,
    "patrimonio_atual": 8000,
    "dividas_percentual": 20,
    "tolerancia_perda_1": 6,
    "tolerancia_perda_2": 5,
    "objetivo_prazo": 2,
    "conhecimento_mercado": 5,
    "estabilidade_emprego": 7,
    "reserva_emergencia": 1,
    "planos_grandes_gastos": 0
}

def test_api():
    base_url = "http://localhost:8000"
    
    # Testar classificação
    print("=== TESTE DE CLASSIFICAÇÃO ===")
    response = requests.post(f"{base_url}/classify-profile", json=test_user)
    if response.status_code == 200:
        result = response.json()
        print(f"Perfil: {result['perfil_risco']}")
        print(f"Confiança: {result['confianca']:.3f}")
        print(f"Probabilidades: {result['probabilidades']}")
    
    # Testar recomendação
    print("\n=== TESTE DE RECOMENDAÇÃO ===")
    response = requests.post(f"{base_url}/recommend-portfolio", json=test_user)
    if response.status_code == 200:
        result = response.json()
        print(f"Alocação: {result['alocacao']}")
        print(f"Retorno esperado: {result['retorno_esperado']}")
        print(f"Ativos específicos: {json.dumps(result['ativos_especificos'], indent=2)}")

if __name__ == "__main__":
    test_api()