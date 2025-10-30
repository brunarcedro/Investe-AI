"""
Gerador de Matriz de Confusao - Versao para Slide
Otimizado para apresentacao com anotacoes visuais
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

# Configuracao
plt.rcParams['figure.figsize'] = (12, 10)
plt.rcParams['font.size'] = 11
sns.set_style("whitegrid")

def gerar_matriz_confusao_slide():
    """Gera matriz de confusao otimizada para slide de apresentacao"""

    print("="*70)
    print("GERANDO MATRIZ DE CONFUSAO PARA SLIDE")
    print("="*70)

    # 1. Carregar e treinar
    print("\n1. Carregando dataset...")
    df = pd.read_csv('data/dataset_simulado.csv')
    print(f"   OK: {len(df)} amostras carregadas")

    X = df.drop('perfil_risco', axis=1)
    y = df['perfil_risco']

    print("\n2. Dividindo dados (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   OK: Treino {len(X_train)} | Teste {len(X_test)}")

    print("\n3. Normalizando e treinando...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = MLPClassifier(
        hidden_layer_sizes=(10, 5),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    print(f"   OK: Treinamento concluido em {model.n_iter_} iteracoes")

    print("\n4. Gerando predicoes...")
    y_pred = model.predict(X_test_scaled)
    cm = confusion_matrix(y_test, y_pred)
    classes = [c.capitalize() for c in model.classes_]

    print("\n5. Criando visualizacao...")

    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 10))

    # Heatmap base com cores invertidas (vermelho escuro = alto)
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd_r', cbar=True,
                xticklabels=classes, yticklabels=classes,
                linewidths=3, linecolor='black', ax=ax,
                annot_kws={'size': 22, 'weight': 'bold'},
                cbar_kws={'label': 'Quantidade de casos', 'shrink': 0.8})

    # Destacar diagonal com retangulos verdes grossos
    for i in range(len(classes)):
        ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=False,
                                   edgecolor='darkgreen', lw=6))

    # Titulos
    ax.set_xlabel('Predito (saida da rede)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Real (classe verdadeira)', fontsize=16, fontweight='bold')
    ax.set_title('Matriz de Confusao - Primeira Rede Neural\nConjunto de Teste (60 amostras)',
                fontsize=19, fontweight='bold', pad=20)

    # Metricas principais
    total = cm.sum()
    corretos = np.trace(cm)
    erros = total - corretos
    acuracia = corretos / total

    # Box 1: Metricas gerais (canto superior direito)
    textstr = f'ACERTOS: {corretos}/{total}\nACURACIA: {acuracia*100:.2f}%\nERROS: {erros}'
    props = dict(boxstyle='round,pad=0.8', facecolor='lightgreen',
                 alpha=0.9, edgecolor='darkgreen', linewidth=3)
    ax.text(3.7, 0.5, textstr, fontsize=15, fontweight='bold',
            verticalalignment='center', bbox=props)

    # Destacar zeros (Conservador-Agressivo)
    # Posicao [0,2] - Conservador classificado como Agressivo
    if cm[0, 2] == 0:
        ax.add_patch(plt.Rectangle((2, 0), 1, 1, fill=False,
                                   edgecolor='blue', lw=5, linestyle='--'))
        ax.text(2.5, 0.15, 'ZERO!', fontsize=16, ha='center',
                fontweight='bold', color='blue',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

    # Posicao [2,0] - Agressivo classificado como Conservador
    if cm[2, 0] == 0:
        ax.add_patch(plt.Rectangle((0, 2), 1, 1, fill=False,
                                   edgecolor='blue', lw=5, linestyle='--'))
        ax.text(0.5, 2.15, 'ZERO!', fontsize=16, ha='center',
                fontweight='bold', color='blue',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

    # Box 2: Insight sobre zeros (canto inferior direito)
    insight_text = 'INSIGHT IMPORTANTE:\nZero confusao entre\nConservador <-> Agressivo\n(perfis opostos!)'
    ax.text(3.7, 2.3, insight_text, fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='lightyellow',
                     alpha=0.9, edgecolor='orange', linewidth=2))

    # Adicionar recalls ao lado direito de cada linha
    recalls = []
    for i, classe in enumerate(classes):
        total_real = cm[i, :].sum()
        acertos_classe = cm[i, i]
        recall = acertos_classe / total_real if total_real > 0 else 0
        recalls.append(recall)

        # Cor baseada no recall
        cor = 'green' if recall > 0.8 else 'orange' if recall > 0.6 else 'red'

        ax.text(3.15, i + 0.5, f'Recall:\n{recall*100:.1f}%',
                fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor=cor, alpha=0.3))

    # Legenda visual
    legend_elements = [
        plt.Rectangle((0,0),1,1, edgecolor='darkgreen', facecolor='none', lw=4, label='Diagonal = Acertos'),
        plt.Rectangle((0,0),1,1, edgecolor='blue', facecolor='none', lw=4, linestyle='--', label='Zero confusao extremos'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)

    plt.tight_layout()

    # Salvar
    output_file = 'grafico_matriz_confusao_slide.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n6. Grafico salvo: {output_file}")

    # Exibir matriz
    print("\n" + "="*70)
    print("MATRIZ DE CONFUSAO (valores):")
    print("="*70)
    print("\n              Predito ->")
    print(f"Real    {classes[0]:12s} {classes[1]:12s} {classes[2]:12s}")
    print("-" * 50)
    for i, classe in enumerate(classes):
        valores = "  ".join([f"{cm[i,j]:3d}" for j in range(len(classes))])
        print(f"{classe:12s}  {valores}")

    print("\n" + "="*70)
    print("RECALLS POR CLASSE:")
    print("="*70)
    for i, (classe, recall) in enumerate(zip(classes, recalls)):
        print(f"{classe:12s}: {recall*100:.2f}% ({cm[i,i]}/{cm[i,:].sum()})")

    print("\n" + "="*70)
    print("CONCLUIDO COM SUCESSO!")
    print("="*70)
    print(f"\nArquivo gerado: {output_file}")
    print("Use este grafico no seu slide 14.2 da apresentacao!")
    print()

if __name__ == "__main__":
    try:
        gerar_matriz_confusao_slide()
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()
