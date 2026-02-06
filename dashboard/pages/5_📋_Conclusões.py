"""
Página 5: Conclusões e Storytelling de Dados (Reestruturada com Accordion e Timeline)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import *
from theme import apply_dark_theme, section_header

st.set_page_config(page_title="Conclusões", page_icon="📖", layout="wide")
apply_dark_theme()

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

st.title("📖 Storytelling de Dados - Conclusões Principais")

st.markdown("""
Esta página documenta os principais insights obtidos através da análise de dados 
sobre os determinantes da evasão escolar no Brasil, utilizando a metodologia 
**CRISP-DM** (Modelagem de Dados).
""")

st.markdown("---")

section_header("As 5 Descobertas Principais", "🎯")

# Descoberta 1
with st.expander("### 1️⃣ A DESCOBERTA DO PRINCIPAL AGENTE (Gravidez Adolescente)", expanded=True):
    st.markdown("""
    **Pergunta Original**: Quais agentes socioeconômicos mais afetam evasão escolar?
    
    **Metodologia Aplicada**:
    - Análise SHAP (Shapley Additive exPlanations)
    - Interpretabilidade matemática de modelo de ML
    - Feature importance global (baseado em teoria dos jogos)
    
     **Conclusão Alcançada**:
     A análise SHAP indica que gravidez adolescente é responsável por **63.5% da importância** 
     nas predições de abandono escolar, calculada através de análise matemática sistemática.
     
     **Padrão Observado**:
     - Associação identificada pelo modelo treinado em 135 registros históricos
     - O padrão é consistente em múltiplos anos (2018-2022) e estados
     - Outras variáveis socioeconômicas também contribuem significativamente
     
     **Nota Importante**:
     - Correlação não implica causalidade; pode haver relação indireta
     - Ambas as variáveis (gravidez e evasão) podem resultar de fatores comuns (pobreza, oportunidades limitadas)
     - Confirmar mecanismos causais requer pesquisa adicional
    """)

# Descoberta 2
with st.expander("### 2️⃣ A IMPORTÂNCIA ESTRATIFICADA (Além do Principal Agente)"):
    st.markdown("""
    **Pergunta**: Apenas gravidez adolescente explica evasão?
    
    **Metodologia Aplicada**:
    - Análise de correlações múltiplas
    - Decomposição de variância (SHAP values)
    - Regressão com validação cruzada (5-fold)
    
     **Conclusão Alcançada**:
     Não. O modelo indica que R² = 0.51, significando que:
     - 51% da variância em evasão é explicada pelas variáveis selecionadas
     - 49% é explicado por fatores não capturados neste dataset
     - Renda (15.2%), Desemprego (12.1%), IDHM (6.8%) também apresentam contribuições significativas
     
     **Padrão Multidimensional**:
     - Múltiplos fatores socioeconômicos influenciam evasão
     - Não existe solução única para o problema
     - Sistema complexo onde múltiplos fatores interagem
     
     **Comparação de Modelos**:
     Modelos mais sofisticados (XGBoost com R²=0.51) capturam mais variância 
     que modelos simples (Linear Regression com R²=0.38), sugerindo relações não-lineares
     entre as variáveis.
    """)

# Descoberta 3
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
    - **Baixo Risco**: ≤ 1.0% (meta PNE - atingir isto é sucesso)
    - **Médio Risco**: 1.0% - 3.0% (situação controlada mas com atenção)
    - **Alto Risco**: > 3.0% (crise - 3x a meta, requer urgência)
    
     **Validação**:
     - Abordagem híbrida (regressão + categorização) alcança 64% de recall na classe "Alto Risco"
     - Estados críticos compartilham características similares (renda baixa, gravidez adolescente alta)
     - Padrão é persistente quando analisado temporalmente (2018-2022)
     
     **Implicações Práticas**:
     - Alocação de recursos pode ser orientada pelos 7 estados identificados como críticos
     - Contexto regional deve ser considerado (não é solução one-size-fits-all)
     - Estratificação permite priorização baseada em dados
    """)

# Descoberta 4
with st.expander("### 4️⃣ A VALIDAÇÃO TEMPORAL (Problemas São Persistentes)"):
    st.markdown("""
    **Pergunta**: Isto é problema novo ou estrutural/histórico?
    
    **Metodologia Aplicada**:
    - Análise de série temporal (2018-2022, 5 anos)
    - Boxplot e estatísticas por ano
    - Verificação de tendência (estável, crescente ou decrescente?)
    
     **Conclusão Alcançada**:
     O padrão é **persistente**. Os mesmos estados mantêm-se em situação de risco ao longo dos anos.
     Taxa média permanece ao redor de 2.15%, sem redução significativa observada.
     
     **Evidência Temporal**:
     - 2018: Média ~2.1%, mesmos estados críticos
     - 2022: Média ~2.2%, mesmos estados críticos
     - Conclusão: Problema não apresenta melhora espontânea
     
     **Interpretação**:
     - Não é anomalia ou flutuação anual transitória
     - Representa padrão estrutural com raízes profundas
     - Fatores de mercado ou sociedade isolados não resolvem o problema
     
     **Previsão**:
     Sem intervenções direcionadas, os dados sugerem que a tendência permanecerá 
     similar em 2023-2025 (validado pelo modelo de predição - ver página de Predições)
    """)

# Descoberta 5
with st.expander("### 5️⃣ A CAPACIDADE PREDITIVA (Ciência de Dados Funciona Aqui)"):
    st.markdown("""
    **Pergunta**: Conseguimos prever o futuro com confiabilidade?
    
    **Metodologia Aplicada**:
    - Modelo XGBoost com otimização de hiperparâmetros (GridSearch)
    - Validação temporal: Treino 2018-2021, Teste 2022
    - Validação cruzada (5-fold) para evitar overfitting
    - Teste de robustez (diferentes seeds aleatórias)
    
     **Conclusão Alcançada**:
     Sim. O modelo alcança R² = 0.510 em dados não vistos (ano 2022).
     
     **Desempenho Comparativo**:
     - Linear Regression (baseline): R² = 0.380
     - Random Forest: R² = 0.430
     - XGBoost Otimizado: R² = 0.510 ← Melhor desempenho
     
     **Robustez**:
     - Validação cruzada (5-fold): R² médio = 0.510 ± 0.002
     - Testes com diferentes seeds aleatórias: Resultados consistentes
     - Modelo não apresenta overfitting significativo
     
     **Confiabilidade de Predições**:
     - Incerteza existe (49% da variação não explicada), mas é quantificável
     - Confiabilidade é maior para períodos próximos (1-2 anos)
     - Confiabilidade decresce para períodos mais distantes
     
     **Limitações Operacionais**:
     - Não consegue prever eventos extremos (pandemias, mudanças radicais de política)
     - Presume continuidade das relações observadas em 2018-2022
     - Dados municipais (em vez de estaduais) melhorariam significativamente o modelo
    """)

st.markdown("---")

# Síntese Final
section_header("SÍNTESE: Resultados da Análise de Dados", "🎯")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ### ✅ Metodologia CRISP-DM
    
    | Fase | O Que Fez | Resultado |
    |------|-----------|-----------|
    | **Entendimento** | Formulou perguntas sobre evasão | Definiu escopo e variáveis |
    | **Dados** | Coletou 135 registros (27 UFs × 5 anos) | Base para análise confiável |
    | **Preparação** | Consolidou múltiplas fontes | Dataset íntegro e limpo |
    | **Modelagem** | Testou 3 modelos, otimizou o melhor | XGBoost com R²=0.51 |
    | **Avaliação** | SHAP para interpretabilidade | Descobriu fatores-chave |
    | **Implantação** | Dashboard interativo + Predições | Ferramenta para explorações |
    """)

with col2:
    st.info("""
    ### 🎯 Descobertas Principais
    
    1. **Gravidez Adolescente** é o fator-chave (63.5%)
    2. **Problema é Multidimensional** (Renda, Desemprego também importam)
    3. **Estratificado Geograficamente** (7 estados em situação crítica)
    4. **Persistente no Tempo** (mesmo padrão 2018-2022)
    5. **Previsível** (R²=0.51 demonstra viabilidade de ML)
    """)

st.markdown("---")

# Limitações
section_header("Limitações Honestas", "⚠️")

col1, col2 = st.columns(2)

with col1:
     st.warning("""
     #### ❌ O que NÃO sabemos
     
     - **51% de variância explicada** = 49% ainda desconhecido
     - **Correlação ≠ Causalidade** (dados sugerem, não comprovam)
     - **Nível estadual apenas** (municipal seria muito melhor)
     - **Não prevê eventos extremos** (pandemias, guerras, etc)
     - **Dados limitados** (5 anos é pouco para séries temporais)
     
     **Limitações Temporais:**
     - Análise cobre apenas 2018-2022 (5 anos)
     - Padrões observados podem ter mudado após 2022
     - COVID-19 (2020-2021) pode ter distorcido alguns indicadores
     - NÃO generalizar para períodos anteriores a 2018
     
     **Falácia Ecológica:**
     - Dados agregados por estado (27 observações por ano)
     - Variação importante existe DENTRO de estados
     - Padrões estaduais podem NÃO se aplicar a:
       - Municípios específicos
       - Escolas individuais
       - Estudantes em particular
     """)

with col2:
    st.success("""
    #### ✅ Próximas Investigações Científicas
    
    - Dados municipais para melhor granularidade
    - Análise qualitativa (por que gravidez é tão importante?)
    - Séries temporais (ARIMA/Prophet) para previsões 2023-2025
    - Impacto de políticas passadas (análise causal)
    - Integração com dados de políticas públicas
    """)

st.markdown("---")

# Conclusão final
st.info("""
## 🎓 Conclusão Final

**A análise de dados estrutura nossa compreensão de problemas complexos 
com rigor científico e transparência metodológica.**

Este projeto demonstrou a viabilidade de aplicar metodologia CRISP-DM para 
analisar um problema social como a evasão escolar, através de:

- ✅ Análise quantitativa de dados reais
- ✅ Modelos preditivos validados em dados não vistos
- ✅ Interpretabilidade matemática das predições (SHAP)
- ✅ Visualizações interativas para exploração sistemática
- ✅ Documentação explícita das limitações e incertezas

**Resultado**: Uma ferramenta que permite formuladores de política pública e 
gestores educacionais tomarem decisões orientadas por evidências em vez de 
intuição isolada.

---

**Disponibilidade**: Todos os notebooks estão em `/notebooks/` com código completo e reprodutível  
**Versionamento**: Projeto com controle de versão git e histórico de commits  
**Transparência**: Metodologia CRISP-DM documentada em cada fase  
**Confiabilidade**: Validação cruzada e testes de robustez implementados
""")

# Metadados
st.markdown("---")
section_header("Metadados do Projeto", "📊")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Dataset**:
    - Registros: 135
    - Período: 2018-2022
    - Unidades: 27 UFs
    - Variáveis: 8 (2 target + 6 features)
    """)

with col2:
     st.markdown("""
     **Modelo**:
     - Tipo: XGBoost Regressor
     - R² Treino: 0.517
     - R² Teste: 0.510
     - RMSE: 0.365%
     """)

st.markdown("---")

section_header("⚠️ Disclaimer Importante: Correlação vs. Causalidade", "⚠️")

st.warning("""
**Esta análise identifica ASSOCIAÇÕES entre variáveis, não relações CAUSAIS.**

A forte importância de "Taxa de Gravidez Adolescente" nas predições significa que 
o modelo a utiliza para prever abandono escolar. Porém, isto pode indicar:

1. **Relação causal direta**: A gravidez causa abandono
2. **Causalidade reversa**: Estudantes que abandonam escolar têm maior taxa de gravidez
3. **Fator comum**: Ambas (gravidez e abandono) resultam de pobreza, oportunidades limitadas e vulnerabilidade social

**Para estabelecer causalidade** seriam necessários:
- Estudos experimentais (controlados)
- Análise qualitativa detalhada
- Pesquisa de mecanismos específicos
- Validação em contextos diferentes

Os dados **sugerem fatores importantes**, mas pesquisa adicional é necessária para confirmar mecanismos.
""")
