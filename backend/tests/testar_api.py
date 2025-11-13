# testar_api.py
"""
Script para testar a API com dupla rede neural
"""

import requests
import json
from datetime import datetime

# URL base da API
BASE_URL = "http://localhost:8000"

def print_resultado(titulo, resposta):
    """Formata e imprime os resultados"""
    print("\n" + "="*60)
    print(f" {titulo}")
    print("="*60)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        print(json.dumps(dados, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Erro: {resposta.status_code}")
        print(resposta.text)

def testar_health_check():
    """Testa se a API está online"""
    print("\n🔍 Testando Health Check...")
    resposta = requests.get(f"{BASE_URL}/")
    print_resultado("STATUS DO SISTEMA", resposta)
    return resposta.status_code == 200

def testar_classificacao_perfil():
    """Testa a primeira rede neural - classificação"""
    
    # Lista de perfis para testar
    perfis_teste = [
        {
            "nome": "Jovem Agressivo",
            "dados": {
                "idade": 25,
                "renda_mensal": 8000,
                "patrimonio_total": 20000,
                "experiencia_investimento": 2,
                "objetivo_principal": "crescimento_patrimonio",
                "horizonte_investimento": 30,
                "tolerancia_risco": "arrojado",
                "conhecimento_mercado": "basico",
                "tem_reserva_emergencia": True,
                "percentual_investir": 30
            }
        },
        {
            "nome": "Aposentado Conservador",
            "dados": {
                "idade": 65,
                "renda_mensal": 15000,
                "patrimonio_total": 800000,
                "experiencia_investimento": 20,
                "objetivo_principal": "renda_passiva",
                "horizonte_investimento": 10,
                "tolerancia_risco": "conservador",
                "conhecimento_mercado": "avancado",
                "tem_reserva_emergencia": True,
                "percentual_investir": 10
            }
        },
        {
            "nome": "Família Moderada",
            "dados": {
                "idade": 40,
                "renda_mensal": 20000,
                "patrimonio_total": 300000,
                "experiencia_investimento": 10,
                "objetivo_principal": "educacao_filhos",
                "horizonte_investimento": 15,
                "tolerancia_risco": "moderado",
                "conhecimento_mercado": "intermediario",
                "tem_reserva_emergencia": True,
                "percentual_investir": 25
            }
        }
    ]
    
    print("\n" + "="*60)
    print(" TESTANDO CLASSIFICAÇÃO DE PERFIL (1ª Rede Neural)")
    print("="*60)
    
    for perfil in perfis_teste:
        print(f"\n📊 Testando: {perfil['nome']}")
        print("-" * 40)
        
        resposta = requests.post(
            f"{BASE_URL}/api/classificar-perfil",
            json=perfil['dados']
        )
        
        if resposta.status_code == 200:
            resultado = resposta.json()
            print(f"✅ Perfil: {resultado['perfil']}")
            print(f"   Score de Risco: {resultado['score_risco']}")
            print(f"   Descrição: {resultado['descricao']}")
            print(f"   Características:")
            for carac in resultado['caracteristicas']:
                print(f"      • {carac}")
        else:
            print(f"❌ Erro: {resposta.status_code}")

def testar_recomendacao_portfolio():
    """Testa a segunda rede neural - alocação"""
    
    perfis_teste = [
        {
            "nome": "Iniciante Conservador",
            "dados": {
                "idade": 22,
                "renda_mensal": 3000,
                "patrimonio_total": 5000,
                "experiencia_investimento": 0,
                "objetivo_principal": "reserva_emergencia",
                "horizonte_investimento": 2,
                "tolerancia_risco": "muito_conservador",
                "conhecimento_mercado": "nenhum",
                "tem_reserva_emergencia": False,
                "percentual_investir": 10
            }
        },
        {
            "nome": "Profissional Arrojado",
            "dados": {
                "idade": 35,
                "renda_mensal": 25000,
                "patrimonio_total": 400000,
                "experiencia_investimento": 8,
                "objetivo_principal": "crescimento_patrimonio",
                "horizonte_investimento": 25,
                "tolerancia_risco": "arrojado",
                "conhecimento_mercado": "avancado",
                "tem_reserva_emergencia": True,
                "percentual_investir": 40
            }
        },
        {
            "nome": "Pré-Aposentadoria Moderado",
            "dados": {
                "idade": 55,
                "renda_mensal": 30000,
                "patrimonio_total": 1000000,
                "experiencia_investimento": 15,
                "objetivo_principal": "aposentadoria",
                "horizonte_investimento": 10,
                "tolerancia_risco": "moderado",
                "conhecimento_mercado": "intermediario",
                "tem_reserva_emergencia": True,
                "percentual_investir": 20
            }
        }
    ]
    
    print("\n" + "="*60)
    print(" TESTANDO RECOMENDAÇÃO DE PORTFOLIO (2ª Rede Neural)")
    print("="*60)
    
    for perfil in perfis_teste:
        print(f"\n💼 Testando: {perfil['nome']}")
        print("-" * 40)
        
        resposta = requests.post(
            f"{BASE_URL}/api/recomendar-portfolio",
            json=perfil['dados']
        )
        
        if resposta.status_code == 200:
            resultado = resposta.json()
            
            print(f"✅ Perfil de Risco: {resultado['perfil_risco']}")
            
            print(f"\n📊 Alocação Recomendada:")
            for ativo, percentual in resultado['alocacao_recomendada'].items():
                barra = "█" * int(percentual/2)  # Barra visual
                print(f"   {ativo:25s}: {percentual:6.1f}% {barra}")
            
            print(f"\n📈 Métricas do Portfolio:")
            metricas = resultado['metricas']
            print(f"   • Retorno Esperado: {metricas.get('retorno_esperado_anual', 0):.2f}% ao ano")
            print(f"   • Risco (volatilidade): {metricas.get('risco_anual', 0):.2f}%")
            print(f"   • Sharpe Ratio: {metricas.get('sharpe_ratio', 0):.2f}")
            
            if resultado.get('alertas'):
                print(f"\n⚠️ Alertas:")
                for alerta in resultado['alertas']:
                    print(f"   {alerta}")
            
            print(f"\n💡 Justificativa:")
            print(f"   {resultado['justificativa']}")
            
            # Mostra alguns produtos sugeridos
            if resultado.get('produtos_sugeridos'):
                print(f"\n🛒 Produtos Sugeridos:")
                for categoria, produtos in resultado['produtos_sugeridos'].items():
                    if produtos:
                        print(f"   {categoria}:")
                        for produto in produtos[:2]:  # Mostra só 2 de cada
                            print(f"      • {produto}")
        else:
            print(f"❌ Erro: {resposta.status_code}")
            print(resposta.text)

def testar_info_sistema():
    """Testa endpoint de informações do sistema"""
    print("\n🔧 Testando Info do Sistema...")
    resposta = requests.get(f"{BASE_URL}/api/info-sistema")
    print_resultado("INFORMAÇÕES DO SISTEMA", resposta)

def menu_interativo():
    """Menu interativo para testar"""
    while True:
        print("\n" + "="*60)
        print(" MENU DE TESTES - API DUPLA REDE NEURAL")
        print("="*60)
        print("1. Testar Health Check")
        print("2. Testar Classificação de Perfil (1ª Rede)")
        print("3. Testar Recomendação de Portfolio (2ª Rede)")
        print("4. Testar Info do Sistema")
        print("5. Executar Todos os Testes")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            testar_health_check()
        elif opcao == "2":
            testar_classificacao_perfil()
        elif opcao == "3":
            testar_recomendacao_portfolio()
        elif opcao == "4":
            testar_info_sistema()
        elif opcao == "5":
            print("\n🚀 EXECUTANDO TODOS OS TESTES...")
            if testar_health_check():
                testar_classificacao_perfil()
                testar_recomendacao_portfolio()
                testar_info_sistema()
            else:
                print("❌ API não está respondendo. Inicie com: python main_v2.py")
        elif opcao == "0":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" TESTADOR DA API DE INVESTIMENTOS")
    print("="*60)
    
    # Verifica se API está online
    print("\n🔍 Verificando se a API está online...")
    try:
        resposta = requests.get(f"{BASE_URL}/", timeout=2)
        if resposta.status_code == 200:
            print("✅ API está online!")
            menu_interativo()
        else:
            print("⚠️ API respondeu com erro")
    except requests.exceptions.ConnectionError:
        print("❌ API não está rodando!")
        print("\n📝 Para iniciar a API:")
        print("   1. Abra outro terminal")
        print("   2. cd backend")
        print("   3. python main_v2.py")
        print("\n👉 Depois volte aqui e execute este teste novamente!")
    except Exception as e:
        print(f"❌ Erro: {e}")