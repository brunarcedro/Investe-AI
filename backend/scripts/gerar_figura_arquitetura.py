"""
Script para gerar Figura 4 - Arquitetura Geral do Sistema Investe-AI
Mostra as 3 camadas principais: Dados, Inteligência Artificial e API REST
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Configurações de estilo
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.unicode_minus'] = False

# Cores do sistema
COR_DADOS = '#E8F4F8'
COR_IA = '#FFF4E6'
COR_API = '#F0F8E8'
COR_FRONTEND = '#F5F0FF'
COR_BORDA = '#2C3E50'
COR_TEXTO = '#2C3E50'
COR_SETA = '#34495E'

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Título
ax.text(7, 9.5, 'Arquitetura Geral do Sistema Investe-AI',
        ha='center', va='top', fontsize=16, fontweight='bold', color=COR_TEXTO)

# =============================================================================
# CAMADA 1: DADOS (Topo)
# =============================================================================
y_dados = 7.5

# Box principal da camada de dados
dados_box = FancyBboxPatch((0.5, y_dados), 13, 1.5,
                           boxstyle="round,pad=0.1",
                           edgecolor=COR_BORDA, facecolor=COR_DADOS,
                           linewidth=2.5, zorder=1)
ax.add_patch(dados_box)

ax.text(7, y_dados + 1.2, 'CAMADA DE DADOS',
        ha='center', va='center', fontsize=12, fontweight='bold', color=COR_TEXTO)

# Datasets
datasets = [
    ('Dataset\nEspecialista\n(430 amostras)', 1.5),
    ('Dataset SCF\n(Survey of Consumer\nFinances)', 4.5),
    ('Dataset\nHíbrido\n(1.000 amostras)', 7.5),
    ('Dataset Sintético\nPortfólio\n(5.000 amostras)', 10.5)
]

for nome, x in datasets:
    box = FancyBboxPatch((x-0.7, y_dados+0.15), 1.4, 0.9,
                         boxstyle="round,pad=0.05",
                         edgecolor=COR_BORDA, facecolor='white',
                         linewidth=1.5, zorder=2)
    ax.add_patch(box)
    ax.text(x, y_dados+0.6, nome, ha='center', va='center',
            fontsize=8, color=COR_TEXTO, multialignment='center')

# =============================================================================
# CAMADA 2: INTELIGÊNCIA ARTIFICIAL (Meio)
# =============================================================================
y_ia = 3.5

# Box principal da camada de IA
ia_box = FancyBboxPatch((0.5, y_ia), 13, 3.5,
                        boxstyle="round,pad=0.1",
                        edgecolor=COR_BORDA, facecolor=COR_IA,
                        linewidth=2.5, zorder=1)
ax.add_patch(ia_box)

ax.text(7, y_ia + 3.2, 'CAMADA DE INTELIGÊNCIA ARTIFICIAL',
        ha='center', va='center', fontsize=12, fontweight='bold', color=COR_TEXTO)

# === REDE NEURAL 1: Classificação de Perfil de Risco ===
rede1_x = 3.5
rede1_y = y_ia + 0.3

# Box da Rede 1
rede1_box = FancyBboxPatch((rede1_x-2.2, rede1_y), 4.4, 2.5,
                           boxstyle="round,pad=0.08",
                           edgecolor='#E74C3C', facecolor='#FADBD8',
                           linewidth=2, zorder=2)
ax.add_patch(rede1_box)

ax.text(rede1_x, rede1_y + 2.2, 'Rede Neural 1: Classificação de Perfil',
        ha='center', va='center', fontsize=10, fontweight='bold', color='#C0392B')

# Características da Rede 1
rede1_info = [
    'Tipo: Voting Classifier Ensemble',
    'Modelos: Random Forest + MLP + SVM',
    'Features: 8 atributos do investidor',
    'Output: 5 classes de perfil de risco',
    'Acurácia: ~88%'
]

for i, info in enumerate(rede1_info):
    ax.text(rede1_x, rede1_y + 1.7 - i*0.35, info,
            ha='center', va='center', fontsize=8, color=COR_TEXTO)

# === REDE NEURAL 2: Alocação de Portfólio ===
rede2_x = 10.5
rede2_y = y_ia + 0.3

# Box da Rede 2
rede2_box = FancyBboxPatch((rede2_x-2.2, rede2_y), 4.4, 2.5,
                           boxstyle="round,pad=0.08",
                           edgecolor='#3498DB', facecolor='#D6EAF8',
                           linewidth=2, zorder=2)
ax.add_patch(rede2_box)

ax.text(rede2_x, rede2_y + 2.2, 'Rede Neural 2: Alocação de Portfólio',
        ha='center', va='center', fontsize=10, fontweight='bold', color='#2874A6')

# Características da Rede 2
rede2_info = [
    'Tipo: Ensemble de 5 Modelos',
    'Modelos: 2 MLP + RF + GB + ET',
    'Features: 27 (com feature engineering)',
    'Output: 6 classes de ativos (%)',
    'R² Score: ~82%'
]

for i, info in enumerate(rede2_info):
    ax.text(rede2_x, rede2_y + 1.7 - i*0.35, info,
            ha='center', va='center', fontsize=8, color=COR_TEXTO)

# =============================================================================
# CAMADA 3: API REST (Inferior)
# =============================================================================
y_api = 1.5

# Box principal da camada de API
api_box = FancyBboxPatch((0.5, y_api), 13, 1.5,
                         boxstyle="round,pad=0.1",
                         edgecolor=COR_BORDA, facecolor=COR_API,
                         linewidth=2.5, zorder=1)
ax.add_patch(api_box)

ax.text(7, y_api + 1.2, 'CAMADA DE API REST (FastAPI)',
        ha='center', va='center', fontsize=12, fontweight='bold', color=COR_TEXTO)

# Endpoints
endpoints = [
    ('/predict\nClassificação\nde Perfil', 2.5),
    ('/allocate\nAlocação de\nPortfólio', 5.5),
    ('/simulate\nSimulação de\nBacktesting', 8.5),
    ('/optimize\nOtimização\nMonte Carlo', 11.5)
]

for nome, x in endpoints:
    box = FancyBboxPatch((x-0.9, y_api+0.15), 1.8, 0.9,
                         boxstyle="round,pad=0.05",
                         edgecolor=COR_BORDA, facecolor='white',
                         linewidth=1.5, zorder=2)
    ax.add_patch(box)
    ax.text(x, y_api+0.6, nome, ha='center', va='center',
            fontsize=7.5, color=COR_TEXTO, multialignment='center')

# =============================================================================
# CAMADA 4: FRONTEND (Inferior)
# =============================================================================
y_frontend = 0.2

# Box do frontend
frontend_box = FancyBboxPatch((0.5, y_frontend), 13, 0.9,
                              boxstyle="round,pad=0.08",
                              edgecolor=COR_BORDA, facecolor=COR_FRONTEND,
                              linewidth=2.5, zorder=1)
ax.add_patch(frontend_box)

ax.text(7, y_frontend + 0.45, 'INTERFACE WEB (React + Vite + TailwindCSS)',
        ha='center', va='center', fontsize=11, fontweight='bold', color=COR_TEXTO)

# =============================================================================
# SETAS DE FLUXO
# =============================================================================

# Setas dos dados para as redes neurais
# Dataset Especialista + SCF + Híbrido -> Rede 1
arrow1 = FancyArrowPatch((4.5, y_dados), (rede1_x, rede1_y + 2.5),
                        arrowstyle='->', mutation_scale=20,
                        linewidth=2, color=COR_SETA, zorder=3)
ax.add_patch(arrow1)

# Dataset Sintético -> Rede 2
arrow2 = FancyArrowPatch((10.5, y_dados), (rede2_x, rede2_y + 2.5),
                        arrowstyle='->', mutation_scale=20,
                        linewidth=2, color=COR_SETA, zorder=3)
ax.add_patch(arrow2)

# Setas das redes neurais para a API
arrow3 = FancyArrowPatch((rede1_x, rede1_y), (3.5, y_api + 1.5),
                        arrowstyle='->', mutation_scale=20,
                        linewidth=2, color=COR_SETA, zorder=3)
ax.add_patch(arrow3)

arrow4 = FancyArrowPatch((rede2_x, rede2_y), (9.5, y_api + 1.5),
                        arrowstyle='->', mutation_scale=20,
                        linewidth=2, color=COR_SETA, zorder=3)
ax.add_patch(arrow4)

# Seta da API para o Frontend
arrow5 = FancyArrowPatch((7, y_api), (7, y_frontend + 0.9),
                        arrowstyle='<->', mutation_scale=20,
                        linewidth=2.5, color=COR_SETA, zorder=3)
ax.add_patch(arrow5)

# Labels nas setas
ax.text(3.2, y_dados - 0.6, 'Treino', ha='center', va='center',
        fontsize=8, color=COR_SETA, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COR_SETA, linewidth=1))

ax.text(11, y_dados - 0.6, 'Treino', ha='center', va='center',
        fontsize=8, color=COR_SETA, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COR_SETA, linewidth=1))

ax.text(2.2, (rede1_y + y_api + 1.5) / 2, 'Predição', ha='center', va='center',
        fontsize=8, color=COR_SETA, style='italic', rotation=75,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COR_SETA, linewidth=1))

ax.text(10.8, (rede2_y + y_api + 1.5) / 2, 'Alocação', ha='center', va='center',
        fontsize=8, color=COR_SETA, style='italic', rotation=-75,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COR_SETA, linewidth=1))

ax.text(7.6, (y_api + y_frontend + 0.9) / 2, 'HTTP/JSON', ha='center', va='center',
        fontsize=8, color=COR_SETA, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COR_SETA, linewidth=1))

# Legenda informativa no canto
legend_items = [
    'Pipeline de dados → Modelos de IA → API → Interface Web',
    'Ensemble de modelos para maior precisão e robustez',
    'Feature Engineering para otimização das redes neurais'
]

y_legend = 0.5
for i, item in enumerate(legend_items):
    ax.text(0.7, y_legend - i*0.2, f'• {item}',
            ha='left', va='top', fontsize=7.5, color='#555', style='italic')

# Salvar figura
plt.tight_layout()
plt.savefig('docs/figuras/figura_04_arquitetura_sistema.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("[OK] Figura 4 salva: docs/figuras/figura_04_arquitetura_sistema.png")

plt.savefig('docs/figuras/figura_04_arquitetura_sistema.pdf',
            bbox_inches='tight', facecolor='white')
print("[OK] Figura 4 salva: docs/figuras/figura_04_arquitetura_sistema.pdf")

plt.close()

print("\n" + "="*70)
print("FIGURA 4 - ARQUITETURA GERAL DO SISTEMA")
print("="*70)
print("[OK] Camada de Dados: 4 datasets diferentes")
print("[OK] Camada de IA: 2 redes neurais ensemble")
print("  - Rede 1: Classificacao de perfil (Voting Classifier)")
print("  - Rede 2: Alocacao de portfolio (Ensemble 5 modelos)")
print("[OK] Camada de API: FastAPI com 4 endpoints principais")
print("[OK] Frontend: React + Vite + TailwindCSS")
print("="*70)
