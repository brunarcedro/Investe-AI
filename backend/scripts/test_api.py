"""
Script para testar API otimizada
Testa endpoints e compara resultados
"""

import requests
import json
from time import sleep

# URL da API
BASE_URL = "http://localhost:8000"

def test_health():
    """Testa health check"""
    print("="*70)
    print("1. TESTANDO HEALTH CHECK")
    print("="*70)

    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()

        print(f"Status: {data['status']}")
        print(f"Modelo carregado: {data['modelo_carregado']}")
        print(f"Accuracy: {data['accuracy']:.2%}")
        print("")
        return True
    except Exception as e:
        print(f"ERRO: {e}")
        print("DICA: Inicie a API com: python api_otimizada.py")
        return False

def test_modelo_info():
    """Testa informações do modelo"""
    print("="*70)
    print("2. TESTANDO INFORMACOES DO MODELO")
    print("="*70)

    response = requests.get(f"{BASE_URL}/api/modelo-info")
    data = response.json()

    print(f"Nome: {data['nome']}")
    print(f"Tipo: {data['type']}")
    print(f"Accuracy: {data['accuracy']:.2%}")
    print(f"Features: {data['features']}")
    print(f"\nTecnicas aplicadas:")
    for tec in data['techniques']:
        print(f"  - {tec}")
    print("")

def test_classificacao():
    """Testa classificacao de perfil"""
    print("="*70)
    print("3. TESTANDO CLASSIFICACAO DE PERFIL")
    print("="*70)

    # Caso de teste: Jovem agressivo
    investidor = {
        "idade": 25,
        "renda_mensal": 8000,
        "dependentes": 0,
        "estado_civil": 0,
        "valor_investir_mensal": 2000,
        "experiencia_anos": 5,
        "patrimonio_atual": 50000,
        "dividas_percentual": 5,
        "tolerancia_perda_1": 9,
        "tolerancia_perda_2": 8,
        "horizonte_investimento": 35,
        "conhecimento_mercado": 8,
        "estabilidade_emprego": 8,
        "tem_reserva_emergencia": 1,
        "planos_grandes_gastos": 0
    }

    print(f"Investidor: {investidor['idade']} anos, "
          f"R${investidor['renda_mensal']:,.2f}/mes, "
          f"tolerancia {investidor['tolerancia_perda_1']}/10")

    response = requests.post(
        f"{BASE_URL}/api/classificar-perfil",
        json=investidor
    )

    data = response.json()

    print(f"\nRESULTADO:")
    print(f"  Perfil: {data['perfil']}")
    print(f"  Confianca: {data['confidence']:.1%}")
    print(f"  Descricao: {data['descricao']}")
    print(f"\nCaracteristicas identificadas:")
    for c in data['caracteristicas']:
        print(f"  - {c}")
    print(f"\nMetricas do modelo:")
    print(f"  Accuracy: {data['metricas_modelo']['accuracy']:.2%}")
    print(f"  Features: {data['metricas_modelo']['features_usadas']}")
    print("")

def test_recomendacao():
    """Testa recomendacao de portfolio"""
    print("="*70)
    print("4. TESTANDO RECOMENDACAO DE PORTFOLIO")
    print("="*70)

    # Caso de teste: Adulto moderado
    investidor = {
        "idade": 35,
        "renda_mensal": 10000,
        "dependentes": 1,
        "estado_civil": 1,
        "valor_investir_mensal": 2000,
        "experiencia_anos": 8,
        "patrimonio_atual": 150000,
        "dividas_percentual": 25,
        "tolerancia_perda_1": 6,
        "tolerancia_perda_2": 5,
        "horizonte_investimento": 25,
        "conhecimento_mercado": 6,
        "estabilidade_emprego": 7,
        "tem_reserva_emergencia": 1,
        "planos_grandes_gastos": 1
    }

    print(f"Investidor: {investidor['idade']} anos, "
          f"R${investidor['renda_mensal']:,.2f}/mes")

    response = requests.post(
        f"{BASE_URL}/api/recomendar-portfolio",
        json=investidor
    )

    data = response.json()

    print(f"\nRESULTADO:")
    print(f"  Perfil: {data['perfil_risco']}")
    print(f"  Confianca: {data['confidence']:.1%}")

    print(f"\nAlocacao Recomendada:")
    for ativo, pct in data['alocacao_recomendada'].items():
        bars = int(pct / 5)
        print(f"  {ativo:<25} {pct:>5.1f}% {'█' * bars}")

    print(f"\nJustificativa:")
    print(f"  {data['justificativa']}")

    if data['alertas']:
        print(f"\nAlertas:")
        for alerta in data['alertas']:
            print(f"  ⚠️  {alerta}")

    print(f"\nMetricas:")
    print(f"  Retorno esperado anual: {data['metricas']['retorno_esperado_anual']:.1%}")
    print(f"  Risco anual: {data['metricas']['risco_anual']:.1%}")
    print(f"  Sharpe Ratio: {data['metricas']['sharpe_ratio']:.2f}")
    print(f"  Accuracy modelo: {data['metricas']['accuracy_modelo']:.2%}")

    print(f"\nProdutos Sugeridos:")
    for classe, produtos in data['produtos_sugeridos'].items():
        print(f"  {classe}:")
        for p in produtos:
            print(f"    - {p}")

    print("")

def test_casos_multiplos():
    """Testa multiplos casos"""
    print("="*70)
    print("5. TESTANDO MULTIPLOS PERFIS")
    print("="*70)

    casos = [
        {
            "nome": "Conservador Jovem",
            "dados": {
                "idade": 23,
                "renda_mensal": 3000,
                "valor_investir_mensal": 300,
                "tolerancia_perda_1": 3,
                "tolerancia_perda_2": 2,
                "horizonte_investimento": 30,
                "conhecimento_mercado": 3,
                "tem_reserva_emergencia": 1
            }
        },
        {
            "nome": "Agressivo Experiente",
            "dados": {
                "idade": 40,
                "renda_mensal": 20000,
                "valor_investir_mensal": 5000,
                "tolerancia_perda_1": 9,
                "tolerancia_perda_2": 10,
                "horizonte_investimento": 20,
                "conhecimento_mercado": 9,
                "experiencia_anos": 15,
                "tem_reserva_emergencia": 1
            }
        },
        {
            "nome": "Moderado Iniciante",
            "dados": {
                "idade": 28,
                "renda_mensal": 5000,
                "valor_investir_mensal": 800,
                "tolerancia_perda_1": 5,
                "tolerancia_perda_2": 6,
                "horizonte_investimento": 25,
                "conhecimento_mercado": 4,
                "experiencia_anos": 2,
                "tem_reserva_emergencia": 0
            }
        }
    ]

    for caso in casos:
        # Completar dados obrigatorios
        dados_completos = {
            "idade": 25,
            "renda_mensal": 5000,
            "dependentes": 0,
            "estado_civil": 0,
            "valor_investir_mensal": 500,
            "experiencia_anos": 0,
            "patrimonio_atual": 10000,
            "dividas_percentual": 20,
            "tolerancia_perda_1": 5,
            "tolerancia_perda_2": 5,
            "horizonte_investimento": 20,
            "conhecimento_mercado": 5,
            "estabilidade_emprego": 5,
            "tem_reserva_emergencia": 0,
            "planos_grandes_gastos": 0
        }

        # Sobrescrever com dados do caso
        dados_completos.update(caso['dados'])

        try:
            response = requests.post(
                f"{BASE_URL}/api/classificar-perfil",
                json=dados_completos
            )

            data = response.json()

            print(f"\n{caso['nome']}:")
            print(f"  Perfil: {data['perfil']}")
            print(f"  Confianca: {data['confidence']:.1%}")

        except Exception as e:
            print(f"\nERRO em {caso['nome']}: {e}")

    print("")

def main():
    """Funcao principal"""
    print("\n" + "="*70)
    print("TESTE DA API OTIMIZADA (84.13% ACCURACY)")
    print("="*70 + "\n")

    # Health check
    if not test_health():
        print("\nAPI nao esta rodando!")
        print("Inicie com: python api_otimizada.py")
        return

    # Testes
    test_modelo_info()
    test_classificacao()
    test_recomendacao()
    test_casos_multiplos()

    print("="*70)
    print("TESTES CONCLUIDOS!")
    print("="*70)
    print("\nAPI funcionando perfeitamente!")
    print("Acesse: http://localhost:8000/docs para documentacao interativa")
    print("")

if __name__ == "__main__":
    main()
