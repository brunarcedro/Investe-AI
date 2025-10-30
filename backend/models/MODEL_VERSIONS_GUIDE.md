# Model Versions Guide - Investe-AI

## 🤔 Where Are My Models?

This guide explains where each model version is located and which ones you should use.

---

## 📦 PRODUCTION MODELS (USE THESE!)

### 🔵 Network 1: Risk Classifier

**Location**: `backend/models/risk_classifier/`

```
risk_classifier/
├── neural_network.py                 ✅ MAIN MODEL CODE
└── neural_network.pkl                ✅ PRODUCTION MODEL (USE THIS!)
```

**What it does**: Classifies investor risk profile (Conservative/Moderate/Aggressive)

**Status**: ✅ **PRODUCTION - Currently used by API**

---

### 🟢 Network 2: Portfolio Allocator

**Location**: `backend/models/portfolio_allocator/`

```
portfolio_allocator/
├── portfolio_network.py              ✅ MAIN MODEL CODE
└── segunda_rede_neural.pkl           ✅ PRODUCTION MODEL (USE THIS!)
```

**What it does**: Recommends portfolio allocation across 6 asset classes

**Status**: ✅ **PRODUCTION - Currently used by API**

---

## 🧪 EXPERIMENTAL MODELS (Alternative versions)

These are variations and experiments. They are NOT used in production but kept for reference.

### Network 1 Variations (in risk_classifier/)

```
risk_classifier/
├── neural_network_hibrido.pkl        🧪 EXPERIMENTAL
│   ├── Trained with hybrid dataset (SCF data + synthetic)
│   ├── Purpose: Testing with real financial data
│   └── Status: Experiment - not in production
│
└── neural_network_otimizado.pkl      🧪 EXPERIMENTAL
    ├── Optimized hyperparameters version
    ├── Purpose: Testing optimization techniques
    └── Status: Experiment - not in production
```

**Why keep them?**
- For comparing performance with production model
- For research and future improvements
- For thesis documentation (showing different approaches)

---

## 🗄️ ARCHIVED MODELS (Old/Deprecated)

**Location**: `backend/archived/`

```
archived/
├── modelo_ultimate.py                ❌ DEPRECATED
│   ├── Ultimate combined model experiment
│   ├── Tried to merge both networks into one
│   └── Conclusion: Dual network works better
│
├── modelo_ultimate.pkl               ❌ DEPRECATED
│   └── Trained version of above
│
└── retreinar_com_hibrido.py          ❌ DEPRECATED
    └── Script to retrain with hybrid dataset
```

**Why archived?**
- Replaced by better dual-network approach
- Kept for historical reference
- Not maintained or used

---

## 📊 DATASETS

### Production Dataset
```
backend/data/
└── dataset_simulado.csv              ✅ MAIN DATASET
    ├── 300 samples for Network 1
    ├── Rule-based generation
    └── Used for production training
```

### Experimental Datasets
```
backend/data/
├── dataset_hibrido.csv               🧪 EXPERIMENTAL
│   ├── Hybrid dataset (SCF data + synthetic)
│   ├── Purpose: Test with real financial data
│   └── Used by: neural_network_hibrido.pkl
│
├── dataset_from_scf.csv              🧪 RAW DATA
│   └── Raw data from Survey of Consumer Finances
│
└── scf_simulated_data.csv            🧪 RAW DATA
    └── Simulated SCF-based data
```

---

## 🎯 WHICH MODEL SHOULD I USE?

### For Production/API
```python
# Network 1 (Risk Classification)
model_path = 'backend/models/risk_classifier/neural_network.pkl'

# Network 2 (Portfolio Allocation)
model_path = 'backend/models/portfolio_allocator/segunda_rede_neural.pkl'
```

### For Research/Comparison
```python
# Try hybrid dataset version
model_path = 'backend/models/risk_classifier/neural_network_hibrido.pkl'

# Try optimized version
model_path = 'backend/models/risk_classifier/neural_network_otimizado.pkl'
```

### For Historical Reference
```python
# Old ultimate model (not recommended)
model_path = 'backend/archived/modelo_ultimate.pkl'
```

---

## 🔄 MODEL EVOLUTION TIMELINE

```
Phase 1: Single Network Approach (Archived)
    └── modelo_ultimate.py
        └── ❌ Didn't work well

Phase 2: Dual Network - Basic (Archived)
    └── Old versions in archived/
        └── ⚠️ Replaced by better versions

Phase 3: Dual Network - Production ✅
    ├── risk_classifier/neural_network.pkl
    └── portfolio_allocator/segunda_rede_neural.pkl
        └── ✅ Currently in use

Phase 4: Experimental Improvements 🧪
    ├── neural_network_hibrido.pkl (hybrid data)
    └── neural_network_otimizado.pkl (optimized)
        └── 🧪 Testing alternatives
```

---

## 📁 FULL DIRECTORY STRUCTURE

```
backend/models/
│
├── README.md                          # Overview of dual architecture
├── MODEL_VERSIONS_GUIDE.md            # This file
│
├── risk_classifier/                   # 🔵 NETWORK 1
│   ├── README.md                      # Detailed docs
│   ├── neural_network.py              # ✅ Production code
│   ├── neural_network.pkl             # ✅ Production model
│   ├── neural_network_hibrido.pkl     # 🧪 Experimental
│   └── neural_network_otimizado.pkl   # 🧪 Experimental
│
├── portfolio_allocator/               # 🟢 NETWORK 2
│   ├── README.md                      # Detailed docs
│   ├── portfolio_network.py           # ✅ Production code
│   ├── segunda_rede_neural.pkl        # ✅ Production model
│   └── portfolio_algo.py              # Rule-based fallback
│
└── [Old files moved to archived/]
```

---

## ❓ FAQ

### Q: Why so many model versions?

**A**: We experimented with different approaches:
- **Production models**: What works best and is currently used
- **Experimental models**: Testing improvements (hybrid data, optimization)
- **Archived models**: Old approaches that didn't work out

### Q: Should I delete the experimental models?

**A**: No! Keep them for:
1. Comparing performance in your thesis
2. Showing different approaches you tried
3. Future reference and improvements

### Q: Which model is the "best"?

**A**: The **production models** (`neural_network.pkl` and `segunda_rede_neural.pkl`) are the best for actual use. They have:
- Best balance of accuracy and performance
- Proven in API with 91% accuracy
- Simplest architecture (easier to maintain)

### Q: What's the difference between "otimizado" and "hibrido"?

**A**:
- **otimizado**: Same architecture, tuned hyperparameters
- **hibrido**: Same architecture, trained on hybrid dataset (real + synthetic data)

### Q: Can I train my own version?

**A**: Yes!
```bash
# Train production model
cd backend/models/risk_classifier
python neural_network.py

# Train with hybrid data
python neural_network.py --dataset=hybrid
```

---

## 🎓 FOR YOUR THESIS

### Models to Mention

1. **Main Approach**: Dual neural network (production models)
   - Explain why this architecture was chosen
   - Show the 91% accuracy results

2. **Experiments**: Mention the alternative versions
   - Hybrid dataset attempt
   - Optimization attempts
   - Ultimate model attempt (didn't work)

3. **Conclusion**: Dual network with production models is best
   - Better accuracy
   - Faster training
   - Easier to maintain

### Metrics to Compare

Create a table like this in your thesis:

| Model Version | Accuracy | Training Time | Dataset | Status |
|---------------|----------|---------------|---------|--------|
| Production (dual) | 91% | < 5s | Synthetic | ✅ In use |
| Hybrid dataset | ~89% | ~8s | Real+Synthetic | 🧪 Experiment |
| Optimized | ~90% | ~6s | Synthetic | 🧪 Experiment |
| Ultimate (single) | ~75% | ~15s | Synthetic | ❌ Deprecated |

---

## 📞 Quick Reference

**Need production model?** → `risk_classifier/neural_network.pkl`

**Need portfolio model?** → `portfolio_allocator/segunda_rede_neural.pkl`

**Want to experiment?** → Try files ending in `_hibrido.pkl` or `_otimizado.pkl`

**Looking at old code?** → Check `archived/` directory

**More details?** → Read README.md in each model directory

---

**Last Updated**: October 29, 2025
**Status**: All models organized and documented
