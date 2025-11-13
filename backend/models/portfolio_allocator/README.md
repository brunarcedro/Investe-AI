# Second Neural Network - Portfolio Allocator

## 🎯 Purpose

This is the **SECOND** neural network in the dual-network architecture.
It recommends personalized portfolio allocation across 6 asset classes based on the investor's risk profile and context.

## 📊 What It Does

**Input**: 8 features
- Risk score from first network (0-1)
- Age, income, assets, experience
- Investment horizon, emergency fund, knowledge

**Output**: Portfolio allocation percentages
- 6 values that sum to 100%
- One for each asset class

## 🏗️ Architecture

- **Type**: Multi-Layer Perceptron Regressor (MLPRegressor)
- **Framework**: scikit-learn
- **Hidden Layers**: (100, 50) neurons
- **Activation**: ReLU
- **Output**: 6 continuous values (normalized to sum to 1)

## 📁 Files in This Directory

### Code
- `portfolio_network.py` - Main implementation (SegundaRedeNeural class)
- `portfolio_algo.py` - Rule-based allocation algorithms (fallback)

### Trained Models
- `segunda_rede_neural.pkl` - Production model

## 🎯 Asset Classes

The network allocates across 6 investment categories:

1. **renda_fixa** - Fixed Income (Treasury bonds, CDBs)
2. **acoes_brasil** - Brazilian Stocks (Bovespa, ETFs)
3. **acoes_internacional** - International Stocks (S&P 500, global)
4. **fundos_imobiliarios** - Real Estate Funds (FIIs)
5. **commodities** - Commodities (Gold, ETFs)
6. **criptomoedas** - Cryptocurrencies (Bitcoin, Ethereum)

## 🎓 Training

```bash
cd backend/models/portfolio_allocator
python portfolio_network.py
```

This will:
1. Generate synthetic training data or load existing dataset
2. Train the neural network
3. Save the trained model as `segunda_rede_neural.pkl`

## 📈 Performance Metrics

- **R² Score**: > 0.85
- **Response Time**: < 100ms
- **Training Samples**: 500+ validated cases

## 🔄 Data Flow

```
[Risk Classifier Network] → Risk Score
    ↓
User Context (age, income, etc.)
    ↓
[Portfolio Allocator Network] ← This network
    ↓
6 Allocation Percentages
    ↓
API Response with products, metrics, alerts
```

## 💡 Usage Example

```python
from backend.models.portfolio_allocator.portfolio_network import SegundaRedeNeural
import numpy as np

# Load trained network
network = SegundaRedeNeural()
# Load model from pkl file...

# Prepare features (8 values normalized)
features = np.array([[
    0.25,  # age / 100
    0.16,  # income / 50000
    0.02,  # assets / 1000000
    0.07,  # experience / 30
    0.75,  # risk_score (from first network!)
    1.0,   # horizon / 30
    1.0,   # has_emergency_fund
    0.67   # knowledge_level
]])

# Predict allocation
allocation = network.prever(features)[0]

# Display results
asset_classes = ['renda_fixa', 'acoes_brasil', 'acoes_internacional',
                 'fundos_imobiliarios', 'commodities', 'criptomoedas']
for i, asset in enumerate(asset_classes):
    print(f"{asset}: {allocation[i]*100:.1f}%")
```

## 🔗 Integration

This network is integrated into the API at `backend/api/main.py`:

```python
# Load second network (portfolio allocation)
from backend.models.portfolio_allocator.portfolio_network import SegundaRedeNeural

model_path = Path(__file__).parent.parent / 'models' / 'portfolio_allocator' / 'segunda_rede_neural.pkl'
dados_segunda_rede = joblib.load(str(model_path))
segunda_rede = SegundaRedeNeural()
segunda_rede.model = dados_segunda_rede['model']
```

## 🎨 Key Features

### Smart Allocation Logic
- Age-based adjustment (younger → more aggressive)
- Experience consideration (beginners → more conservative)
- Emergency fund check (missing → increase cash reserves)
- Long horizon → more equity exposure

### Portfolio Constraints
- All allocations sum to 100%
- Non-negative values
- Normalized output from neural network

## 📚 Related Documentation

- [Complete System Explanation](../../../docs/markdown/complete_system_explanation.md)
- [API Documentation](../../api/README.md)
- [First Network](../risk_classifier/README.md)

---

**This is Network 2 of 2** → Previous: [Risk Classifier](../risk_classifier/)
