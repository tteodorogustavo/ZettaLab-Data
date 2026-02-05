"""
Página 2: Análise por Estado
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import *

st.set_page_config(page_title="Análise de Estados", page_icon="🗺️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

st.title("🗺️ Análise por Estado")

# Seletor de estado
col1, col2 = st.columns([1, 2])

with col1:
    estado = st.selectbox("Selecione um Estado:", sorted(df['UF'].unique()))

with col2:
    anos_range = st.slider("Período:", min_value=2018, max_value=2022, 
                           value=(2018, 2022))

# Filtrar dados
df_estado = df[(df['UF'] == estado) & 
              (df['Ano'] >= anos_range[0]) & (df['Ano'] <= anos_range[1])].copy()

if df_estado.empty:
    st.error("Sem dados para este período")
else:
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    ultima_taxa = df_estado.iloc[-1]['Taxa_Abandono_Media']
    media_taxa = df_estado['Taxa_Abandono_Media'].mean()
    renda = df_estado.iloc[-1]['Renda_Per_Capita']
    
    with col1:
        st.metric("Taxa 2022", f"{ultima_taxa:.2f}%")
    with col2:
        st.metric("Média Período", f"{media_taxa:.2f}%")
    with col3:
        st.metric("Renda Per Capita", f"R$ {renda:,.0f}")
    with col4:
        classe = "Alto" if ultima_taxa > THRESHOLD_ALTO else ("Médio" if ultima_taxa > THRESHOLD_BAIXO else "Baixo")
        st.metric("Classe Risco", classe)
    
    st.markdown("---")
    
    # Série temporal
    st.subheader("📈 Série Temporal - Taxa de Abandono")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_estado['Ano'], y=df_estado['Taxa_Abandono_Media'],
                            mode='lines+markers', name='Taxa Abandono',
                            line=dict(color='#1f77b4', width=3)))
    fig.add_hline(y=THRESHOLD_BAIXO, line_dash="dash", line_color="green", 
                 annotation_text="Meta PNE (1.0%)")
    fig.add_hline(y=THRESHOLD_ALTO, line_dash="dash", line_color="red",
                 annotation_text="Nível Crítico (3.0%)")
    fig.update_layout(title=f"Evolução - {estado}", xaxis_title="Ano",
                     yaxis_title="Taxa (%)", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Indicadores Socioeconômicos
    st.subheader("📊 Indicadores Socioeconômicos - Última Observação")
    
    ultima_obs = df_estado.iloc[-1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        indicators = {
            'IDHM': f"{ultima_obs['IDHM']:.3f}",
            'Taxa Desemprego': f"{ultima_obs['Taxa_Desemprego']:.2f}%",
            'Renda Per Capita': f"R$ {ultima_obs['Renda_Per_Capita']:,.0f}",
        }
        for ind, val in indicators.items():
            st.write(f"**{ind}**: {val}")
    
    with col2:
        indicators2 = {
            'Índice Gini': f"{ultima_obs['Indice_Gini']:.3f}",
            'Gravidez Adolescente': f"{ultima_obs['Taxa_Gravidez_Adolescente']:.2f}%",
            'PIB': f"R$ {ultima_obs['PIB_Total_MilReais']:,.0f}M",
        }
        for ind, val in indicators2.items():
            st.write(f"**{ind}**: {val}")
    
    st.markdown("---")
    
    # Comparação com Brasil
    st.subheader("🔄 Comparação: Estado vs Brasil")
    
    media_brasil = df[df['Ano'] == df_estado.iloc[-1]['Ano']]['Taxa_Abandono_Media'].mean()
    
    fig = go.Figure(data=[
        go.Bar(name=estado, x=[estado], y=[ultima_taxa], marker_color='#1f77b4'),
        go.Bar(name='Média Brasil', x=['Brasil'], y=[media_brasil], marker_color='#ff7f0e')
    ])
    fig.update_layout(title=f"Comparação 2022", barmode='group', height=400)
    st.plotly_chart(fig, use_container_width=True)
