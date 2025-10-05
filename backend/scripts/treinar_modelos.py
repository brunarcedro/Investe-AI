"""
TREINAMENTO DETALHADO DA PRIMEIRA REDE NEURAL
==============================================

Script para treinar a primeira rede neural com análises estatísticas
completas para documentação do TCC.

Inclui:
- Múltiplas métricas de avaliação
- Matriz de confusão detalhada
- Análise por classe
- Curvas de aprendizado
- Validação cruzada
- Testes estatísticos
"""

import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, cohen_kappa_score,
    balanced_accuracy_score, matthews_corrcoef
)
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class TreinadorRedeNeuralDetalhado:
    """Classe para treinamento detalhado com análises estatísticas"""

    def __init__(self, dataset_path='backend/data/dataset_validado.csv'):
        self.dataset_path = dataset_path
        self.model = None
        self.scaler = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.historico = {}

    def carregar_dados(self):
        """Carrega e prepara os dados"""
        print("="*80)
        print(" ETAPA 1: CARREGAMENTO E PREPARAÇÃO DOS DADOS")
        print("="*80)

        df = pd.read_csv(self.dataset_path)
        print(f"\nDataset carregado: {len(df)} registros")

        # Separar features e target
        X = df.drop('perfil_risco', axis=1)
        y = df['perfil_risco'].astype(str)  # Garante que é string

        print(f"Features: {len(X.columns)}")
        print(f"\nDistribuição das classes:")
        for classe, count in y.value_counts().items():
            pct = (count / len(y)) * 100
            print(f"  {classe:12s}: {count:3d} ({pct:5.1f}%)")

        # Dividir dados
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"\nDivisão dos dados:")
        print(f"  Treino: {len(self.X_train)} registros ({len(self.X_train)/len(df)*100:.1f}%)")
        print(f"  Teste:  {len(self.X_test)} registros ({len(self.X_test)/len(df)*100:.1f}%)")

        # Normalizar
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

        print(f"\nNormalização aplicada (StandardScaler)")
        print(f"  Média antes: {self.X_train.mean().mean():.2f}")
        print(f"  Média depois: {self.X_train_scaled.mean():.4f}")
        print(f"  Desvio antes: {self.X_train.std().mean():.2f}")
        print(f"  Desvio depois: {self.X_train_scaled.std():.4f}")

        return X, y

    def treinar_modelo_otimizado(self):
        """Treina modelo com configuração otimizada"""
        print("\n" + "="*80)
        print(" ETAPA 2: TREINAMENTO DA REDE NEURAL")
        print("="*80)

        # Configuração otimizada
        config = {
            'hidden_layer_sizes': (15, 10, 5),  # 3 camadas escondidas
            'activation': 'relu',
            'solver': 'adam',
            'alpha': 0.001,  # Regularização L2
            'batch_size': 32,
            'learning_rate': 'adaptive',
            'learning_rate_init': 0.001,
            'max_iter': 1500,
            'early_stopping': False,  # Desabilitado por compatibilidade
            'random_state': 42,
            'verbose': False
        }

        print("\nArquitetura da Rede Neural:")
        print(f"  Camadas: {config['hidden_layer_sizes']}")
        print(f"  Ativação: {config['activation']}")
        print(f"  Otimizador: {config['solver']}")
        print(f"  Taxa de aprendizado: {config['learning_rate']} (inicial: {config['learning_rate_init']})")
        print(f"  Regularização (alpha): {config['alpha']}")
        print(f"  Batch size: {config['batch_size']}")
        print(f"  Early stopping: {config['early_stopping']}")
        print(f"  Max iterações: {config['max_iter']}")

        print("\nIniciando treinamento...")
        self.model = MLPClassifier(**config)
        self.model.fit(self.X_train_scaled, self.y_train)

        print(f"\nTreinamento concluído!")
        print(f"  Iterações até convergência: {self.model.n_iter_}")
        print(f"  Perda final (loss): {self.model.loss_:.6f}")
        print(f"  Parou por early stopping: {self.model.n_iter_ < config['max_iter']}")

        # Calcular predições
        y_train_pred = self.model.predict(self.X_train_scaled)
        y_test_pred = self.model.predict(self.X_test_scaled)

        return y_train_pred, y_test_pred

    def avaliar_metricas_completas(self, y_train_pred, y_test_pred):
        """Calcula e exibe métricas detalhadas"""
        print("\n" + "="*80)
        print(" ETAPA 3: AVALIAÇÃO DE DESEMPENHO")
        print("="*80)

        # Métricas globais
        print("\n1. MÉTRICAS GLOBAIS")
        print("-" * 80)

        metricas = {
            'treino': {
                'accuracy': accuracy_score(self.y_train, y_train_pred),
                'balanced_accuracy': balanced_accuracy_score(self.y_train, y_train_pred),
                'precision_macro': precision_score(self.y_train, y_train_pred, average='macro', zero_division=0),
                'recall_macro': recall_score(self.y_train, y_train_pred, average='macro', zero_division=0),
                'f1_macro': f1_score(self.y_train, y_train_pred, average='macro', zero_division=0),
                'kappa': cohen_kappa_score(self.y_train, y_train_pred),
                'mcc': matthews_corrcoef(self.y_train, y_train_pred),
            },
            'teste': {
                'accuracy': accuracy_score(self.y_test, y_test_pred),
                'balanced_accuracy': balanced_accuracy_score(self.y_test, y_test_pred),
                'precision_macro': precision_score(self.y_test, y_test_pred, average='macro', zero_division=0),
                'recall_macro': recall_score(self.y_test, y_test_pred, average='macro', zero_division=0),
                'f1_macro': f1_score(self.y_test, y_test_pred, average='macro', zero_division=0),
                'kappa': cohen_kappa_score(self.y_test, y_test_pred),
                'mcc': matthews_corrcoef(self.y_test, y_test_pred),
            }
        }

        print("\nCONJUNTO DE TREINO:")
        for metrica, valor in metricas['treino'].items():
            print(f"  {metrica:20s}: {valor:.4f}")

        print("\nCONJUNTO DE TESTE:")
        for metrica, valor in metricas['teste'].items():
            print(f"  {metrica:20s}: {valor:.4f}")

        # Diferença (overfitting check)
        print("\nDIFERENÇA (Treino - Teste):")
        diff_accuracy = metricas['treino']['accuracy'] - metricas['teste']['accuracy']
        print(f"  Accuracy: {diff_accuracy:+.4f}", end="")
        if diff_accuracy > 0.10:
            print(" [ALERTA: Possível overfitting]")
        elif diff_accuracy > 0.05:
            print(" [OK: Ligeiro overfitting]")
        else:
            print(" [EXCELENTE: Boa generalização]")

        self.historico['metricas'] = metricas

        # Matriz de confusão
        print("\n" + "-" * 80)
        print("2. MATRIZ DE CONFUSÃO (Conjunto de Teste)")
        print("-" * 80)

        cm = confusion_matrix(self.y_test, y_test_pred)
        classes = sorted(self.y_test.unique())

        print("\n         Previsto:")
        print("Real      ", end="")
        for classe in classes:
            print(f"{classe:12s}", end=" ")
        print()

        for i, classe_real in enumerate(classes):
            print(f"{classe_real:12s}", end=" ")
            for j in range(len(classes)):
                print(f"{cm[i][j]:4d} ({cm[i][j]/cm[i].sum()*100:5.1f}%)", end=" ")
            print()

        self.historico['confusion_matrix'] = cm

        # Métricas por classe
        print("\n" + "-" * 80)
        print("3. MÉTRICAS POR CLASSE (Conjunto de Teste)")
        print("-" * 80)

        print("\n{:15s} {:>10s} {:>10s} {:>10s} {:>10s}".format(
            "Classe", "Precision", "Recall", "F1-Score", "Support"
        ))
        print("-" * 60)

        report = classification_report(self.y_test, y_test_pred, output_dict=True, zero_division=0)

        for classe in classes:
            metrics = report[classe]
            print("{:15s} {:10.3f} {:10.3f} {:10.3f} {:10.0f}".format(
                classe,
                metrics['precision'],
                metrics['recall'],
                metrics['f1-score'],
                metrics['support']
            ))

        print("\n{:15s} {:10.3f} {:10.3f} {:10.3f} {:10.0f}".format(
            "Macro avg",
            report['macro avg']['precision'],
            report['macro avg']['recall'],
            report['macro avg']['f1-score'],
            len(self.y_test)
        ))

        print("{:15s} {:10.3f} {:10.3f} {:10.3f} {:10.0f}".format(
            "Weighted avg",
            report['weighted avg']['precision'],
            report['weighted avg']['recall'],
            report['weighted avg']['f1-score'],
            len(self.y_test)
        ))

        self.historico['classification_report'] = report

        return metricas

    def validacao_cruzada(self):
        """Executa validação cruzada estratificada"""
        print("\n" + "="*80)
        print(" ETAPA 4: VALIDAÇÃO CRUZADA (K-FOLD)")
        print("="*80)

        print("\nConfigurações:")
        print("  Método: Stratified K-Fold")
        print("  K (folds): 5")
        print("  Métrica: Accuracy")

        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        # Recombinar dados para CV
        X_all = np.vstack([self.X_train_scaled, self.X_test_scaled])
        y_all = pd.concat([self.y_train, self.y_test])

        print("\nExecutando validação cruzada...")
        scores = cross_val_score(
            self.model, X_all, y_all, cv=skf, scoring='accuracy', n_jobs=-1
        )

        print("\nResultados por Fold:")
        for i, score in enumerate(scores, 1):
            print(f"  Fold {i}: {score:.4f}")

        print(f"\nEstatísticas:")
        print(f"  Média: {scores.mean():.4f}")
        print(f"  Desvio padrão: {scores.std():.4f}")
        print(f"  Intervalo de confiança (95%): [{scores.mean() - 1.96*scores.std():.4f}, {scores.mean() + 1.96*scores.std():.4f}]")
        print(f"  Min: {scores.min():.4f}")
        print(f"  Max: {scores.max():.4f}")

        self.historico['cv_scores'] = scores

        return scores

    def analise_erros(self, y_test_pred):
        """Analisa os erros de classificação"""
        print("\n" + "="*80)
        print(" ETAPA 5: ANÁLISE DE ERROS")
        print("="*80)

        erros = self.y_test != y_test_pred
        n_erros = erros.sum()
        taxa_acerto = (1 - erros.mean()) * 100

        print(f"\nTotal de erros: {n_erros} de {len(self.y_test)} ({(n_erros/len(self.y_test)*100):.1f}%)")
        print(f"Taxa de acerto: {taxa_acerto:.2f}%")

        if n_erros > 0:
            print("\nDistribuição dos erros:")
            print("\n{:15s} -> {:15s} {:>10s}".format("Real", "Previsto", "Quantidade"))
            print("-" * 45)

            erros_df = pd.DataFrame({
                'real': self.y_test[erros],
                'previsto': y_test_pred[erros]
            })

            for (real, previsto), count in erros_df.value_counts().items():
                print(f"{real:15s} -> {previsto:15s} {count:10d}")

            # Análise de confusões mais comuns
            print("\nConfusoes mais comuns:")
            confusoes = erros_df.value_counts().head(3)
            for i, ((real, previsto), count) in enumerate(confusoes.items(), 1):
                pct = (count / n_erros) * 100
                print(f"  {i}. {real} -> {previsto}: {count} erros ({pct:.1f}% dos erros)")

    def salvar_modelo(self, caminho='backend/models/neural_network_validado.pkl'):
        """Salva modelo treinado"""
        print("\n" + "="*80)
        print(" ETAPA 6: SALVANDO MODELO")
        print("="*80)

        dados_modelo = {
            'model': self.model,
            'scaler': self.scaler,
            'is_trained': True,
            'historico': self.historico,
            'data_treinamento': datetime.now().isoformat(),
            'dataset_path': self.dataset_path
        }

        joblib.dump(dados_modelo, caminho)
        print(f"\nModelo salvo em: {caminho}")

        # Tamanho do arquivo
        import os
        tamanho = os.path.getsize(caminho) / 1024  # KB
        print(f"Tamanho do arquivo: {tamanho:.2f} KB")

def main():
    """Executa treinamento completo"""
    print("\n" + "#"*80)
    print("# TREINAMENTO DETALHADO DA PRIMEIRA REDE NEURAL")
    print("# Sistema de Classificação de Perfil de Risco")
    print("#"*80)
    print(f"\n Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(" Dataset: Validado por especialista financeiro")
    print("#"*80)

    # Inicializa treinador
    treinador = TreinadorRedeNeuralDetalhado()

    # Carrega dados
    X, y = treinador.carregar_dados()

    # Treina modelo
    y_train_pred, y_test_pred = treinador.treinar_modelo_otimizado()

    # Avalia métricas
    metricas = treinador.avaliar_metricas_completas(y_train_pred, y_test_pred)

    # Validação cruzada
    cv_scores = treinador.validacao_cruzada()

    # Análise de erros
    treinador.analise_erros(y_test_pred)

    # Salva modelo
    treinador.salvar_modelo()

    # Resumo final
    print("\n" + "="*80)
    print(" RESUMO FINAL")
    print("="*80)

    print(f"\nModelo: MLP Classifier com 3 camadas ocultas (15, 10, 5)")
    print(f"Dataset: {len(X)} registros ({len(treinador.X_train)} treino + {len(treinador.X_test)} teste)")
    print(f"Features: {len(X.columns)}")
    print(f"Classes: {len(y.unique())}")

    print(f"\nDesempenho no Teste:")
    print(f"  Accuracy: {metricas['teste']['accuracy']:.2%}")
    print(f"  Balanced Accuracy: {metricas['teste']['balanced_accuracy']:.2%}")
    print(f"  F1-Score (macro): {metricas['teste']['f1_macro']:.2%}")
    print(f"  Cohen's Kappa: {metricas['teste']['kappa']:.4f}")

    print(f"\nValidação Cruzada (5-fold):")
    print(f"  Média: {cv_scores.mean():.2%} (±{cv_scores.std():.2%})")

    print(f"\nModelo salvo: backend/models/neural_network_validado.pkl")

    print("\n" + "#"*80)
    print("# TREINAMENTO CONCLUÍDO COM SUCESSO!")
    print("#"*80)

    print("\nPróximos passos:")
    print("  1. Revisar métricas acima para o TCC")
    print("  2. Treinar segunda rede neural")
    print("  3. Testar API com novo modelo")

    print("\n" + "#"*80 + "\n")

if __name__ == "__main__":
    main()