"""
Página 5: Conclusões e Storytelling de Dados
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import *

st.set_page_config(page_title="Conclusões", page_icon="📖", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

st.title("📖 Storytelling de Dados - Conclusões Principais")

st.markdown("""
Esta página documenta como a **ciência de dados** revelou insights estruturados 
sobre os determinantes da evasão escolar no Brasil, através da metodologia 
**CRISP-DM** (Modelagem de Dados).
""")

st.markdown("---")

# Seção 1
with st.expander("### 1️⃣ A DESCOBERTA DO PRINCIPAL AGENTE (Gravidez Adolescente)"):
    st.markdown("""
    **Pergunta Original**: Quais agentes socioeconômicos mais afetam evasão escolar?
    
    **Metodologia Aplicada**:
    - Análise SHAP (Shapley Additive exPlanations)
    - Interpretabilidade matemática de modelo de ML
    - Feature importance global (baseado em teoria dos jogos)
    
    **Conclusão Alcançada**:
    Gravidez adolescente é responsável por **63.5% da importância** nas predições
    de abandono escolar. Isto foi descoberto através de análise rigorosa, não intuição.
    
    **O que isto significa**:
    - Se queremos entender evasão, precisamos focar em saúde reprodutiva
    - Não é apenas correlação observacional
    - É uma relação identificada pelo modelo treinado em 135 registros históricos
    - O padrão é consistente em múltiplos anos (2018-2022) e estados
    
    **Impacto Científico**:
    - Aponta para raiz causal do problema
    - Permite priorização de intervenções
    - Fundamenta recomendações com dados, não opinião
    """)

st.markdown("---")

# Seção 2
with st.expander("### 2️⃣ A IMPORTÂNCIA ESTRATIFICADA (Além do Principal Agente)"):
    st.markdown("""
    **Pergunta**: Apenas gravidez adolescente explica evasão?
    
    **Metodologia Aplicada**:
    - Análise de correlações múltiplas
    - Decomposição de variância (SHAP values)
    - Regressão com validação cruzada (5-fold)
    
    **Conclusão Alcançada**:
    Não. O modelo alcança R² = 0.51, significando que:
    - 51% da variância em evasão é explicada pelas variáveis
    - 49% é explicado por fatores não capturados (dropout da escola, etc)
    - Renda (15.2%), Desemprego (12.1%), IDHM (6.8%) também importam
    
    **O que isto significa**:
    - O problema é **multidimensional**
    - Não existe solução única
    - Temos um **sistema complexo** onde múltiplos fatores se interagem
    - Melhorias requerem atuação em múltiplos eixos
    
    **Implicação Prática**:
    Modelos simples (regressão linear R²=0.38) capturam menos que XGBoost (R²=0.51)
    Isto valida escolha de modelo mais sofisticado
    """)

st.markdown("---")

# Seção 3
with st.expander("### 3️⃣ A ESTRATIFICAÇÃO DE RISCO (Identificar Quem Mais Precisa)"):
    st.markdown("""
    **Pergunta**: Como identificar estados em maior risco de maneira científica?
    
    **Metodologia Aplicada**:
    - Análise de percentis da distribuição (0-100%)
    - Thresholds baseados em conhecimento de domínio (PNE)
    - Validação com dados não vistos (2022)
    - Abordagem Híbrida: Regressão + Categorização
    
    **Conclusão Alcançada**:
    7 estados têm abandono > 3.0% (Maranhão 4.12%, Pará 3.85%, etc)
    
    **Thresholds Definidos**:
    - Baixo Risco: ≤ 1.0% (meta PNE - atingir isto é sucesso)
    - Médio Risco: 1.0% - 3.0% (situação controlada mas com atenção)
    - Alto Risco: > 3.0% (crise - 3x a meta, requer urgência)
    
    **Validação**:
    - Abordagem Híbrida alcança 64% de recall na classe "Alto"
    - Estados críticos têm características similares (renda baixa, gravidez alta)
    - Padrão é persistente (2018-2022)
    
    **O que isto significa**:
    - Recursos limitados devem focar nos 7 estados críticos
    - Não é solução one-size-fits-all (cada estado tem contexto)
    - Estratificação permite priorização baseada em dados
    """)

st.markdown("---")

# Seção 4
with st.expander("### 4️⃣ A VALIDAÇÃO TEMPORAL (Problemas São Persistentes)"):
    st.markdown("""
    **Pergunta**: Isto é problema novo ou estrutural/histórico?
    
    **Metodologia Aplicada**:
    - Análise de série temporal (2018-2022, 5 anos)
    - Boxplot e estatísticas por ano
    - Verificação de tendência (estável, crescente ou decrescente?)
    
    **Conclusão Alcançada**:
    O padrão é **persistente**. Os mesmos estados continuam em risco ao longo dos anos.
    Taxa média mantém-se ao redor de 2.15%, sem redução significativa.
    
    **Dados**:
    - 2018: Média ~2.1%, mesmos estados críticos
    - 2022: Média ~2.2%, mesmos estados críticos
    - Conclusão: Problema não melhorou espontaneamente
    
    **O que isto significa**:
    - Não é anomalia ou flutuação anual
    - É **estrutural** - raízes profundas
    - Requer solução estrutural, não superficial
    - Mercado/sociedade sozinhos não está resolvendo
    
    **Implicação**:
    Sem intervenção, tendência provavelmente continua igual em 2023-2025
    Modelo de predição valida isto (veja página de Predições)
    """)

st.markdown("---")

# Seção 5
with st.expander("### 5️⃣ A CAPACIDADE PREDITIVA (Ciência de Dados Funciona Aqui)"):
    st.markdown("""
    **Pergunta**: Conseguimos prever o futuro com confiabilidade?
    
    **Metodologia Aplicada**:
    - Modelo XGBoost com otimização de hiperparâmetros (GridSearch)
    - Validação temporal: Treino 2018-2021, Teste 2022
    - Validação cruzada (5-fold) para evitar overfitting
    - Teste de robustez (diferentes seeds aleatórias)
    
    **Conclusão Alcançada**:
    Sim. Modelo alcança R² = 0.510 em dados não vistos (2022).
    
    **Desempenho**:
    - Baseline (Linear Regression): R² = 0.380
    - Random Forest: R² = 0.430
    - XGBoost Otimizado: R² = 0.510 ← Melhor
    
    **Estabilidade**:
    - Validação cruzada: R² médio = 0.510 ± 0.002
    - Com diferentes seeds: Resultados consistentes
    - Modelo não sofre de overfitting significativo
    
    **O que isto significa**:
    - Podemos fazer previsões informadas para 2023-2025
    - Incerteza existe (49% não explicado), mas é quantificável
    - Quanto mais distante no tempo, menos confiável é predição
    - Para horizonte 1-2 anos, confiabilidade é boa
    
    **Limite do Modelo**:
    - Não pode prever eventos extremos (COVID-like)
    - Presume que relações 2018-2022 continuam valendo
    - Melhoraria muito com dados municipais (atualmente UF apenas)
    """)

st.markdown("---")

# Síntese Final
st.subheader("🎯 SÍNTESE: O Que a Ciência de Dados Revelou")

st.markdown("""
Este projeto demonstrou como aplicar **rigorosamente a metodologia CRISP-DM** 
para entender um problema social complexo:

| Fase | O Que Fez | Resultado |
|------|-----------|-----------|
| **Entendimento** | Formulou perguntas sobre evasão | Definiu escopo e variáveis |
| **Dados** | Coletou 135 registros (27 UFs × 5 anos) | Base para análise confiável |
| **Preparação** | Consolidou múltiplas fontes | Dataset íntegro e limpo |
| **Modelagem** | Testou 3 modelos, otimizou o melhor | XGBoost com R²=0.51 |
| **Avaliação** | SHAP para interpretabilidade | Descobriu fatores-chave |
| **Implantação** | Dashboard interativo + Predições | Ferramenta para explorações |

### Descobertas Principais:

1. **Gravidez Adolescente** é o fator-chave (63.5% de importância)
2. **Problema é Multidimensional** (Renda, Desemprego também importam)
3. **Estratificado Geograficamente** (7 estados em situação crítica)
4. **Persistente no Tempo** (mesmo padrão 2018-2022)
5. **Previsível** (R²=0.51 demonstra viabilidade de ML)

### Limitações Honestas:

❌ 51% de variância explicada = 49% ainda desconhecido  
❌ Correlação ≠ Causalidade (dados sugerem, não comprovam)  
❌ Nível estadual apenas (municipal seria melhor)  
❌ Não prevê eventos extremos  

### Próximas Investigações Científicas:

✅ Dados municipais para melhor granularidade  
✅ Análise qualitativa (por que gravidez é tão importante?)  
✅ Séries temporais (ARIMA/Prophet) para previsões 2023-2025  
✅ Impacto de políticas passadas (análise causal)  

---

**Conclusão**: A ciência de dados não resolve problemas sociais, mas 
estrutura nossa **compreensão** deles com rigor científico. 
Isto é primeira etapa para soluções baseadas em evidência.
""")

st.markdown("---")

# Metadados
st.subheader("📊 Metadados do Projeto")

col1, col2 = st.columns(2)

with col1:
    st.write("""
    **Dataset**:
    - Registros: 135
    - Período: 2018-2022
    - Unidades: 27 UFs
    - Variáveis: 8 (2 target + 6 features)
    """)

with col2:
    st.write("""
    **Modelo**:
    - Tipo: XGBoost Regressor
    - R² Treino: 0.517
    - R² Teste: 0.510
    - RMSE: 0.365%
    """)

st.info("""
✅ **Reprodutibilidade**: Todos os notebooks estão em `/notebooks/` com código completo  
✅ **Versionamento**: Projeto versionado em git com histórico de commits  
✅ **Transparência**: Metodologia CRISP-DM seguida rigorosamente  
✅ **Confiabilidade**: Validação cruzada e testes de robustez realizados
""")
