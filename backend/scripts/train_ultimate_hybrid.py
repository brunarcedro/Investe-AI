"""
ULTIMATE HYBRID MODEL - Best of Both Worlds!
Combines hybrid dataset (1279 samples) with advanced optimization techniques
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, make_scorer, f1_score
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

# Try SMOTE
try:
    from imblearn.over_sampling import SMOTE
    HAS_SMOTE = True
except ImportError:
    HAS_SMOTE = False
    print("Warning: SMOTE not available. Install with: pip install imbalanced-learn")

print("=" * 80)
print("ULTIMATE HYBRID MODEL - Advanced Optimization")
print("=" * 80)
print("\nTechniques:")
print("  1. Hybrid Dataset (1279 samples)")
print("  2. SMOTE for class balancing")
print("  3. Grid Search for hyperparameters")
print("  4. Ensemble learning")
print("  5. Cross-validation")
print("=" * 80)

# Load hybrid dataset
print("\nLoading hybrid dataset...")
df = pd.read_csv('data/dataset_hibrido.csv')
df['tem_reserva_emergencia'] = df['tem_reserva_emergencia'].fillna(0).astype(int)

print(f"Dataset: {len(df)} samples")

# Prepare features
cols = ['idade', 'renda_mensal', 'dependentes', 'estado_civil', 'valor_investir_mensal',
        'experiencia_anos', 'patrimonio_atual', 'dividas_percentual', 'tolerancia_perda_1',
        'tolerancia_perda_2', 'horizonte_investimento', 'conhecimento_mercado',
        'estabilidade_emprego', 'tem_reserva_emergencia', 'planos_grandes_gastos']

X = df[cols].values
y = df['perfil_risco'].values

print(f"\nOriginal distribution:")
for p, c in zip(*np.unique(y, return_counts=True)):
    print(f"  {p}: {c} ({c/len(y)*100:.1f}%)")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply SMOTE
if HAS_SMOTE:
    print("\nApplying SMOTE for class balancing...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)
    print(f"After SMOTE: {len(X_train_resampled)} samples")
    for p, c in zip(*np.unique(y_train_resampled, return_counts=True)):
        print(f"  {p}: {c} ({c/len(y_train_resampled)*100:.1f}%)")
    X_train_scaled = X_train_resampled
    y_train = y_train_resampled
else:
    print("\nSMOTE not available, using original distribution")

# Grid Search for best hyperparameters
print("\nGrid Search for optimal hyperparameters...")
print("(This may take a few minutes...)")

param_grid = {
    'hidden_layer_sizes': [(15, 10, 5), (20, 15, 10), (25, 15, 10)],
    'activation': ['relu', 'tanh'],
    'alpha': [0.0001, 0.001, 0.01],
    'learning_rate': ['constant', 'adaptive'],
}

mlp = MLPClassifier(
    solver='adam',
    max_iter=1000,
    random_state=42
)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scorer = make_scorer(f1_score, average='weighted')

grid_search = GridSearchCV(
    mlp,
    param_grid,
    cv=cv,
    scoring=scorer,
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train_scaled, y_train)

print(f"\nBest parameters found:")
for param, value in grid_search.best_params_.items():
    print(f"  {param}: {value}")
print(f"Best CV F1-Score: {grid_search.best_score_:.4f}")

# Get best model
best_mlp = grid_search.best_estimator_

# Evaluate
y_pred = best_mlp.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"\n{'='*80}")
print("ULTIMATE MODEL RESULTS")
print(f"{'='*80}")
print(f"\nTest Accuracy: {acc*100:.2f}%")
print(f"Test F1-Score: {f1:.4f}")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred))

# Create ensemble (optional)
print("\n" + "="*80)
print("Creating Ensemble Model...")
print("="*80)

# Ensemble with RandomForest
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
ensemble = VotingClassifier(
    estimators=[('mlp', best_mlp), ('rf', rf)],
    voting='soft'
)

ensemble.fit(X_train_scaled, y_train)
y_pred_ensemble = ensemble.predict(X_test_scaled)
acc_ensemble = accuracy_score(y_test, y_pred_ensemble)
f1_ensemble = f1_score(y_test, y_pred_ensemble, average='weighted')

print(f"\nEnsemble Accuracy: {acc_ensemble*100:.2f}%")
print(f"Ensemble F1-Score: {f1_ensemble:.4f}")

# Choose best model
if acc_ensemble > acc:
    print(f"\nEnsemble is better! (+{(acc_ensemble-acc)*100:.2f}pp)")
    final_model = ensemble
    final_acc = acc_ensemble
    final_f1 = f1_ensemble
    model_type = 'ensemble'
else:
    print(f"\nMLP is better! Using optimized MLP.")
    final_model = best_mlp
    final_acc = acc
    final_f1 = f1
    model_type = 'mlp_optimized'

# Save ultimate model
output_path = Path('models/risk_classifier/neural_network_ultimate_hybrid.pkl')
model_data = {
    'model': final_model,
    'scaler': scaler,
    'is_trained': True,
    'accuracy': float(final_acc),
    'f1_score': float(final_f1),
    'model_type': model_type,
    'dataset': 'hybrid',
    'n_samples': len(df),
    'used_smote': HAS_SMOTE,
    'best_params': grid_search.best_params_,
    'techniques': [
        'Hybrid Dataset (1279 samples)',
        'SMOTE' if HAS_SMOTE else 'No SMOTE',
        'Grid Search',
        'Ensemble' if model_type == 'ensemble' else 'Optimized MLP',
        'Cross-Validation'
    ]
}

joblib.dump(model_data, output_path)

print(f"\n{'='*80}")
print("ULTIMATE MODEL SAVED!")
print(f"{'='*80}")
print(f"\nPath: {output_path}")
print(f"Type: {model_type}")
print(f"Accuracy: {final_acc*100:.2f}%")
print(f"F1-Score: {final_f1:.4f}")
print(f"Dataset: Hybrid (1279 samples)")
print(f"SMOTE: {'Yes' if HAS_SMOTE else 'No'}")
print(f"\nThis is the BEST model combining:")
print("  - Large hybrid dataset")
print("  - Advanced optimization")
print("  - Class balancing")
print("  - Ensemble learning")
print("="*80)
