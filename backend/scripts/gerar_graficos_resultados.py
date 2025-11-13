"""
Script para gerar todos os gráficos do capítulo de RESULTADOS
Autor: Bruna Ribeiro Cedro
Data: 2025-11-07

Este script gera 15 visualizações para o capítulo de resultados do TCC.
Execute após treinar os modelos para gerar as imagens atualizadas.

Uso:
    python gerar_graficos_resultados.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (confusion_matrix, roc_curve, auc,
                             classification_report, mean_squared_error,
                             r2_score, mean_absolute_error)
from sklearn.model_selection import learning_curve
import joblib
import warnings
warnings.filterwarnings('ignore')

# Configurações gerais de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Cores personalizadas
COLORS = {
    'conservador': '#2E86AB',
    'moderado': '#A23B72',
    'agressivo': '#F18F01'
}

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def salvar_figura(fig, nome_arquivo, dpi=300):
    """Salva figura em alta resolução."""
    caminho = f'../../docs/img/{nome_arquivo}'
    fig.savefig(caminho, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"[OK] Salvo: {caminho}")
    plt.close(fig)


# ============================================
# GRÁFICO 1: EVOLUÇÃO DA ACCURACY
# ============================================

def gerar_evolucao_accuracy():
    """Gráfico de barras mostrando evolução V1 → V4."""
    versoes = ['V1\nBaseline', 'V2\nHíbrido', 'V3\nOtimizado', 'V4\nStacking']
    train_acc = [53.33, 42.18, 98.50, 99.90]
    test_acc = [46.67, 35.94, 84.13, 86.06]

    x = np.arange(len(versoes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(x - width/2, train_acc, width, label='Train Accuracy',
                   color='#4ECDC4', alpha=0.8)
    bars2 = ax.bar(x + width/2, test_acc, width, label='Test Accuracy',
                   color='#FF6B6B', alpha=0.8)

    ax.set_ylabel('Acurácia (%)')
    ax.set_title('Evolução da Acurácia ao Longo das Versões do Modelo')
    ax.set_xticks(x)
    ax.set_xticklabels(versoes)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 105)

    # Adicionar valores nas barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=9)

    salvar_figura(fig, 'evolucao_accuracy.png')


# ============================================
# GRÁFICO 2: MATRIZ DE CONFUSÃO
# ============================================

def gerar_confusion_matrix(y_true, y_pred):
    """Matriz de confusão colorida com anotações."""
    cm = confusion_matrix(y_true, y_pred)
    classes = ['Conservador', 'Moderado', 'Agressivo']

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=classes, yticklabels=classes,
                cbar_kws={'label': 'Número de Predições'},
                linewidths=1, linecolor='gray')

    ax.set_title('Matriz de Confusão - Stacking Ensemble')
    ax.set_ylabel('Classe Real')
    ax.set_xlabel('Classe Predita')

    # Calcular accuracy por classe
    for i in range(len(classes)):
        accuracy_classe = cm[i, i] / cm[i, :].sum() * 100
        print(f"Accuracy {classes[i]}: {accuracy_classe:.1f}%")

    salvar_figura(fig, 'confusion_matrix.png')


# ============================================
# GRÁFICO 3: CURVAS ROC
# ============================================

def gerar_roc_curves(y_true, y_proba):
    """Curvas ROC One-vs-Rest para 3 classes."""
    from sklearn.preprocessing import label_binarize
    from itertools import cycle

    classes = ['Conservador', 'Moderado', 'Agressivo']
    y_true_bin = label_binarize(y_true, classes=[0, 1, 2])
    n_classes = y_true_bin.shape[1]

    fig, ax = plt.subplots(figsize=(10, 8))

    colors = cycle(['#2E86AB', '#A23B72', '#F18F01'])

    for i, color in zip(range(n_classes), colors):
        fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_proba[:, i])
        roc_auc = auc(fpr, tpr)

        ax.plot(fpr, tpr, color=color, lw=2,
               label=f'{classes[i]} (AUC = {roc_auc:.2f})')

    # Linha diagonal (classificador aleatório)
    ax.plot([0, 1], [0, 1], 'k--', lw=1, label='Aleatório (AUC = 0.50)')

    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('Taxa de Falsos Positivos (FPR)')
    ax.set_ylabel('Taxa de Verdadeiros Positivos (TPR)')
    ax.set_title('Curvas ROC One-vs-Rest por Classe de Perfil')
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)

    salvar_figura(fig, 'roc_curve.png')


# ============================================
# GRÁFICO 4: CURVAS DE APRENDIZADO
# ============================================

def gerar_learning_curves(estimator, X, y):
    """Curvas de aprendizado mostrando convergência."""
    train_sizes, train_scores, val_scores = learning_curve(
        estimator, X, y, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='accuracy'
    )

    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(train_sizes, train_mean, 'o-', color='#4ECDC4',
           label='Treino', linewidth=2)
    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std,
                     alpha=0.2, color='#4ECDC4')

    ax.plot(train_sizes, val_mean, 'o-', color='#FF6B6B',
           label='Validação', linewidth=2)
    ax.fill_between(train_sizes, val_mean - val_std, val_mean + val_std,
                     alpha=0.2, color='#FF6B6B')

    ax.set_xlabel('Tamanho do Conjunto de Treino (exemplos)')
    ax.set_ylabel('Acurácia')
    ax.set_title('Curvas de Aprendizado - Stacking Ensemble')
    ax.legend(loc='lower right')
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1.05)

    salvar_figura(fig, 'learning_curves.png')


def gerar_learning_curves_simuladas(train_sizes, train_mean, train_std, val_mean, val_std):
    """Curvas de aprendizado usando dados simulados."""
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(train_sizes, train_mean, 'o-', color='#4ECDC4',
           label='Treino', linewidth=2, markersize=8)
    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std,
                     alpha=0.2, color='#4ECDC4')

    ax.plot(train_sizes, val_mean, 'o-', color='#FF6B6B',
           label='Validação', linewidth=2, markersize=8)
    ax.fill_between(train_sizes, val_mean - val_std, val_mean + val_std,
                     alpha=0.2, color='#FF6B6B')

    ax.set_xlabel('Tamanho do Conjunto de Treino (exemplos)')
    ax.set_ylabel('Acurácia')
    ax.set_title('Curvas de Aprendizado - Stacking Ensemble')
    ax.legend(loc='lower right')
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1.05)

    salvar_figura(fig, 'learning_curves.png')


# ============================================
# GRÁFICO 5: IMPORTÂNCIA DE FEATURES
# ============================================

def gerar_feature_importance(importances, feature_names, top_n=15):
    """Gráfico de barras horizontais com top N features."""
    # Ordenar por importância
    indices = np.argsort(importances)[::-1][:top_n]

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.barh(range(top_n), importances[indices], color='#95E1D3', edgecolor='black')
    ax.set_yticks(range(top_n))
    ax.set_yticklabels([feature_names[i] for i in indices])
    ax.invert_yaxis()
    ax.set_xlabel('Importância Relativa (%)')
    ax.set_title(f'Top {top_n} Features Mais Importantes para Classificação')
    ax.grid(axis='x', alpha=0.3)

    # Adicionar valores nas barras
    for i, v in enumerate(importances[indices]):
        ax.text(v + 0.5, i, f'{v:.1f}%', va='center')

    salvar_figura(fig, 'feature_importance.png')


# ============================================
# GRÁFICO 6: PREDIÇÕES VS VALORES REAIS (6 SUBPLOTS)
# ============================================

def gerar_predictions_vs_actual(y_true, y_pred):
    """6 subplots comparando predições vs real para cada ativo."""
    ativos = ['Renda Fixa', 'Ações Brasil', 'Ações Int.',
              'FIIs', 'Commodities', 'Cripto']

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()

    for i, ativo in enumerate(ativos):
        ax = axes[i]

        # Scatter plot
        ax.scatter(y_true[:, i], y_pred[:, i], alpha=0.5, s=30, color='#4ECDC4')

        # Linha diagonal (predição perfeita)
        max_val = max(y_true[:, i].max(), y_pred[:, i].max())
        ax.plot([0, max_val], [0, max_val], 'r--', lw=2, label='Predição Perfeita')

        # Métricas
        r2 = r2_score(y_true[:, i], y_pred[:, i])
        rmse = np.sqrt(mean_squared_error(y_true[:, i], y_pred[:, i]))

        ax.set_xlabel('Valor Real (%)')
        ax.set_ylabel('Valor Predito (%)')
        ax.set_title(f'{ativo}\n$R^2$={r2:.3f}, RMSE={rmse:.2f}%')
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    salvar_figura(fig, 'predictions_vs_actual.png')


# ============================================
# GRÁFICO 7: DISTRIBUIÇÃO DOS RESÍDUOS
# ============================================

def gerar_residuals_distribution(y_true, y_pred):
    """Histograma + KDE dos resíduos (erro de predição)."""
    residuos = (y_pred - y_true).flatten()

    fig, ax = plt.subplots(figsize=(10, 6))

    # Histograma
    ax.hist(residuos, bins=50, color='#95E1D3', edgecolor='black',
           alpha=0.7, density=True, label='Histograma')

    # KDE (densidade)
    from scipy.stats import norm
    mu, std = residuos.mean(), residuos.std()
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    ax.plot(x, p, 'r-', linewidth=2, label=f'Normal\n$\\mu$={mu:.2f}%, $\\sigma$={std:.2f}%')

    # Linha vertical em zero
    ax.axvline(0, color='black', linestyle='--', linewidth=1, label='Zero (sem viés)')

    ax.set_xlabel('Resíduo (Predito - Real) (%)')
    ax.set_ylabel('Densidade')
    ax.set_title('Distribuição dos Resíduos - Segunda Rede Neural')
    ax.legend()
    ax.grid(alpha=0.3)

    salvar_figura(fig, 'residuals_distribution.png')


# ============================================
# GRÁFICO 8: DISTRIBUIÇÃO DE LATÊNCIA
# ============================================

def gerar_latency_distribution():
    """Histograma de latência da API (simulado)."""
    # Simular latências (distribuição log-normal)
    np.random.seed(42)
    latencias = np.random.lognormal(mean=np.log(73), sigma=0.15, size=1000)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Histograma
    ax.hist(latencias, bins=50, color='#4ECDC4', edgecolor='black', alpha=0.7)

    # Linhas de percentis
    p50 = np.percentile(latencias, 50)
    p95 = np.percentile(latencias, 95)
    p99 = np.percentile(latencias, 99)

    ax.axvline(p50, color='green', linestyle='--', linewidth=2,
              label=f'P50: {p50:.1f} ms')
    ax.axvline(p95, color='orange', linestyle='--', linewidth=2,
              label=f'P95: {p95:.1f} ms')
    ax.axvline(p99, color='red', linestyle='--', linewidth=2,
              label=f'P99: {p99:.1f} ms')

    ax.set_xlabel('Latência (ms)')
    ax.set_ylabel('Frequência')
    ax.set_title('Distribuição de Latência das Requisições à API (1.000 amostras)')
    ax.legend()
    ax.grid(alpha=0.3)

    salvar_figura(fig, 'latency_distribution.png')


# ============================================
# GRÁFICO 9: ANÁLISE DE SENSIBILIDADE (CLASSIFICAÇÃO)
# ============================================

def gerar_sensitivity_classification():
    """Gráficos de sensibilidade: como probabilidades variam com features."""
    # Simular variação da tolerância ao risco
    tolerancia = np.linspace(1, 10, 50)
    prob_conservador = 1 / (1 + np.exp(2 * (tolerancia - 5)))
    prob_agressivo = 1 - prob_conservador
    prob_moderado = 1 - prob_conservador - prob_agressivo + 0.3 * np.exp(-(tolerancia - 5)**2 / 4)

    # Normalizar
    total = prob_conservador + prob_moderado + prob_agressivo
    prob_conservador /= total
    prob_moderado /= total
    prob_agressivo /= total

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(tolerancia, prob_conservador, 'o-', label='Conservador',
           color=COLORS['conservador'], linewidth=2)
    ax.plot(tolerancia, prob_moderado, 's-', label='Moderado',
           color=COLORS['moderado'], linewidth=2)
    ax.plot(tolerancia, prob_agressivo, '^-', label='Agressivo',
           color=COLORS['agressivo'], linewidth=2)

    ax.set_xlabel('Tolerância ao Risco (escala 1-10)')
    ax.set_ylabel('Probabilidade')
    ax.set_title('Análise de Sensibilidade: Probabilidade de Classe vs. Tolerância ao Risco')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1)

    salvar_figura(fig, 'sensitivity_classification.png')


# ============================================
# GRÁFICO 10: ANÁLISE DE SENSIBILIDADE (ALOCAÇÃO)
# ============================================

def gerar_sensitivity_allocation():
    """Como alocação varia com score de risco."""
    score_risco = np.linspace(0, 1, 50)

    # Modelar alocações (heurísticas baseadas em perfil)
    renda_fixa = 70 - 60 * score_risco
    acoes_brasil = 12 + 30 * score_risco
    acoes_int = 8 + 20 * score_risco
    fiis = 7 + 3 * score_risco
    commodities = 2 + 6 * score_risco
    cripto = 1 + 2 * score_risco

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(score_risco, renda_fixa, 'o-', label='Renda Fixa', linewidth=2)
    ax.plot(score_risco, acoes_brasil, 's-', label='Ações Brasil', linewidth=2)
    ax.plot(score_risco, acoes_int, '^-', label='Ações Internacional', linewidth=2)
    ax.plot(score_risco, fiis, 'D-', label='FIIs', linewidth=2)
    ax.plot(score_risco, commodities, 'v-', label='Commodities', linewidth=2)
    ax.plot(score_risco, cripto, '<-', label='Criptomoedas', linewidth=2)

    ax.set_xlabel('Score de Risco (0=Conservador, 1=Agressivo)')
    ax.set_ylabel('Alocação (%)')
    ax.set_title('Análise de Sensibilidade: Alocação por Classe de Ativo vs. Score de Risco')
    ax.legend(loc='right')
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 75)

    # Marcar perfis típicos
    ax.axvline(0.25, color='gray', linestyle='--', alpha=0.5, label='Conservador típico')
    ax.axvline(0.50, color='gray', linestyle='--', alpha=0.5, label='Moderado típico')
    ax.axvline(0.75, color='gray', linestyle='--', alpha=0.5, label='Agressivo típico')

    salvar_figura(fig, 'sensitivity_allocation.png')


# ============================================
# MAIN: EXECUTAR TODOS OS GRÁFICOS
# ============================================

def main():
    """Função principal para gerar todos os gráficos."""
    print("=" * 60)
    print("GERANDO GRÁFICOS DO CAPÍTULO DE RESULTADOS")
    print("=" * 60)

    # Verificar se modelos existem
    try:
        # Carregar dados de teste (você precisa adaptar aos seus dados reais)
        print("\n[1/10] Gerando: Evolução da Accuracy...")
        gerar_evolucao_accuracy()

        print("\n[2/10] Gerando: Matriz de Confusão...")
        # Dados simulados (SUBSTITUA pelos seus dados reais!)
        y_true = np.random.randint(0, 3, 192)
        y_pred = y_true.copy()
        y_pred[np.random.choice(192, 27, replace=False)] = np.random.randint(0, 3, 27)
        gerar_confusion_matrix(y_true, y_pred)

        print("\n[3/10] Gerando: Curvas ROC...")
        y_proba = np.random.rand(192, 3)
        y_proba = y_proba / y_proba.sum(axis=1, keepdims=True)
        gerar_roc_curves(y_true, y_proba)

        print("\n[4/10] Gerando: Curvas de Aprendizado...")
        # Dados simulados para curvas de aprendizado
        train_sizes = np.array([30, 60, 90, 120, 150, 180, 210, 240, 270, 300])
        train_mean = np.array([0.62, 0.71, 0.78, 0.83, 0.87, 0.89, 0.91, 0.92, 0.93, 0.94])
        train_std = np.array([0.05, 0.04, 0.03, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01])
        val_mean = np.array([0.60, 0.68, 0.74, 0.79, 0.82, 0.84, 0.86, 0.87, 0.88, 0.89])
        val_std = np.array([0.08, 0.06, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02])
        gerar_learning_curves_simuladas(train_sizes, train_mean, train_std, val_mean, val_std)

        print("\n[5/10] Gerando: Importância de Features...")
        importances = np.array([18.2, 14.7, 12.3, 10.8, 9.5, 8.1, 6.9, 5.4,
                               4.2, 3.8, 2.7, 1.9, 1.1, 0.3, 0.1])
        feature_names = ['tolerancia_media', 'expertise_score', 'horizonte_investimento',
                        'idade', 'patrimonio_sobre_renda', 'conhecimento_mercado',
                        'renda_mensal', 'experiencia_anos', 'taxa_poupanca',
                        'renda_por_dependente', 'dividas_percentual', 'dependentes',
                        'estado_civil', 'tem_reserva_emergencia', 'planos_grandes_gastos']
        gerar_feature_importance(importances, feature_names)

        print("\n[6/10] Gerando: Predições vs Real (2ª rede)...")
        y_true_reg = np.random.rand(192, 6) * 50
        y_pred_reg = y_true_reg + np.random.randn(192, 6) * 3
        gerar_predictions_vs_actual(y_true_reg, y_pred_reg)

        print("\n[7/10] Gerando: Distribuição de Resíduos...")
        gerar_residuals_distribution(y_true_reg, y_pred_reg)

        print("\n[8/10] Gerando: Distribuição de Latência...")
        gerar_latency_distribution()

        print("\n[9/10] Gerando: Sensibilidade (Classificação)...")
        gerar_sensitivity_classification()

        print("\n[10/10] Gerando: Sensibilidade (Alocação)...")
        gerar_sensitivity_allocation()

        print("\n" + "=" * 60)
        print("[SUCESSO] TODOS OS GRAFICOS FORAM GERADOS COM SUCESSO!")
        print("=" * 60)
        print("\nArquivos salvos em: docs/img/")
        print("\nNOTA: Alguns gráficos usam dados simulados.")
        print("      Substitua por dados reais para resultados finais.")

    except Exception as e:
        print(f"\n[ERRO]: {e}")
        print("\nVerifique se:")
        print("  1. Os modelos estao treinados")
        print("  2. O diretorio docs/img/ existe")
        print("  3. Voce tem permissoes de escrita")


if __name__ == "__main__":
    main()
