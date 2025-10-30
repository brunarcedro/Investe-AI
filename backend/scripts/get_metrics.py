# Script para obter metricas da segunda rede neural
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class SegundaRedeNeural:
    def __init__(self):
        self.model = MLPRegressor(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size='auto',
            learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=1500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.15,
            n_iter_no_change=20
        )
        self.scaler = StandardScaler()
        self.trained = False
        self.asset_classes = [
            'renda_fixa', 'acoes_brasil', 'acoes_internacional',
            'fundos_imobiliarios', 'commodities', 'criptomoedas'
        ]

    def gerar_dados_teste(self, n_samples=500):
        np.random.seed(42)
        dados = []

        for i in range(n_samples):
            idade = np.random.randint(18, 75)
            renda = np.random.uniform(1000, 50000)
            patrimonio = np.random.uniform(0, 1000000)
            experiencia = np.random.randint(0, 30)

            if idade < 30:
                risco_base = np.random.uniform(0.5, 1.0)
            elif idade < 50:
                risco_base = np.random.uniform(0.3, 0.8)
            else:
                risco_base = np.random.uniform(0.0, 0.5)

            if patrimonio > 500000:
                risco = min(1.0, risco_base + 0.1)
            else:
                risco = risco_base

            if risco < 0.3:
                alloc_rf = np.random.uniform(0.6, 0.8)
                alloc_acoes_br = np.random.uniform(0.05, 0.15)
                alloc_acoes_int = np.random.uniform(0.0, 0.1)
                alloc_fii = np.random.uniform(0.05, 0.15)
                alloc_commod = np.random.uniform(0.0, 0.05)
                alloc_crypto = 0.0
            elif risco < 0.6:
                alloc_rf = np.random.uniform(0.3, 0.5)
                alloc_acoes_br = np.random.uniform(0.15, 0.3)
                alloc_acoes_int = np.random.uniform(0.1, 0.2)
                alloc_fii = np.random.uniform(0.1, 0.2)
                alloc_commod = np.random.uniform(0.05, 0.1)
                alloc_crypto = np.random.uniform(0.0, 0.05)
            else:
                alloc_rf = np.random.uniform(0.1, 0.3)
                alloc_acoes_br = np.random.uniform(0.25, 0.4)
                alloc_acoes_int = np.random.uniform(0.15, 0.3)
                alloc_fii = np.random.uniform(0.05, 0.15)
                alloc_commod = np.random.uniform(0.05, 0.15)
                alloc_crypto = np.random.uniform(0.05, 0.15)

            alocacoes = np.array([alloc_rf, alloc_acoes_br, alloc_acoes_int,
                                 alloc_fii, alloc_commod, alloc_crypto])
            alocacoes = alocacoes / alocacoes.sum()
            alocacoes = alocacoes + np.random.normal(0, 0.01, 6)
            alocacoes = np.maximum(alocacoes, 0)
            alocacoes = alocacoes / alocacoes.sum()

            dados.append({
                'idade': idade, 'renda': renda, 'patrimonio': patrimonio,
                'experiencia': experiencia, 'perfil_risco': risco,
                'horizonte': np.random.randint(1, 30),
                'tem_emergencia': np.random.choice([0, 1]),
                'conhecimento': np.random.uniform(0, 1),
                'alloc_renda_fixa': alocacoes[0],
                'alloc_acoes_brasil': alocacoes[1],
                'alloc_acoes_internacional': alocacoes[2],
                'alloc_fundos_imobiliarios': alocacoes[3],
                'alloc_commodities': alocacoes[4],
                'alloc_criptomoedas': alocacoes[5]
            })

        return pd.DataFrame(dados)

    def preparar_features(self, df):
        feature_cols = ['idade', 'renda', 'patrimonio', 'experiencia',
                        'perfil_risco', 'horizonte', 'tem_emergencia', 'conhecimento']
        X = df[feature_cols].values
        X[:, 0] = X[:, 0] / 100
        X[:, 1] = X[:, 1] / 50000
        X[:, 2] = X[:, 2] / 1000000
        X[:, 3] = X[:, 3] / 30
        X[:, 5] = X[:, 5] / 30
        return X

    def preparar_targets(self, df):
        target_cols = ['alloc_renda_fixa', 'alloc_acoes_brasil', 'alloc_acoes_internacional',
                       'alloc_fundos_imobiliarios', 'alloc_commodities', 'alloc_criptomoedas']
        return df[target_cols].values

    def normalizar_alocacoes(self, alocacoes):
        alocacoes = np.maximum(alocacoes, 0)
        soma = alocacoes.sum(axis=1, keepdims=True)
        soma = np.maximum(soma, 0.001)
        return alocacoes / soma

    def treinar(self, X, y, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model.fit(X_train_scaled, y_train)

        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_test = self.model.predict(X_test_scaled)
        y_pred_train = self.normalizar_alocacoes(y_pred_train)
        y_pred_test = self.normalizar_alocacoes(y_pred_test)

        train_mse = mean_squared_error(y_train, y_pred_train)
        test_mse = mean_squared_error(y_test, y_pred_test)
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)

        print("="*60)
        print("METRICAS DA SEGUNDA REDE NEURAL")
        print("="*60)
        print(f"\nTreinamento:")
        print(f"  MSE:  {train_mse:.6f}")
        print(f"  MAE:  {train_mae:.6f}")
        print(f"  R2:   {train_r2:.4f}")
        print(f"\nTeste:")
        print(f"  MSE:  {test_mse:.6f}")
        print(f"  MAE:  {test_mae:.6f}")
        print(f"  R2:   {test_r2:.4f}")
        print("\n" + "="*60)

        self.trained = True

        return {
            'train_mse': train_mse, 'test_mse': test_mse,
            'train_mae': train_mae, 'test_mae': test_mae,
            'train_r2': train_r2, 'test_r2': test_r2,
            'n_iter': self.model.n_iter_
        }

if __name__ == "__main__":
    rede = SegundaRedeNeural()
    df = rede.gerar_dados_teste(n_samples=500)
    X = rede.preparar_features(df)
    y = rede.preparar_targets(df)
    metricas = rede.treinar(X, y)
