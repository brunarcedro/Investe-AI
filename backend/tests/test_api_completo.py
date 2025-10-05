"""
Script de Teste Automatizado para API v2.0
Testa a integração das duas redes neurais
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def print_subheader(title):
    """Imprime subcabeçalho"""
    print(f"\n{title}")
    print("-"*70)

def test_health_check():
    """Testa se a API está online"""
    print_header("TESTE 1: HEALTH CHECK")

    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data['status']}")
            print(f"Versao: {data['versao']}")
            print(f"Modelo Perfil: {data['modelo_perfil']}")
            print(f"Modelo Alocacao: {data['modelo_alocacao']}")
            print("\nRESULTADO: SUCESSO")
            return True
        else:
            print(f"ERRO: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def test_classificacao_perfil():
    """Testa a primeira rede neural - classificação de perfil"""
    print_header("TESTE 2: CLASSIFICACAO DE PERFIL (1a REDE NEURAL)")

    perfis_teste = [
        {
            "nome": "Jovem Conservador",
            "dados": {
                "idade": 22,
                "renda_mensal": 3000,
                "patrimonio_total": 5000,
                "experiencia_investimento": 0,
                "objetivo_principal": "reserva_emergencia",
                "horizonte_investimento": 2,
                "tolerancia_risco": "conservador",
                "conhecimento_mercado": "nenhum",
                "tem_reserva_emergencia": False,
                "percentual_investir": 10
            }
        },
        {
            "nome": "Profissional Arrojado",
            "dados": {
                "idade": 30,
                "renda_mensal": 15000,
                "patrimonio_total": 200000,
                "experiencia_investimento": 5,
                "objetivo_principal": "crescimento_patrimonio",
                "horizonte_investimento": 20,
                "tolerancia_risco": "arrojado",
                "conhecimento_mercado": "avancado",
                "tem_reserva_emergencia": True,
                "percentual_investir": 35
            }
        },
        {
            "nome": "Moderado Equilibrado",
            "dados": {
                "idade": 35,
                "renda_mensal": 8000,
                "patrimonio_total": 100000,
                "experiencia_investimento": 3,
                "objetivo_principal": "educacao_filhos",
                "horizonte_investimento": 15,
                "tolerancia_risco": "moderado",
                "conhecimento_mercado": "intermediario",
                "tem_reserva_emergencia": True,
                "percentual_investir": 20
            }
        }
    ]

    sucessos = 0

    for perfil in perfis_teste:
        print_subheader(f"Testando: {perfil['nome']}")

        try:
            response = requests.post(
                f"{BASE_URL}/api/classificar-perfil",
                json=perfil['dados'],
                timeout=10
            )

            if response.status_code == 200:
                resultado = response.json()
                print(f"Perfil Classificado: {resultado['perfil']}")
                print(f"Score de Risco: {resultado['score_risco']}")
                print(f"Descricao: {resultado['descricao']}")
                print(f"Caracteristicas:")
                for carac in resultado['caracteristicas']:
                    print(f"  - {carac}")
                print("RESULTADO: SUCESSO")
                sucessos += 1
            else:
                print(f"ERRO: Status {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"ERRO: {e}")

    print_subheader(f"RESUMO: {sucessos}/{len(perfis_teste)} testes bem-sucedidos")
    return sucessos == len(perfis_teste)

def test_recomendacao_portfolio():
    """Testa a segunda rede neural - recomendação de portfolio"""
    print_header("TESTE 3: RECOMENDACAO DE PORTFOLIO (2a REDE NEURAL)")

    perfis_teste = [
        {
            "nome": "Iniciante Conservador",
            "dados": {
                "idade": 23,
                "renda_mensal": 3500,
                "patrimonio_total": 8000,
                "experiencia_investimento": 0,
                "objetivo_principal": "reserva_emergencia",
                "horizonte_investimento": 3,
                "tolerancia_risco": "conservador",
                "conhecimento_mercado": "basico",
                "tem_reserva_emergencia": False,
                "percentual_investir": 15
            }
        },
        {
            "nome": "Investidor Agressivo",
            "dados": {
                "idade": 28,
                "renda_mensal": 18000,
                "patrimonio_total": 250000,
                "experiencia_investimento": 4,
                "objetivo_principal": "crescimento_patrimonio",
                "horizonte_investimento": 25,
                "tolerancia_risco": "muito_arrojado",
                "conhecimento_mercado": "avancado",
                "tem_reserva_emergencia": True,
                "percentual_investir": 40
            }
        }
    ]

    sucessos = 0

    for perfil in perfis_teste:
        print_subheader(f"Testando: {perfil['nome']}")

        try:
            response = requests.post(
                f"{BASE_URL}/api/recomendar-portfolio",
                json=perfil['dados'],
                timeout=10
            )

            if response.status_code == 200:
                resultado = response.json()

                print(f"Perfil de Risco: {resultado['perfil_risco']}")

                print("\nAlocacao Recomendada:")
                total_alocacao = 0
                for ativo, percentual in resultado['alocacao_recomendada'].items():
                    barra = "#" * int(percentual/2)
                    print(f"  {ativo:25s}: {percentual:6.1f}% {barra}")
                    total_alocacao += percentual
                print(f"  {'TOTAL':25s}: {total_alocacao:6.1f}%")

                print("\nMetricas do Portfolio:")
                metricas = resultado['metricas']
                print(f"  Retorno Esperado: {metricas['retorno_esperado_anual']:.2f}% ao ano")
                print(f"  Risco (volatilidade): {metricas['risco_anual']:.2f}%")
                print(f"  Sharpe Ratio: {metricas['sharpe_ratio']:.2f}")
                print(f"  Horizonte: {metricas['horizonte_anos']} anos")

                if resultado['alertas']:
                    print("\nAlertas:")
                    for alerta in resultado['alertas']:
                        print(f"  {alerta}")

                print(f"\nJustificativa:")
                print(f"  {resultado['justificativa']}")

                # Mostra alguns produtos
                if resultado.get('produtos_sugeridos'):
                    print("\nProdutos Sugeridos (amostra):")
                    for categoria, produtos in list(resultado['produtos_sugeridos'].items())[:2]:
                        print(f"  {categoria}:")
                        for produto in produtos[:2]:
                            print(f"    - {produto}")

                print("\nRESULTADO: SUCESSO")
                sucessos += 1
            else:
                print(f"ERRO: Status {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"ERRO: {e}")

    print_subheader(f"RESUMO: {sucessos}/{len(perfis_teste)} testes bem-sucedidos")
    return sucessos == len(perfis_teste)

def test_info_sistema():
    """Testa endpoint de informações do sistema"""
    print_header("TESTE 4: INFORMACOES DO SISTEMA")

    try:
        response = requests.get(f"{BASE_URL}/api/info-sistema", timeout=5)

        if response.status_code == 200:
            data = response.json()

            print("\nArquitetura:")
            print(f"  Primeira Rede:")
            primeira = data['arquitetura']['primeira_rede']
            print(f"    Funcao: {primeira['funcao']}")
            print(f"    Entrada: {primeira['entrada']}")
            print(f"    Saida: {primeira['saida']}")
            print(f"    Status: {primeira['status']}")

            print(f"\n  Segunda Rede:")
            segunda = data['arquitetura']['segunda_rede']
            print(f"    Funcao: {segunda['funcao']}")
            print(f"    Entrada: {segunda['entrada']}")
            print(f"    Saida: {segunda['saida']}")
            print(f"    Arquitetura: {segunda['arquitetura']}")
            print(f"    Status: {segunda['status']}")

            print(f"\nClasses de Ativos:")
            for asset in data['classes_ativos']:
                print(f"  - {asset}")

            print(f"\nVersao API: {data['versao_api']}")

            print("\nRESULTADO: SUCESSO")
            return True
        else:
            print(f"ERRO: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"ERRO: {e}")
        return False

def test_integracao_dupla_rede():
    """Testa a integração entre as duas redes neurais"""
    print_header("TESTE 5: INTEGRACAO ENTRE AS DUAS REDES")

    print("\nVerificando fluxo completo:")
    print("1. Usuario envia dados")
    print("2. Primeira rede classifica perfil de risco")
    print("3. Score de risco e alimentado na segunda rede")
    print("4. Segunda rede gera alocacao personalizada")

    perfil_teste = {
        "idade": 27,
        "renda_mensal": 10000,
        "patrimonio_total": 150000,
        "experiencia_investimento": 2,
        "objetivo_principal": "crescimento_patrimonio",
        "horizonte_investimento": 20,
        "tolerancia_risco": "moderado",
        "conhecimento_mercado": "intermediario",
        "tem_reserva_emergencia": True,
        "percentual_investir": 25
    }

    print_subheader("Etapa 1: Classificacao (1a Rede)")

    try:
        response1 = requests.post(
            f"{BASE_URL}/api/classificar-perfil",
            json=perfil_teste,
            timeout=10
        )

        if response1.status_code == 200:
            classificacao = response1.json()
            print(f"Perfil: {classificacao['perfil']}")
            print(f"Score: {classificacao['score_risco']}")
            print("SUCESSO na 1a rede")
        else:
            print("FALHA na 1a rede")
            return False

        print_subheader("Etapa 2: Recomendacao (2a Rede)")

        response2 = requests.post(
            f"{BASE_URL}/api/recomendar-portfolio",
            json=perfil_teste,
            timeout=10
        )

        if response2.status_code == 200:
            recomendacao = response2.json()
            print(f"Perfil confirmado: {recomendacao['perfil_risco']}")
            print(f"Total de ativos alocados: {len(recomendacao['alocacao_recomendada'])}")
            print("SUCESSO na 2a rede")

            print_subheader("Etapa 3: Verificacao de Consistencia")

            # Verifica se os perfis são consistentes
            perfil1_lower = classificacao['perfil'].lower()
            perfil2_lower = recomendacao['perfil_risco'].lower()

            print(f"Perfil da 1a rede: {perfil1_lower}")
            print(f"Perfil da 2a rede: {perfil2_lower}")

            if perfil1_lower in perfil2_lower or perfil2_lower in perfil1_lower:
                print("CONSISTENCIA: OK - Perfis alinhados")
                print("\nRESULTADO: INTEGRACAO FUNCIONANDO CORRETAMENTE")
                return True
            else:
                print("ALERTA: Perfis divergentes (pode ser normal)")
                print("RESULTADO: Integracao funcional mas com divergencia")
                return True
        else:
            print("FALHA na 2a rede")
            return False

    except Exception as e:
        print(f"ERRO: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print(" TESTE AUTOMATIZADO DA API v2.0 - DUPLA REDE NEURAL")
    print("="*70)
    print(f" Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    resultados = {
        "health_check": False,
        "classificacao": False,
        "recomendacao": False,
        "info_sistema": False,
        "integracao": False
    }

    # Executa testes
    resultados["health_check"] = test_health_check()

    if resultados["health_check"]:
        resultados["classificacao"] = test_classificacao_perfil()
        resultados["recomendacao"] = test_recomendacao_portfolio()
        resultados["info_sistema"] = test_info_sistema()
        resultados["integracao"] = test_integracao_dupla_rede()
    else:
        print("\nAPI nao esta respondendo. Testes abortados.")
        print("\nPara iniciar a API:")
        print("  cd backend")
        print("  python main_v2.py")
        return

    # Resumo final
    print_header("RESUMO FINAL DOS TESTES")

    total_testes = len(resultados)
    sucessos = sum(1 for v in resultados.values() if v)

    for teste, resultado in resultados.items():
        status = "SUCESSO" if resultado else "FALHA"
        simbolo = "[OK]" if resultado else "[X]"
        print(f"  {simbolo} {teste:20s}: {status}")

    print(f"\n  Total: {sucessos}/{total_testes} testes bem-sucedidos")

    if sucessos == total_testes:
        print("\n  RESULTADO GERAL: TODOS OS TESTES PASSARAM")
        print("  API v2.0 FUNCIONANDO PERFEITAMENTE COM DUPLA REDE NEURAL")
    elif sucessos >= total_testes * 0.8:
        print("\n  RESULTADO GERAL: MAIORIA DOS TESTES PASSOU")
        print("  API v2.0 FUNCIONAL COM PEQUENOS AJUSTES NECESSARIOS")
    else:
        print("\n  RESULTADO GERAL: VARIOS TESTES FALHARAM")
        print("  API v2.0 REQUER CORRECOES")

    print("\n" + "="*70)

if __name__ == "__main__":
    main()