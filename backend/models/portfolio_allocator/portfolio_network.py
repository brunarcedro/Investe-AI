# segunda_rede_neural.py
"""
Segunda Rede Neural - Sistema de Alocação de Portfolios
Versão simplificada para teste inicial
"""

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

class SegundaRedeNeural:
    """
    Segunda rede neural para alocação de carteiras
    Input: Perfil do investidor + contexto de mercado
    Output: 6 percentuais de alocação
    """
    
    def __init__(self):
        # Configuração da rede neural
        self.model = MLPRegressor(
            hidden_layer_sizes=(100, 50),  # 2 camadas ocultas
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size='auto',
            learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=1500,  # Aumentado para evitar warning
            random_state=42,
            early_stopping=True,
            validation_fraction=0.15,
            n_iter_no_change=20
        )
        
        self.scaler = StandardScaler()
        self.trained = False
        
        # Classes de ativos
        self.asset_classes = [
            'renda_fixa',
            'acoes_brasil', 
            'acoes_internacional',
            'fundos_imobiliarios',
            'commodities',
            'criptomoedas'
        ]
    
    def gerar_dados_teste(self, n_samples=500):
        """
        Gera dados sintéticos para teste inicial
        Simula perfis de investidores e suas alocações ideais
        """
        np.random.seed(42)
        
        dados = []
        
        for i in range(n_samples):
            # Gera perfil aleatório
            idade = np.random.randint(18, 75)
            renda = np.random.uniform(1000, 50000)
            patrimonio = np.random.uniform(0, 1000000)
            experiencia = np.random.randint(0, 30)
            
            # Score de risco (0=conservador, 1=agressivo)
            if idade < 30:
                risco_base = np.random.uniform(0.5, 1.0)  # Jovens mais agressivos
            elif idade < 50:
                risco_base = np.random.uniform(0.3, 0.8)  # Meia idade moderado
            else:
                risco_base = np.random.uniform(0.0, 0.5)  # Idosos conservadores
            
            # Ajusta risco baseado em patrimônio
            if patrimonio > 500000:
                risco = min(1.0, risco_base + 0.1)
            else:
                risco = risco_base
            
            # Gera alocações baseadas no perfil
            # Lógica: quanto maior o risco, menos renda fixa e mais renda variável
            
            if risco < 0.3:  # Conservador
                alloc_rf = np.random.uniform(0.6, 0.8)
                alloc_acoes_br = np.random.uniform(0.05, 0.15)
                alloc_acoes_int = np.random.uniform(0.0, 0.1)
                alloc_fii = np.random.uniform(0.05, 0.15)
                alloc_commod = np.random.uniform(0.0, 0.05)
                alloc_crypto = 0.0
                
            elif risco < 0.6:  # Moderado
                alloc_rf = np.random.uniform(0.3, 0.5)
                alloc_acoes_br = np.random.uniform(0.15, 0.3)
                alloc_acoes_int = np.random.uniform(0.1, 0.2)
                alloc_fii = np.random.uniform(0.1, 0.2)
                alloc_commod = np.random.uniform(0.05, 0.1)
                alloc_crypto = np.random.uniform(0.0, 0.05)
                
            else:  # Agressivo
                alloc_rf = np.random.uniform(0.1, 0.3)
                alloc_acoes_br = np.random.uniform(0.25, 0.4)
                alloc_acoes_int = np.random.uniform(0.15, 0.3)
                alloc_fii = np.random.uniform(0.05, 0.15)
                alloc_commod = np.random.uniform(0.05, 0.15)
                alloc_crypto = np.random.uniform(0.05, 0.15)
            
            # Normaliza para somar 1.0
            alocacoes = np.array([alloc_rf, alloc_acoes_br, alloc_acoes_int, 
                                 alloc_fii, alloc_commod, alloc_crypto])
            alocacoes = alocacoes / alocacoes.sum()
            
            # Adiciona ruído pequeno
            alocacoes = alocacoes + np.random.normal(0, 0.01, 6)
            alocacoes = np.maximum(alocacoes, 0)  # Sem valores negativos
            alocacoes = alocacoes / alocacoes.sum()  # Renormaliza
            
            dados.append({
                'idade': idade,
                'renda': renda,
                'patrimonio': patrimonio,
                'experiencia': experiencia,
                'perfil_risco': risco,
                'horizonte': np.random.randint(1, 30),
                'tem_emergencia': np.random.choice([0, 1]),
                'conhecimento': np.random.uniform(0, 1),
                # Alocações target
                'alloc_renda_fixa': alocacoes[0],
                'alloc_acoes_brasil': alocacoes[1],
                'alloc_acoes_internacional': alocacoes[2],
                'alloc_fundos_imobiliarios': alocacoes[3],
                'alloc_commodities': alocacoes[4],
                'alloc_criptomoedas': alocacoes[5]
            })
        
        return pd.DataFrame(dados)
    
    def preparar_features(self, df):
        """
        Prepara features para treino
        """
        feature_cols = [
            'idade', 'renda', 'patrimonio', 'experiencia',
            'perfil_risco', 'horizonte', 'tem_emergencia', 'conhecimento'
        ]
        
        X = df[feature_cols].values
        
        # Normalização manual de algumas features
        X[:, 0] = X[:, 0] / 100  # idade
        X[:, 1] = X[:, 1] / 50000  # renda
        X[:, 2] = X[:, 2] / 1000000  # patrimônio
        X[:, 3] = X[:, 3] / 30  # experiência
        X[:, 5] = X[:, 5] / 30  # horizonte
        
        return X
    
    def preparar_targets(self, df):
        """
        Prepara targets (alocações)
        """
        target_cols = [
            'alloc_renda_fixa', 'alloc_acoes_brasil', 'alloc_acoes_internacional',
            'alloc_fundos_imobiliarios', 'alloc_commodities', 'alloc_criptomoedas'
        ]
        
        return df[target_cols].values
    
    def treinar(self, X, y, test_size=0.2):
        """
        Treina a rede neural
        """
        print("=" * 60)
        print("TREINANDO SEGUNDA REDE NEURAL")
        print("=" * 60)
        
        # Divide dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        print(f"Dados de treino: {X_train.shape[0]} amostras")
        print(f"Dados de teste: {X_test.shape[0]} amostras")
        print(f"Features: {X_train.shape[1]}")
        print(f"Outputs: {y_train.shape[1]}")
        
        # Normaliza features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treina modelo
        print("\nTreinando modelo...")
        self.model.fit(X_train_scaled, y_train)
        
        # Avalia
        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_test = self.model.predict(X_test_scaled)
        
        # Normaliza predições para somar 1
        y_pred_train = self.normalizar_alocacoes(y_pred_train)
        y_pred_test = self.normalizar_alocacoes(y_pred_test)
        
        # Métricas
        train_mse = mean_squared_error(y_train, y_pred_train)
        test_mse = mean_squared_error(y_test, y_pred_test)
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        
        print("\n" + "=" * 60)
        print("RESULTADOS DO TREINAMENTO")
        print("=" * 60)
        print(f"Iterações até convergência: {self.model.n_iter_}")
        print(f"\nMétricas de TREINO:")
        print(f"  MSE:  {train_mse:.6f}")
        print(f"  MAE:  {train_mae:.6f}")
        print(f"  R²:   {train_r2:.4f}")
        print(f"\nMétricas de TESTE:")
        print(f"  MSE:  {test_mse:.6f}")
        print(f"  MAE:  {test_mae:.6f}")
        print(f"  R²:   {test_r2:.4f}")
        
        # Erro por classe de ativo
        print("\n" + "-" * 60)
        print("ERRO MÉDIO POR CLASSE DE ATIVO (teste):")
        print("-" * 60)
        for i, asset in enumerate(self.asset_classes):
            mae_asset = mean_absolute_error(y_test[:, i], y_pred_test[:, i])
            print(f"  {asset:25s}: {mae_asset*100:6.2f}%")
        
        self.trained = True
        
        return {
            'train_mse': train_mse, 'test_mse': test_mse,
            'train_mae': train_mae, 'test_mae': test_mae,
            'train_r2': train_r2, 'test_r2': test_r2,
            'n_iter': self.model.n_iter_
        }
    
    def normalizar_alocacoes(self, alocacoes):
        """
        Normaliza alocações para somar 1 e serem >= 0
        """
        # Garante valores não negativos
        alocacoes = np.maximum(alocacoes, 0)
        
        # Normaliza cada linha para somar 1
        soma = alocacoes.sum(axis=1, keepdims=True)
        soma = np.maximum(soma, 0.001)  # Evita divisão por zero
        
        return alocacoes / soma
    
    def prever(self, X):
        """
        Faz predição para novos dados
        """
        if not self.trained:
            raise ValueError("Modelo não treinado!")
        
        X_scaled = self.scaler.transform(X)
        pred = self.model.predict(X_scaled)
        return self.normalizar_alocacoes(pred)
    
    def testar_exemplo(self):
        """
        Testa com alguns exemplos específicos
        """
        print("\n" + "=" * 60)
        print("TESTANDO EXEMPLOS ESPECÍFICOS")
        print("=" * 60)
        
        exemplos = [
            {
                'nome': 'Jovem Agressivo',
                'idade': 25, 'renda': 8000, 'patrimonio': 20000,
                'experiencia': 2, 'perfil_risco': 0.8,
                'horizonte': 30, 'tem_emergencia': 1, 'conhecimento': 0.6
            },
            {
                'nome': 'Conservador Aposentado',
                'idade': 65, 'renda': 15000, 'patrimonio': 800000,
                'experiencia': 20, 'perfil_risco': 0.2,
                'horizonte': 10, 'tem_emergencia': 1, 'conhecimento': 0.8
            },
            {
                'nome': 'Família Moderada',
                'idade': 40, 'renda': 20000, 'patrimonio': 200000,
                'experiencia': 10, 'perfil_risco': 0.5,
                'horizonte': 20, 'tem_emergencia': 1, 'conhecimento': 0.5
            }
        ]
        
        for exemplo in exemplos:
            nome = exemplo.pop('nome')
            
            # Prepara dados
            X_exemplo = np.array([[
                exemplo['idade'] / 100,
                exemplo['renda'] / 50000,
                exemplo['patrimonio'] / 1000000,
                exemplo['experiencia'] / 30,
                exemplo['perfil_risco'],
                exemplo['horizonte'] / 30,
                exemplo['tem_emergencia'],
                exemplo['conhecimento']
            ]])
            
            # Predição
            alocacao = self.prever(X_exemplo)[0]
            
            print(f"\n{nome}:")
            print(f"  Perfil: Risco={exemplo['perfil_risco']:.1f}, "
                  f"Horizonte={exemplo['horizonte']}a")
            print(f"  Alocação recomendada:")
            for i, asset in enumerate(self.asset_classes):
                print(f"    {asset:25s}: {alocacao[i]*100:6.2f}%")


# TESTE PRINCIPAL
if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# TESTE DA SEGUNDA REDE NEURAL - ALOCAÇÃO DE PORTFOLIOS")
    print("#" * 60)
    
    # Cria instância
    rede = SegundaRedeNeural()
    
    # Gera dados de teste
    print("\n1. Gerando dados sintéticos...")
    df = rede.gerar_dados_teste(n_samples=500)
    print(f"   ✓ {len(df)} amostras geradas")
    
    # Prepara dados
    print("\n2. Preparando features e targets...")
    X = rede.preparar_features(df)
    y = rede.preparar_targets(df)
    print(f"   ✓ Shape X: {X.shape}")
    print(f"   ✓ Shape y: {y.shape}")
    
    # Treina
    print("\n3. Treinando rede neural...")
    metricas = rede.treinar(X, y)
    
    # Testa exemplos
    print("\n4. Testando com exemplos específicos...")
    rede.testar_exemplo()
    
    # Salva modelo
    print("\n5. Salvando modelo...")
    joblib.dump({
        'model': rede.model,
        'scaler': rede.scaler,
        'asset_classes': rede.asset_classes
    }, 'segunda_rede_neural.pkl')
    print("   ✓ Modelo salvo como 'segunda_rede_neural.pkl'")
    
    print("\n" + "#" * 60)
    print("# TESTE CONCLUÍDO COM SUCESSO!")
    print("#" * 60)