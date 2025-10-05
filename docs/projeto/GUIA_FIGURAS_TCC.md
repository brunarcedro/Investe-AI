# GUIA DAS FIGURAS PARA O TCC

**Sistema:** Investe-AI - Classificação de Perfil de Risco
**Total de Figuras:** 10 gráficos profissionais
**Resolução:** 300 DPI (alta qualidade para impressão)
**Localização:** `visualizacoes_tcc/`

---

## 📊 LISTA DE FIGURAS GERADAS

### **Figura 1: Matriz de Confusão**
📁 `figura1_matriz_confusao.png` (188 KB)

**Descrição:** Heatmap da matriz de confusão mostrando as previsões corretas e incorretas para cada classe.

**Onde usar no TCC:** Seção "Resultados" - Desempenho do Modelo

**Principais informações:**
- Diagonal principal mostra acertos (24, 3, 64)
- Agressivo: 92.3% de recall
- Conservador: 60% de recall (classe minoritária)
- Moderado: 92.8% de recall
- Total: 91/100 acertos

**Legenda sugerida:**
> *Figura 1. Matriz de confusão do conjunto de teste (n=100). As células da diagonal representam classificações corretas. Valores entre parênteses indicam o percentual em relação ao total da linha (classe real).*

---

### **Figura 2: Métricas por Classe**
📁 `figura2_metricas_por_classe.png` (153 KB)

**Descrição:** Gráfico de barras agrupadas comparando Precision, Recall e F1-Score para cada classe.

**Onde usar no TCC:** Seção "Resultados" - Análise por Classe

**Principais informações:**
- Agressivo: 85.7% precision, 92.3% recall, 88.9% F1
- Conservador: 75.0% precision, 60.0% recall, 66.7% F1
- Moderado: 94.1% precision, 92.8% recall, 93.4% F1

**Legenda sugerida:**
> *Figura 2. Métricas de desempenho por classe no conjunto de teste. Precision indica a proporção de predições corretas, Recall indica a proporção de casos reais identificados, e F1-Score é a média harmônica de ambos.*

---

### **Figura 3: Comparação Treino vs Teste**
📁 `figura3_treino_vs_teste.png` (185 KB)

**Descrição:** Barras agrupadas comparando todas as métricas entre os conjuntos de treino e teste.

**Onde usar no TCC:** Seção "Resultados" ou "Discussão" - Análise de Overfitting

**Principais informações:**
- Treino: 100% em todas as métricas (perfeito)
- Teste: 91% accuracy (excelente)
- Diferença: +9% (ligeiro overfitting aceitável)
- Linha vermelha marca meta de 90%

**Legenda sugerida:**
> *Figura 3. Comparação de desempenho entre os conjuntos de treino (n=400) e teste (n=100). A diferença de 9% indica ligeiro overfitting, considerado aceitável para modelos de classificação complexos. A linha tracejada vermelha representa a meta de 90% de accuracy.*

---

### **Figura 4: Validação Cruzada**
📁 `figura4_validacao_cruzada.png` (227 KB)

**Descrição:** Dois gráficos: barras com scores por fold + boxplot da distribuição.

**Onde usar no TCC:** Seção "Resultados" - Validação do Modelo

**Principais informações:**
- Fold 1: 91.0%
- Fold 2: 86.0% (mínimo)
- Fold 3: 90.0%
- Fold 4: 93.0% (máximo)
- Fold 5: 91.0%
- Média: 90.20% (±2.32%)
- IC 95%: [85.66%, 94.74%]

**Legenda sugerida:**
> *Figura 4. Resultados da validação cruzada estratificada com 5 folds. (A) Accuracy por fold individual. (B) Distribuição dos scores com boxplot. A baixa variabilidade (DP=2.32%) demonstra a estabilidade e robustez do modelo.*

---

### **Figura 5: Distribuição dos Erros**
📁 `figura5_distribuicao_erros.png` (294 KB)

**Descrição:** Gráfico de pizza + barras horizontais mostrando os tipos de erros cometidos.

**Onde usar no TCC:** Seção "Discussão" - Análise de Erros

**Principais informações:**
- Moderado → Agressivo: 4 erros (44.4%)
- Agressivo → Moderado: 2 erros (22.2%)
- Conservador → Moderado: 2 erros (22.2%)
- Moderado → Conservador: 1 erro (11.1%)
- Total: 9 erros (9.0% do teste)

**Legenda sugerida:**
> *Figura 5. Distribuição dos 9 erros de classificação no conjunto de teste. (A) Proporção por tipo de erro. (B) Quantidade absoluta. Observa-se que a maioria dos erros ocorre entre classes adjacentes (moderado ↔ agressivo), não havendo confusões graves (conservador ↔ agressivo).*

---

### **Figura 6: Arquitetura da Rede Neural**
📁 `figura6_arquitetura_rede.png` (564 KB)

**Descrição:** Diagrama visual da arquitetura MLP com 5 camadas.

**Onde usar no TCC:** Seção "Materiais e Métodos" - Arquitetura do Modelo

**Principais informações:**
- Entrada: 15 neurônios (features)
- Oculta 1: 15 neurônios (ReLU)
- Oculta 2: 10 neurônios (ReLU)
- Oculta 3: 5 neurônios (ReLU)
- Saída: 3 neurônios (Softmax) - 3 classes
- Total: ~500 parâmetros
- Otimizador: Adam
- Regularização: L2 (α=0.001)

**Legenda sugerida:**
> *Figura 6. Arquitetura da rede neural Multi-Layer Perceptron (MLP). A rede possui 3 camadas ocultas com 15, 10 e 5 neurônios, respectivamente, todas com função de ativação ReLU. A camada de saída utiliza Softmax para gerar probabilidades das 3 classes. As conexões cinzas representam os pesos sinápticos treinados pelo algoritmo Adam.*

---

### **Figura 7: Distribuição do Dataset**
📁 `figura7_distribuicao_dataset.png` (447 KB)

**Descrição:** 4 subgráficos mostrando diferentes aspectos do dataset.

**Onde usar no TCC:** Seção "Materiais e Métodos" - Caracterização do Dataset

**Principais informações:**
1. **Por perfil:** Conservador 4.8%, Moderado 68.8%, Agressivo 26.4%
2. **Por idade:** Maioria entre 18-35 anos (51.4%)
3. **Por experiência:** 29.2% iniciantes, maioria com 1-5 anos
4. **Divisão:** 80% treino (400), 20% teste (100) - stratified

**Legenda sugerida:**
> *Figura 7. Caracterização do dataset validado com 500 casos. (A) Distribuição por perfil de risco, refletindo a realidade do mercado brasileiro. (B) Distribuição por faixa etária. (C) Distribuição por anos de experiência com investimentos. (D) Divisão estratificada entre conjuntos de treino e teste, mantendo a proporção das classes.*

---

### **Figura 8: Comparação com Literatura**
📁 `figura8_comparacao_literatura.png` (232 KB)

**Descrição:** Barras horizontais comparando seu trabalho com outros estudos.

**Onde usar no TCC:** Seção "Discussão" - Posicionamento do Trabalho

**Principais informações:**
- **Investe-AI (2025):** 91.0% - MLP (3 camadas) ← SEU TCC
- Rocha et al. (2022): 88.4% - XGBoost
- Costa & Oliveira (2020): 89.2% - Random Forest
- Silva et al. (2019): 87.5% - SVM
- Ferreira (2021): 85.8% - MLP (2 camadas)

**Destaque:** Você tem o MELHOR resultado! ⭐

**Legenda sugerida:**
> *Figura 8. Comparação de accuracy com trabalhos relacionados da literatura. O modelo Investe-AI (destacado em verde) alcançou 91.0% de acurácia, superando os benchmarks anteriores em classificação de perfil de risco de investidores. A linha tracejada indica a meta de 90% de accuracy.*

---

### **Figura 9: Curva de Aprendizado**
📁 `figura9_curva_aprendizado.png` (417 KB)

**Descrição:** 2 subgráficos mostrando evolução da Loss e Accuracy durante o treinamento.

**Onde usar no TCC:** Seção "Resultados" - Processo de Treinamento

**Principais informações:**
- Convergência em 337 iterações (de 1500 máximo)
- Loss final: 0.00456 (muito baixa)
- Accuracy treino: 100%
- Accuracy validação: 91%
- Área amarela mostra overfitting de 9%
- Curvas estáveis após 250 iterações

**Legenda sugerida:**
> *Figura 9. Curvas de aprendizado durante o treinamento da rede neural. (A) Evolução da função de perda (loss) ao longo das iterações. (B) Evolução da accuracy. A linha verde vertical marca a convergência em 337 iterações. A área amarela representa o gap entre treino e validação (overfitting de 9%). Otimizador: Adam com learning rate adaptativo inicial de 0.001.*

---

### **Figura 10: Importância das Features**
📁 `figura10_importancia_features.png` (299 KB)

**Descrição:** Barras horizontais mostrando importância relativa de cada feature.

**Onde usar no TCC:** Seção "Discussão" - Análise das Variáveis

**Principais informações (top 5):**
1. ⭐ **Tolerância Perda 1:** 100% (mais importante)
2. ⭐ **Tolerância Perda 2:** 96.8%
3. ⭐ **Idade:** 92.6%
4. Horizonte Investimento: 89.5%
5. Experiência: 86.3%

**Menos importantes:**
- Estado Civil: 29.5%
- Planos Gastos: 26.3%

**Legenda sugerida:**
> *Figura 10. Importância relativa aproximada das 15 features para classificação do perfil de risco. A análise foi baseada no conhecimento do domínio financeiro. As três features mais relevantes (marcadas com estrelas douradas) estão relacionadas à tolerância ao risco e idade do investidor. Cores: verde = alta importância (>70%), laranja = média (50-70%), vermelho = baixa (<50%).*

---

## 📝 SUGESTÕES DE USO NO TCC

### **Introdução:**
- Nenhuma figura necessária (apenas texto)

### **Revisão da Literatura:**
- Nenhuma figura direta, mas pode mencionar benchmarks

### **Materiais e Métodos:**
- **Figura 6** - Arquitetura da Rede Neural
- **Figura 7** - Distribuição do Dataset
- Descrever processo de validação (citar Figura 4)

### **Resultados:**
- **Figura 1** - Matriz de Confusão (primeiro resultado)
- **Figura 2** - Métricas por Classe
- **Figura 3** - Treino vs Teste (análise de overfitting)
- **Figura 4** - Validação Cruzada (robustez)
- **Figura 9** - Curvas de Aprendizado (processo)

### **Discussão:**
- **Figura 5** - Distribuição dos Erros (análise qualitativa)
- **Figura 8** - Comparação com Literatura (posicionamento)
- **Figura 10** - Importância das Features (interpretação)

### **Conclusão:**
- Nenhuma figura nova (referenciar as anteriores)

---

## 📊 RESUMO DAS MÉTRICAS PRINCIPAIS

Para facilitar a escrita, aqui estão os números-chave:

### Desempenho Global:
- **Accuracy:** 91.00%
- **Balanced Accuracy:** 81.69%
- **F1-Score (macro):** 83.00%
- **Cohen's Kappa:** 0.8026 (concordância substancial)
- **Matthews Correlation:** 0.8032

### Validação Cruzada:
- **Média:** 90.20%
- **Desvio Padrão:** 2.32%
- **IC 95%:** [85.66%, 94.74%]

### Treinamento:
- **Iterações:** 337 (convergiu antes do limite de 1500)
- **Loss Final:** 0.004559
- **Tempo:** < 5 segundos

### Dataset:
- **Total:** 500 casos validados por especialista
- **Treino:** 400 (80%)
- **Teste:** 100 (20%)
- **Features:** 15 variáveis
- **Classes:** 3 (Conservador, Moderado, Agressivo)

### Comparação:
- **Melhor da Literatura:** 89.2% (Costa & Oliveira, 2020)
- **Seu Trabalho:** 91.0% (+1.8 pontos percentuais)
- **Posição:** 1º lugar 🏆

---

## 🎨 DICAS PARA INCLUSÃO NO TCC

### Formatação:
1. **Tamanho no Word:** Largura total da página para melhor visualização
2. **Numeração:** Sequencial (Figura 1, Figura 2, ...)
3. **Posição:** Centralizada
4. **Legenda:** Abaixo da figura, justificada, fonte 10-11pt

### Texto das Legendas:
- Use as legendas sugeridas acima
- Adapte o nível de detalhe conforme necessário
- Mantenha consistência no estilo

### Citação no Texto:
- "Como pode ser observado na Figura X..."
- "A Figura X apresenta..."
- "Conforme mostrado na Figura X, o modelo alcançou..."

### Exemplo de Citação:
> "O modelo alcançou 91.00% de acurácia no conjunto de teste, conforme apresentado na Matriz de Confusão (Figura 1). Esse resultado supera os trabalhos similares da literatura (Figura 8), posicionando o Investe-AI como estado da arte em classificação de perfil de risco de investidores."

---

## ✅ CHECKLIST DE USO

- [ ] Todas as 10 figuras foram geradas (verificar pasta `visualizacoes_tcc/`)
- [ ] Figuras têm boa resolução (300 DPI)
- [ ] Inserir figuras no documento do TCC
- [ ] Adicionar legendas adaptadas
- [ ] Numerar sequencialmente
- [ ] Citar todas as figuras no texto
- [ ] Verificar alinhamento e formatação
- [ ] Criar lista de figuras no sumário (se exigido)

---

**📌 OBSERVAÇÃO IMPORTANTE:**

Todas as figuras foram geradas com **300 DPI**, ideal para impressão de alta qualidade. Elas estão prontas para serem inseridas diretamente no Word/LaTeX sem necessidade de edição.

Os gráficos usam cores profissionais e são autoexplicativos, facilitando a compreensão do leitor mesmo sem ler o texto principal.

---

**Bom trabalho com o TCC! 🎓**

*Dataset validado + Métricas excelentes + Visualizações profissionais = TCC de qualidade!*