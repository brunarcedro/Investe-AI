"""
Gerador de Casos de Teste - Versao para Slide
Mostra 3 exemplos praticos de classificacao
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Configuracao
plt.rcParams['font.size'] = 11
plt.rcParams['figure.facecolor'] = 'white'

def criar_casos_teste_visual():
    """Cria visualizacao dos 3 casos de teste (Joao, Carlos, Maria)"""

    print("="*70)
    print("GERANDO CASOS DE TESTE PARA SLIDE")
    print("="*70)

    # Dados dos 3 casos
    casos = {
        'Joao': {
            'idade': 65,
            'renda': 'R$ 15.000',
            'patrimonio': 'R$ 800k',
            'experiencia': '20 anos',
            'tolerancia': '2/10',
            'horizonte': '10 anos',
            'dependentes': 0,
            'perfil': 'CONSERVADOR',
            'prob': '91%',
            'score': '0.18',
            'cor': '#2ecc71',
            'analise': [
                'Idoso (65 anos)',
                'Baixa tolerancia (2/10)',
                'Horizonte curto (10a)',
                'Alta confianca (91%)'
            ]
        },
        'Carlos': {
            'idade': 40,
            'renda': 'R$ 20.000',
            'patrimonio': 'R$ 200k',
            'experiencia': '10 anos',
            'tolerancia': '5/10',
            'horizonte': '20 anos',
            'dependentes': 2,
            'perfil': 'MODERADO',
            'prob': '68%',
            'score': '0.48',
            'cor': '#f39c12',
            'analise': [
                'Meia-idade (40 anos)',
                'Tolerancia media (5/10)',
                '2 dependentes',
                'Confianca media (68%)'
            ]
        },
        'Maria': {
            'idade': 24,
            'renda': 'R$ 8.000',
            'patrimonio': 'R$ 15k',
            'experiencia': '3 anos',
            'tolerancia': '9/10',
            'horizonte': '30 anos',
            'dependentes': 0,
            'perfil': 'AGRESSIVO',
            'prob': '87%',
            'score': '0.82',
            'cor': '#e74c3c',
            'analise': [
                'Muito jovem (24 anos)',
                'Alta tolerancia (9/10)',
                'Horizonte longo (30a)',
                'Alta confianca (87%)'
            ]
        }
    }

    # Criar figura
    fig = plt.figure(figsize=(18, 12))

    # Titulo principal
    fig.suptitle('Casos de Teste Praticos - Primeira Rede Neural\nExemplos de Classificacao de Perfil de Risco',
                 fontsize=20, fontweight='bold', y=0.98)

    # Grid 3 colunas
    gs = fig.add_gridspec(1, 3, hspace=0.3, wspace=0.15,
                          left=0.05, right=0.95, top=0.90, bottom=0.05)

    nomes = ['Joao', 'Carlos', 'Maria']

    for idx, nome in enumerate(nomes):
        caso = casos[nome]
        ax = fig.add_subplot(gs[0, idx])
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 15)
        ax.axis('off')

        # Box principal com cor do perfil
        box_principal = FancyBboxPatch(
            (0.5, 0.5), 9, 14,
            boxstyle="round,pad=0.1",
            edgecolor=caso['cor'],
            facecolor='white',
            linewidth=4,
            zorder=1
        )
        ax.add_patch(box_principal)

        # Header com nome e idade
        header_box = FancyBboxPatch(
            (0.5, 12.5), 9, 2,
            boxstyle="round,pad=0.05",
            edgecolor='black',
            facecolor=caso['cor'],
            linewidth=2,
            alpha=0.8,
            zorder=2
        )
        ax.add_patch(header_box)

        # Nome
        ax.text(5, 13.5, f'{nome.upper()}', ha='center', va='center',
                fontsize=18, fontweight='bold', color='white', zorder=3)
        ax.text(5, 13.0, f'{caso["idade"]} anos', ha='center', va='center',
                fontsize=14, fontweight='bold', color='white', zorder=3)

        # Dados financeiros e demograficos
        y_pos = 11.5
        dados = [
            ('Renda Mensal:', caso['renda']),
            ('Patrimonio:', caso['patrimonio']),
            ('Experiencia:', caso['experiencia']),
            ('Tolerancia:', caso['tolerancia']),
            ('Horizonte:', caso['horizonte']),
            ('Dependentes:', str(caso['dependentes'])),
        ]

        for label, valor in dados:
            ax.text(1, y_pos, label, ha='left', va='center',
                   fontsize=11, fontweight='bold', zorder=3)
            ax.text(9, y_pos, valor, ha='right', va='center',
                   fontsize=11, zorder=3)
            y_pos -= 1.3

        # Separador
        ax.plot([1, 9], [y_pos + 0.5, y_pos + 0.5], 'k-', linewidth=2, zorder=3)
        y_pos -= 0.5

        # Resultado da classificacao
        resultado_box = FancyBboxPatch(
            (1, y_pos - 2.2), 8, 2,
            boxstyle="round,pad=0.1",
            edgecolor=caso['cor'],
            facecolor=caso['cor'],
            linewidth=2,
            alpha=0.3,
            zorder=2
        )
        ax.add_patch(resultado_box)

        ax.text(5, y_pos - 0.5, caso['perfil'], ha='center', va='center',
               fontsize=16, fontweight='bold', color=caso['cor'], zorder=3)
        ax.text(5, y_pos - 1.2, f'Probabilidade: {caso["prob"]}', ha='center', va='center',
               fontsize=12, fontweight='bold', zorder=3)
        ax.text(5, y_pos - 1.8, f'Score de Risco: {caso["score"]}', ha='center', va='center',
               fontsize=12, fontweight='bold', color=caso['cor'], zorder=3)

        y_pos -= 3

        # Separador
        ax.plot([1, 9], [y_pos + 0.5, y_pos + 0.5], 'k--', linewidth=1, zorder=3)
        y_pos -= 0.3

        # Analise
        ax.text(5, y_pos, 'ANALISE:', ha='center', va='center',
               fontsize=12, fontweight='bold', style='italic', zorder=3)
        y_pos -= 0.6

        for item in caso['analise']:
            ax.text(5, y_pos, f'• {item}', ha='center', va='center',
                   fontsize=10, zorder=3)
            y_pos -= 0.5

    # Legenda inferior
    fig.text(0.5, 0.02,
             'Score de Risco: 0.0-0.3 = Conservador | 0.3-0.7 = Moderado | 0.7-1.0 = Agressivo',
             ha='center', fontsize=13, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow',
                      edgecolor='black', linewidth=2))

    # Salvar
    output_file = 'grafico_casos_teste_slide.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n1. Grafico salvo: {output_file}")

    # Estatisticas
    print("\n" + "="*70)
    print("CASOS DE TESTE GERADOS:")
    print("="*70)
    for nome in nomes:
        caso = casos[nome]
        print(f"\n{nome.upper()} ({caso['idade']} anos)")
        print(f"  Perfil: {caso['perfil']} (Score: {caso['score']})")
        print(f"  Confianca: {caso['prob']}")
        print(f"  Tolerancia: {caso['tolerancia']} | Horizonte: {caso['horizonte']}")

    print("\n" + "="*70)
    print("CONCLUIDO COM SUCESSO!")
    print("="*70)
    print(f"\nArquivo gerado: {output_file}")
    print("Use este grafico no seu slide 14.3 da apresentacao!")
    print()

    plt.close()

if __name__ == "__main__":
    try:
        criar_casos_teste_visual()
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()
