# First Neural Network - Risk Profile Classifier

## 🎯 Purpose

This is the **FIRST** neural network in the dual-network architecture.
It classifies the investor's risk profile based on their personal and financial characteristics.

## 📊 What It Does

**Input**: 15 features about the investor
- Age, income, experience, knowledge, etc.

**Output**: Risk profile classification
- Conservative (Conservador)
- Moderate (Moderado)
- Aggressive (Agressivo)
- Plus a risk score from 0 to 1

## 🏗️ Architecture

- **Type**: Multi-Layer Perceptron Classifier (MLPClassifier)
- **Framework**: scikit-learn
- **Hidden Layers**: (15, 10, 5) neurons
- **Activation**: ReLU
- **Output**: 3 classes (softmax)

## 📁 Files in This Directory

### Code
- `neural_network.py` - Main implementation and training code

### Trained Models
- `neural_network.pkl` - Main production model
- `neural_network_validado.pkl` - Validated model version
- `neural_network_hibrido.pkl` - Hybrid dataset model
- `neural_network_otimizado.pkl` - Optimized model version

## 🎓 Training

```bash
cd backend/models/risk_classifier
python neural_network.py
```

This will:
1. Load training data from `backend/data/dataset_simulado.csv`
2. Train the neural network
3. Save the trained model as `neural_network.pkl`

## 📈 Performance Metrics

- **Accuracy**: 91%
- **F1-Score**: 83%
- **Cohen's Kappa**: 0.80 (substantial agreement)
- **Training Time**: < 5 seconds

## 🔄 Data Flow

```
User Input (10 fields)
    ↓
[Feature Engineering] → 15 features
    ↓
[Risk Classifier Network] ← This network
    ↓
Risk Profile + Score (0-1)
    ↓
[Portfolio Allocator Network] → Second network
```

## 💡 Usage Example

```python
from backend.models.risk_classifier.neural_network import load_model

# Load trained model
model_data = load_model()
model = model_data['model']
scaler = model_data['scaler']

# Prepare features (15 values)
features = [25, 8000, 0, 0, 2400, 2, 20000, 0, 5, 5, 30, 6, 7, 1, 0]

# Normalize and predict
features_scaled = scaler.transform([features])
prediction = model.predict(features_scaled)[0]
probabilities = model.predict_proba(features_scaled)[0]

print(f"Risk Profile: {prediction}")
print(f"Confidence: {max(probabilities):.2%}")
```

## 🔗 Integration

This network is integrated into the API at `backend/api/main.py`:

```python
# Load first network (risk classification)
model_path = Path(__file__).parent.parent / 'models' / 'risk_classifier' / 'neural_network.pkl'
dados_primeira_rede = joblib.load(str(model_path))
```

## 📚 Related Documentation

- [Complete System Explanation](../../../docs/markdown/complete_system_explanation.md)
- [API Documentation](../../api/README.md)
- [Second Network](../portfolio_allocator/README.md)

---

**This is Network 1 of 2** → Next: [Portfolio Allocator](../portfolio_allocator/)
