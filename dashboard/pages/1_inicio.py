"""
Página 1: Início - KPIs e Visão Geral
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Adicionar diretório pai ao path para importar config
sys.path.append(str(Path(__file__).parent))
from config import *

st.set_page_config(page_title="Início - Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

st.title("📊 Análise de Evasão Escolar - Visão Geral")
st.markdown("**Desafio 2 - Ciência e Governança de Dados (Zetta Lab)**")

# KPIs
col1, col2, col3, col4 = st.columns(4)

taxa_media = df['Taxa_Abandono_Media'].mean()
n_criticos = (df[df['Ano'] == 2022]['Taxa_Abandono_Media'] > THRESHOLD_ALTO).sum()
n_estados = df['UF'].nunique()
r2_modelo = 0.510

with col1:
    st.metric("📈 Taxa Média", f"{taxa_media:.2f}%", "2018-2022")

with col2:
    st.metric("🚨 Estados Críticos", f"{n_criticos}", "em 2022 (>3%)")

with col3:
    st.metric("🗺️ Total UFs", f"{n_estados}")

with col4:
    st.metric("🤖 R² Modelo", f"{r2_modelo:.3f}", "XGBoost Otimizado")

st.markdown("---")

# Distribuição de Risco
st.subheader("📊 Distribuição de Risco (2022)")

df_2022 = df[df['Ano'] == 2022].copy()
df_2022['Classe'] = pd.cut(
    df_2022['Taxa_Abandono_Media'],
    bins=[0, THRESHOLD_BAIXO, THRESHOLD_ALTO, float('inf')],
    labels=['Baixo', 'Médio', 'Alto']
)

col1, col2 = st.columns([1, 2])

with col1:
    dist = df_2022['Classe'].value_counts().sort_index()
    st.write("**Contagem:**")
    for cls, cnt in dist.items():
        st.write(f"• **{cls}**: {cnt} estado(s)")

with col2:
    fig = px.pie(values=dist.values, names=dist.index, 
                color=dist.index, color_discrete_map=CORES_RISCO)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Top 5
st.subheader("🔴 Top 5 Estados com Maior Risco")

top5 = df_2022.nlargest(5, 'Taxa_Abandono_Media')[['UF', 'Taxa_Abandono_Media']]
top5.columns = ['Estado', 'Taxa (%)']

col1, col2 = st.columns([1, 2])

with col1:
    st.dataframe(top5.reset_index(drop=True))

with col2:
    fig = go.Figure([go.Bar(x=top5['Estado'], y=top5['Taxa (%)'],
                            marker=dict(color=top5['Taxa (%)'], colorscale='Reds'))])
    fig.update_layout(title="Taxa de Abandono", xaxis_title="Estado", 
                     yaxis_title="Taxa (%)", height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Tendência
st.subheader("📉 Tendência Temporal")

tendencia = df.groupby('Ano')['Taxa_Abandono_Media'].agg(['mean', 'min', 'max']).reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=tendencia['Ano'], y=tendencia['mean'],
                        mode='lines+markers', name='Média'))
fig.update_layout(title="Evolução da Taxa", xaxis_title="Ano", 
                 yaxis_title="Taxa (%)", height=400)
st.plotly_chart(fig, use_container_width=True)
