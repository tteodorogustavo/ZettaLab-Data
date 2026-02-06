# Planejamento Desafio II - Ciência e Governança de Dados

## Modelagem Preditiva e Recomendações Estratégicas

---

### Informações do Projeto

| Campo | Valor |
|-------|-------|
| **Autor** | Gustavo Teodoro |
| **Programa** | Zetta Lab - 2025/2 |
| **Fase** | Desafio 2 - Modelagem e Recomendações Estratégicas |
| **Metodologia Base** | CRISP-DM |
| **Data de Criação** | Fevereiro/2026 |

---

## Índice

1. [Análise do Estado Atual](#1-análise-do-estado-atual-desafio-1-concluído)
2. [Análise e Aquisição de Novos Dados](#2-análise-e-aquisição-de-novos-dados)
3. [Desenvolvimento de Modelos de Machine Learning](#3-desenvolvimento-de-modelos-de-machine-learning)
4. [Análise da Importância das Variáveis](#4-análise-da-importância-das-variáveis)
5. [Dashboard Interativo (Streamlit)](#5-dashboard-interativo-streamlit)
6. [Recomendações Estratégicas](#6-recomendações-estratégicas)
7. [Estrutura de Arquivos Proposta](#7-estrutura-de-arquivos-proposta)
8. [Atualização do requirements.txt](#8-atualização-do-requirementstxt)
9. [Cronograma Sugerido](#9-cronograma-sugerido)
10. [Checklist de Entregáveis](#10-checklist-de-entregáveis)
11. [Referências Técnicas](#11-referências-técnicas)
12. [Análise de Séries Temporais e Forecasting](#12-análise-de-séries-temporais-e-forecasting)
13. [Visualização Geoespacial (Mapas)](#13-visualização-geoespacial-mapas)

---

## 1. Análise do Estado Atual (Desafio 1 Concluído)

### 1.1 Dados Disponíveis

| Arquivo | Variáveis | Observações | Descrição |
|---------|-----------|-------------|-----------|
| `dados_finais_analise.csv` | 5 colunas | 27 (UFs) | DataFrame consolidado |

**Variáveis atuais:**

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `UF` | Categórica | Unidade Federativa (chave) |
| `Tempo_Deslocamento_Medio_Minutos` | Numérica | Tempo médio ponderado casa-escola |
| `Indice_Saneamento_Basico` | Numérica | Média entre coleta e tratamento de esgoto |
| `Taxa_Evasao_Media` | Numérica | Média entre EF e EM |
| `Taxa_Repetencia_Media` | Numérica | Média entre EF e EM |

### 1.2 Limitações Identificadas

| Limitação | Impacto | Solução Proposta |
|-----------|---------|------------------|
| Apenas 27 observações | Modelos podem sofrer overfitting | Aquisição de dados temporais (2018-2022) |
| Apenas 4 variáveis preditoras | Baixa capacidade explicativa | Inclusão de novas variáveis socioeconômicas |
| Dados apenas de 2022 | Impossibilidade de análise temporal | Coleta de séries históricas |

### 1.3 Insights do Desafio 1

Os 9 gráficos gerados no Desafio 1 revelaram:

- **Correlação fraca** entre deslocamento e evasão
- **Correlação moderada negativa** entre saneamento e evasão
- **Grande variação regional** nos indicadores
- **UFs críticas identificadas**: Paraná, Rio Grande do Sul, Maranhão (alta evasão)
- **UFs referência**: São Paulo, Amazonas (baixa evasão)

---

## 2. Análise e Aquisição de Novos Dados

### 2.1 Diagnóstico de Necessidade

**Problema Identificado:**

O dataset atual possui apenas **27 observações** (uma por UF) e **4 variáveis explicativas**. Para modelos de Machine Learning robustos, recomenda-se:

- Mínimo de 10-20 observações por variável preditora
- Variáveis que capturem múltiplas dimensões do problema
- Dados temporais para análise de tendências

**Recomendação: NECESSÁRIO adquirir novos dados para garantir qualidade dos modelos.**

### 2.2 Novos Dados Recomendados

#### Categoria A: Indicadores Econômicos (Alta Prioridade)

| Variável | Fonte | Justificativa | URL |
|----------|-------|---------------|-----|
| PIB per capita por UF | IBGE/Base dos Dados | Proxy para desenvolvimento econômico | basedosdados.org |
| Taxa de Desemprego | IBGE - PNAD | Correlação com vulnerabilidade socioeconômica | sidra.ibge.gov.br |
| Renda Média Domiciliar | IBGE - Censo 2022 | Indicador de capacidade financeira | censo2022.ibge.gov.br |

#### Categoria B: Indicadores Sociais (Alta Prioridade)

| Variável | Fonte | Justificativa | URL |
|----------|-------|---------------|-----|
| IDH por UF | PNUD/Atlas Brasil | Índice composto (saúde, educação, renda) | atlasbrasil.org.br |
| Taxa de Pobreza | IBGE | Indicador de vulnerabilidade social | sidra.ibge.gov.br |
| Acesso à Internet | IBGE - PNAD TIC | Relevante para educação remota | basedosdados.org |

#### Categoria C: Indicadores de Infraestrutura (Média Prioridade)

| Variável | Fonte | Justificativa | URL |
|----------|-------|---------------|-----|
| Escolas com Infraestrutura Adequada | Censo Escolar/INEP | Qualidade do ambiente de ensino | gov.br/inep |
| Transporte Escolar Disponível | Censo Escolar/INEP | Alternativa ao deslocamento próprio | gov.br/inep |
| Número de Professores por Aluno | Censo Escolar/INEP | Qualidade do ensino | gov.br/inep |

#### Categoria D: Dados Temporais (Alta Prioridade)

| Período | Justificativa |
|---------|---------------|
| 2018-2022 | Permite análise de séries temporais, aumenta n de 27 para ~135 observações |
| Pré e Pós-COVID | Permite identificar impacto da pandemia nos indicadores |

### 2.3 Resultado Esperado Após Aquisição

| Métrica | Antes | Depois |
|---------|-------|--------|
| Observações | 27 | ~135 (5 anos x 27 UFs) |
| Variáveis Preditoras | 4 | 10-12 |
| Dimensões Capturadas | 2 (deslocamento, saneamento) | 5+ (econômica, social, infraestrutura, temporal) |

### 2.4 Processo de Aquisição

**Etapa 1: Coleta**
1. Acessar Base dos Dados (basedosdados.org)
2. Executar queries SQL para cada indicador
3. Exportar em formato CSV

**Etapa 2: Limpeza**
1. Padronizar nomes de UFs
2. Tratar valores ausentes
3. Verificar consistência temporal

**Etapa 3: Integração**
1. Merge por UF e Ano
2. Criar dataset consolidado v2
3. Documentar transformações

---

## 3. Desenvolvimento de Modelos de Machine Learning

### 3.1 Definição do Problema

**Pergunta Central:** "Como poderíamos avaliar e prever os agentes/fenômenos que mais causam impactos socioeconômicos no Brasil?"

**Variáveis Alvo (Target):**

| Variável | Tipo de Problema | Descrição |
|----------|-----------------|-----------|
| `Taxa_Evasao_Media` | Regressão | Prever valor contínuo da taxa |
| `Taxa_Repetencia_Media` | Regressão | Prever valor contínuo da taxa |
| `Nivel_Risco` | Classificação | Categorizar UFs (Alto/Médio/Baixo) |

### 3.2 Estratégia de Modelagem

#### 3.2.1 Modelos de Regressão

| Modelo | Complexidade | Interpretabilidade | Uso |
|--------|--------------|-------------------|-----|
| Linear Regression | Baixa | Alta | Baseline |
| Ridge/Lasso | Baixa | Alta | Regularização |
| Random Forest Regressor | Média | Média | Principal |
| Gradient Boosting (XGBoost) | Alta | Baixa | Comparação |
| SVR (Support Vector Regression) | Média | Baixa | Comparação |

**Fluxo de Implementação - Regressão:**

1. Carregar dados processados
2. Separar features (X) e targets (y)
3. Dividir em treino/teste (80/20) com random_state=42
4. Treinar modelo baseline (Linear Regression)
5. Treinar modelos avançados (Random Forest, XGBoost)
6. Avaliar métricas: MAE, MSE, RMSE, R²
7. Comparar resultados

#### 3.2.2 Modelos de Classificação

**Criação da Variável Target (Nivel_Risco):**

Baseado em quartis da Taxa de Evasão:
- **Alto Risco**: Taxa_Evasao > Q3 (75º percentil)
- **Médio Risco**: Q1 < Taxa_Evasao <= Q3
- **Baixo Risco**: Taxa_Evasao <= Q1 (25º percentil)

| Modelo | Complexidade | Interpretabilidade | Uso |
|--------|--------------|-------------------|-----|
| Logistic Regression | Baixa | Alta | Baseline |
| Decision Tree | Baixa | Alta | Visualização |
| Random Forest Classifier | Média | Média | Principal |
| Gradient Boosting (XGBoost) | Alta | Baixa | Comparação |
| SVM | Média | Baixa | Comparação |

**Fluxo de Implementação - Classificação:**

1. Criar variável categórica Nivel_Risco
2. Balancear classes se necessário (SMOTE ou class_weight)
3. Dividir em treino/teste com stratify=y
4. Treinar modelos
5. Avaliar métricas: Accuracy, Precision, Recall, F1-Score
6. Gerar Matriz de Confusão
7. Comparar resultados

### 3.3 Otimização de Hiperparâmetros

**Técnica:** GridSearchCV com Validação Cruzada (cv=5)

#### Random Forest - Grid de Hiperparâmetros:

| Parâmetro | Valores a Testar |
|-----------|------------------|
| n_estimators | [50, 100, 200] |
| max_depth | [3, 5, 10, None] |
| min_samples_split | [2, 5, 10] |
| min_samples_leaf | [1, 2, 4] |

#### XGBoost - Grid de Hiperparâmetros:

| Parâmetro | Valores a Testar |
|-----------|------------------|
| n_estimators | [50, 100, 200] |
| max_depth | [3, 5, 7] |
| learning_rate | [0.01, 0.1, 0.3] |
| subsample | [0.8, 1.0] |

### 3.4 Métricas de Avaliação

#### Métricas de Regressão:

| Métrica | Descrição | Interpretação |
|---------|-----------|---------------|
| MAE | Mean Absolute Error | Erro médio em unidades originais |
| MSE | Mean Squared Error | Penaliza erros grandes |
| RMSE | Root Mean Squared Error | Erro na escala original |
| R² | Coeficiente de Determinação | % da variância explicada (0-1) |

#### Métricas de Classificação:

| Métrica | Descrição | Interpretação |
|---------|-----------|---------------|
| Accuracy | (TP+TN)/Total | Proporção de acertos gerais |
| Precision | TP/(TP+FP) | Qualidade dos positivos previstos |
| Recall | TP/(TP+FN) | Cobertura dos positivos reais |
| F1-Score | 2*(P*R)/(P+R) | Média harmônica de P e R |

### 3.5 Validação dos Modelos

**Técnicas de Validação:**

1. **Hold-out**: 80% treino / 20% teste
2. **K-Fold Cross-Validation**: k=5 para robustez
3. **Stratified K-Fold**: Para classificação (manter proporção das classes)

**Prevenção de Overfitting:**

- Regularização (Ridge/Lasso)
- Early stopping (XGBoost)
- Limitação de profundidade (árvores)
- Validação cruzada

---

## 4. Análise da Importância das Variáveis

### 4.1 Objetivo

Identificar quais fatores (variáveis) mais influenciam os impactos socioeconômicos, permitindo:

- Direcionar políticas públicas
- Priorizar investimentos
- Comunicar resultados a stakeholders

### 4.2 Métodos a Implementar

| Método | Biblioteca | Descrição |
|--------|------------|-----------|
| Feature Importance | scikit-learn | Importância baseada em redução de impureza (Random Forest) |
| Permutation Importance | scikit-learn | Importância baseada em permutação de valores |
| SHAP Values | shap | Contribuição individual de cada feature para cada previsão |

### 4.3 Feature Importance (Random Forest)

**Conceito:** Mede a redução média de impureza (Gini ou Entropia) proporcionada por cada variável nas árvores do ensemble.

**Vantagens:**
- Rápido de calcular
- Nativo do modelo
- Fácil interpretação

**Limitações:**
- Viés para variáveis com muitas categorias
- Não captura interações

### 4.4 Permutation Importance

**Conceito:** Mede a queda no desempenho do modelo quando os valores de uma variável são embaralhados aleatoriamente.

**Vantagens:**
- Agnóstico ao modelo
- Considera interações
- Mais robusto que Feature Importance

**Limitações:**
- Computacionalmente mais caro
- Pode ser instável com variáveis correlacionadas

### 4.5 SHAP Values (SHapley Additive exPlanations)

**Conceito:** Baseado na teoria dos jogos, calcula a contribuição marginal de cada variável para cada previsão individual.

**Tipos de Visualização SHAP:**

| Visualização | Descrição | Uso |
|--------------|-----------|-----|
| Summary Plot | Distribuição de SHAP values por feature | Visão geral |
| Bar Plot | Média absoluta de SHAP values | Ranking simples |
| Force Plot | Contribuição para uma previsão específica | Explicação individual |
| Dependence Plot | Relação entre feature e SHAP value | Análise de interações |
| Waterfall Plot | Decomposição de uma previsão | Explicação detalhada |

**Vantagens do SHAP:**
- Explicações consistentes e justas
- Funciona para qualquer modelo
- Visualizações ricas
- Captura interações

### 4.6 Interpretação dos Resultados

**Exemplo de Interpretação:**

Se `Indice_Saneamento_Basico` tiver alta importância negativa:
- UFs com **maior** saneamento tendem a ter **menor** evasão
- **Recomendação:** Investir em infraestrutura de saneamento

Se `Tempo_Deslocamento_Medio` tiver alta importância positiva:
- UFs com **maior** deslocamento tendem a ter **maior** evasão
- **Recomendação:** Expandir transporte escolar

### 4.7 Ferramentas e Bibliotecas

| Ferramenta | Instalação | Documentação |
|------------|------------|--------------|
| scikit-learn | pip install scikit-learn | scikit-learn.org |
| SHAP | pip install shap | shap.readthedocs.io |
| ELI5 | pip install eli5 | eli5.readthedocs.io |

---

## 5. Dashboard Interativo (Streamlit)

### 5.1 Objetivo

Criar uma interface web interativa para:

- Explorar os dados e visualizações
- Apresentar resultados dos modelos
- Mostrar importância das variáveis
- Comunicar recomendações estratégicas

### 5.2 Estrutura do Dashboard

```
dashboard/
├── app.py                    # Aplicação principal
├── pages/
│   ├── 01_visao_geral.py    # Visão geral dos dados
│   ├── 02_modelos.py        # Resultados dos modelos
│   ├── 03_importancia.py    # Análise de importância
│   ├── 04_recomendacoes.py  # Recomendações estratégicas
│   ├── 05_series_temporais.py # Previsões temporais
│   └── 06_mapas.py          # Visualização geoespacial
├── utils/
│   ├── data_loader.py       # Funções de carregamento
│   └── visualizations.py    # Funções de gráficos
└── assets/
    └── style.css            # Estilos customizados
```

### 5.3 Funcionalidades por Página

#### Página 1: Visão Geral

| Componente | Descrição |
|------------|-----------|
| KPI Cards | Métricas gerais (média evasão, saneamento, etc.) |
| Filtros | Seleção de UF, métrica, período |
| Tabela | Dados completos com ordenação |
| Gráficos | Reprodução dos insights do Desafio 1 |

#### Página 2: Modelos de ML

| Componente | Descrição |
|------------|-----------|
| Seletor | Dropdown para escolher modelo |
| Métricas | Gauge charts com MAE, RMSE, R², F1 |
| Scatter Plot | Valores reais vs previstos |
| Matriz de Confusão | Para modelos de classificação |
| Comparação | Bar chart comparando modelos |

#### Página 3: Importância das Variáveis

| Componente | Descrição |
|------------|-----------|
| SHAP Summary | Plot interativo de SHAP values |
| Feature Ranking | Bar chart de importância |
| Dependence Plot | Scatter plot interativo |
| Explicação Individual | Seleção de UF para análise específica |

#### Página 4: Recomendações

| Componente | Descrição |
|------------|-----------|
| UFs Prioritárias | Lista das 5 UFs com maior risco |
| Fatores Críticos | Cards com principais variáveis |
| Recomendações | Texto formatado com ações sugeridas |
| Simulador | Sliders para simular impacto de mudanças |

#### Página 5: Séries Temporais

| Componente | Descrição |
|------------|-----------|
| Gráfico Temporal | Linha com histórico e previsões |
| Seletor de Modelo | ARIMA vs Prophet |
| Intervalo de Confiança | Área sombreada com IC 95% |
| Tabela de Previsões | Valores previstos por ano |

#### Página 6: Mapas

| Componente | Descrição |
|------------|-----------|
| Mapa Coroplético | Brasil colorido por métrica |
| Seletor de Métrica | Dropdown para escolher indicador |
| Tooltip | Informações ao passar o mouse |
| Legenda | Escala de cores |

### 5.4 Componentes Streamlit Principais

| Componente | Uso |
|------------|-----|
| st.title(), st.header() | Títulos e cabeçalhos |
| st.metric() | Exibição de KPIs |
| st.selectbox(), st.multiselect() | Filtros de seleção |
| st.slider() | Seleção de ranges |
| st.plotly_chart() | Gráficos interativos Plotly |
| st.dataframe() | Tabelas de dados |
| st.columns() | Layout em colunas |
| st.sidebar | Menu lateral |
| st.tabs() | Abas de navegação |

### 5.5 Execução do Dashboard

**Comando para executar:**

```bash
streamlit run dashboard/app.py
```

**Acesso:** http://localhost:8501

---

## 6. Recomendações Estratégicas

### 6.1 Estrutura das Recomendações

As recomendações serão baseadas em:

1. **Insights dos modelos** - Quais variáveis mais impactam
2. **Análise de clusters** - Agrupamento de UFs similares
3. **Benchmarking** - Comparação com UFs de melhor desempenho
4. **Séries temporais** - Tendências identificadas

### 6.2 Framework de Recomendações

| Categoria | Variável Relacionada | Tipo de Ação |
|-----------|---------------------|--------------|
| Infraestrutura | Saneamento, Transporte | Investimento em infraestrutura básica |
| Mobilidade | Tempo de Deslocamento | Expansão de transporte escolar |
| Educação | Taxa de Evasão/Repetência | Programas de acompanhamento pedagógico |
| Economia | PIB, Renda | Programas de transferência de renda |

### 6.3 Formato das Recomendações

Cada recomendação seguirá o template:

---

**RECOMENDAÇÃO #N: [Título]**

**UFs Prioritárias:** [Lista de UFs]

**Problema Identificado:** [Descrição baseada nos dados]

**Evidência do Modelo:** [Importância da variável, correlação, etc.]

**Ação Recomendada:** [Descrição detalhada da intervenção]

**Impacto Esperado:** [Estimativa baseada no modelo - ex: redução de X% na evasão]

**Prazo Sugerido:** [Curto prazo (1 ano) / Médio prazo (2-3 anos) / Longo prazo (5+ anos)]

**Indicadores de Acompanhamento:** [Métricas para monitorar o progresso]

---

### 6.4 Exemplos de Recomendações Esperadas

| # | Título | UFs Alvo | Variável Chave |
|---|--------|----------|----------------|
| 1 | Expansão do Transporte Escolar | Amazonas, Pará, Amapá | Tempo de Deslocamento |
| 2 | Investimento em Saneamento Básico | Amapá, Amazonas, Maranhão | Índice de Saneamento |
| 3 | Programa de Combate à Evasão | Paraná, RS, Maranhão | Taxa de Evasão |
| 4 | Melhoria da Infraestrutura Escolar | UFs com baixo IDH | Infraestrutura |

---

## 7. Estrutura de Arquivos Proposta

```
ZettaLab-Data/
├── .github/
│   ├── copilot-instructions.md
│   └── PLANEJAMENTO_DESAFIO_2.md      # Este arquivo
│
├── data/
│   ├── Raw/
│   │   ├── Deslocamento.csv
│   │   ├── RELATORIO_DTB_BRASIL_2024_DISTRITOS.csv
│   │   └── [novos dados brutos]
│   ├── Processed/
│   │   ├── dados_finais_analise.csv
│   │   ├── dados_modelo_v2.csv         # NOVO - com dados adicionais
│   │   └── dados_temporais.csv         # NOVO - séries históricas
│   ├── geojson/
│   │   └── brazil-states.geojson       # NOVO - geometria das UFs
│   └── vizualizations/
│       ├── [gráficos do Desafio 1]
│       ├── [novos gráficos de modelos]
│       └── [mapas HTML]
│
├── notebooks/
│   ├── clean-data.ipynb
│   ├── extract-info.ipynb
│   ├── vizualizations.ipynb
│   ├── 01_aquisicao_novos_dados.ipynb  # NOVO
│   ├── 02_modelagem_regressao.ipynb    # NOVO
│   ├── 03_modelagem_classificacao.ipynb # NOVO
│   ├── 04_analise_importancia.ipynb    # NOVO
│   ├── 05_series_temporais.ipynb       # NOVO
│   └── 06_visualizacao_mapas.ipynb     # NOVO
│
├── models/                              # NOVA PASTA
│   ├── random_forest_regressor.pkl
│   ├── random_forest_classifier.pkl
│   ├── xgboost_regressor.pkl
│   ├── xgboost_classifier.pkl
│   ├── prophet_model.pkl
│   └── model_metrics.json
│
├── dashboard/                           # NOVA PASTA
│   ├── app.py
│   ├── pages/
│   │   ├── 01_visao_geral.py
│   │   ├── 02_modelos.py
│   │   ├── 03_importancia.py
│   │   ├── 04_recomendacoes.py
│   │   ├── 05_series_temporais.py
│   │   └── 06_mapas.py
│   ├── utils/
│   │   ├── data_loader.py
│   │   └── visualizations.py
│   └── assets/
│       └── style.css
│
├── reports/                             # NOVA PASTA
│   └── recomendacoes_estrategicas.md
│
├── requirements.txt                     # ATUALIZADO
└── README.md                            # ATUALIZADO
```

---

## 8. Atualização do requirements.txt

### Dependências Atuais (Desafio 1)

```
pandas
numpy
ydata
pyarrow
openpyxl
seaborn
matplotlib
```

### Dependências Adicionais (Desafio 2)

```
# Manipulação de Dados
pandas>=2.0.0
numpy>=1.24.0

# Visualização
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0

# Machine Learning
scikit-learn>=1.3.0
xgboost>=1.7.0
shap>=0.42.0

# Séries Temporais
statsmodels>=0.14.0
prophet>=1.1.0
pmdarima>=2.0.0

# Dashboard
streamlit>=1.28.0
streamlit-folium>=0.15.0

# Mapas e Geoespacial
folium>=0.14.0
geopandas>=0.14.0
branca>=0.6.0

# Profiling e Análise
ydata-profiling>=4.5.0

# Utilitários
pyarrow>=12.0.0
openpyxl>=3.1.0
joblib>=1.3.0
```

---

## 9. Cronograma Sugerido

### Visão Geral

| Fase | Duração | Dias |
|------|---------|------|
| Fase 1: Preparação | 2 dias | 1-2 |
| Fase 2: Modelagem | 3 dias | 3-5 |
| Fase 3: Análise de Importância | 2 dias | 6-7 |
| Fase 4: Séries Temporais | 2 dias | 8-9 |
| Fase 5: Mapas | 1 dia | 10 |
| Fase 6: Dashboard | 3 dias | 11-13 |
| Fase 7: Documentação | 2 dias | 14-15 |
| **Total** | **15 dias** | |

### Detalhamento por Fase

#### Fase 1: Preparação (Dias 1-2)

- [ ] Aquisição de novos dados (PIB, IDH, desemprego)
- [ ] Download de dados históricos (2018-2022)
- [ ] Limpeza e padronização dos novos dados
- [ ] Integração com dataset existente
- [ ] Criação do dataset consolidado v2
- [ ] Atualização do requirements.txt
- [ ] Configuração do ambiente virtual

#### Fase 2: Modelagem (Dias 3-5)

- [ ] Notebook de modelagem de regressão
  - [ ] Implementar Linear Regression (baseline)
  - [ ] Implementar Random Forest Regressor
  - [ ] Implementar XGBoost Regressor
  - [ ] Avaliar métricas (MAE, RMSE, R²)
  
- [ ] Notebook de modelagem de classificação
  - [ ] Criar variável Nivel_Risco
  - [ ] Implementar Logistic Regression (baseline)
  - [ ] Implementar Random Forest Classifier
  - [ ] Implementar XGBoost Classifier
  - [ ] Avaliar métricas (Accuracy, F1-Score)

- [ ] Otimização de hiperparâmetros (GridSearchCV)
- [ ] Comparação e seleção dos melhores modelos
- [ ] Salvar modelos treinados (.pkl)

#### Fase 3: Análise de Importância (Dias 6-7)

- [ ] Implementar Feature Importance
- [ ] Implementar Permutation Importance
- [ ] Implementar SHAP values
- [ ] Gerar visualizações SHAP
  - [ ] Summary Plot
  - [ ] Bar Plot
  - [ ] Dependence Plots
  - [ ] Force Plots
- [ ] Interpretar resultados
- [ ] Documentar insights

#### Fase 4: Séries Temporais (Dias 8-9)

- [ ] Preparar dados temporais
- [ ] Análise exploratória de séries
- [ ] Implementar modelo ARIMA
- [ ] Implementar modelo Prophet
- [ ] Gerar previsões (2023-2025)
- [ ] Comparar modelos temporais
- [ ] Documentar resultados

#### Fase 5: Mapas (Dia 10)

- [ ] Obter shapefile/GeoJSON do Brasil
- [ ] Criar mapas coropléticos (Folium)
- [ ] Criar mapas com Plotly
- [ ] Criar mapa de calor
- [ ] Salvar mapas em HTML
- [ ] Testar interatividade

#### Fase 6: Dashboard (Dias 11-13)

- [ ] Estruturar projeto Streamlit
- [ ] Desenvolver página de Visão Geral
- [ ] Desenvolver página de Modelos
- [ ] Desenvolver página de Importância
- [ ] Desenvolver página de Recomendações
- [ ] Desenvolver página de Séries Temporais
- [ ] Desenvolver página de Mapas
- [ ] Integrar todas as páginas
- [ ] Testes e ajustes de UX
- [ ] Deploy local

#### Fase 7: Documentação (Dias 14-15)

- [ ] Elaborar recomendações estratégicas detalhadas
- [ ] Atualizar README.md com novos conteúdos
- [ ] Revisar comentários nos notebooks
- [ ] Criar documentação do dashboard
- [ ] Revisão final do repositório
- [ ] Preparar para entrega

---

## 10. Checklist de Entregáveis

### Entregáveis Obrigatórios (conforme Desafio 2)

#### Notebook Jupyter Atualizado

- [ ] Código de aquisição de novos dados (se aplicável)
- [ ] Código de desenvolvimento dos modelos de regressão
- [ ] Código de desenvolvimento dos modelos de classificação
- [ ] Otimização de hiperparâmetros documentada
- [ ] Análise de importância das variáveis (SHAP, Feature Importance)
- [ ] Visualizações dos resultados
- [ ] Comentários explicativos em cada célula
- [ ] Células executadas e outputs visíveis

#### README Atualizado

- [ ] Explicação das escolhas metodológicas para modelagem
- [ ] Justificativa para aquisição de novos dados (se houver)
- [ ] Descrição dos principais passos da modelagem
- [ ] Métricas de avaliação dos modelos
- [ ] Insights e resultados obtidos
- [ ] Análise de importância das variáveis
- [ ] Recomendações estratégicas detalhadas
- [ ] Instruções de reprodutibilidade

#### Repositório Organizado

- [ ] Estrutura clara de pastas (conforme seção 7)
- [ ] Versionamento com Git (commits frequentes e descritivos)
- [ ] requirements.txt atualizado
- [ ] Link público para avaliação
- [ ] Arquivos desnecessários no .gitignore

#### Dashboard Final

- [ ] Interface funcional em Streamlit
- [ ] Visualizações interativas
- [ ] Resultados da modelagem apresentados
- [ ] Análise de importância visualizada
- [ ] Mapas geoespaciais funcionais
- [ ] Previsões de séries temporais
- [ ] Recomendações estratégicas
- [ ] Instruções de execução

### Critérios de Avaliação

| Critério | Como será atendido | Status |
|----------|-------------------|--------|
| Clareza na escolha de novos dados | Documentação detalhada das fontes e justificativas | [ ] |
| Qualidade dos modelos preditivos | Múltiplos modelos com métricas documentadas | [ ] |
| Validação e otimização | GridSearchCV com cross-validation | [ ] |
| Análise de importância das variáveis | SHAP, Feature Importance, Permutation | [ ] |
| Visualizações estruturadas | Dashboard Streamlit + gráficos nos notebooks | [ ] |
| Relevância das recomendações | Baseadas em evidências dos modelos | [ ] |
| Qualidade da escrita | README e notebooks bem documentados | [ ] |

---

## 11. Referências Técnicas

### Documentação Oficial

| Ferramenta | URL |
|------------|-----|
| Scikit-learn | https://scikit-learn.org/stable/ |
| SHAP | https://shap.readthedocs.io/ |
| Streamlit | https://docs.streamlit.io/ |
| XGBoost | https://xgboost.readthedocs.io/ |
| Prophet | https://facebook.github.io/prophet/ |
| Folium | https://python-visualization.github.io/folium/ |
| GeoPandas | https://geopandas.org/ |
| Plotly | https://plotly.com/python/ |
| Statsmodels | https://www.statsmodels.org/ |

### Fontes de Dados

| Fonte | URL | Dados Disponíveis |
|-------|-----|-------------------|
| Base dos Dados | https://basedosdados.org/ | PIB, IDH, indicadores diversos |
| IBGE Sidra | https://sidra.ibge.gov.br/ | Censo, PNAD, estatísticas |
| INEP | https://www.gov.br/inep/ | Indicadores educacionais |
| Atlas Brasil | http://www.atlasbrasil.org.br/ | IDH municipal e estadual |
| SNIS | http://www.snis.gov.br/ | Dados de saneamento |

### Livros de Referência (E-book Ciência de Dados)

| Livro | Autor | Foco |
|-------|-------|------|
| Storytelling com Dados | Cole Nussbaumer Knaflic | Visualização |
| Data Science from Scratch | Joel Grus | Fundamentos |
| Introduction to Machine Learning with Python | Müller & Guido | Scikit-learn |
| Python para Análise de Dados | Wes McKinney | Pandas |
| Data Science para Negócios | Provost & Fawcett | Aplicações |

---

## 12. Análise de Séries Temporais e Forecasting

### 12.1 Objetivo

Prever a evolução das taxas de evasão e repetência para os próximos anos (2023-2025), permitindo:

- Identificar tendências de longo prazo
- Antecipar cenários críticos por UF
- Avaliar impacto de políticas públicas
- Planejar intervenções preventivas

### 12.2 Requisitos de Dados

| Período | Anos | Observações por UF | Total |
|---------|------|-------------------|-------|
| Histórico | 2018-2022 | 5 | 135 (27 UFs x 5 anos) |
| Previsão | 2023-2025 | 3 | Gerado pelo modelo |

**Fontes para dados históricos:**

- INEP - Indicadores Educacionais (séries históricas)
- Base dos Dados - tabela `br_inep_indicadores_educacionais.taxa_transicao`

### 12.3 Bibliotecas Necessárias

| Biblioteca | Versão | Uso |
|------------|--------|-----|
| statsmodels | >=0.14.0 | ARIMA, decomposição, testes estatísticos |
| prophet | >=1.1.0 | Facebook Prophet para previsões |
| pmdarima | >=2.0.0 | Auto-ARIMA (seleção automática de parâmetros) |

### 12.4 Estrutura dos Dados Temporais

O DataFrame temporal deve ter a seguinte estrutura:

| UF | ano | Taxa_Evasao_Media | Taxa_Repetencia_Media | PIB_per_capita | ... |
|----|-----|-------------------|----------------------|----------------|-----|
| Acre | 2018 | 5.8 | 10.2 | 18500 | ... |
| Acre | 2019 | 5.5 | 9.8 | 19200 | ... |
| Acre | 2020 | 4.9 | 8.5 | 18800 | ... |
| Acre | 2021 | 5.1 | 9.0 | 19500 | ... |
| Acre | 2022 | 5.2 | 9.45 | 20100 | ... |

### 12.5 Análise Exploratória Temporal

**Componentes a analisar:**

1. **Tendência**: Direção geral da série (crescente/decrescente)
2. **Sazonalidade**: Padrões repetitivos (menos relevante para dados anuais)
3. **Ruído**: Variações aleatórias
4. **Outliers**: Anos atípicos (ex: 2020-2021 devido à COVID)

**Visualizações:**

| Gráfico | Objetivo |
|---------|----------|
| Linha temporal | Visualizar evolução por UF |
| Decomposição | Separar tendência, sazonalidade e resíduo |
| ACF (Autocorrelação) | Identificar dependências temporais |
| PACF (Autocorrelação Parcial) | Auxiliar na escolha de parâmetros ARIMA |

### 12.6 Modelo ARIMA

**Conceito:** AutoRegressive Integrated Moving Average

- **AR (p)**: Termos autorregressivos
- **I (d)**: Ordem de diferenciação
- **MA (q)**: Termos de média móvel

**Auto-ARIMA:** Seleciona automaticamente os melhores parâmetros (p, d, q) minimizando AIC/BIC.

**Etapas de implementação:**

1. Verificar estacionariedade (teste ADF)
2. Aplicar diferenciação se necessário
3. Identificar p e q via ACF/PACF
4. Treinar modelo
5. Validar resíduos
6. Gerar previsões com intervalo de confiança

### 12.7 Modelo Prophet

**Conceito:** Modelo aditivo desenvolvido pelo Facebook, especialmente bom para:

- Séries com tendências não-lineares
- Efeitos de feriados/eventos
- Dados com valores ausentes
- Mudanças abruptas de tendência

**Componentes do Prophet:**

```
y(t) = g(t) + s(t) + h(t) + e(t)
```

- g(t): Tendência (growth)
- s(t): Sazonalidade
- h(t): Efeitos de feriados
- e(t): Erro

**Vantagens:**

- Fácil de usar
- Robusto a outliers
- Intervalos de confiança automáticos
- Permite adicionar regressores externos

### 12.8 Comparação de Modelos

| Aspecto | ARIMA | Prophet |
|---------|-------|---------|
| Complexidade | Média | Baixa |
| Interpretabilidade | Baixa | Alta |
| Dados necessários | Mais | Menos |
| Sazonalidade | Manual | Automática |
| Regressores externos | Limitado | Suportado |
| Intervalos de confiança | Paramétrico | Bayesiano |

**Métricas de avaliação:**

| Métrica | Descrição |
|---------|-----------|
| MAE | Erro absoluto médio |
| RMSE | Raiz do erro quadrático médio |
| MAPE | Erro percentual absoluto médio |
| AIC/BIC | Critérios de informação (apenas ARIMA) |

### 12.9 Fluxo de Implementação

1. **Preparação dos dados**
   - Carregar dados históricos (2018-2022)
   - Formatar como série temporal
   - Tratar valores ausentes

2. **Análise exploratória**
   - Plotar séries por UF
   - Decomposição temporal
   - Testes de estacionariedade

3. **Modelagem ARIMA**
   - Auto-ARIMA para cada UF
   - Validação com holdout (último ano)
   - Gerar previsões

4. **Modelagem Prophet**
   - Configurar modelo
   - Treinar para cada UF
   - Gerar previsões

5. **Comparação e seleção**
   - Calcular métricas de erro
   - Selecionar melhor modelo por UF
   - Documentar resultados

6. **Previsões finais**
   - Gerar previsões 2023-2025
   - Calcular intervalos de confiança
   - Visualizar resultados

### 12.10 Outputs Esperados

| Output | Descrição |
|--------|-----------|
| Gráficos temporais | Histórico + previsões por UF |
| Tabela de previsões | Valores previstos com IC 95% |
| Comparação de modelos | Métricas ARIMA vs Prophet |
| Insights | Tendências identificadas |
| Alertas | UFs com tendência de piora |

---

## 13. Visualização Geoespacial (Mapas)

### 13.1 Objetivo

Criar mapas interativos do Brasil que visualizem os indicadores socioeconômicos e resultados dos modelos por UF, facilitando:

- Identificação de padrões regionais
- Comparação visual entre UFs
- Comunicação efetiva de resultados
- Identificação de áreas prioritárias

### 13.2 Tipos de Mapas

| Tipo | Descrição | Uso |
|------|-----------|-----|
| Coroplético | UFs coloridas por valor | Distribuição de métricas |
| Marcadores | Pontos nos centróides | Ranking e destaques |
| Calor (Heatmap) | Gradiente de intensidade | Concentração de valores |
| Bolhas | Círculos proporcionais | Múltiplas variáveis |

### 13.3 Bibliotecas Necessárias

| Biblioteca | Versão | Uso |
|------------|--------|-----|
| folium | >=0.14.0 | Mapas interativos Leaflet |
| geopandas | >=0.14.0 | Manipulação de dados geográficos |
| branca | >=0.6.0 | Elementos HTML para Folium |
| streamlit-folium | >=0.15.0 | Integração Folium + Streamlit |
| plotly | >=5.14.0 | Mapas com Plotly Express |

### 13.4 Obtenção dos Dados Geográficos

**Fonte do GeoJSON:**

| Fonte | URL | Formato |
|-------|-----|---------|
| IBGE | geociencias/downloads | Shapefile |
| GitHub (codeforamerica) | click_that_hood/brazil-states | GeoJSON |
| Natural Earth | naturalearthdata.com | Shapefile |

**Estrutura do GeoJSON:**

```
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "São Paulo",
        "sigla": "SP"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [...]
      }
    },
    ...
  ]
}
```

### 13.5 Preparação dos Dados

**Etapas:**

1. Carregar GeoJSON das UFs
2. Padronizar nomes das UFs (acentos, maiúsculas)
3. Fazer merge com dados de análise
4. Calcular centróides para marcadores
5. Verificar UFs não correspondidas

**Correções de nomes comuns:**

| GeoJSON | Dados | Correção |
|---------|-------|----------|
| Federal District | Distrito Federal | Sim |
| Parana | Paraná | Sim |
| Sao Paulo | São Paulo | Sim |

### 13.6 Mapa Coroplético (Folium)

**Conceito:** Mapa onde cada UF é colorida de acordo com o valor de uma métrica.

**Componentes:**

| Componente | Descrição |
|------------|-----------|
| Base Map | Mapa de fundo (CartoDB, OpenStreetMap) |
| GeoJSON Layer | Polígonos das UFs |
| Color Scale | Escala de cores (YlOrRd, Blues, etc.) |
| Tooltip | Informações ao passar o mouse |
| Legend | Legenda com escala de valores |

**Paletas de cores recomendadas:**

| Paleta | Uso |
|--------|-----|
| YlOrRd | Valores negativos (evasão, pobreza) |
| Blues | Valores positivos (saneamento, IDH) |
| RdYlGn | Escala divergente (bom/ruim) |
| Viridis | Uso geral (acessível) |

### 13.7 Mapa de Marcadores

**Conceito:** Círculos nos centróides das UFs, com tamanho e cor variáveis.

**Componentes:**

| Componente | Descrição |
|------------|-----------|
| CircleMarker | Marcador circular |
| Radius | Tamanho proporcional ao valor |
| Color | Cor baseada em ranking ou categoria |
| Popup | Informações detalhadas ao clicar |
| Tooltip | Informações rápidas ao hover |

**Categorização por cores:**

| Ranking | Cor | Significado |
|---------|-----|-------------|
| Top 5 (piores) | Vermelho | Atenção urgente |
| 6º - 10º | Laranja | Atenção moderada |
| Intermediários | Azul | Situação média |
| Top 5 (melhores) | Verde | Referência |

### 13.8 Mapa de Calor

**Conceito:** Gradiente de cores mostrando intensidade/concentração.

**Componentes:**

| Componente | Descrição |
|------------|-----------|
| HeatMap | Plugin do Folium |
| Data | Lista de [lat, lon, intensidade] |
| Radius | Raio de influência de cada ponto |
| Blur | Suavização do gradiente |
| Gradient | Escala de cores personalizada |

**Uso recomendado:**

- Visualizar concentração de problemas
- Identificar clusters regionais
- Destacar hotspots

### 13.9 Mapa com Plotly

**Vantagens sobre Folium:**

- Melhor integração com Streamlit
- Mais opções de customização
- Performance melhor para muitos dados
- Exportação fácil

**Componentes:**

| Componente | Descrição |
|------------|-----------|
| px.choropleth | Função principal |
| geojson | Dados geográficos |
| locations | Coluna de identificação |
| featureidkey | Chave no GeoJSON |
| color | Coluna para colorir |
| hover_data | Dados adicionais no tooltip |

### 13.10 Integração com Dashboard

**Página de Mapas (Streamlit):**

| Componente | Função |
|------------|--------|
| st.sidebar | Filtros e configurações |
| st.selectbox | Seleção de métrica |
| st.radio | Tipo de mapa |
| st_folium | Exibir mapa Folium |
| st.plotly_chart | Exibir mapa Plotly |
| st.metric | Estatísticas da métrica |
| st.dataframe | Top/Bottom 5 UFs |

**Interatividade:**

- Seleção de UF ao clicar
- Zoom e pan
- Tooltips informativos
- Atualização dinâmica com filtros

### 13.11 Estrutura de Arquivos para Mapas

```
data/
├── geojson/
│   └── brazil-states.geojson    # Geometria das UFs
├── vizualizations/
│   ├── mapa_evasao.html         # Coroplético - evasão
│   ├── mapa_saneamento.html     # Coroplético - saneamento
│   ├── mapa_deslocamento.html   # Coroplético - deslocamento
│   ├── mapa_ranking.html        # Marcadores - ranking
│   ├── mapa_calor.html          # Heatmap
│   └── mapa_previsao.html       # Previsões temporais
```

### 13.12 Outputs Esperados

| Output | Formato | Descrição |
|--------|---------|-----------|
| Mapas HTML | .html | Mapas interativos standalone |
| Página Streamlit | .py | Integração no dashboard |
| Screenshots | .png | Imagens para README |
| GeoDataFrame | .pkl | Dados processados |

---

## Conclusão

Este planejamento detalha todas as etapas necessárias para completar o **Desafio II** do programa Zetta Lab, incluindo:

1. **Análise criteriosa** do estado atual e limitações
2. **Estratégia clara** para aquisição de novos dados
3. **Metodologia robusta** para desenvolvimento de modelos
4. **Técnicas avançadas** de interpretabilidade (SHAP)
5. **Análise temporal** para previsões futuras
6. **Visualização geoespacial** para comunicação efetiva
7. **Dashboard interativo** para apresentação dos resultados
8. **Recomendações estratégicas** baseadas em evidências

O sucesso do projeto depende da execução disciplinada de cada fase, com documentação contínua e foco nos critérios de avaliação estabelecidos.

---

**Documento criado em:** Fevereiro/2026

**Última atualização:** Fevereiro/2026

**Autor:** Gustavo Teodoro

**Programa:** Zetta Lab - 2025/2
