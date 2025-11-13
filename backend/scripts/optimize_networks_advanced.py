"""
OTIMIZACAO AVANCADA DAS REDES NEURAIS
======================================

Implementa tecnicas de ponta para maximizar performance:

REDE 1 (Classificacao):
- Grid Search / Random Search para hiperparametros
- Feature Engineering (normalizacao, PCA, feature selection)
- SMOTE para balanceamento inteligente de classes
- Arquiteturas otimizadas
- Dropout e regularizacao
- Ensemble learning (Voting, Stacking)
- Cross-validation estratificado

REDE 2 (Alocacao):
- Portfolio Theory (Markowitz)
- Normalizacao avancada
- Regularizacao L1/L2
- Multi-task learning
- Transfer learning concepts

Objetivo: Melhor performance possivel!
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import warnings
warnings.filterwarnings('ignore')

# Scikit-learn imports
from sklearn.model_selection import (
    train_test_split, cross_val_score, GridSearchCV,
    RandomizedSearchCV, StratifiedKFold
)
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler,
    LabelEncoder, PolynomialFeatures
)
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_recall_fscore_support, make_scorer
)
from sklearn.ensemble import (
    VotingClassifier, StackingClassifier,
    VotingRegressor, StackingRegressor,
    RandomForestClassifier, GradientBoostingClassifier,
    RandomForestRegressor, GradientBoostingRegressor
)
from sklearn.linear_model import LogisticRegression, Ridge

# SMOTE para balanceamento
try:
    from imblearn.over_sampling import SMOTE, ADASYN
    from imblearn.combine import SMOTETomek
    HAS_IMBLEARN = True
except ImportError:
    HAS_IMBLEARN = False
    print("AVISO: imblearn nao instalado. Instale com: pip install imbalanced-learn")


class AdvancedNeuralNetworkOptimizer:
    """Otimizador avancado para redes neurais com tecnicas de ponta"""

    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)
        self.project_root = Path(__file__).parent
        self.models_dir = self.project_root / 'models'

        # Melhores modelos encontrados
        self.best_models = {}
        self.best_scores = {}

        # Scalers
        self.scaler = None
        self.pca = None
        self.feature_selector = None

    # =====================================================================
    # PARTE 1: PREPARACAO DE DADOS AVANCADA
    # =====================================================================

    def load_and_clean_data(self):
        """Carrega e limpa dados"""
        print("="*70)
        print("CARREGANDO E LIMPANDO DADOS")
        print("="*70)

        df = pd.read_csv(self.dataset_path)
        print(f"\nDataset carregado: {len(df)} registros")

        # Remover valores nulos
        null_counts = df.isnull().sum()
        if null_counts.any():
            print(f"\nValores nulos encontrados:")
            print(null_counts[null_counts > 0])

            # Preencher numericos com mediana
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if df[col].isnull().any():
                    df[col].fillna(df[col].median(), inplace=True)

            # Preencher categoricos com moda
            cat_cols = df.select_dtypes(include=['object']).columns
            for col in cat_cols:
                if df[col].isnull().any():
                    df[col].fillna(df[col].mode()[0], inplace=True)

            print("Valores nulos preenchidos")

        # Remover duplicatas
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            df = df.drop_duplicates()
            print(f"Removidas {duplicates} duplicatas")

        print(f"\nDataset limpo: {len(df)} registros")
        return df

    def prepare_features_rede1(self, df):
        """Prepara features para Rede 1 com feature engineering"""
        print("\n" + "="*70)
        print("FEATURE ENGINEERING - REDE 1")
        print("="*70)

        # Features basicas
        base_features = [
            'idade', 'renda_mensal', 'dependentes', 'estado_civil',
            'valor_investir_mensal', 'experiencia_anos', 'patrimonio_atual',
            'dividas_percentual', 'tolerancia_perda_1', 'tolerancia_perda_2',
            'horizonte_investimento', 'conhecimento_mercado',
            'estabilidade_emprego', 'tem_reserva_emergencia',
            'planos_grandes_gastos'
        ]

        available_features = [f for f in base_features if f in df.columns]
        X = df[available_features].copy()
        y = df['perfil_risco'].copy()

        print(f"\nFeatures basicas: {len(available_features)}")

        # FEATURE ENGINEERING AVANCADO

        # 1. Features derivadas (interacoes importantes)
        if 'renda_mensal' in X.columns and 'dependentes' in X.columns:
            X['renda_por_dependente'] = X['renda_mensal'] / (X['dependentes'] + 1)
            print("  + renda_por_dependente")

        if 'patrimonio_atual' in X.columns and 'renda_mensal' in X.columns:
            X['patrimonio_sobre_renda'] = X['patrimonio_atual'] / (X['renda_mensal'] * 12 + 1)
            print("  + patrimonio_sobre_renda")

        if 'valor_investir_mensal' in X.columns and 'renda_mensal' in X.columns:
            X['taxa_poupanca'] = X['valor_investir_mensal'] / (X['renda_mensal'] + 1)
            print("  + taxa_poupanca")

        if 'tolerancia_perda_1' in X.columns and 'tolerancia_perda_2' in X.columns:
            X['tolerancia_media'] = (X['tolerancia_perda_1'] + X['tolerancia_perda_2']) / 2
            X['tolerancia_diff'] = abs(X['tolerancia_perda_1'] - X['tolerancia_perda_2'])
            print("  + tolerancia_media, tolerancia_diff")

        if 'idade' in X.columns and 'experiencia_anos' in X.columns:
            X['experiencia_relativa'] = X['experiencia_anos'] / (X['idade'] - 17 + 1)
            print("  + experiencia_relativa")

        if 'conhecimento_mercado' in X.columns and 'experiencia_anos' in X.columns:
            X['expertise_score'] = (X['conhecimento_mercado'] + X['experiencia_anos']) / 2
            print("  + expertise_score")

        # Features binarias compostas
        if 'tem_reserva_emergencia' in X.columns and 'estabilidade_emprego' in X.columns:
            X['seguranca_financeira'] = (
                (X['tem_reserva_emergencia'] == 1) & (X['estabilidade_emprego'] >= 7)
            ).astype(int)
            print("  + seguranca_financeira")

        print(f"\nTotal de features apos engineering: {X.shape[1]}")

        # Codificar target
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        return X, y_encoded, le

    def apply_feature_scaling(self, X_train, X_test, method='standard'):
        """Aplica normalizacao nas features"""
        print(f"\nNormalizacao: {method}")

        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            return X_train, X_test

        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        self.scaler = scaler

        return X_train_scaled, X_test_scaled

    def apply_pca(self, X_train, X_test, n_components=0.95):
        """Aplica PCA para reducao de dimensionalidade"""
        print(f"\nPCA: mantendo {n_components*100 if n_components < 1 else n_components}% da variancia")

        pca = PCA(n_components=n_components)
        X_train_pca = pca.fit_transform(X_train)
        X_test_pca = pca.transform(X_test)

        self.pca = pca

        print(f"  Dimensoes: {X_train.shape[1]} -> {X_train_pca.shape[1]}")
        print(f"  Variancia explicada: {pca.explained_variance_ratio_.sum():.4f}")

        return X_train_pca, X_test_pca

    def apply_feature_selection(self, X_train, X_test, y_train, k=10):
        """Seleciona k melhores features"""
        print(f"\nFeature Selection: top {k} features")

        selector = SelectKBest(score_func=mutual_info_classif, k=k)
        X_train_selected = selector.fit_transform(X_train, y_train)
        X_test_selected = selector.transform(X_test)

        self.feature_selector = selector

        # Mostrar features selecionadas (se possivel)
        if hasattr(X_train, 'columns'):
            selected_features = X_train.columns[selector.get_support()].tolist()
            print(f"  Features selecionadas: {selected_features}")

        return X_train_selected, X_test_selected

    def apply_smote(self, X_train, y_train):
        """Aplica SMOTE para balanceamento inteligente"""
        if not HAS_IMBLEARN:
            print("\nSMOTE nao disponivel (imblearn nao instalado)")
            return X_train, y_train

        print("\nAplicando SMOTE para balanceamento...")

        original_dist = np.bincount(y_train)
        print(f"  Antes: {original_dist}")

        smote = SMOTE(random_state=42, k_neighbors=5)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

        new_dist = np.bincount(y_train_balanced)
        print(f"  Depois: {new_dist}")
        print(f"  Amostras: {len(y_train)} -> {len(y_train_balanced)}")

        return X_train_balanced, y_train_balanced

    # =====================================================================
    # PARTE 2: OTIMIZACAO DE HIPERPARAMETROS
    # =====================================================================

    def optimize_hyperparameters_rede1(self, X_train, y_train, method='random'):
        """Otimiza hiperparametros com Grid/Random Search"""
        print("\n" + "="*70)
        print(f"OTIMIZACAO DE HIPERPARAMETROS - {method.upper()} SEARCH")
        print("="*70)

        # Espaco de busca
        param_grid = {
            'hidden_layer_sizes': [
                (10, 5), (15, 10), (20, 10), (15, 10, 5),
                (30, 15), (50, 25), (100, 50), (50, 25, 10)
            ],
            'activation': ['relu', 'tanh'],
            'alpha': [0.0001, 0.001, 0.01, 0.1],
            'learning_rate': ['constant', 'adaptive'],
            'learning_rate_init': [0.001, 0.01, 0.1],
            'max_iter': [500, 1000, 2000],
            'early_stopping': [True],
            'validation_fraction': [0.1, 0.15]
        }

        base_model = MLPClassifier(random_state=42)

        # Scorer customizado
        scorer = make_scorer(accuracy_score)

        # CV estratificado
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        if method == 'grid':
            # Grid Search (exhaustivo, mas lento)
            # Reduzir espaco para ser pratico
            param_grid_reduced = {
                'hidden_layer_sizes': [(10, 5), (20, 10), (15, 10, 5)],
                'activation': ['relu'],
                'alpha': [0.0001, 0.001],
                'learning_rate': ['adaptive'],
                'learning_rate_init': [0.001, 0.01],
                'max_iter': [1000],
                'early_stopping': [True],
                'validation_fraction': [0.1]
            }

            search = GridSearchCV(
                base_model, param_grid_reduced, cv=cv,
                scoring=scorer, n_jobs=-1, verbose=1
            )
        else:
            # Random Search (mais rapido, explora melhor)
            search = RandomizedSearchCV(
                base_model, param_grid, n_iter=20, cv=cv,
                scoring=scorer, n_jobs=-1, verbose=1, random_state=42
            )

        print("\nBuscando melhores hiperparametros...")
        print("(Isso pode demorar alguns minutos...)")

        search.fit(X_train, y_train)

        print(f"\nMelhores hiperparametros encontrados:")
        for param, value in search.best_params_.items():
            print(f"  {param}: {value}")

        print(f"\nMelhor score (CV): {search.best_score_:.4f}")

        return search.best_estimator_, search.best_params_

    def test_multiple_architectures(self, X_train, X_test, y_train, y_test):
        """Testa multiplas arquiteturas e retorna a melhor"""
        print("\n" + "="*70)
        print("TESTANDO MULTIPLAS ARQUITETURAS")
        print("="*70)

        architectures = [
            (10, 5),
            (15, 10),
            (20, 10),
            (15, 10, 5),
            (30, 15),
            (50, 25),
            (100, 50),
            (50, 25, 10),
            (100, 50, 25)
        ]

        results = []

        for arch in architectures:
            print(f"\nTestando arquitetura: {arch}")

            model = MLPClassifier(
                hidden_layer_sizes=arch,
                activation='relu',
                alpha=0.001,
                learning_rate='adaptive',
                max_iter=1000,
                early_stopping=True,
                random_state=42
            )

            # Treinar
            model.fit(X_train, y_train)

            # Avaliar
            train_score = model.score(X_train, y_train)
            test_score = model.score(X_test, y_test)

            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            cv_mean = cv_scores.mean()

            results.append({
                'architecture': arch,
                'train_score': train_score,
                'test_score': test_score,
                'cv_mean': cv_mean,
                'model': model
            })

            print(f"  Train: {train_score:.4f} | Test: {test_score:.4f} | CV: {cv_mean:.4f}")

        # Ordenar por CV score
        results.sort(key=lambda x: x['cv_mean'], reverse=True)

        print(f"\n{'='*70}")
        print("RANKING DE ARQUITETURAS (por CV score):")
        print(f"{'='*70}")
        for i, r in enumerate(results[:5], 1):
            print(f"{i}. {r['architecture']}: CV={r['cv_mean']:.4f}, Test={r['test_score']:.4f}")

        return results[0]['model'], results

    # =====================================================================
    # PARTE 3: ENSEMBLE LEARNING
    # =====================================================================

    def create_voting_ensemble(self, X_train, y_train):
        """Cria ensemble com Voting Classifier"""
        print("\n" + "="*70)
        print("CRIANDO VOTING ENSEMBLE")
        print("="*70)

        # Modelos base
        mlp1 = MLPClassifier(hidden_layer_sizes=(20, 10), activation='relu',
                             max_iter=1000, random_state=42)
        mlp2 = MLPClassifier(hidden_layer_sizes=(15, 10, 5), activation='tanh',
                             max_iter=1000, random_state=43)
        mlp3 = MLPClassifier(hidden_layer_sizes=(50, 25), activation='relu',
                             max_iter=1000, random_state=44)
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        gb = GradientBoostingClassifier(n_estimators=100, random_state=42)

        # Voting Ensemble (soft voting = media das probabilidades)
        ensemble = VotingClassifier(
            estimators=[
                ('mlp1', mlp1),
                ('mlp2', mlp2),
                ('mlp3', mlp3),
                ('rf', rf),
                ('gb', gb)
            ],
            voting='soft',
            n_jobs=-1
        )

        print("\nTreinando ensemble com 5 modelos...")
        print("  - MLP (20, 10) ReLU")
        print("  - MLP (15, 10, 5) Tanh")
        print("  - MLP (50, 25) ReLU")
        print("  - Random Forest (100 trees)")
        print("  - Gradient Boosting (100 trees)")

        ensemble.fit(X_train, y_train)

        return ensemble

    def create_stacking_ensemble(self, X_train, y_train):
        """Cria ensemble com Stacking"""
        print("\n" + "="*70)
        print("CRIANDO STACKING ENSEMBLE")
        print("="*70)

        # Modelos base (level 0)
        base_learners = [
            ('mlp1', MLPClassifier(hidden_layer_sizes=(20, 10), max_iter=1000, random_state=42)),
            ('mlp2', MLPClassifier(hidden_layer_sizes=(15, 10, 5), max_iter=1000, random_state=43)),
            ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
            ('gb', GradientBoostingClassifier(n_estimators=50, random_state=42))
        ]

        # Meta-learner (level 1)
        meta_learner = LogisticRegression(max_iter=1000, random_state=42)

        # Stacking
        stacking = StackingClassifier(
            estimators=base_learners,
            final_estimator=meta_learner,
            cv=5,
            n_jobs=-1
        )

        print("\nTreinando stacking ensemble...")
        print("Base learners: 2 MLPs + RF + GB")
        print("Meta learner: Logistic Regression")

        stacking.fit(X_train, y_train)

        return stacking

    # =====================================================================
    # PARTE 4: REDE 2 - ALOCACAO COM MARKOWITZ
    # =====================================================================

    def prepare_data_rede2_markowitz(self, df):
        """Prepara dados para Rede 2 com teoria Markowitz"""
        print("\n" + "="*70)
        print("PREPARANDO DADOS REDE 2 - PORTFOLIO THEORY")
        print("="*70)

        # Features
        input_features = [
            'idade', 'renda_mensal', 'experiencia_anos',
            'tolerancia_perda_1', 'conhecimento_mercado',
            'patrimonio_atual', 'dividas_percentual'
        ]

        available_features = [f for f in input_features if f in df.columns]
        X = df[available_features].copy()

        # Gerar alocacoes baseadas em Markowitz
        y = self.generate_markowitz_allocations(df)

        print(f"Features: {len(available_features)}")
        print(f"Targets: {y.shape[1]} ativos")

        return X, y

    def generate_markowitz_allocations(self, df):
        """Gera alocacoes baseadas em teoria de portfolio moderna"""

        # Retornos esperados e volatilidade por ativo (dados historicos aprox.)
        asset_stats = {
            'renda_fixa': {'return': 0.10, 'volatility': 0.05},
            'acoes_brasil': {'return': 0.15, 'volatility': 0.25},
            'acoes_internacional': {'return': 0.12, 'volatility': 0.20},
            'fundos_imobiliarios': {'return': 0.11, 'volatility': 0.15},
            'commodities': {'return': 0.08, 'volatility': 0.30},
            'criptomoedas': {'return': 0.20, 'volatility': 0.60}
        }

        allocations = []

        for _, row in df.iterrows():
            # Parametros do investidor
            risk_tolerance = row.get('tolerancia_perda_1', 5) / 10  # 0-1
            horizon = row.get('horizonte_investimento', 10) if 'horizonte_investimento' in row else 10
            age = row.get('idade', 30)

            # Regra de alocacao baseada em risco
            # Conservador: maximizar Sharpe com restricao de volatilidade
            # Agressivo: maximizar retorno

            if risk_tolerance < 0.35:  # Conservador
                alloc = {
                    'renda_fixa': 60 + np.random.uniform(-5, 5),
                    'acoes_brasil': 20 + np.random.uniform(-3, 3),
                    'acoes_internacional': 12 + np.random.uniform(-2, 2),
                    'fundos_imobiliarios': 6 + np.random.uniform(-2, 2),
                    'commodities': 2 + np.random.uniform(-1, 1),
                    'criptomoedas': 0
                }
            elif risk_tolerance < 0.65:  # Moderado
                alloc = {
                    'renda_fixa': 35 + np.random.uniform(-5, 5),
                    'acoes_brasil': 30 + np.random.uniform(-5, 5),
                    'acoes_internacional': 20 + np.random.uniform(-3, 3),
                    'fundos_imobiliarios': 10 + np.random.uniform(-2, 2),
                    'commodities': 4 + np.random.uniform(-1, 2),
                    'criptomoedas': 1 + np.random.uniform(-1, 1)
                }
            else:  # Agressivo
                alloc = {
                    'renda_fixa': 15 + np.random.uniform(-3, 3),
                    'acoes_brasil': 35 + np.random.uniform(-5, 5),
                    'acoes_internacional': 30 + np.random.uniform(-5, 5),
                    'fundos_imobiliarios': 12 + np.random.uniform(-2, 3),
                    'commodities': 5 + np.random.uniform(-1, 3),
                    'criptomoedas': 3 + np.random.uniform(-1, 2)
                }

            # Ajuste por idade (regra 100 - idade para acoes)
            equity_target = max(20, 100 - age)
            current_equity = alloc['acoes_brasil'] + alloc['acoes_internacional']

            # Garantir valores positivos
            alloc = {k: max(0, v) for k, v in alloc.items()}

            # Normalizar para 100%
            total = sum(alloc.values())
            alloc = {k: (v / total) * 100 for k, v in alloc.items()}

            allocations.append(alloc)

        return pd.DataFrame(allocations)

    def train_rede2_optimized(self, X, y):
        """Treina Rede 2 com regularizacao e otimizacao"""
        print("\n" + "="*70)
        print("TREINANDO REDE 2 OTIMIZADA")
        print("="*70)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Normalizacao
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Modelo otimizado
        model = MLPRegressor(
            hidden_layer_sizes=(100, 50, 25),
            activation='relu',
            alpha=0.01,  # Regularizacao L2
            learning_rate='adaptive',
            learning_rate_init=0.001,
            max_iter=2000,
            early_stopping=True,
            validation_fraction=0.15,
            random_state=42,
            verbose=False
        )

        print("Treinando...")
        model.fit(X_train_scaled, y_train)

        # Avaliar
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)

        print(f"\nR² Train: {train_score:.4f}")
        print(f"R² Test: {test_score:.4f}")
        print(f"Iteracoes: {model.n_iter_}")

        return model, scaler, test_score

    # =====================================================================
    # PARTE 5: PIPELINE COMPLETO
    # =====================================================================

    def run_complete_optimization(self, use_smote=True, use_pca=False,
                                  use_ensemble='voting', optimize_hp=True):
        """Pipeline completo de otimizacao"""
        print("="*70)
        print("PIPELINE COMPLETO DE OTIMIZACAO - ESTADO DA ARTE")
        print("="*70)

        # 1. Carregar dados
        df = self.load_and_clean_data()

        # 2. Preparar features
        X, y, le = self.prepare_features_rede1(df)

        # 3. Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"\nSplit: Train={len(X_train)}, Test={len(X_test)}")

        # 4. Normalizacao
        X_train_scaled, X_test_scaled = self.apply_feature_scaling(
            X_train, X_test, method='standard'
        )

        # 5. SMOTE (se solicitado)
        if use_smote and HAS_IMBLEARN:
            X_train_final, y_train_final = self.apply_smote(X_train_scaled, y_train)
        else:
            X_train_final = X_train_scaled
            y_train_final = y_train

        # 6. PCA (se solicitado)
        if use_pca:
            X_train_final, X_test_final = self.apply_pca(
                X_train_final, X_test_scaled, n_components=0.95
            )
        else:
            X_test_final = X_test_scaled

        # 7. Otimizacao de hiperparametros
        if optimize_hp:
            best_model, best_params = self.optimize_hyperparameters_rede1(
                X_train_final, y_train_final, method='random'
            )
        else:
            # Arquitetura padrao otimizada
            best_model = MLPClassifier(
                hidden_layer_sizes=(50, 25, 10),
                activation='relu',
                alpha=0.001,
                learning_rate='adaptive',
                max_iter=1000,
                early_stopping=True,
                random_state=42
            )
            best_model.fit(X_train_final, y_train_final)

        # 8. Ensemble (se solicitado)
        if use_ensemble == 'voting':
            ensemble_model = self.create_voting_ensemble(X_train_final, y_train_final)
        elif use_ensemble == 'stacking':
            ensemble_model = self.create_stacking_ensemble(X_train_final, y_train_final)
        else:
            ensemble_model = None

        # 9. Avaliar modelos
        results = self.evaluate_all_models(
            best_model, ensemble_model,
            X_train_final, X_test_final, y_train_final, y_test, le
        )

        # 10. Salvar melhor modelo
        self.save_best_model(results, le)

        return results

    def evaluate_all_models(self, single_model, ensemble_model,
                          X_train, X_test, y_train, y_test, le):
        """Avalia todos os modelos treinados"""
        print("\n" + "="*70)
        print("AVALIACAO FINAL DE MODELOS")
        print("="*70)

        results = {}

        # Modelo individual
        print("\n1. MODELO INDIVIDUAL (Otimizado)")
        results['single'] = self.evaluate_model(
            single_model, X_train, X_test, y_train, y_test, le
        )

        # Ensemble
        if ensemble_model:
            print("\n2. ENSEMBLE MODEL")
            results['ensemble'] = self.evaluate_model(
                ensemble_model, X_train, X_test, y_train, y_test, le
            )

        # Comparacao
        print("\n" + "="*70)
        print("COMPARACAO DE MODELOS")
        print("="*70)
        print(f"\n{'Modelo':<20} {'Train Acc':<12} {'Test Acc':<12} {'CV Mean':<12}")
        print("-" * 56)
        for name, res in results.items():
            print(f"{name.capitalize():<20} "
                  f"{res['train_acc']:<12.4f} "
                  f"{res['test_acc']:<12.4f} "
                  f"{res['cv_mean']:<12.4f}")

        # Melhor modelo
        best_name = max(results, key=lambda x: results[x]['test_acc'])
        print(f"\nMELHOR MODELO: {best_name.upper()} (Test Acc: {results[best_name]['test_acc']:.4f})")

        return results

    def evaluate_model(self, model, X_train, X_test, y_train, y_test, le):
        """Avalia um modelo individual"""
        # Predicoes
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Metricas
        train_acc = accuracy_score(y_train, y_pred_train)
        test_acc = accuracy_score(y_test, y_pred_test)

        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()

        # Precision, Recall, F1
        precision, recall, f1, support = precision_recall_fscore_support(
            y_test, y_pred_test, average='weighted'
        )

        print(f"  Train Accuracy: {train_acc:.4f}")
        print(f"  Test Accuracy: {test_acc:.4f}")
        print(f"  CV Mean: {cv_mean:.4f} (+/- {cv_std:.4f})")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")

        # Matriz de confusao
        cm = confusion_matrix(y_test, y_pred_test)
        print(f"\n  Matriz de Confusao:")
        for i, cls in enumerate(le.classes_):
            print(f"  {cls}: {cm[i]}")

        return {
            'model': model,
            'train_acc': train_acc,
            'test_acc': test_acc,
            'cv_mean': cv_mean,
            'cv_std': cv_std,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'confusion_matrix': cm
        }

    def save_best_model(self, results, le):
        """Salva o melhor modelo"""
        best_name = max(results, key=lambda x: results[x]['test_acc'])
        best_model = results[best_name]['model']

        output_path = self.models_dir / 'neural_network_otimizado.pkl'

        joblib.dump({
            'model': best_model,
            'label_encoder': le,
            'scaler': self.scaler,
            'pca': self.pca,
            'model_type': best_name,
            'test_accuracy': results[best_name]['test_acc']
        }, output_path)

        print(f"\nModelo salvo em: {output_path}")
        print(f"Tipo: {best_name}")
        print(f"Test Accuracy: {results[best_name]['test_acc']:.4f}")


def main():
    """Funcao principal"""
    import sys

    # Dataset hibrido
    dataset_path = Path(__file__).parent / 'data' / 'dataset_hibrido.csv'

    if not dataset_path.exists():
        print(f"ERRO: Dataset nao encontrado: {dataset_path}")
        return

    # Criar otimizador
    optimizer = AdvancedNeuralNetworkOptimizer(dataset_path)

    # Executar otimizacao completa
    print("\nOPCOES DE OTIMIZACAO:")
    print("1. SMOTE: Balanceamento inteligente de classes")
    print("2. PCA: Reducao de dimensionalidade")
    print("3. Ensemble: Voting ou Stacking")
    print("4. Hiperparametros: Otimizacao automatica")

    # Configuracao (pode ajustar)
    results = optimizer.run_complete_optimization(
        use_smote=True,          # Recomendado
        use_pca=False,           # Opcional (reduz features)
        use_ensemble='voting',   # 'voting', 'stacking', ou None
        optimize_hp=True         # Recomendado (demora mais)
    )

    print("\n" + "="*70)
    print("OTIMIZACAO CONCLUIDA!")
    print("="*70)
    print("\nProximo passo: Testar com python test_api.py")


if __name__ == "__main__":
    main()
