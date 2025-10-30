# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Investe-AI** - Sistema Inteligente de Recomendação de Carteiras de Investimento

TCC (Sistemas de Informação) implementing a dual neural network system for investment portfolio recommendations targeted at young Brazilian investors (18-25 years old).

## Architecture

### Dual Neural Network System

**First Neural Network** (`backend/models/neural_network.py`):
- **Purpose**: Risk profile classification
- **Input**: 15 features describing investor profile (age, income, experience, risk tolerance, etc.)
- **Output**: Risk profile classification (conservador/moderado/agressivo) with confidence scores
- **Architecture**: MLP with hidden layers (10, 5) using ReLU activation
- **Dataset**: `backend/data/dataset_simulado.csv` (300 samples with rule-based classification)

**Second Neural Network** (`backend/segunda_rede_neural.py`):
- **Purpose**: Portfolio allocation recommendation
- **Input**: 8 features (investor profile + risk score from first network)
- **Output**: 6 allocation percentages across asset classes
- **Asset Classes**: renda_fixa, acoes_brasil, acoes_internacional, fundos_imobiliarios, commodities, criptomoedas
- **Architecture**: MLPRegressor with hidden layers (100, 50), adaptive learning rate

### API Versions

**Version 1** (`backend/main.py`):
- Basic implementation with first neural network
- Manual portfolio allocation rules
- Endpoints: `/classify-profile`, `/recommend-portfolio`

**Version 2** (`backend/main_v2.py`):
- **Recommended version** - Full dual neural network integration
- Advanced portfolio recommendations using both networks
- Enhanced endpoints: `/api/classificar-perfil`, `/api/recomendar-portfolio`, `/api/info-sistema`
- Includes product suggestions, metrics calculation (Sharpe ratio, expected returns), and personalized alerts

### Data Flow

1. User provides 15-feature profile through API
2. First network classifies risk profile and generates risk score (0-1)
3. Risk score + user context fed into second network
4. Second network outputs optimal allocation percentages
5. API enriches response with specific product recommendations, expected returns, and warnings

## Common Commands

### Setup and Installation

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt
```

Requirements: FastAPI, uvicorn, scikit-learn, pandas, numpy, yfinance, joblib

### Running the API

```bash
# Version 1 (basic)
cd backend
python main.py

# Version 2 (recommended - dual neural network)
cd backend
python main_v2.py

# Alternative with uvicorn
uvicorn main_v2:app --reload --host 0.0.0.0 --port 8000
```

API runs on `http://localhost:8000`

### Training Neural Networks

```bash
# Train first neural network (risk classification)
cd backend/models
python neural_network.py

# Train second neural network (portfolio allocation)
cd backend
python segunda_rede_neural.py

# Generate training dataset (if needed)
cd ..
python generate_dataset.py
```

### Testing the API

```bash
# Basic test (v1)
python test_api.py

# Comprehensive interactive test (v2)
python testar_api.py

# Simple neural network test
python test_neural.py
```

The `testar_api.py` script provides an interactive menu to test:
- Health check
- Profile classification
- Portfolio recommendations
- System information

## Key Implementation Details

### 15 Input Features for Risk Classification

From `generate_dataset.py` and user profile models:

1. `idade`: Age (18-100)
2. `renda_mensal`: Monthly income (R$)
3. `dependentes`: Number of dependents
4. `estado_civil`: Marital status (0=single, 1=married, 2=divorced)
5. `valor_investir_mensal`: Monthly investment amount (R$)
6. `experiencia_anos`: Years of investment experience
7. `patrimonio_atual/patrimonio_total`: Current total assets (R$)
8. `dividas_percentual`: Debt percentage
9. `tolerancia_perda_1`: Risk tolerance question 1 (1-10 scale)
10. `tolerancia_perda_2`: Risk tolerance question 2 (1-10 scale)
11. `objetivo_prazo/horizonte_investimento`: Investment horizon (years)
12. `conhecimento_mercado`: Market knowledge level (1-10 or categorical)
13. `estabilidade_emprego`: Job stability (1-10 scale)
14. `reserva_emergencia/tem_reserva_emergencia`: Has emergency fund (boolean)
15. `planos_grandes_gastos`: Plans for large expenses (boolean)

### Portfolio Allocation Strategy

The second neural network considers:
- Age-based adjustments (younger = more aggressive)
- Experience level (beginners get more conservative allocation)
- Emergency fund status (missing = increased cash reserves)
- Investment horizon (longer = more equity exposure)

Portfolio constraints:
- All allocations sum to 100%
- Non-negative allocations
- Normalized output from neural network

### Model Persistence

Trained models are saved as pickle files:
- `backend/models/neural_network.pkl`: First network (risk classification)
- `backend/models/segunda_rede_neural.pkl`: Second network (portfolio allocation)
- Models are loaded on API startup (v2) or can fall back to rule-based logic

### API Response Structure (Version 2)

**Classification Response**:
```json
{
  "perfil": "Moderado",
  "score_risco": 0.52,
  "descricao": "Equilibra segurança e crescimento",
  "caracteristicas": ["Jovem com horizonte longo", "Possui reserva de emergência"]
}
```

**Recommendation Response**:
```json
{
  "perfil_risco": "Moderado",
  "alocacao_recomendada": {
    "Renda Fixa": 35.2,
    "Ações Brasil": 28.5,
    "Ações Internacional": 18.3,
    "Fundos Imobiliários": 12.0,
    "Commodities": 5.0,
    "Criptomoedas": 1.0
  },
  "produtos_sugeridos": {...},
  "justificativa": "...",
  "alertas": ["⚠️ warnings"],
  "metricas": {
    "retorno_esperado_anual": 12.5,
    "risco_anual": 15.8,
    "sharpe_ratio": 0.85
  }
}
```

## Project Structure

```
backend/
├── main.py                      # API v1 (basic)
├── main_v2.py                   # API v2 (dual neural network)
├── segunda_rede_neural.py       # Second neural network implementation
├── coletor_dados_especialistas.py  # Expert validation data collection
├── models/
│   ├── neural_network.py        # First neural network (risk classification)
│   ├── portfolio_algo.py        # Rule-based portfolio allocator (v1)
│   ├── neural_network.pkl       # Trained first network
│   └── segunda_rede_neural.pkl  # Trained second network
├── data/
│   ├── dataset_simulado.csv     # Training data (300 samples)
│   ├── dataset_validado.csv     # Expert-validated data
│   └── validacao_especialistas.xlsx  # Expert validation results
└── requirements.txt

generate_dataset.py              # Dataset generator (root level)
test_api.py                      # API v1 test script
testar_api.py                    # API v2 interactive test script
test_neural.py                   # Neural network unit test
```

## Development Notes

- The project uses **scikit-learn's MLPClassifier** for classification and **MLPRegressor** for allocation prediction
- Dataset generation uses rule-based classification with randomness to create training data
- Risk score calculation considers multiple factors: age, income, experience, tolerance, knowledge, dependencies, emergency reserves
- The system includes validation data from financial experts (`validacao_especialistas.xlsx`)
- Version 2 (main_v2.py) is the production-ready implementation with full feature set