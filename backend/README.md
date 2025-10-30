# Backend - Investe-AI

Sistema de recomendação de carteiras de investimento com dupla rede neural.

## Estrutura de Diretórios

```
backend/
├── api/                        # API FastAPI
│   └── main.py                 # API principal (versão 2.0)
├── models/                     # Modelos de ML
│   ├── neural_network.py       # Primeira rede (classificação de perfil)
│   ├── neural_network.pkl      # Modelo treinado da primeira rede
│   ├── segunda_rede_neural.pkl # Modelo treinado da segunda rede
│   └── portfolio_algo.py       # Algoritmos de portfolio
├── data/                       # Dados de treinamento
│   ├── dataset_simulado.csv    # Dataset principal (300 amostras)
│   └── dataset_validado.csv    # Dataset validado por especialistas
├── simulacao/                  # Módulos de simulação
│   ├── backtesting.py          # Backtesting com dados reais
│   └── monte_carlo.py          # Simulações Monte Carlo
├── scripts/                    # Scripts auxiliares
│   ├── gerar_graficos_apresentacao.py
│   ├── gerar_matriz_confusao_slide.py
│   ├── comparar_metricas_completo.py
│   ├── otimizar_redes_avancado.py
│   └── testar_api_otimizada.py
├── outputs/                    # Outputs gerados
│   ├── graficos/               # Gráficos PNG
│   └── tabelas/                # (removido - agora em docs/latex)
├── archived/                   # Versões antigas arquivadas
│   ├── api_otimizada.py
│   ├── modelo_ultimate.py
│   └── frontend_streamlit.py
├── models/
│   └── portfolio_network.py     # Second network (portfolio allocation)
└── requirements.txt            # Dependências Python
```

## Arquitetura do Sistema

### Primeira Rede Neural
- **Arquivo**: `models/neural_network.py`
- **Função**: Classificação de perfil de risco
- **Entrada**: 15 features do investidor
- **Saída**: Perfil de risco (conservador/moderado/agressivo) + score (0-1)
- **Modelo**: MLPClassifier do scikit-learn

### Second Neural Network (Portfolio Allocation)
- **File**: `models/portfolio_network.py`
- **Function**: Portfolio allocation recommendation
- **Input**: 8 features (risk profile + investor context)
- **Output**: 6 allocation percentages across asset classes
- **Model**: MLPRegressor from scikit-learn

### API FastAPI
- **Arquivo**: `api/main.py`
- **Versão**: 2.0 (com dupla rede neural integrada)
- **Endpoints principais**:
  - `POST /api/classificar-perfil` - Classifica perfil de risco
  - `POST /api/recomendar-portfolio` - Recomenda alocação personalizada
  - `POST /api/simular-backtesting` - Simula com dados históricos
  - `POST /api/projetar-monte-carlo` - Projeta cenários futuros

## Como Executar

### Instalação

```bash
cd backend
pip install -r requirements.txt
```

### Treinar Modelos (Opcional)

```bash
# Train first network (risk classification)
cd models
python neural_network.py

# Train second network (portfolio allocation)
python portfolio_network.py
```

### Executar API

```bash
# Método 1
python api/main.py

# Método 2
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## Scripts Auxiliares

Scripts in `scripts/` folder are tools for analysis and optimization:

- **Generate charts**: `python scripts/generate_presentation_charts.py`
- **Optimize networks**: `python scripts/optimize_networks_advanced.py`
- **Test API**: `python scripts/test_api.py`
- **Compare metrics**: `python scripts/compare_metrics.py`

## Arquivos Arquivados

Versões antigas e experimentais foram movidas para `archived/`:

- `api_otimizada.py` / `api_otimizada_v4.py` - Versões antigas da API
- `modelo_ultimate.py` - Modelo experimental
- `frontend_streamlit.py` - Interface Streamlit (substituída pelo frontend React)

Esses arquivos são mantidos para referência, mas não são usados na versão de produção.

## Dependências Principais

- FastAPI - Framework web
- scikit-learn - Modelos de machine learning
- pandas / numpy - Manipulação de dados
- yfinance - Dados financeiros reais
- joblib - Persistência de modelos

Ver `requirements.txt` para lista completa.

## Documentação Completa

- Documentação em Markdown: [../docs/markdown/](../docs/markdown/)
- Guias de API: [../docs/guides/GUIA_API.md](../docs/guides/GUIA_API.md)
- Resultados completos: [../docs/markdown/RESULTADOS_FINAIS_COMPLETO.md](../docs/markdown/RESULTADOS_FINAIS_COMPLETO.md)
