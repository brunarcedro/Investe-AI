"""
Script para comparar métricas completas das redes neurais:
- Rede 1 (Classificação de Perfil): Sintético vs Híbrido
- Rede 2 (Alocação de Portfólio): Sintético vs Híbrido

Gera relatório detalhado com todas as métricas
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_recall_fscore_support, mean_squared_error, r2_score,
    mean_absolute_error
)
import warnings
warnings.filterwarnings('ignore')


class MetricsComparator:
    """Compara métricas entre datasets sintético e híbrido"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.data_dir = self.project_root / 'data'
        self.models_dir = self.project_root / 'models'

        # Datasets
        self.dataset_sintetico = self.data_dir / 'dataset_simulado.csv'
        self.dataset_hibrido = self.data_dir / 'dataset_hibrido.csv'

        # Resultados
        self.resultados = {
            'rede1_sintetico': {},
            'rede1_hibrido': {},
            'rede2_sintetico': {},
            'rede2_hibrido': {}
        }

    def load_and_prepare_data_rede1(self, dataset_path):
        """Prepara dados para Rede 1 (classificação)"""
        df = pd.read_csv(dataset_path)

        # Features principais (tentar usar o máximo possível)
        all_features = [
            'idade', 'renda_mensal', 'dependentes', 'estado_civil',
            'valor_investir_mensal', 'experiencia_anos', 'patrimonio_atual',
            'dividas_percentual', 'tolerancia_perda_1', 'tolerancia_perda_2',
            'horizonte_investimento', 'conhecimento_mercado',
            'estabilidade_emprego', 'tem_reserva_emergencia',
            'planos_grandes_gastos'
        ]

        # Usar apenas features disponíveis
        available_features = [f for f in all_features if f in df.columns]

        X = df[available_features].copy()
        y = df['perfil_risco'].copy()

        # Tratar valores nulos
        X = X.fillna(X.mean())

        # Codificar target
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        return X, y_encoded, le, available_features

    def train_and_evaluate_rede1(self, X, y, label_encoder, dataset_name):
        """Treina e avalia Rede 1 com métricas completas"""
        print(f"\n{'='*70}")
        print(f"REDE NEURAL 1 - {dataset_name.upper()}")
        print(f"{'='*70}")

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"Train: {len(X_train)} | Test: {len(X_test)} | Features: {X.shape[1]}")

        # Modelo
        model = MLPClassifier(
            hidden_layer_sizes=(10, 5),
            activation='relu',
            max_iter=1000,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )

        # Treinar
        print("Treinando...")
        model.fit(X_train, y_train)

        # Predições
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Métricas básicas
        acc_train = accuracy_score(y_train, y_pred_train)
        acc_test = accuracy_score(y_test, y_pred_test)

        # Precision, Recall, F1 por classe
        precision, recall, f1, support = precision_recall_fscore_support(
            y_test, y_pred_test, average=None
        )

        # Média ponderada
        precision_avg, recall_avg, f1_avg, _ = precision_recall_fscore_support(
            y_test, y_pred_test, average='weighted'
        )

        # Cross-validation (5-fold)
        print("Executando cross-validation...")
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred_test)

        # Armazenar resultados
        resultados = {
            'dataset': dataset_name,
            'n_samples': len(X),
            'n_features': X.shape[1],
            'n_train': len(X_train),
            'n_test': len(X_test),
            'accuracy_train': acc_train,
            'accuracy_test': acc_test,
            'precision_weighted': precision_avg,
            'recall_weighted': recall_avg,
            'f1_weighted': f1_avg,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'n_iterations': model.n_iter_,
            'confusion_matrix': cm,
            'classes': label_encoder.classes_,
            'precision_per_class': dict(zip(label_encoder.classes_, precision)),
            'recall_per_class': dict(zip(label_encoder.classes_, recall)),
            'f1_per_class': dict(zip(label_encoder.classes_, f1)),
            'support_per_class': dict(zip(label_encoder.classes_, support))
        }

        # Imprimir
        self.print_rede1_results(resultados)

        return resultados

    def print_rede1_results(self, res):
        """Imprime resultados da Rede 1"""
        print(f"\nRESULTADOS - {res['dataset']}:")
        print(f"  Amostras: {res['n_samples']} (Train: {res['n_train']}, Test: {res['n_test']})")
        print(f"  Features: {res['n_features']}")
        print(f"  Iteracoes: {res['n_iterations']}")

        print(f"\nMETRICA GERAL:")
        print(f"  Accuracy (Train): {res['accuracy_train']:.4f}")
        print(f"  Accuracy (Test):  {res['accuracy_test']:.4f}")
        print(f"  Precision:        {res['precision_weighted']:.4f}")
        print(f"  Recall:           {res['recall_weighted']:.4f}")
        print(f"  F1-Score:         {res['f1_weighted']:.4f}")

        print(f"\nCROSS-VALIDATION (5-fold):")
        print(f"  Media: {res['cv_mean']:.4f}")
        print(f"  Desvio padrao: {res['cv_std']:.4f}")

        print(f"\nMETRICAS POR CLASSE:")
        print(f"{'Classe':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
        print("-" * 65)
        for cls in res['classes']:
            print(f"{cls.capitalize():<15} "
                  f"{res['precision_per_class'][cls]:<12.4f} "
                  f"{res['recall_per_class'][cls]:<12.4f} "
                  f"{res['f1_per_class'][cls]:<12.4f} "
                  f"{res['support_per_class'][cls]:<10}")

        print(f"\nMATRIZ DE CONFUSAO:")
        print(f"Predito →    {' '.join([c[:4].ljust(8) for c in res['classes']])}")
        print(f"Real ↓")
        for i, cls in enumerate(res['classes']):
            row = res['confusion_matrix'][i]
            print(f"{cls.capitalize():<12} {' '.join([str(v).ljust(8) for v in row])}")

    def load_and_prepare_data_rede2(self, dataset_path):
        """Prepara dados para Rede 2 (alocação de portfólio)"""
        df = pd.read_csv(dataset_path)

        # Features de entrada (perfil do investidor)
        input_features = [
            'idade', 'renda_mensal', 'experiencia_anos',
            'tolerancia_perda_1', 'conhecimento_mercado',
            'patrimonio_atual', 'dividas_percentual'
        ]

        # Verificar features disponíveis
        available_features = [f for f in input_features if f in df.columns]

        # Targets (alocações) - se não existirem, vamos simular baseado no perfil
        target_columns = [
            'renda_fixa', 'acoes_brasil', 'acoes_internacional',
            'fundos_imobiliarios', 'commodities', 'criptomoedas'
        ]

        # Verificar se targets existem
        has_targets = all(col in df.columns for col in target_columns)

        if not has_targets:
            print("\nAVISO: Dataset nao possui colunas de alocacao")
            print("Gerando alocacoes simuladas baseadas no perfil de risco...")
            df = self.generate_portfolio_allocations(df)

        X = df[available_features].copy()
        y = df[target_columns].copy()

        # Tratar valores nulos
        X = X.fillna(X.mean())
        y = y.fillna(0)

        # Normalizar y para somar 100%
        y_sum = y.sum(axis=1)
        y_normalized = y.div(y_sum, axis=0) * 100

        return X, y_normalized, available_features, target_columns

    def generate_portfolio_allocations(self, df):
        """Gera alocações simuladas baseadas no perfil de risco"""

        def get_allocation(perfil):
            """Retorna alocação típica por perfil"""
            if perfil == 'conservador':
                return {
                    'renda_fixa': 70,
                    'acoes_brasil': 15,
                    'acoes_internacional': 10,
                    'fundos_imobiliarios': 5,
                    'commodities': 0,
                    'criptomoedas': 0
                }
            elif perfil == 'moderado':
                return {
                    'renda_fixa': 40,
                    'acoes_brasil': 30,
                    'acoes_internacional': 20,
                    'fundos_imobiliarios': 8,
                    'commodities': 2,
                    'criptomoedas': 0
                }
            else:  # agressivo
                return {
                    'renda_fixa': 20,
                    'acoes_brasil': 35,
                    'acoes_internacional': 30,
                    'fundos_imobiliarios': 10,
                    'commodities': 3,
                    'criptomoedas': 2
                }

        # Gerar alocações com pequena variação aleatória
        for col in ['renda_fixa', 'acoes_brasil', 'acoes_internacional',
                    'fundos_imobiliarios', 'commodities', 'criptomoedas']:
            df[col] = 0.0

        for idx, row in df.iterrows():
            base_alloc = get_allocation(row['perfil_risco'])
            # Adicionar variação aleatória de ±5%
            for asset, value in base_alloc.items():
                noise = np.random.uniform(-5, 5)
                df.at[idx, asset] = max(0, value + noise)

        # Normalizar para somar 100%
        asset_cols = ['renda_fixa', 'acoes_brasil', 'acoes_internacional',
                      'fundos_imobiliarios', 'commodities', 'criptomoedas']
        total = df[asset_cols].sum(axis=1)
        for col in asset_cols:
            df[col] = (df[col] / total) * 100

        return df

    def train_and_evaluate_rede2(self, X, y, dataset_name):
        """Treina e avalia Rede 2 com métricas completas"""
        print(f"\n{'='*70}")
        print(f"REDE NEURAL 2 - {dataset_name.upper()}")
        print(f"{'='*70}")

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print(f"Train: {len(X_train)} | Test: {len(X_test)} | Features: {X.shape[1]}")
        print(f"Targets: {y.shape[1]} ativos")

        # Modelo
        model = MLPRegressor(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            max_iter=1000,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            learning_rate='adaptive'
        )

        # Treinar
        print("Treinando...")
        model.fit(X_train, y_train)

        # Predições
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Garantir valores não-negativos
        y_pred_train = np.maximum(0, y_pred_train)
        y_pred_test = np.maximum(0, y_pred_test)

        # Normalizar para somar 100%
        y_pred_train = (y_pred_train.T / y_pred_train.sum(axis=1)).T * 100
        y_pred_test = (y_pred_test.T / y_pred_test.sum(axis=1)).T * 100

        # Métricas de regressão
        mse_train = mean_squared_error(y_train, y_pred_train)
        mse_test = mean_squared_error(y_test, y_pred_test)
        mae_train = mean_absolute_error(y_train, y_pred_train)
        mae_test = mean_absolute_error(y_test, y_pred_test)
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)

        # RMSE
        rmse_train = np.sqrt(mse_train)
        rmse_test = np.sqrt(mse_test)

        # Métricas por ativo
        mse_per_asset = {}
        mae_per_asset = {}
        for i, col in enumerate(y.columns):
            mse_per_asset[col] = mean_squared_error(y_test.iloc[:, i], y_pred_test[:, i])
            mae_per_asset[col] = mean_absolute_error(y_test.iloc[:, i], y_pred_test[:, i])

        # Cross-validation
        print("Executando cross-validation...")
        from sklearn.model_selection import cross_val_score
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')

        # Armazenar resultados
        resultados = {
            'dataset': dataset_name,
            'n_samples': len(X),
            'n_features': X.shape[1],
            'n_targets': y.shape[1],
            'n_train': len(X_train),
            'n_test': len(X_test),
            'mse_train': mse_train,
            'mse_test': mse_test,
            'rmse_train': rmse_train,
            'rmse_test': rmse_test,
            'mae_train': mae_train,
            'mae_test': mae_test,
            'r2_train': r2_train,
            'r2_test': r2_test,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'n_iterations': model.n_iter_,
            'mse_per_asset': mse_per_asset,
            'mae_per_asset': mae_per_asset,
            'asset_names': list(y.columns)
        }

        # Imprimir
        self.print_rede2_results(resultados)

        return resultados

    def print_rede2_results(self, res):
        """Imprime resultados da Rede 2"""
        print(f"\nRESULTADOS - {res['dataset']}:")
        print(f"  Amostras: {res['n_samples']} (Train: {res['n_train']}, Test: {res['n_test']})")
        print(f"  Features: {res['n_features']}")
        print(f"  Targets: {res['n_targets']} ativos")
        print(f"  Iteracoes: {res['n_iterations']}")

        print(f"\nMETRICAS GERAIS (Test Set):")
        print(f"  MSE (Mean Squared Error):      {res['mse_test']:.4f}")
        print(f"  RMSE (Root MSE):               {res['rmse_test']:.4f}")
        print(f"  MAE (Mean Absolute Error):     {res['mae_test']:.4f}")
        print(f"  R² Score:                      {res['r2_test']:.4f}")

        print(f"\nCROSS-VALIDATION (5-fold R²):")
        print(f"  Media: {res['cv_mean']:.4f}")
        print(f"  Desvio padrao: {res['cv_std']:.4f}")

        print(f"\nERRO POR ATIVO (Test Set):")
        print(f"{'Ativo':<25} {'MSE':<12} {'MAE':<12}")
        print("-" * 50)
        for asset in res['asset_names']:
            print(f"{asset:<25} "
                  f"{res['mse_per_asset'][asset]:<12.4f} "
                  f"{res['mae_per_asset'][asset]:<12.4f}")

    def generate_comparison_report(self):
        """Gera relatório comparativo final"""
        print("\n" + "="*70)
        print("RELATORIO COMPARATIVO FINAL")
        print("="*70)

        # Rede 1
        print("\n" + "="*70)
        print("REDE 1 - CLASSIFICACAO DE PERFIL DE RISCO")
        print("="*70)

        if self.resultados['rede1_sintetico'] and self.resultados['rede1_hibrido']:
            self.print_rede1_comparison()
        else:
            print("Dados incompletos para comparacao")

        # Rede 2
        print("\n" + "="*70)
        print("REDE 2 - ALOCACAO DE PORTFOLIO")
        print("="*70)

        if self.resultados['rede2_sintetico'] and self.resultados['rede2_hibrido']:
            self.print_rede2_comparison()
        else:
            print("Dados incompletos para comparacao")

        # Conclusão
        self.print_conclusion()

    def print_rede1_comparison(self):
        """Imprime comparação Rede 1"""
        sint = self.resultados['rede1_sintetico']
        hibr = self.resultados['rede1_hibrido']

        print(f"\n{'Metrica':<30} {'Sintetico':<15} {'Hibrido':<15} {'Diferenca':<20}")
        print("-" * 80)

        metrics = [
            ('Amostras totais', 'n_samples', ''),
            ('Features', 'n_features', ''),
            ('Accuracy (Test)', 'accuracy_test', '%'),
            ('Precision', 'precision_weighted', '%'),
            ('Recall', 'recall_weighted', '%'),
            ('F1-Score', 'f1_weighted', '%'),
            ('CV Media', 'cv_mean', '%'),
            ('CV Desvio', 'cv_std', ''),
        ]

        for label, key, unit in metrics:
            val_sint = sint[key]
            val_hibr = hibr[key]

            if unit == '%' and key not in ['n_samples', 'n_features']:
                diff = (val_hibr - val_sint) * 100
                diff_pct = (diff / (val_sint * 100)) if val_sint != 0 else 0
                print(f"{label:<30} {val_sint*100:<15.2f} {val_hibr*100:<15.2f} "
                      f"{diff:+.2f}pp ({diff_pct:+.1f}%)")
            else:
                diff = val_hibr - val_sint
                diff_pct = (diff / val_sint * 100) if val_sint != 0 else 0
                print(f"{label:<30} {val_sint:<15.0f} {val_hibr:<15.0f} "
                      f"{diff:+.0f} ({diff_pct:+.1f}%)")

    def print_rede2_comparison(self):
        """Imprime comparação Rede 2"""
        sint = self.resultados['rede2_sintetico']
        hibr = self.resultados['rede2_hibrido']

        print(f"\n{'Metrica':<30} {'Sintetico':<15} {'Hibrido':<15} {'Diferenca':<20}")
        print("-" * 80)

        metrics = [
            ('Amostras totais', 'n_samples'),
            ('MSE (Test)', 'mse_test'),
            ('RMSE (Test)', 'rmse_test'),
            ('MAE (Test)', 'mae_test'),
            ('R² (Test)', 'r2_test'),
            ('CV Media (R²)', 'cv_mean'),
        ]

        for label, key in metrics:
            val_sint = sint[key]
            val_hibr = hibr[key]
            diff = val_hibr - val_sint
            diff_pct = (diff / val_sint * 100) if val_sint != 0 else 0

            print(f"{label:<30} {val_sint:<15.4f} {val_hibr:<15.4f} "
                  f"{diff:+.4f} ({diff_pct:+.1f}%)")

    def print_conclusion(self):
        """Imprime conclusão da comparação"""
        print("\n" + "="*70)
        print("CONCLUSAO")
        print("="*70)

        print("\nREDE 1 (Classificacao):")
        if self.resultados['rede1_hibrido']:
            hibr = self.resultados['rede1_hibrido']
            sint = self.resultados['rede1_sintetico']

            acc_diff = (hibr['accuracy_test'] - sint['accuracy_test']) * 100

            if acc_diff > 0:
                print(f"  ✓ MELHOROU: Accuracy aumentou {acc_diff:.2f} pontos percentuais")
            else:
                print(f"  ✗ PIOROU: Accuracy diminuiu {abs(acc_diff):.2f} pontos percentuais")

            print(f"\n  Explicacao:")
            if acc_diff < 0:
                print(f"  - Dataset hibrido eh mais DESAFIADOR (dados reais com ruido)")
                print(f"  - Classes BALANCEADAS (evita vies para perfil majoritario)")
                print(f"  - Modelo precisa APRENDER DE VERDADE (nao decorar padroes simples)")
                print(f"  - Menor accuracy =/= pior modelo (pode ser mais HONESTO)")
            else:
                print(f"  - Dataset maior (+{hibr['n_samples'] - sint['n_samples']} amostras)")
                print(f"  - Distribuicoes reais melhoram generalizacao")

        print("\nREDE 2 (Alocacao):")
        if self.resultados['rede2_hibrido']:
            hibr = self.resultados['rede2_hibrido']
            sint = self.resultados['rede2_sintetico']

            r2_diff = hibr['r2_test'] - sint['r2_test']

            if r2_diff > 0:
                print(f"  ✓ MELHOROU: R² aumentou {r2_diff:.4f}")
            else:
                print(f"  ✗ PIOROU: R² diminuiu {abs(r2_diff):.4f}")

            mae_diff = hibr['mae_test'] - sint['mae_test']
            if mae_diff < 0:
                print(f"  ✓ MELHOROU: MAE diminuiu {abs(mae_diff):.4f}")
            else:
                print(f"  ✗ PIOROU: MAE aumentou {mae_diff:.4f}")

    def run_full_comparison(self):
        """Executa comparação completa"""
        print("="*70)
        print("COMPARACAO COMPLETA DE METRICAS")
        print("Dataset Sintetico vs Dataset Hibrido")
        print("="*70)

        # REDE 1 - Sintético
        try:
            X, y, le, features = self.load_and_prepare_data_rede1(self.dataset_sintetico)
            self.resultados['rede1_sintetico'] = self.train_and_evaluate_rede1(
                X, y, le, "Sintetico"
            )
        except Exception as e:
            print(f"\nERRO ao processar Rede 1 (Sintetico): {e}")

        # REDE 1 - Híbrido
        try:
            X, y, le, features = self.load_and_prepare_data_rede1(self.dataset_hibrido)
            self.resultados['rede1_hibrido'] = self.train_and_evaluate_rede1(
                X, y, le, "Hibrido"
            )
        except Exception as e:
            print(f"\nERRO ao processar Rede 1 (Hibrido): {e}")

        # REDE 2 - Sintético
        try:
            X, y, features, targets = self.load_and_prepare_data_rede2(self.dataset_sintetico)
            self.resultados['rede2_sintetico'] = self.train_and_evaluate_rede2(
                X, y, "Sintetico"
            )
        except Exception as e:
            print(f"\nERRO ao processar Rede 2 (Sintetico): {e}")

        # REDE 2 - Híbrido
        try:
            X, y, features, targets = self.load_and_prepare_data_rede2(self.dataset_hibrido)
            self.resultados['rede2_hibrido'] = self.train_and_evaluate_rede2(
                X, y, "Hibrido"
            )
        except Exception as e:
            print(f"\nERRO ao processar Rede 2 (Hibrido): {e}")

        # Relatório final
        self.generate_comparison_report()

        # Salvar resultados
        self.save_results()

    def save_results(self):
        """Salva resultados em arquivo"""
        import json

        output_file = self.data_dir / 'comparacao_metricas.json'

        # Preparar dados para JSON (remover objetos numpy)
        json_data = {}
        for key, val in self.resultados.items():
            if val:
                json_data[key] = {
                    k: v for k, v in val.items()
                    if not isinstance(v, (np.ndarray, type(None)))
                }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print(f"\nResultados salvos em: {output_file}")


def main():
    comparator = MetricsComparator()
    comparator.run_full_comparison()


if __name__ == "__main__":
    main()
