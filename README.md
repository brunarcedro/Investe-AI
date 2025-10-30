# 🤖 Investe-AI

> Sistema Inteligente de Recomendação de Carteiras de Investimento usando Redes Neurais Artificiais

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Sobre o Projeto

**Investe-AI** é um sistema de recomendação de investimentos desenvolvido como Trabalho de Conclusão de Curso (TCC) do curso de Sistemas de Informação. O sistema utiliza **duas redes neurais artificiais** trabalhando em conjunto para:

1. **Classificar o perfil de risco** do investidor (Conservador, Moderado ou Agressivo)
2. **Recomendar alocação personalizada** de portfólio em 6 classes de ativos

### 🎯 Público-Alvo

Jovens investidores brasileiros (18-45 anos) buscando democratização do acesso a assessoria de investimentos inteligente.

### 🏆 Resultados Alcançados

- ✅ **91% de acurácia** na classificação de perfil de risco
- ✅ **F1-Score: 83%** com validação cruzada de 90.20% (±2.32%)
- ✅ **Cohen's Kappa: 0.8026** (concordância substancial)
- ✅ **R² > 0.85** na recomendação de alocação de portfólio
- ✅ **< 50ms** tempo de resposta (classificação) e **< 100ms** (alocação)
- ✅ **1.279 casos** no dataset híbrido validado

---

## 🏗️ Arquitetura do Sistema

### Arquitetura Dual de Redes Neurais

```
┌─────────────────────┐
│   Usuário (10       │
│   informações)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│  1ª Rede Neural                 │
│  (Classificação de Perfil)      │
│                                 │
│  • Entrada: 15 features         │
│  • Arquitetura: MLP (10, 5)     │
│  • Saída: Perfil + Score (0-1)  │
│  • Acurácia: 91% | F1: 83%      │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  2ª Rede Neural                 │
│  (Alocação de Portfólio)        │
│                                 │
│  • Entrada: Score + 7 features  │
│  • Arquitetura: MLP (8-100-50-6)│
│  • Saída: 6 alocações %         │
│  • R²: > 0.85                   │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Resposta Enriquecida           │
│  • Alocação personalizada       │
│  • Produtos sugeridos           │
│  • Métricas (Sharpe, retorno)   │
│  • Alertas personalizados       │
└─────────────────────────────────┘
```

### 6 Classes de Ativos

1. 💰 **Renda Fixa** (Tesouro Direto, CDBs)
2. 📈 **Ações Brasil** (Bovespa, ETFs)
3. 🌎 **Ações Internacional** (S&P 500, MSCI World)
4. 🏢 **Fundos Imobiliários** (FIIs)
5. 🥇 **Commodities** (Ouro, ETFs)
6. ₿ **Criptomoedas** (Bitcoin, Ethereum)

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.13+
- pip

### Instalação

```bash
# Clonar o repositório
git clone https://github.com/brunarcedro/Investe-AI.git
cd Investe-AI

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r backend/requirements.txt
```

### Executar a API

```bash
# Navegar para o diretório da API
cd backend/api

# Iniciar servidor
python main.py
```

A API estará disponível em: **http://localhost:8000**

### Documentação Interativa

Acesse a documentação Swagger em: **http://localhost:8000/docs**

---

## 📡 Endpoints da API

### 1. Health Check

```http
GET /
```

**Resposta:**
```json
{
  "status": "online",
  "versao": "2.0.0",
  "modelo_perfil": "Carregado",
  "modelo_alocacao": "Carregado"
}
```

### 2. Classificar Perfil

```http
POST /api/classificar-perfil
```

**Body:**
```json
{
  "idade": 25,
  "renda_mensal": 8000,
  "patrimonio_total": 20000,
  "experiencia_investimento": 2,
  "objetivo_principal": "crescimento_patrimonio",
  "horizonte_investimento": 30,
  "tolerancia_risco": "arrojado",
  "conhecimento_mercado": "basico",
  "tem_reserva_emergencia": true,
  "percentual_investir": 30
}
```

**Resposta:**
```json
{
  "perfil": "Muito Arrojado",
  "score_risco": 0.8,
  "descricao": "Busca maximizar retornos aceitando alta volatilidade"
}
```

### 3. Recomendar Portfólio (Completo)

```http
POST /api/recomendar-portfolio
```

**Resposta:**
```json
{
  "perfil_risco": "Muito Arrojado",
  "alocacao_recomendada": {
    "Renda Fixa": 15.7,
    "Ações Brasil": 31.9,
    "Ações Internacional": 19.8,
    "Fundos Imobiliários": 9.5,
    "Commodities": 14.3,
    "Criptomoedas": 8.8
  },
  "produtos_sugeridos": {...},
  "metricas": {
    "retorno_esperado_anual": 13.18,
    "risco_anual": 21.51,
    "sharpe_ratio": 0.07
  },
  "alertas": [...]
}
```

---

## 🧪 Testes

```bash
# Executar todos os testes
python -m pytest backend/tests/

# Teste específico
python backend/tests/test_api_completo.py
```

**Cobertura:** 100% (5/5 testes passando)

---

## 📊 Dataset

O sistema foi treinado com **1.279 casos** em dataset híbrido, combinando:
- Dados sintéticos gerados com regras de negócio validadas
- Casos reais validados por especialista financeiro
- Conformidade com normas **CVM 539/2013** (Suitability) e **ANBIMA**

### Características do Dataset

| Característica | Valor |
|----------------|-------|
| Total de Casos | 1.279 |
| Features de Entrada | 15 |
| Classes de Ativos | 6 |
| Perfis de Risco | 3 (Conservador, Moderado, Agressivo) |
| Validação | Especialista + Regras de Negócio |

---

## 📁 Estrutura do Projeto

```
investe-ai/
├── backend/                          # Backend principal
│   ├── api/                          # API FastAPI v2.0
│   │   └── main.py                   # Servidor com dupla rede neural
│   ├── models/                       # Modelos de ML
│   │   ├── risk_classifier/          # Classificador de perfil de risco
│   │   │   ├── risk_network.py       # Implementação da 1ª rede neural
│   │   │   └── best_risk_classifier.pkl  # Modelo treinado (acurácia 91%)
│   │   └── portfolio_allocator/      # Alocador de portfólio
│   │       ├── portfolio_network.py  # Implementação da 2ª rede neural
│   │       └── best_portfolio_allocator.pkl  # Modelo treinado (R² > 0.85)
│   ├── data/                         # Datasets e scripts ETL
│   │   ├── dataset_hibrido.csv       # Dataset híbrido validado (1.279 casos)
│   │   ├── merge_datasets.py         # Fusão de datasets
│   │   └── validate_hybrid_dataset.py # Validação de dados
│   ├── simulacao/                    # Módulos de simulação financeira
│   │   ├── backtesting.py            # Backtesting com dados históricos reais
│   │   └── monte_carlo.py            # Simulações estocásticas
│   ├── scripts/                      # Scripts de treinamento e análise
│   │   ├── train_models.py           # Treinamento dos modelos
│   │   ├── generate_confusion_matrix.py  # Matriz de confusão
│   │   ├── generate_network_charts.py    # Visualizações das redes
│   │   ├── test_api.py               # Testes da API
│   │   └── compare_all_models.py     # Comparação de modelos
│   └── requirements.txt              # Dependências Python
├── docs/                             # Documentação do TCC
│   └── latex/                        # Arquivos LaTeX da monografia
│       └── tabelas/                  # Tabelas LaTeX
├── frontend/                         # Frontend React (em desenvolvimento)
├── LICENSE                           # Licença MIT
├── Procfile                          # Deploy Heroku
└── README.md                         # Este arquivo
```

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.13** - Linguagem principal
- **FastAPI 0.104** - Framework web moderno e rápido
- **scikit-learn 1.3.2** - Machine Learning
- **Pandas 2.1.3** - Manipulação de dados
- **NumPy 1.26.2** - Computação numérica
- **Uvicorn 0.24** - Servidor ASGI

### Machine Learning
- **Multi-Layer Perceptron (MLP)** - Redes neurais
- **StandardScaler** - Normalização z-score
- **Stratified K-Fold** - Validação cruzada
- **Adam Optimizer** - Otimização adaptativa

---

## 📈 Métricas de Desempenho

### Primeira Rede Neural (Classificação de Perfil de Risco)

| Métrica | Valor |
|---------|-------|
| Acurácia | 91,00% |
| F1-Score (macro) | 83,00% |
| Cohen's Kappa | 0,8026 (concordância substancial) |
| Validação Cruzada | 90,20% (±2,32%) |
| Tempo de Treinamento | < 5 segundos |
| Tempo de Resposta | < 50ms |
| Arquitetura | MLPClassifier (10, 5) + ReLU |

### Segunda Rede Neural (Alocação de Portfólio)

| Métrica | Valor |
|---------|-------|
| R² Score | > 0,85 |
| Tempo de Treinamento | ~10 segundos |
| Tempo de Resposta | < 100ms |
| Arquitetura | MLPRegressor (100, 50) + adaptive |
| Classes de Ativos | 6 (cobertura completa) |

### Comparação com Literatura

| Estudo | Método | Acurácia |
|--------|--------|----------|
| **Investe-AI** | **MLP** | **91,00%** ✅ |
| Costa & Oliveira (2020) | Random Forest | 89,2% |
| Rocha et al. (2022) | XGBoost | 88,4% |
| Silva et al. (2019) | SVM | 87,5% |

---

## 📚 Documentação Adicional

### Backend
- [README do Backend](backend/README.md) - Documentação detalhada do backend
- [Informações dos Modelos](backend/models/BEST_MODELS_INFO.md) - Detalhes dos modelos treinados
- [Guia de Versões](backend/models/MODEL_VERSIONS_GUIDE.md) - Histórico de versões dos modelos

### LaTeX e Monografia
- [Tabelas LaTeX](docs/latex/tabelas/) - Tabelas formatadas para a monografia

---

## 🤝 Contribuindo

Este é um projeto de TCC, mas sugestões são bem-vindas:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Autoria

**Bruna Ribeiro Cedro**
Bacharelado em Sistemas de Informação
IFES - Instituto Federal do Espírito Santo

**Orientadora:** Prof.ª Susana Bunoro

---

## 🎯 Roadmap

### ✅ Concluído
- [x] Backend com API REST
- [x] Duas redes neurais treinadas
- [x] Testes automatizados
- [x] Documentação completa

### 🚧 Em Desenvolvimento
- [ ] Frontend React Native
- [ ] Sistema de autenticação
- [ ] Dashboard de análises

### 📅 Futuro
- [ ] App mobile (iOS/Android)
- [ ] Integração com corretoras
- [ ] Machine Learning contínuo
- [ ] Análise de sentimento de mercado

---

## 📧 Contato

Para dúvidas ou sugestões:
- 📧 Email: bruna@underlinetech.com.br
- 💼 LinkedIn: [linkedin.com/in/brunarcedro](https://linkedin.com/in/brunarcedro)
- 🐙 GitHub: [@brunarcedro](https://github.com/brunarcedro)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Desenvolvido com ❤️ por Bruna Ribeiro Cedro

</div>
