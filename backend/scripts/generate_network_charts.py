"""
Gerador de Gráficos e Métricas - PRIMEIRA REDE NEURAL
Com dados atualizados do treinamento real
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, precision_recall_fscore_support,
                             roc_auc_score, precision_score, recall_score, f1_score)

# Configuração global
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11
sns.set_style("whitegrid")

# CORES PADRÃO
CORES_PERFIS = {
    'conservador': '#2ecc71',
    'moderado': '#f39c12',
    'agressivo': '#e74c3c'
}

def carregar_e_treinar():
    """Carrega dataset e treina a primeira rede neural"""
    print("\n" + "="*70)
    print("TREINANDO PRIMEIRA REDE NEURAL - DADOS REAIS")
    print("="*70)

    # Carregar dataset
    print("\n1. Carregando dataset...")
    df = pd.read_csv('data/dataset_simulado.csv')
    print(f"   ✓ {len(df)} amostras carregadas")

    X = df.drop('perfil_risco', axis=1)
    y = df['perfil_risco']

    print(f"\n   Distribuição das classes:")
    dist = y.value_counts()
    for perfil, count in dist.items():
        print(f"   • {perfil.capitalize()}: {count} ({count/len(y)*100:.1f}%)")

    # Split treino/teste
    print("\n2. Dividindo dados (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   ✓ Treino: {len(X_train)} | Teste: {len(X_test)}")

    # Normalização
    print("\n3. Normalizando features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("   ✓ StandardScaler aplicado")

    # Treinar modelo - ARQUITETURA CORRETA: (10, 5)
    print("\n4. Treinando rede neural MLP(10, 5)...")
    model = MLPClassifier(
        hidden_layer_sizes=(10, 5),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    print(f"   ✓ Convergiu em {model.n_iter_} iterações")

    # Predições
    print("\n5. Gerando predições...")
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    y_test_proba = model.predict_proba(X_test_scaled)

    # Métricas
    print("\n6. Calculando métricas...")
    metricas = {
        'train_accuracy': accuracy_score(y_train, y_train_pred),
        'test_accuracy': accuracy_score(y_test, y_test_pred),
        'test_precision': precision_score(y_test, y_test_pred, average='weighted'),
        'test_recall': recall_score(y_test, y_test_pred, average='weighted'),
        'test_f1': f1_score(y_test, y_test_pred, average='weighted'),
        'confusion_matrix': confusion_matrix(y_test, y_test_pred),
        'classification_report': classification_report(y_test, y_test_pred, output_dict=True),
        'classes': model.classes_,
        'n_iter': model.n_iter_
    }

    # ROC-AUC (multiclass)
    try:
        from sklearn.preprocessing import label_binarize
        y_test_bin = label_binarize(y_test, classes=model.classes_)
        metricas['test_roc_auc'] = roc_auc_score(y_test_bin, y_test_proba, average='weighted', multi_class='ovr')
    except:
        metricas['test_roc_auc'] = None

    print("   ✓ Métricas calculadas")

    # Exibir resultados
    print("\n" + "="*70)
    print("RESULTADOS DO TREINAMENTO")
    print("="*70)
    print(f"Acurácia Treino: {metricas['train_accuracy']:.4f} ({metricas['train_accuracy']*100:.2f}%)")
    print(f"Acurácia Teste:  {metricas['test_accuracy']:.4f} ({metricas['test_accuracy']*100:.2f}%)")
    print(f"Precision:       {metricas['test_precision']:.4f}")
    print(f"Recall:          {metricas['test_recall']:.4f}")
    print(f"F1-Score:        {metricas['test_f1']:.4f}")
    if metricas['test_roc_auc']:
        print(f"ROC-AUC:         {metricas['test_roc_auc']:.4f}")
    print(f"Iterações:       {metricas['n_iter']}")

    print("\n--- Matriz de Confusão ---")
    print(metricas['confusion_matrix'])

    return model, X_test, y_test, y_test_pred, y_test_proba, metricas, scaler


def gerar_tabela_latex_metricas(metricas):
    """Gera tabela LaTeX com métricas de teste"""

    latex = r"""\begin{table}[htbp]
\centering
\caption{Métricas de Performance da Primeira Rede Neural (Conjunto de Teste)}
\label{tab:metricas_rede1}
\begin{tabular}{lcc}
\toprule
\textbf{Métrica} & \textbf{Valor} & \textbf{Percentual} \\
\midrule
Acurácia (Accuracy) & """ + f"{metricas['test_accuracy']:.4f}" + r""" & """ + f"{metricas['test_accuracy']*100:.2f}" + r"""\% \\
Precisão (Precision) & """ + f"{metricas['test_precision']:.4f}" + r""" & """ + f"{metricas['test_precision']*100:.2f}" + r"""\% \\
Revocação (Recall) & """ + f"{metricas['test_recall']:.4f}" + r""" & """ + f"{metricas['test_recall']*100:.2f}" + r"""\% \\
F1-Score & """ + f"{metricas['test_f1']:.4f}" + r""" & """ + f"{metricas['test_f1']*100:.2f}" + r"""\% \\"""

    if metricas['test_roc_auc']:
        latex += f"\nROC-AUC & {metricas['test_roc_auc']:.4f} & {metricas['test_roc_auc']*100:.2f}\\% \\\\"

    latex += r"""
\bottomrule
\end{tabular}
\end{table}"""

    return latex


def gerar_tabela_latex_por_classe(metricas):
    """Gera tabela LaTeX com métricas por classe"""

    report = metricas['classification_report']
    classes = metricas['classes']

    latex = r"""\begin{table}[htbp]
\centering
\caption{Métricas de Performance por Classe de Perfil}
\label{tab:metricas_por_classe}
\begin{tabular}{lccc}
\toprule
\textbf{Perfil} & \textbf{Precision} & \textbf{Recall} & \textbf{F1-Score} \\
\midrule
"""

    for classe in classes:
        nome = classe.capitalize()
        p = report[classe]['precision']
        r = report[classe]['recall']
        f1 = report[classe]['f1-score']
        latex += f"{nome} & {p:.4f} & {r:.4f} & {f1:.4f} \\\\\n"

    # Média ponderada
    latex += r"""\midrule
\textbf{Média Ponderada} & """ + f"{metricas['test_precision']:.4f}" + r""" & """ + f"{metricas['test_recall']:.4f}" + r""" & """ + f"{metricas['test_f1']:.4f}" + r""" \\
\bottomrule
\end{tabular}
\end{table}"""

    return latex


def grafico_1_arquitetura():
    """Gráfico da arquitetura da rede neural - CORRIGIDO para (10, 5)"""

    fig, ax = plt.subplots(figsize=(16, 10))
    ax.axis('off')

    # Camadas - ARQUITETURA CORRETA
    layers = [
        {'name': 'Input\n(15 neurônios)', 'neurons': 15, 'x': 0.1, 'color': '#3498db'},
        {'name': 'Hidden 1\n(10 neurônios)', 'neurons': 10, 'x': 0.37, 'color': '#9b59b6'},
        {'name': 'Hidden 2\n(5 neurônios)', 'neurons': 5, 'x': 0.63, 'color': '#9b59b6'},
        {'name': 'Output\n(3 neurônios)', 'neurons': 3, 'x': 0.9, 'color': '#e74c3c'}
    ]

    # Desenhar neurônios
    neuron_positions = {}
    for layer_idx, layer in enumerate(layers):
        x = layer['x']
        neurons = layer['neurons']
        y_positions = np.linspace(0.15, 0.85, neurons)
        neuron_positions[layer_idx] = []

        for y in y_positions:
            circle = plt.Circle((x, y), 0.015, color=layer['color'], alpha=0.8, ec='black', linewidth=2)
            ax.add_patch(circle)
            neuron_positions[layer_idx].append(y)

        # Título da camada
        ax.text(x, 0.05, layer['name'], ha='center', fontsize=13, fontweight='bold')

    # Linhas conectando camadas (amostra)
    for i in range(len(layers) - 1):
        x1 = layers[i]['x']
        x2 = layers[i + 1]['x']
        y1_positions = neuron_positions[i]
        y2_positions = neuron_positions[i + 1]

        # Conectar apenas alguns neurônios
        n1 = len(y1_positions)
        n2 = len(y2_positions)

        if n1 <= 5:
            indices1 = range(n1)
        else:
            indices1 = [0, n1//4, n1//2, 3*n1//4, n1-1]

        for idx1 in indices1:
            for idx2 in range(min(3, n2)):  # Conecta aos 3 primeiros da próxima
                ax.plot([x1, x2], [y1_positions[idx1], y2_positions[idx2]],
                       'k-', alpha=0.08, linewidth=0.5)

    # Anotações de ativação
    ax.text(0.235, 0.92, 'ReLU', ha='center', fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6))
    ax.text(0.5, 0.92, 'ReLU', ha='center', fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6))
    ax.text(0.765, 0.92, 'Softmax', ha='center', fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))

    # Features de entrada (15)
    features = ['Idade', 'Renda Mensal', 'Dependentes', 'Estado Civil',
               'Valor Investir', 'Experiência', 'Patrimônio', 'Dívidas',
               'Tolerância 1', 'Tolerância 2', 'Horizonte', 'Conhecimento',
               'Estabilidade', 'Reserva Emerg.', 'Grandes Gastos']

    y_pos_input = neuron_positions[0]
    for i, (feat, y) in enumerate(zip(features, y_pos_input)):
        # Destaque para tolerâncias
        color = 'gold' if 'Tolerância' in feat else 'white'
        weight = 'bold' if 'Tolerância' in feat else 'normal'
        ax.text(0.02, y, feat, ha='right', fontsize=9, fontweight=weight,
               bbox=dict(boxstyle='round', facecolor=color, alpha=0.7, edgecolor='black'))

    # Outputs (3)
    outputs = ['Conservador', 'Moderado', 'Agressivo']
    y_pos_out = neuron_positions[3]
    cores_out = ['#2ecc71', '#f39c12', '#e74c3c']
    for out, y, cor in zip(outputs, y_pos_out, cores_out):
        ax.text(0.98, y, out, ha='left', fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor=cor, alpha=0.7, edgecolor='black'))

    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(0, 1)
    ax.set_title('Arquitetura da Primeira Rede Neural (MLPClassifier)\nCamadas Ocultas: 10 e 5 neurônios',
                fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('grafico_arquitetura_rede1.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico 1 salvo: grafico_arquitetura_rede1.png")
    plt.close()


def grafico_2_matriz_confusao(metricas):
    """Gráfico da matriz de confusão com heatmap - VERSÃO PARA SLIDE"""

    cm = metricas['confusion_matrix']
    classes = [c.capitalize() for c in metricas['classes']]

    fig, ax = plt.subplots(figsize=(12, 10))

    # Criar heatmap customizado
    # Cores: verde escuro na diagonal, amarelo nos erros, branco nos zeros
    mask_diagonal = np.eye(len(classes), dtype=bool)
    mask_zeros = cm == 0

    # Heatmap base
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd_r', cbar=True,
                xticklabels=classes, yticklabels=classes,
                linewidths=3, linecolor='black', ax=ax,
                annot_kws={'size': 20, 'weight': 'bold'},
                cbar_kws={'label': 'Quantidade de casos'})

    # Destacar diagonal com retângulos verdes
    for i in range(len(classes)):
        ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=False,
                                   edgecolor='green', lw=5))

    ax.set_xlabel('Predito →', fontsize=16, fontweight='bold')
    ax.set_ylabel('Real ↓', fontsize=16, fontweight='bold')
    ax.set_title('Matriz de Confusão - Primeira Rede Neural\nConjunto de Teste (60 amostras)',
                fontsize=18, fontweight='bold', pad=20)

    # Calcular e exibir métricas
    total = cm.sum()
    corretos = np.trace(cm)
    erros = total - corretos
    acuracia = corretos / total

    # Anotações importantes
    # 1. Box com acurácia
    textstr = f'✅ Acertos: {corretos}/{total}\n📊 Acurácia: {acuracia*100:.2f}%\n❌ Erros: {erros}'
    props = dict(boxstyle='round', facecolor='lightgreen', alpha=0.8, edgecolor='darkgreen', linewidth=3)
    ax.text(3.5, 0.5, textstr, fontsize=14, fontweight='bold',
            verticalalignment='center', bbox=props)

    # 2. Destacar zeros (Cons↔Agr)
    # Conservador→Agressivo (posição [0,2])
    if cm[0, 2] == 0:
        ax.add_patch(plt.Rectangle((2, 0), 1, 1, fill=False,
                                   edgecolor='blue', lw=4, linestyle='--'))
        ax.text(2.5, 0.2, '⭐', fontsize=24, ha='center', va='center', color='blue')

    # Agressivo→Conservador (posição [2,0])
    if cm[2, 0] == 0:
        ax.add_patch(plt.Rectangle((0, 2), 1, 1, fill=False,
                                   edgecolor='blue', lw=4, linestyle='--'))
        ax.text(0.5, 2.2, '⭐', fontsize=24, ha='center', va='center', color='blue')

    # 3. Legenda explicativa
    legend_text = '🟩 Verde = Diagonal (Acertos)\n⭐ Azul = Zero confusão Cons↔Agr'
    ax.text(3.5, 2.3, legend_text, fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

    # 4. Adicionar recalls por linha
    for i, classe in enumerate(classes):
        total_real = cm[i, :].sum()
        acertos_classe = cm[i, i]
        recall = acertos_classe / total_real if total_real > 0 else 0
        ax.text(3.2, i + 0.7, f'Recall: {recall*100:.1f}%',
                fontsize=11, fontweight='bold', style='italic')

    plt.tight_layout()
    plt.savefig('grafico_matriz_confusao_rede1.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico 2 salvo: grafico_matriz_confusao_rede1.png")
    plt.close()


def grafico_3_metricas_por_classe(metricas):
    """Gráfico de barras com métricas por classe"""

    report = metricas['classification_report']
    classes = [c.capitalize() for c in metricas['classes']]

    # Dados
    precisoes = [report[c.lower()]['precision'] for c in classes]
    recalls = [report[c.lower()]['recall'] for c in classes]
    f1s = [report[c.lower()]['f1-score'] for c in classes]

    x = np.arange(len(classes))
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 7))

    bars1 = ax.bar(x - width, precisoes, width, label='Precision',
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x, recalls, width, label='Recall',
                   color='#e67e22', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars3 = ax.bar(x + width, f1s, width, label='F1-Score',
                   color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)

    ax.set_xlabel('Perfil de Risco', fontsize=14, fontweight='bold')
    ax.set_ylabel('Score', fontsize=14, fontweight='bold')
    ax.set_title('Métricas de Performance por Classe de Perfil\nPrimeira Rede Neural',
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(classes, fontsize=12)
    ax.legend(fontsize=12, loc='lower right')
    ax.set_ylim(0, 1.05)
    ax.grid(axis='y', alpha=0.3)

    # Valores nas barras
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('grafico_metricas_por_classe_rede1.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico 3 salvo: grafico_metricas_por_classe_rede1.png")
    plt.close()


def grafico_4_comparacao_perfis(metricas):
    """Comparação visual dos 3 perfis com support"""

    report = metricas['classification_report']
    classes = [c.capitalize() for c in metricas['classes']]
    cores = [CORES_PERFIS[c.lower()] for c in classes]

    supports = [report[c.lower()]['support'] for c in classes]
    f1s = [report[c.lower()]['f1-score'] for c in classes]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Pizza - distribuição
    wedges, texts, autotexts = ax1.pie(supports, labels=classes, colors=cores,
                                        autopct='%1.1f%%', startangle=90,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(13)
        autotext.set_fontweight('bold')

    ax1.set_title('Distribuição das Classes\nno Conjunto de Teste',
                 fontsize=14, fontweight='bold')

    # Barras - F1-Score
    bars = ax2.bar(classes, f1s, color=cores, alpha=0.8, edgecolor='black', linewidth=2)
    ax2.set_ylabel('F1-Score', fontsize=13, fontweight='bold')
    ax2.set_title('F1-Score por Classe', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 1.05)
    ax2.grid(axis='y', alpha=0.3)

    for bar, f1 in zip(bars, f1s):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{f1:.3f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.suptitle('Análise por Perfil de Risco - Primeira Rede Neural',
                fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('grafico_analise_perfis_rede1.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico 4 salvo: grafico_analise_perfis_rede1.png")
    plt.close()


# ============================================================================
# EXECUTAR TODOS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("GERADOR DE GRÁFICOS E MÉTRICAS - PRIMEIRA REDE NEURAL")
    print("="*70)

    try:
        # Treinar e obter métricas reais
        model, X_test, y_test, y_test_pred, y_test_proba, metricas, scaler = carregar_e_treinar()

        # Gerar gráficos
        print("\n" + "="*70)
        print("GERANDO GRÁFICOS")
        print("="*70 + "\n")

        grafico_1_arquitetura()
        grafico_2_matriz_confusao(metricas)
        grafico_3_metricas_por_classe(metricas)
        grafico_4_comparacao_perfis(metricas)

        # Gerar tabelas LaTeX
        print("\n" + "="*70)
        print("GERANDO TABELAS LATEX")
        print("="*70)

        latex1 = gerar_tabela_latex_metricas(metricas)
        latex2 = gerar_tabela_latex_por_classe(metricas)

        # Salvar LaTeX
        with open('tabela_metricas_rede1.tex', 'w', encoding='utf-8') as f:
            f.write(latex1)
        print("\n✅ Tabela LaTeX 1 salva: tabela_metricas_rede1.tex")

        with open('tabela_metricas_por_classe_rede1.tex', 'w', encoding='utf-8') as f:
            f.write(latex2)
        print("✅ Tabela LaTeX 2 salva: tabela_metricas_por_classe_rede1.tex")

        # Exibir tabelas
        print("\n" + "="*70)
        print("TABELA LATEX 1: MÉTRICAS GERAIS")
        print("="*70)
        print(latex1)

        print("\n" + "="*70)
        print("TABELA LATEX 2: MÉTRICAS POR CLASSE")
        print("="*70)
        print(latex2)

        print("\n" + "="*70)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("="*70)
        print("\n📁 Arquivos gerados:")
        print("   • grafico_arquitetura_rede1.png")
        print("   • grafico_matriz_confusao_rede1.png")
        print("   • grafico_metricas_por_classe_rede1.png")
        print("   • grafico_analise_perfis_rede1.png")
        print("   • tabela_metricas_rede1.tex")
        print("   • tabela_metricas_por_classe_rede1.tex")
        print()

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
