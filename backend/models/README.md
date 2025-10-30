# Neural Networks - Investe-AI

This directory contains the **dual neural network architecture** that powers the Investe-AI recommendation system.

## 🧠 Two-Network Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                           │
│  (10 fields: age, income, experience, goals, etc.)      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────────┐
         │   FEATURE ENGINEERING      │
         │   (10 → 15 features)       │
         └───────────┬───────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│  🔵 NETWORK 1: Risk Profile Classifier                 │
│  📁 Directory: risk_classifier/                        │
│                                                         │
│  • Input: 15 features (investor profile)               │
│  • Output: Risk category + Score (0-1)                 │
│  • Type: MLPClassifier                                 │
│  • Classes: Conservative, Moderate, Aggressive         │
│  • Accuracy: 91%                                       │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼ (risk_score)
         ┌───────────────────────────┐
         │   CONTEXT PREPARATION      │
         │   (score + 7 features)     │
         └───────────┬───────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│  🟢 NETWORK 2: Portfolio Allocator                     │
│  📁 Directory: portfolio_allocator/                    │
│                                                         │
│  • Input: 8 features (risk_score + context)            │
│  • Output: 6 allocation percentages                    │
│  • Type: MLPRegressor                                  │
│  • Assets: Fixed Income, Stocks BR/Intl, REITs,       │
│           Commodities, Crypto                          │
│  • R² Score: > 0.85                                    │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────────┐
         │   RESPONSE ENRICHMENT      │
         │   (products, metrics,      │
         │    alerts, justification)  │
         └───────────┬───────────────┘
                     │
                     ▼
            ┌────────────────┐
            │  FINAL OUTPUT  │
            └────────────────┘
```

## 📂 Directory Structure

```
models/
├── README.md                      # This file
├── __init__.py                    # Package initialization
│
├── risk_classifier/               # 🔵 FIRST NETWORK
│   ├── README.md                  # Detailed docs for network 1
│   ├── neural_network.py          # Implementation & training
│   ├── neural_network.pkl         # Trained model (production)
│   ├── neural_network_validado.pkl
│   ├── neural_network_hibrido.pkl
│   └── neural_network_otimizado.pkl
│
└── portfolio_allocator/           # 🟢 SECOND NETWORK
    ├── README.md                  # Detailed docs for network 2
    ├── portfolio_network.py       # Implementation (SegundaRedeNeural)
    ├── portfolio_algo.py          # Rule-based algorithms (fallback)
    └── segunda_rede_neural.pkl    # Trained model (production)
```

## 🚀 Quick Start

### Understanding the Flow

1. **First, classify risk** → Use `risk_classifier/`
2. **Then, allocate portfolio** → Use `portfolio_allocator/`

### Training Networks

```bash
# Train first network (risk classification)
cd risk_classifier
python neural_network.py

# Train second network (portfolio allocation)
cd ../portfolio_allocator
python portfolio_network.py
```

### Using in API

Both networks are automatically loaded in `backend/api/main.py`:

```python
# First network
model_path = Path(__file__).parent.parent / 'models' / 'risk_classifier' / 'neural_network.pkl'
modelo_perfil = joblib.load(str(model_path))

# Second network
from backend.models.portfolio_allocator.portfolio_network import SegundaRedeNeural
model_path = Path(__file__).parent.parent / 'models' / 'portfolio_allocator' / 'segunda_rede_neural.pkl'
segunda_rede = SegundaRedeNeural()
segunda_rede.model = joblib.load(str(model_path))['model']
```

## 📊 Comparison

| Feature | Network 1 (Risk Classifier) | Network 2 (Portfolio Allocator) |
|---------|----------------------------|----------------------------------|
| **Purpose** | Classify investor risk profile | Recommend asset allocation |
| **Type** | Classification | Regression |
| **Input Size** | 15 features | 8 features |
| **Output Size** | 3 classes | 6 percentages |
| **Architecture** | MLP (15-10-5) | MLP (100-50) |
| **Main Metric** | Accuracy: 91% | R²: > 0.85 |
| **Training Time** | < 5 sec | ~10 sec |
| **Response Time** | < 50ms | < 100ms |

## 🎯 Why Two Networks?

### Separation of Concerns
- **Network 1**: Focuses on understanding the investor
- **Network 2**: Focuses on portfolio optimization

### Better Performance
- Each network specializes in its task
- Simpler architectures → faster training
- Easier to debug and improve

### Flexibility
- Can update one network without affecting the other
- Can swap algorithms independently
- Can add more networks for other tasks

## 🔄 Data Flow Example

```python
# User input
user_data = {
    "age": 25,
    "income": 8000,
    "experience": 2,
    # ... more fields
}

# Step 1: Feature engineering (10 → 15)
features_15 = engineer_features(user_data)  # [25, 8000, 0, 0, ...]

# Step 2: Risk classification (Network 1)
risk_profile, risk_score = network1.predict(features_15)
# Output: "Aggressive", 0.75

# Step 3: Context preparation (score + 7 context features → 8)
features_8 = prepare_context(user_data, risk_score)  # [0.25, 0.16, ..., 0.75]

# Step 4: Portfolio allocation (Network 2)
allocation = network2.predict(features_8)
# Output: [0.15, 0.32, 0.20, 0.10, 0.14, 0.09]
#         [RF,   BR,   Intl, FII,  Comm, Crypto]
```

## 📚 Detailed Documentation

### Network 1 (Risk Classifier)
- [Read full documentation](./risk_classifier/README.md)
- Main file: `risk_classifier/neural_network.py`
- Model: `risk_classifier/neural_network.pkl`

### Network 2 (Portfolio Allocator)
- [Read full documentation](./portfolio_allocator/README.md)
- Main file: `portfolio_allocator/portfolio_network.py`
- Model: `portfolio_allocator/segunda_rede_neural.pkl`

## 🧪 Testing

```bash
# Test both networks
cd backend
python -c "
from models.risk_classifier.neural_network import load_model
from models.portfolio_allocator.portfolio_network import SegundaRedeNeural
print('✓ Both networks loaded successfully')
"
```

## 📖 Related Documentation

- [Backend README](../README.md) - Overall backend structure
- [API Documentation](../api/README.md) - How networks integrate with API
- [Complete System Guide](../../docs/markdown/complete_system_explanation.md)

---

**Need Help?**
- Unclear about which network does what? Read the individual READMEs in each directory
- Want to train models? Follow the Quick Start guide above
- Need to modify networks? Check the source code with detailed comments
