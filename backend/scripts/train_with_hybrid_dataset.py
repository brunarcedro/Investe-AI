"""
Train both neural networks with the HYBRID DATASET (1279 samples)
This dataset combines real SCF data with synthetic data for better coverage
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, r2_score

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def train_network_1_hybrid():
    """Train Network 1 (Risk Classifier) with hybrid dataset"""
    print("=" * 80)
    print("TRAINING NETWORK 1: Risk Classifier with HYBRID DATASET")
    print("=" * 80)

    # Load hybrid dataset
    data_path = Path(__file__).parent.parent / 'data' / 'dataset_hibrido.csv'
    df = pd.read_csv(data_path)

    print(f"\nDataset loaded: {len(df)} samples")
    print(f"Columns: {list(df.columns)}")

    # Prepare features (15 features for network 1)
    feature_cols = [
        'idade', 'renda_mensal', 'dependentes', 'estado_civil',
        'valor_investir_mensal', 'experiencia_anos', 'patrimonio_atual',
        'dividas_percentual', 'tolerancia_perda_1', 'tolerancia_perda_2',
        'horizonte_investimento', 'conhecimento_mercado', 'estabilidade_emprego',
        'tem_reserva_emergencia', 'planos_grandes_gastos'
    ]

    X = df[feature_cols].values
    y = df['perfil_risco'].values

    print(f"\nFeatures shape: {X.shape}")
    print(f"Target distribution:")
    for perfil, count in zip(*np.unique(y, return_counts=True)):
        print(f"  {perfil}: {count} ({count/len(y)*100:.1f}%)")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    print("\nTraining MLPClassifier...")
    model = MLPClassifier(
        hidden_layer_sizes=(15, 10, 5),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=10,
        verbose=True
    )

    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n{'='*80}")
    print(f"NETWORK 1 RESULTS (Hybrid Dataset - {len(df)} samples)")
    print(f"{'='*80}")
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    output_path = Path(__file__).parent.parent / 'models' / 'risk_classifier' / 'neural_network_hybrid.pkl'
    model_data = {
        'model': model,
        'scaler': scaler,
        'is_trained': True,
        'accuracy': accuracy,
        'dataset': 'hybrid',
        'n_samples': len(df),
        'features': feature_cols
    }

    joblib.dump(model_data, output_path)
    print(f"\n✅ Model saved to: {output_path}")

    return model, scaler, accuracy

def train_network_2_hybrid():
    """Train Network 2 (Portfolio Allocator) with hybrid dataset"""
    print("\n\n" + "=" * 80)
    print("TRAINING NETWORK 2: Portfolio Allocator with HYBRID DATASET")
    print("=" * 80)

    # Load hybrid dataset
    data_path = Path(__file__).parent.parent / 'data' / 'dataset_hibrido.csv'
    df = pd.read_csv(data_path)

    print(f"\nDataset loaded: {len(df)} samples")

    # Prepare features (8 features for network 2)
    # We need to generate portfolio allocations for training
    # For now, we'll use rule-based allocations based on risk profile

    def generate_allocation(row):
        """Generate portfolio allocation based on risk profile"""
        perfil = row['perfil_risco']
        idade = row['idade']
        experiencia = row['experiencia_anos']

        if perfil == 'conservador':
            return {
                'renda_fixa': 60 + np.random.uniform(-5, 5),
                'acoes_brasil': 15 + np.random.uniform(-5, 5),
                'acoes_internacional': 10 + np.random.uniform(-5, 5),
                'fundos_imobiliarios': 10 + np.random.uniform(-3, 3),
                'commodities': 3 + np.random.uniform(-2, 2),
                'criptomoedas': 2 + np.random.uniform(-1, 1)
            }
        elif perfil == 'moderado':
            return {
                'renda_fixa': 35 + np.random.uniform(-5, 5),
                'acoes_brasil': 30 + np.random.uniform(-5, 5),
                'acoes_internacional': 20 + np.random.uniform(-5, 5),
                'fundos_imobiliarios': 10 + np.random.uniform(-3, 3),
                'commodities': 3 + np.random.uniform(-2, 2),
                'criptomoedas': 2 + np.random.uniform(-1, 1)
            }
        else:  # agressivo
            return {
                'renda_fixa': 15 + np.random.uniform(-5, 5),
                'acoes_brasil': 35 + np.random.uniform(-5, 5),
                'acoes_internacional': 25 + np.random.uniform(-5, 5),
                'fundos_imobiliarios': 10 + np.random.uniform(-3, 3),
                'commodities': 10 + np.random.uniform(-3, 3),
                'criptomoedas': 5 + np.random.uniform(-2, 2)
            }

    # Generate allocations
    allocations = df.apply(generate_allocation, axis=1)
    alloc_df = pd.DataFrame(allocations.tolist())

    # Normalize to sum to 100
    alloc_df = alloc_df.div(alloc_df.sum(axis=1), axis=0) * 100

    # Prepare features
    # Map perfil_risco to score
    perfil_map = {'conservador': 0.25, 'moderado': 0.5, 'agressivo': 0.75}
    df['risk_score'] = df['perfil_risco'].map(perfil_map)

    feature_cols = [
        'idade', 'renda_mensal', 'patrimonio_atual', 'experiencia_anos',
        'risk_score', 'horizonte_investimento', 'tem_reserva_emergencia',
        'conhecimento_mercado'
    ]

    X = df[feature_cols].values
    y = alloc_df.values

    print(f"\nFeatures shape: {X.shape}")
    print(f"Targets shape: {y.shape}")
    print(f"Asset classes: {list(alloc_df.columns)}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    print("\nTraining MLPRegressor...")
    model = MLPRegressor(
        hidden_layer_sizes=(100, 50),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=10,
        verbose=True
    )

    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)

    print(f"\n{'='*80}")
    print(f"NETWORK 2 RESULTS (Hybrid Dataset - {len(df)} samples)")
    print(f"{'='*80}")
    print(f"\nR² Score: {r2:.4f}")

    # Save model
    output_path = Path(__file__).parent.parent / 'models' / 'portfolio_allocator' / 'segunda_rede_neural_hybrid.pkl'
    model_data = {
        'model': model,
        'scaler': scaler,
        'trained': True,
        'r2_score': r2,
        'dataset': 'hybrid',
        'n_samples': len(df),
        'asset_classes': list(alloc_df.columns),
        'features': feature_cols
    }

    joblib.dump(model_data, output_path)
    print(f"\n✅ Model saved to: {output_path}")

    return model, scaler, r2

def main():
    print("\n" + "="*80)
    print("TRAINING BOTH NETWORKS WITH HYBRID DATASET (1279 samples)")
    print("="*80)
    print("\nThis will train both neural networks using the hybrid dataset")
    print("which combines real SCF data with synthetic data for better coverage.\n")

    # Train Network 1
    model1, scaler1, acc1 = train_network_1_hybrid()

    # Train Network 2
    model2, scaler2, r2_2 = train_network_2_hybrid()

    # Summary
    print("\n\n" + "="*80)
    print("TRAINING COMPLETE - SUMMARY")
    print("="*80)
    print(f"\n✅ Network 1 (Risk Classifier):")
    print(f"   - Dataset: Hybrid (1279 samples)")
    print(f"   - Accuracy: {acc1*100:.2f}%")
    print(f"   - Saved as: neural_network_hybrid.pkl")

    print(f"\n✅ Network 2 (Portfolio Allocator):")
    print(f"   - Dataset: Hybrid (1279 samples)")
    print(f"   - R² Score: {r2_2:.4f}")
    print(f"   - Saved as: segunda_rede_neural_hybrid.pkl")

    print("\n📝 NEXT STEPS:")
    print("   1. Copy hybrid models to best_model.pkl:")
    print("      cp models/risk_classifier/neural_network_hybrid.pkl models/risk_classifier/best_model.pkl")
    print("      cp models/portfolio_allocator/segunda_rede_neural_hybrid.pkl models/portfolio_allocator/best_model.pkl")
    print("   2. Restart API to use new models")
    print("   3. Test with: python api/main.py")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
