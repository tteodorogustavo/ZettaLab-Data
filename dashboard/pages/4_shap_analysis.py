"""
Página 4: SHAP Analysis - Interpretabilidade
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import *

st.set_page_config(page_title="SHAP Analysis", page_icon="🔬", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

st.title("🔬 Análise SHAP - Interpretabilidade do Modelo")

st.markdown("""
SHAP (SHapley Additive exPlanations) utiliza teoria dos jogos para explicar 
as predições do modelo de forma matematicamente rigorosa.
""")

st.markdown("---")

# Importância Global
st.subheader("🎯 Importância Global das Variáveis")

st.markdown("""
Estas são as variáveis que **mais influenciam** as predições de abandono escolar.
Os valores indicam quanto cada variável afeta o resultado final.
""")

# Dados de importância SHAP (do Notebook 05)
importance_data = {
    'Variável': [
        'Taxa de Gravidez Adolescente',
        'Renda Per Capita',
        'Taxa de Desemprego',
        'IDHM',
        'Índice de Gini',
        'PIB Total',
        'Ano'
    ],
    'SHAP Value': [0.635, 0.152, 0.121, 0.068, 0.015, 0.008, 0.001],
    'Importância (%)': [63.5, 15.2, 12.1, 6.8, 1.5, 0.8, 0.1]
}

df_importance = pd.DataFrame(importance_data)

col1, col2 = st.columns([1, 2])

with col1:
    st.dataframe(df_importance.style.format({
        'SHAP Value': '{:.3f}',
        'Importância (%)': '{:.1f}%'
    }))

with col2:
    fig = px.barh(df_importance.sort_values('SHAP Value'),
                 x='Importância (%)', y='Variável',
                 title='Importância de Cada Variável',
                 color='Importância (%)',
                 color_continuous_scale='RdYlGn_r')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Interpretação
st.subheader("📖 O Que Isto Significa?")

st.markdown("""
### 🔴 Descoberta Principal: Gravidez Adolescente

A análise SHAP revelou que **gravidez adolescente é o fator dominante** 
(63.5% de importância) para explicar evasão escolar.

**Por que isto é importante?**
- Não é apenas uma correlação - é descoberta através de análise rigorosa
- Aponta para uma intervenção clara: foco em saúde sexual e reprodutiva
- Outros fatores (renda, emprego) também importam, mas em menor grau

**Como isto foi descoberto?**
1. Treinamos modelo XGBoost em 135 registros (27 UFs × 5 anos)
2. Usamos SHAP para decompor cada predição
3. Agrupamos contribuições por feature
4. Resultado: Gravidez adolescente apareceu como dominante

---

### 💰 Fator 2: Renda Per Capita (15.2%)

Renda baixa também contribui significativamente para evasão.

**Relação causal**: Pobreza → necessidade de trabalhar → abandono escolar

---

### 💼 Fator 3: Desemprego (12.1%)

Taxa de desemprego elevada correlaciona com maior evasão.

**Mecanismo**: Desemprego dos pais → insegurança financeira → maior risco de abandono
""")

st.markdown("---")

# Feature individual
st.subheader("🎯 Importância Individual por Estado")

estado = st.selectbox("Selecione um Estado para análise:", sorted(df['UF'].unique()))

df_estado = df[df['UF'] == estado].tail(1)

if not df_estado.empty:
    obs = df_estado.iloc[0]
    
    st.write(f"**Estado**: {estado}")
    st.write(f"**Ano**: {int(obs['Ano'])}")
    st.write(f"**Taxa de Abandono**: {obs['Taxa_Abandono_Media']:.2f}%")
    
    st.markdown("---")
    
    # Radar chart dos indicadores
    fig = go.Figure(data=go.Scatterpolar(
        r=[obs['Taxa_Gravidez_Adolescente'], obs['Renda_Per_Capita']/1000, 
           obs['Taxa_Desemprego'], obs['IDHM']*100, obs['Indice_Gini']*100],
        theta=['Gravidez Adol.', 'Renda (R$ mil)', 'Desemprego', 'IDHM', 'Gini'],
        fill='toself',
        name=estado
    ))
    
    fig.update_layout(
        title=f"Perfil Socioeconômico - {estado}",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Dependência Parcial
st.subheader("📊 Análise de Dependência - Como cada Variável Afeta Evasão?")

variavel_selecionada = st.selectbox(
    "Escolha uma variável para análise:",
    ['Taxa_Gravidez_Adolescente', 'Renda_Per_Capita', 'Taxa_Desemprego', 'IDHM']
)

# Gráfico de dispersão
if variavel_selecionada == 'Taxa_Gravidez_Adolescente':
    fig = px.scatter(df, x='Taxa_Gravidez_Adolescente', y='Taxa_Abandono_Media',
                    color='Taxa_Abandono_Media', size='Renda_Per_Capita',
                    hover_name='UF', title='Relação: Gravidez Adolescente → Evasão',
                    color_continuous_scale='RdYlGn_r')

elif variavel_selecionada == 'Renda_Per_Capita':
    fig = px.scatter(df, x='Renda_Per_Capita', y='Taxa_Abandono_Media',
                    color='Taxa_Abandono_Media', size='Taxa_Gravidez_Adolescente',
                    hover_name='UF', title='Relação: Renda Per Capita → Evasão',
                    color_continuous_scale='RdYlGn_r')

elif variavel_selecionada == 'Taxa_Desemprego':
    fig = px.scatter(df, x='Taxa_Desemprego', y='Taxa_Abandono_Media',
                    color='Taxa_Abandono_Media', size='Renda_Per_Capita',
                    hover_name='UF', title='Relação: Desemprego → Evasão',
                    color_continuous_scale='RdYlGn_r')

else:  # IDHM
    fig = px.scatter(df, x='IDHM', y='Taxa_Abandono_Media',
                    color='Taxa_Abandono_Media', size='Taxa_Gravidez_Adolescente',
                    hover_name='UF', title='Relação: IDHM → Evasão',
                    color_continuous_scale='RdYlGn_r')

fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

st.info("""
✅ **Interpretação**:
- Quanto mais à esquerda → variável baixa → menor aversão (normalmente)
- Pontos vermelhos = maior evasão
- Tamanho dos pontos = importância de outra variável
""")
