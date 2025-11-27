"""
Script de Teste de Integração Completa
Testa a API v3.0 com os novos modelos
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def test_health_check():
    """Testa health check da API"""
    print_section("1. HEALTH CHECK")

    try:
        response = requests.get(f"{API_URL}/")
        data = response.json()

        print(f"✅ Status: {data['status']}")
        print(f"✅ Versão: {data['versao']}")
        print(f"✅ Rede 1: {data['rede_1']}")
        print(f"✅ Rede 2: {data['rede_2']}")
        print(f"✅ R² Score: {data['r2_score']}")

        return True
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def test_classificar_perfil():
    """Testa endpoint de classificação de perfil"""
    print_section("2. CLASSIFICAÇÃO DE PERFIL")

    payload = {
        "idade": 25,
        "renda_mensal": 5000,
        "patrimonio_total": 20000,
        "experiencia_investimento": 2,
        "perfil_risco": 4,
        "horizonte_investimento": 15,
        "conhecimento_mercado": 3,
        "tem_reserva_emergencia": True
    }

    print("Enviando dados:")
    print(json.dumps(payload, indent=2))

    try:
        start = time.time()
        response = requests.post(f"{API_URL}/api/classificar-perfil", json=payload)
        end = time.time()

        data = response.json()

        print(f"\n✅ Perfil: {data['perfil']}")
        print(f"✅ Score Risco: {data['score_risco']}")
        print(f"✅ Confiança: {data['confianca']}")
        print(f"✅ Probabilidades:")
        for classe, prob in data.get('probabilidades', {}).items():
            print(f"   - {classe}: {prob}%")
        print(f"✅ Tempo de resposta: {(end-start)*1000:.2f}ms")

        return True
    except Exception as e:
        print(f"❌ ERRO: {e}")
        if hasattr(e, 'response'):
            print(f"Resposta: {e.response.text}")
        return False

def test_recomendar_portfolio():
    """Testa endpoint de recomendação completa"""
    print_section("3. RECOMENDAÇÃO COMPLETA (Rede 1 + Rede 2)")

    payload = {
        "idade": 25,
        "renda_mensal": 5000,
        "patrimonio_total": 20000,
        "experiencia_investimento": 2,
        "perfil_risco": 4,
        "horizonte_investimento": 15,
        "conhecimento_mercado": 3,
        "tem_reserva_emergencia": True,
        "objetivo_principal": "aposentadoria",
        "percentual_investir": 10
    }

    print("Enviando dados:")
    print(json.dumps(payload, indent=2))

    try:
        start = time.time()
        response = requests.post(f"{API_URL}/api/recomendar-portfolio", json=payload)
        end = time.time()

        data = response.json()

        print(f"\n✅ Perfil: {data['perfil_risco']}")
        print(f"✅ Confiança: {data['confianca_classificacao']}")

        print(f"\n✅ Alocação Recomendada:")
        total = 0
        for ativo, percentual in data['alocacao_recomendada'].items():
            print(f"   - {ativo}: {percentual}%")
            total += percentual
        print(f"   TOTAL: {total:.1f}%")

        if 99.5 <= total <= 100.5:
            print(f"   ✅ Soma válida!")
        else:
            print(f"   ❌ ERRO: Soma deveria ser ~100%")

        print(f"\n✅ Métricas:")
        for metrica, valor in data['metricas'].items():
            print(f"   - {metrica}: {valor}")

        if data.get('alertas'):
            print(f"\n⚠️  Alertas:")
            for alerta in data['alertas']:
                print(f"   - {alerta}")

        print(f"\n✅ Tempo de resposta: {(end-start)*1000:.2f}ms")

        return True
    except Exception as e:
        print(f"❌ ERRO: {e}")
        if hasattr(e, 'response'):
            print(f"Resposta: {e.response.text}")
        return False

def test_info_sistema():
    """Testa endpoint de informações do sistema"""
    print_section("4. INFORMAÇÕES DO SISTEMA")

    try:
        response = requests.get(f"{API_URL}/api/info-sistema")
        data = response.json()

        print(f"✅ Versão: {data['versao']}")

        print(f"\nRede 1 (Classificação):")
        rede1 = data['rede_1']
        for key, value in rede1.items():
            print(f"  - {key}: {value}")

        print(f"\nRede 2 (Alocação):")
        rede2 = data['rede_2']
        for key, value in rede2.items():
            if key != 'pesos_dinamicos':
                print(f"  - {key}: {value}")

        if rede2.get('pesos_dinamicos'):
            print(f"  - Pesos Dinâmicos: {rede2['pesos_dinamicos']}")

        return True
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def test_casos_extremos():
    """Testa casos extremos"""
    print_section("5. TESTES DE CASOS EXTREMOS")

    casos = [
        {
            "nome": "Jovem Conservador",
            "dados": {
                "idade": 20,
                "renda_mensal": 2000,
                "patrimonio_total": 5000,
                "experiencia_investimento": 0,
                "perfil_risco": 1,
                "horizonte_investimento": 5,
                "conhecimento_mercado": 1,
                "tem_reserva_emergencia": False
            }
        },
        {
            "nome": "Experiente Agressivo",
            "dados": {
                "idade": 35,
                "renda_mensal": 15000,
                "patrimonio_total": 500000,
                "experiencia_investimento": 10,
                "perfil_risco": 5,
                "horizonte_investimento": 30,
                "conhecimento_mercado": 5,
                "tem_reserva_emergencia": True
            }
        },
        {
            "nome": "Pré-Aposentadoria",
            "dados": {
                "idade": 60,
                "renda_mensal": 10000,
                "patrimonio_total": 800000,
                "experiencia_investimento": 20,
                "perfil_risco": 2,
                "horizonte_investimento": 5,
                "conhecimento_mercado": 4,
                "tem_reserva_emergencia": True
            }
        }
    ]

    resultados = []
    for caso in casos:
        print(f"\n{caso['nome']}:")
        try:
            response = requests.post(f"{API_URL}/api/recomendar-portfolio", json=caso['dados'])
            data = response.json()

            print(f"  ✅ Perfil: {data['perfil_risco']}")
            print(f"  ✅ Renda Fixa: {data['alocacao_recomendada'].get('Renda Fixa', 0)}%")
            print(f"  ✅ Ações: {data['alocacao_recomendada'].get('Ações Brasil', 0) + data['alocacao_recomendada'].get('Ações Internacional', 0)}%")

            resultados.append(True)
        except Exception as e:
            print(f"  ❌ ERRO: {e}")
            resultados.append(False)

    return all(resultados)

def main():
    """Executa todos os testes"""
    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#" + " TESTE DE INTEGRAÇÃO COMPLETA - INVESTE-AI V3.0".center(68) + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)

    tests = [
        ("Health Check", test_health_check),
        ("Classificação de Perfil", test_classificar_perfil),
        ("Recomendação Completa", test_recomendar_portfolio),
        ("Informações do Sistema", test_info_sistema),
        ("Casos Extremos", test_casos_extremos)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ ERRO CRÍTICO em {name}: {e}")
            results.append(False)

    # Resumo final
    print_section("RESUMO DOS TESTES")

    passed = sum(results)
    total = len(results)

    for i, (name, _) in enumerate(tests):
        status = "✅ PASSOU" if results[i] else "❌ FALHOU"
        print(f"{status} - {name}")

    print(f"\nResultado Final: {passed}/{total} testes passaram")

    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema 100% funcional!")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Verifique os erros acima.")

    print("\n" + "#" * 70)

if __name__ == "__main__":
    main()
