"""
Script para gerar diagramas e visualizações do capítulo de DESENVOLVIMENTO
Autor: Bruna Ribeiro Cedro
Data: 2025-11-09

Este script gera diagramas arquiteturais para o capítulo 4 do TCC.

Uso:
    python gerar_graficos_desenvolvimento.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Configurações gerais
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'

def salvar_figura(fig, nome_arquivo, dpi=300):
    """Salva figura em alta resolução."""
    caminho = f'../../docs/img/{nome_arquivo}'
    fig.savefig(caminho, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"[OK] Salvo: {caminho}")
    plt.close(fig)


# ============================================
# DIAGRAMA 1: ARQUITETURA GERAL (3 CAMADAS)
# ============================================

def gerar_arquitetura_geral():
    """Diagrama de arquitetura de 3 camadas do sistema."""

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Cores
    cor_camada1 = '#E8F4F8'  # Azul claro - Dados
    cor_camada2 = '#FFF4E6'  # Laranja claro - IA
    cor_camada3 = '#E8F5E9'  # Verde claro - API
    cor_borda = '#2C3E50'

    # ========== CAMADA 1: DADOS ==========
    y_base = 9

    # Título da camada
    ax.text(5, y_base + 0.8, 'CAMADA DE DADOS',
            ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=cor_camada1,
                     edgecolor=cor_borda, linewidth=2))

    # Componentes da Camada de Dados
    box1 = FancyBboxPatch((0.5, y_base - 1.2), 2.5, 0.8,
                           boxstyle="round,pad=0.1",
                           facecolor=cor_camada1, edgecolor=cor_borda, linewidth=1.5)
    ax.add_patch(box1)
    ax.text(1.75, y_base - 0.8, 'Dataset Híbrido\n1.279 registros',
            ha='center', va='center', fontsize=9, fontweight='bold')

    box2 = FancyBboxPatch((3.5, y_base - 1.2), 2.5, 0.8,
                           boxstyle="round,pad=0.1",
                           facecolor=cor_camada1, edgecolor=cor_borda, linewidth=1.5)
    ax.add_patch(box2)
    ax.text(4.75, y_base - 0.8, 'Modelos Treinados\n(.pkl files)',
            ha='center', va='center', fontsize=9, fontweight='bold')

    box3 = FancyBboxPatch((6.5, y_base - 1.2), 2.5, 0.8,
                           boxstyle="round,pad=0.1",
                           facecolor=cor_camada1, edgecolor=cor_borda, linewidth=1.5)
    ax.add_patch(box3)
    ax.text(7.75, y_base - 0.8, 'Logs Sistema\n(RotatingFileHandler)',
            ha='center', va='center', fontsize=9, fontweight='bold')

    # ========== CAMADA 2: INTELIGÊNCIA ARTIFICIAL ==========
    y_base = 5.5

    # Título da camada
    ax.text(5, y_base + 0.8, 'CAMADA DE INTELIGÊNCIA ARTIFICIAL',
            ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=cor_camada2,
                     edgecolor=cor_borda, linewidth=2))

    # Primeira Rede Neural (Classificação)
    box_rn1 = FancyBboxPatch((0.5, y_base - 2), 4, 1.5,
                             boxstyle="round,pad=0.15",
                             facecolor=cor_camada2, edgecolor='#E67E22', linewidth=2)
    ax.add_patch(box_rn1)
    ax.text(2.5, y_base - 0.8, '1ª REDE NEURAL',
            ha='center', va='center', fontsize=11, fontweight='bold', color='#E67E22')
    ax.text(2.5, y_base - 1.25, 'Stacking Ensemble\n(7 modelos base + meta-modelo)\n→ Perfil de Risco',
            ha='center', va='center', fontsize=8)

    # Segunda Rede Neural (Alocação)
    box_rn2 = FancyBboxPatch((5.5, y_base - 2), 4, 1.5,
                             boxstyle="round,pad=0.15",
                             facecolor=cor_camada2, edgecolor='#E67E22', linewidth=2)
    ax.add_patch(box_rn2)
    ax.text(7.5, y_base - 0.8, '2ª REDE NEURAL',
            ha='center', va='center', fontsize=11, fontweight='bold', color='#E67E22')
    ax.text(7.5, y_base - 1.25, 'MLPRegressor\n(100, 50 neurônios)\n→ Alocação 6 Ativos',
            ha='center', va='center', fontsize=8)

    # Pipeline de Pré-processamento
    box_pipeline = FancyBboxPatch((1.5, y_base - 3), 7, 0.6,
                                  boxstyle="round,pad=0.1",
                                  facecolor='#FFF9E6', edgecolor=cor_borda, linewidth=1.5)
    ax.add_patch(box_pipeline)
    ax.text(5, y_base - 2.7, 'Pipeline: Feature Engineering → Normalização → Encoding → SMOTE',
            ha='center', va='center', fontsize=9, style='italic')

    # ========== CAMADA 3: API REST ==========
    y_base = 1.5

    # Título da camada
    ax.text(5, y_base + 0.8, 'CAMADA DE API REST',
            ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=cor_camada3,
                     edgecolor=cor_borda, linewidth=2))

    # Endpoints
    box_api1 = FancyBboxPatch((0.8, y_base - 1), 2, 0.7,
                              boxstyle="round,pad=0.1",
                              facecolor=cor_camada3, edgecolor='#27AE60', linewidth=1.5)
    ax.add_patch(box_api1)
    ax.text(1.8, y_base - 0.65, 'POST /classificar-perfil',
            ha='center', va='center', fontsize=8, fontweight='bold')

    box_api2 = FancyBboxPatch((3.2, y_base - 1), 2.2, 0.7,
                              boxstyle="round,pad=0.1",
                              facecolor=cor_camada3, edgecolor='#27AE60', linewidth=1.5)
    ax.add_patch(box_api2)
    ax.text(4.3, y_base - 0.65, 'POST /recomendar-portfolio',
            ha='center', va='center', fontsize=8, fontweight='bold')

    box_api3 = FancyBboxPatch((5.8, y_base - 1), 1.6, 0.7,
                              boxstyle="round,pad=0.1",
                              facecolor=cor_camada3, edgecolor='#27AE60', linewidth=1.5)
    ax.add_patch(box_api3)
    ax.text(6.6, y_base - 0.65, 'GET /info-sistema',
            ha='center', va='center', fontsize=8, fontweight='bold')

    box_api4 = FancyBboxPatch((7.8, y_base - 1), 1.4, 0.7,
                              boxstyle="round,pad=0.1",
                              facecolor=cor_camada3, edgecolor='#27AE60', linewidth=1.5)
    ax.add_patch(box_api4)
    ax.text(8.5, y_base - 0.65, 'Swagger UI',
            ha='center', va='center', fontsize=8, fontweight='bold')

    # ========== SETAS DE FLUXO ==========

    # Dados → IA
    arrow1 = FancyArrowPatch((1.75, 7.5), (2.5, 6.8),
                            arrowstyle='->', mutation_scale=20,
                            linewidth=2, color='#34495E')
    ax.add_patch(arrow1)

    arrow2 = FancyArrowPatch((4.75, 7.5), (5, 6.8),
                            arrowstyle='->', mutation_scale=20,
                            linewidth=2, color='#34495E')
    ax.add_patch(arrow2)

    # IA → API
    arrow3 = FancyArrowPatch((2.5, 3.3), (1.8, 2.5),
                            arrowstyle='->', mutation_scale=20,
                            linewidth=2, color='#34495E')
    ax.add_patch(arrow3)

    arrow4 = FancyArrowPatch((7.5, 3.3), (4.3, 2.5),
                            arrowstyle='->', mutation_scale=20,
                            linewidth=2, color='#34495E')
    ax.add_patch(arrow4)

    # Feedback API → Logs
    arrow5 = FancyArrowPatch((6.6, 2.2), (7.75, 7.5),
                            arrowstyle='->', mutation_scale=15,
                            linewidth=1.5, color='#95A5A6', linestyle='dashed')
    ax.add_patch(arrow5)
    ax.text(7.3, 4.5, 'Logs', ha='center', fontsize=8,
            style='italic', color='#7F8C8D', rotation=70)

    # Título geral
    ax.text(5, 11.3, 'Arquitetura Modular do Sistema Investe-AI',
            ha='center', va='center', fontsize=16, fontweight='bold')

    salvar_figura(fig, 'arquitetura_geral.png')


# ============================================
# DIAGRAMA 2: STACKING ENSEMBLE ARCHITECTURE
# ============================================

def gerar_stacking_architecture():
    """Diagrama detalhado da arquitetura Stacking Ensemble."""

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Cores
    cor_input = '#E3F2FD'
    cor_base = '#FFF3E0'
    cor_meta = '#E8F5E9'
    cor_output = '#F3E5F5'
    cor_borda = '#37474F'

    # ========== ENTRADA (NÍVEL 0) ==========
    y_nivel0 = 9

    box_input = FancyBboxPatch((4, y_nivel0), 6, 1.2,
                               boxstyle="round,pad=0.15",
                               facecolor=cor_input, edgecolor=cor_borda, linewidth=2)
    ax.add_patch(box_input)
    ax.text(7, y_nivel0 + 0.85, 'ENTRADA',
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(7, y_nivel0 + 0.4, '26 Features (15 originais + 11 derivadas)',
            ha='center', va='center', fontsize=10)

    # ========== MODELOS BASE (NÍVEL 1) ==========
    y_nivel1 = 5.8

    ax.text(7, y_nivel1 + 1.8, 'NÍVEL 1: MODELOS BASE (7 estimadores)',
            ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=cor_base,
                     edgecolor=cor_borda, linewidth=1.5))

    modelos_base = [
        'MLP 1\n(100, 50)',
        'MLP 2\n(50, 25)',
        'Random\nForest',
        'Gradient\nBoosting',
        'XGBoost',
        'LightGBM',
        'Extra\nTrees'
    ]

    x_start = 0.8
    box_width = 1.7
    spacing = 0.2

    for i, modelo in enumerate(modelos_base):
        x_pos = x_start + i * (box_width + spacing)

        box = FancyBboxPatch((x_pos, y_nivel1), box_width, 1.2,
                             boxstyle="round,pad=0.1",
                             facecolor=cor_base, edgecolor='#FF9800', linewidth=2)
        ax.add_patch(box)
        ax.text(x_pos + box_width/2, y_nivel1 + 0.6, modelo,
                ha='center', va='center', fontsize=8, fontweight='bold')

        # Seta da entrada para cada modelo base
        arrow = FancyArrowPatch((7, y_nivel0 - 0.1),
                               (x_pos + box_width/2, y_nivel1 + 1.3),
                               arrowstyle='->', mutation_scale=15,
                               linewidth=1.5, color='#546E7A', alpha=0.7)
        ax.add_patch(arrow)

    # ========== PREDIÇÕES DOS MODELOS BASE ==========
    y_pred_base = 4.5

    box_pred = FancyBboxPatch((3, y_pred_base), 8, 0.7,
                              boxstyle="round,pad=0.1",
                              facecolor='#FFF9C4', edgecolor=cor_borda, linewidth=1.5)
    ax.add_patch(box_pred)
    ax.text(7, y_pred_base + 0.35, 'Predições dos 7 Modelos Base (predict_proba)',
            ha='center', va='center', fontsize=10, style='italic')

    # Setas dos modelos base para predições
    for i in range(7):
        x_pos = x_start + i * (box_width + spacing) + box_width/2
        arrow = FancyArrowPatch((x_pos, y_nivel1 - 0.1),
                               (x_pos, y_pred_base + 0.8),
                               arrowstyle='->', mutation_scale=12,
                               linewidth=1.2, color='#FF9800', alpha=0.8)
        ax.add_patch(arrow)

    # ========== META-MODELO (NÍVEL 2) ==========
    y_nivel2 = 2.5

    ax.text(7, y_nivel2 + 1.3, 'NÍVEL 2: META-MODELO',
            ha='center', va='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=cor_meta,
                     edgecolor=cor_borda, linewidth=1.5))

    box_meta = FancyBboxPatch((4.5, y_nivel2), 5, 1,
                              boxstyle="round,pad=0.15",
                              facecolor=cor_meta, edgecolor='#4CAF50', linewidth=2.5)
    ax.add_patch(box_meta)
    ax.text(7, y_nivel2 + 0.7, 'Logistic Regression',
            ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(7, y_nivel2 + 0.3, '(multi_class=multinomial, solver=lbfgs)',
            ha='center', va='center', fontsize=9)

    # Seta das predições para meta-modelo
    arrow_meta = FancyArrowPatch((7, y_pred_base - 0.1),
                                 (7, y_nivel2 + 1.1),
                                 arrowstyle='->', mutation_scale=20,
                                 linewidth=2.5, color='#388E3C')
    ax.add_patch(arrow_meta)

    # ========== SAÍDA FINAL ==========
    y_output = 0.5

    box_output = FancyBboxPatch((4, y_output), 6, 1.2,
                                boxstyle="round,pad=0.15",
                                facecolor=cor_output, edgecolor=cor_borda, linewidth=2)
    ax.add_patch(box_output)
    ax.text(7, y_output + 0.85, 'SAÍDA FINAL',
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(7, y_output + 0.4, 'Perfil de Risco: Conservador | Moderado | Agressivo',
            ha='center', va='center', fontsize=10)

    # Seta do meta-modelo para saída
    arrow_output = FancyArrowPatch((7, y_nivel2 - 0.1),
                                   (7, y_output + 1.3),
                                   arrowstyle='->', mutation_scale=20,
                                   linewidth=2.5, color='#7B1FA2')
    ax.add_patch(arrow_output)

    # ========== ANOTAÇÕES LATERAIS ==========

    # Cross-validation
    ax.text(0.3, y_nivel1 + 0.6, 'CV=5\nfolds',
            ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFECB3',
                     edgecolor='#F57C00', linewidth=1.5))

    # Stack method
    ax.text(13.2, y_pred_base + 0.35, 'stack_method:\npredict_proba',
            ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#C8E6C9',
                     edgecolor='#388E3C', linewidth=1.5))

    # Título
    ax.text(7, 10.5, 'Arquitetura Stacking Ensemble - Primeira Rede Neural',
            ha='center', va='center', fontsize=16, fontweight='bold')

    salvar_figura(fig, 'stacking_architecture.png')


# ============================================
# MAIN
# ============================================

def main():
    print("\n" + "=" * 60)
    print("GERANDO DIAGRAMAS DO CAPITULO DE DESENVOLVIMENTO")
    print("=" * 60)

    try:
        print("\n[1/2] Gerando: Arquitetura Geral (3 camadas)...")
        gerar_arquitetura_geral()

        print("\n[2/2] Gerando: Stacking Ensemble Architecture...")
        gerar_stacking_architecture()

        print("\n" + "=" * 60)
        print("[SUCESSO] TODOS OS DIAGRAMAS FORAM GERADOS!")
        print("=" * 60)
        print("\nArquivos salvos em: docs/img/")
        print("  - arquitetura_geral.png")
        print("  - stacking_architecture.png")

    except Exception as e:
        print(f"\n[ERRO]: {e}")
        print("\nVerifique se:")
        print("  1. O diretorio docs/img/ existe")
        print("  2. Voce tem permissoes de escrita")


if __name__ == "__main__":
    main()
