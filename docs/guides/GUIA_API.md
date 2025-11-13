# 🚀 GUIA RÁPIDO - API v2.0 COM DUPLA REDE NEURAL

## ✅ Status: IMPLEMENTADO E FUNCIONAL

A API v2.0 está **100% operacional** com integração completa entre as duas redes neurais.

---

## 📦 INSTALAÇÃO

### 1. Verificar Dependências
```bash
cd backend
pip install -r requirements.txt
```

### 2. Verificar Modelos Treinados
Os modelos já estão treinados e salvos em:
- `backend/models/neural_network.pkl` (36 KB) - 1ª rede
- `backend/models/segunda_rede_neural.pkl` (165 KB) - 2ª rede

---

## 🏃 COMO EXECUTAR

### Iniciar a API v2.0:
```bash
cd backend
python main_v2.py
```

Saída esperada:
```
Primeira rede neural carregada
Segunda rede neural carregada

============================================================
 SISTEMA DE INVESTIMENTOS COM DUPLA REDE NEURAL v2.0
============================================================

Primeira rede: Classificacao de perfil
Segunda rede: Alocacao de portfolio

Iniciando servidor...
------------------------------------------------------------
INFO:     Uvicorn running on http://0.0.0.0:8000
```

A API estará disponível em: **http://localhost:8000**

---

## 🧪 TESTES

### Teste Rápido (Health Check):
```bash
curl http://localhost:8000/
```

### Teste Completo Automatizado:
```bash
python test_api_v2_completo.py
```

Esperado: **5/5 testes passando**

### Teste Interativo (Menu):
```bash
python testar_api.py
```

---

## 📍 ENDPOINTS DISPONÍVEIS

### 1. Health Check
**GET** `http://localhost:8000/`

**Resposta:**
```json
{
  "status": "online",
  "versao": "2.0.0",
  "modelo_perfil": "Carregado",
  "modelo_alocacao": "Carregado",
  "timestamp": "2025-09-29T18:17:04.481762"
}
```

---

### 2. Classificar Perfil (1ª Rede Neural)
**POST** `http://localhost:8000/api/classificar-perfil`

**Body (JSON):**
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
  "descricao": "Busca maximizar retornos aceitando alta volatilidade",
  "caracteristicas": [
    "Jovem com horizonte longo",
    "Possui reserva de emergencia"
  ]
}
```

---

### 3. Recomendar Portfolio (Dupla Rede Neural)
**POST** `http://localhost:8000/api/recomendar-portfolio`

**Body (JSON):** *(mesmo formato do endpoint anterior)*

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
  "produtos_sugeridos": {
    "renda_fixa": [
      "Tesouro Selic (liquidez diária)",
      "CDB de bancos grandes (100-110% CDI)"
    ],
    "acoes_brasil": [
      "ETF BOVA11 (índice Bovespa)",
      "Ações de dividendos (BBAS3, ITUB4)"
    ]
  },
  "justificativa": "Para seu perfil Muito Arrojado, com 25 anos e horizonte de 30 anos...",
  "alertas": [
    "ALERTA: Criptomoedas são muito voláteis - invista com cuidado"
  ],
  "metricas": {
    "retorno_esperado_anual": 13.18,
    "risco_anual": 21.51,
    "sharpe_ratio": 0.07,
    "valor_projetado": 1044812.56,
    "horizonte_anos": 30
  }
}
```

---

### 4. Informações do Sistema
**GET** `http://localhost:8000/api/info-sistema`

**Resposta:**
```json
{
  "arquitetura": {
    "primeira_rede": {
      "funcao": "Classificação de perfil de risco",
      "entrada": "15 features do investidor",
      "saida": "Score de risco (0-1)",
      "status": "Operacional"
    },
    "segunda_rede": {
      "funcao": "Recomendação de alocação",
      "entrada": "8 features (perfil + contexto)",
      "saida": "6 percentuais de alocação",
      "arquitetura": "MLP com 2 camadas ocultas (100, 50)",
      "status": "Treinada"
    }
  },
  "classes_ativos": [
    "renda_fixa",
    "acoes_brasil",
    "acoes_internacional",
    "fundos_imobiliarios",
    "commodities",
    "criptomoedas"
  ],
  "versao_api": "2.0.0"
}
```

---

## 🔄 FLUXO COMPLETO DA DUPLA REDE

```
┌──────────────────┐
│  Dados Usuario   │
│  (10 campos)     │
└────────┬─────────┘
         │
         ▼
┌────────────────────────────────┐
│  1ª REDE NEURAL                │
│  (Classificação de Perfil)     │
│                                │
│  Input: 15 features            │
│  Output: Perfil + Score        │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  2ª REDE NEURAL                │
│  (Alocação de Portfolio)       │
│                                │
│  Input: Score + 7 features     │
│  Output: 6 alocações %         │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  RESPOSTA ENRIQUECIDA          │
│  - Alocação                    │
│  - Produtos                    │
│  - Métricas                    │
│  - Alertas                     │
└────────────────────────────────┘
```

---

## 📊 CAMPOS DE ENTRADA

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `idade` | int | Idade em anos (18-100) | 25 |
| `renda_mensal` | float | Renda mensal em R$ | 8000 |
| `patrimonio_total` | float | Patrimônio total em R$ | 20000 |
| `experiencia_investimento` | int | Anos de experiência (0-50) | 2 |
| `objetivo_principal` | string | Objetivo do investimento | "crescimento_patrimonio" |
| `horizonte_investimento` | int | Horizonte em anos (1-50) | 30 |
| `tolerancia_risco` | string | Tolerância ao risco | "arrojado" |
| `conhecimento_mercado` | string | Nível de conhecimento | "basico" |
| `tem_reserva_emergencia` | bool | Possui reserva? | true |
| `percentual_investir` | float | % da renda para investir (0-100) | 30 |

### Valores Válidos:

**objetivo_principal:**
- `"reserva_emergencia"`
- `"crescimento_patrimonio"`
- `"renda_passiva"`
- `"educacao_filhos"`
- `"aposentadoria"`

**tolerancia_risco:**
- `"muito_conservador"`
- `"conservador"`
- `"moderado"`
- `"arrojado"`
- `"muito_arrojado"`

**conhecimento_mercado:**
- `"nenhum"`
- `"basico"`
- `"intermediario"`
- `"avancado"`

---

## 🛠️ TROUBLESHOOTING

### Problema: "API não está respondendo"
**Solução:**
1. Verifique se o servidor está rodando: `python backend/main_v2.py`
2. Verifique se a porta 8000 está livre
3. Tente acessar: http://localhost:8000

### Problema: "Modelo não encontrado"
**Solução:**
1. Retreine a primeira rede: `python backend/models/neural_network.py`
2. Verifique arquivos: `ls -lh backend/models/*.pkl`

### Problema: "ModuleNotFoundError"
**Solução:**
```bash
cd backend
pip install fastapi uvicorn scikit-learn pandas numpy joblib
```

### Problema: "UnicodeEncodeError"
**Causa:** Emojis no console Windows
**Status:** ✅ Já corrigido na versão atual

---

## 📈 MÉTRICAS ESPERADAS

| Métrica | Valor Esperado | Observação |
|---------|----------------|------------|
| Tempo de resposta | < 100ms | Latência baixa |
| Acurácia 1ª rede | 78.3% | Com dados sintéticos |
| R² 2ª rede | > 0.85 | Alta precisão |
| Testes passando | 5/5 | 100% |

---

## 🎯 INTEGRAÇÃO COM FRONTEND

### Exemplo de requisição (JavaScript):
```javascript
const response = await fetch('http://localhost:8000/api/recomendar-portfolio', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    idade: 25,
    renda_mensal: 8000,
    patrimonio_total: 20000,
    experiencia_investimento: 2,
    objetivo_principal: "crescimento_patrimonio",
    horizonte_investimento: 30,
    tolerancia_risco: "arrojado",
    conhecimento_mercado: "basico",
    tem_reserva_emergencia: true,
    percentual_investir: 30
  })
});

const data = await response.json();
console.log(data.alocacao_recomendada);
console.log(data.metricas);
```

### Exemplo React Native:
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000';

async function recomendarPortfolio(perfilUsuario) {
  try {
    const response = await axios.post(
      `${API_URL}/api/recomendar-portfolio`,
      perfilUsuario
    );
    return response.data;
  } catch (error) {
    console.error('Erro na API:', error);
    throw error;
  }
}
```

---

## 📝 PRÓXIMAS MELHORIAS

1. **Adicionar autenticação JWT**
2. **Implementar rate limiting**
3. **Adicionar cache de respostas**
4. **Documentação Swagger/OpenAPI**
5. **Logging estruturado**
6. **Deploy em produção (Docker)**

---

## 💡 DICAS

✅ **Use sempre o endpoint de recomendação** (`/api/recomendar-portfolio`) para obter a resposta completa com dupla rede

✅ **Valide os campos no frontend** antes de enviar para a API

✅ **Trate os alertas** (`alertas`) para exibir ao usuário

✅ **Use as métricas** (`metricas`) para mostrar projeções ao usuário

✅ **Produtos sugeridos** (`produtos_sugeridos`) podem ser exibidos como cards

---

## 📞 SUPORTE

Para dúvidas ou problemas:
1. Consulte o `RELATORIO_IMPLEMENTACAO_V2.md`
2. Execute o teste automatizado: `python test_api_v2_completo.py`
3. Verifique os logs do servidor

---

**Versão:** 2.0.0
**Status:** ✅ PRODUÇÃO
**Última atualização:** 29/09/2025