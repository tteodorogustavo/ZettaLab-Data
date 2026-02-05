"""
Página 3: Predições Futuras
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import sys
import pickle

sys.path.append(str(Path(__file__).parent.parent))
from config import *

st.set_page_config(page_title="Predições", page_icon="🔮", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

@st.cache_resource
def load_model():
    with open(MODEL_FILE, 'rb') as f:
        return pickle.load(f)

df = load_data()
model = load_model()

st.title("🔮 Predições Futuras")

col1, col2 = st.columns([1, 1])

with col1:
    estado = st.selectbox("Selecione um Estado:", sorted(df['UF'].unique()), key='pred_estado')

with col2:
    ano_final = st.slider("Prever até o ano:", 2023, 2025, 2024)

# Obter última observação do estado
ultima_obs = df[df['UF'] == estado].iloc[-1].copy()

# Criar predições
predicoes = []
for ano in range(2023, ano_final + 1):
    # Copiar últimos valores (assumindo estabilidade)
    pred_obs = ultima_obs.copy()
    pred_obs['Ano'] = ano
    
    # Features para modelo
    features_pred = pred_obs[FEATURES].values.reshape(1, -1)
    taxa_pred = model.predict(features_pred)[0]
    
    predicoes.append({
        'Ano': ano,
        'Taxa Abandono Predita': taxa_pred,
        'IDHM': pred_obs['IDHM'],
        'Desemprego': pred_obs['Taxa_Desemprego'],
        'Renda': pred_obs['Renda_Per_Capita']
    })

df_pred = pd.DataFrame(predicoes)

st.markdown("---")

# Tabela de predições
st.subheader("📋 Tabela de Predições")
st.dataframe(df_pred.style.format({
    'Taxa Abandono Predita': '{:.2f}%',
    'IDHM': '{:.3f}',
    'Desemprego': '{:.2f}%',
    'Renda': 'R$ {:.0f}'
}), use_container_width=True)

st.markdown("---")

# Gráfico: Histórico + Predições
st.subheader("📈 Série Histórica + Predições")

df_hist = df[df['UF'] == estado][['Ano', 'Taxa_Abandono_Media']].copy()
df_hist.columns = ['Ano', 'Taxa']
df_hist['Tipo'] = 'Histórico'

df_pred_plot = df_pred[['Ano', 'Taxa Abandono Predita']].copy()
df_pred_plot.columns = ['Ano', 'Taxa']
df_pred_plot['Tipo'] = 'Predição'

df_combined = pd.concat([df_hist, df_pred_plot], ignore_index=True)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_hist['Ano'], y=df_hist['Taxa'],
    mode='lines+markers', name='Histórico',
    line=dict(color='#1f77b4', width=3)
))

fig.add_trace(go.Scatter(
    x=df_pred_plot['Ano'], y=df_pred_plot['Taxa'],
    mode='lines+markers', name='Predição',
    line=dict(color='#ff7f0e', width=3, dash='dash')
))

fig.add_hline(y=THRESHOLD_BAIXO, line_dash="dash", line_color="green",
             annotation_text="Meta PNE")
fig.add_hline(y=THRESHOLD_ALTO, line_dash="dash", line_color="red",
             annotation_text="Crítico")

fig.update_layout(
    title=f"Predição para {estado}",
    xaxis_title="Ano",
    yaxis_title="Taxa de Abandono (%)",
    hovermode='x unified',
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Cenários
st.subheader("📊 Análise de Cenários - 'E se...'")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **Cenário 1: Melhora de IDHM em 5%**
    
    Se conseguíssemos aumentar IDHM em 5%, qual seria 
    o impacto na taxa de abandono?
    """)
    
    if st.button("Simular Cenário 1"):
        pred_cenario1 = ultima_obs.copy()
        pred_cenario1['IDHM'] = pred_cenario1['IDHM'] * 1.05
        pred_cenario1['Ano'] = 2025
        
        features_c1 = pred_cenario1[FEATURES].values.reshape(1, -1)
        taxa_c1 = model.predict(features_c1)[0]
        taxa_original = df_pred.iloc[-1]['Taxa Abandono Predita']
        
        st.success(f"""
        **Resultado do Cenário:**
        - Taxa Original (2025): {taxa_original:.2f}%
        - Taxa com IDHM +5%: {taxa_c1:.2f}%
        - Redução: {taxa_original - taxa_c1:.2f}% (ou {((taxa_original - taxa_c1)/taxa_original)*100:.1f}%)
        """)

with col2:
    st.info("""
    **Cenário 2: Redução de Desemprego em 10%**
    
    Se a taxa de desemprego caísse em 10%, qual seria 
    o impacto na taxa de abandono?
    """)
    
    if st.button("Simular Cenário 2"):
        pred_cenario2 = ultima_obs.copy()
        pred_cenario2['Taxa_Desemprego'] = pred_cenario2['Taxa_Desemprego'] * 0.90
        pred_cenario2['Ano'] = 2025
        
        features_c2 = pred_cenario2[FEATURES].values.reshape(1, -1)
        taxa_c2 = model.predict(features_c2)[0]
        taxa_original = df_pred.iloc[-1]['Taxa Abandono Predita']
        
        st.success(f"""
        **Resultado do Cenário:**
        - Taxa Original (2025): {taxa_original:.2f}%
        - Taxa com Desemprego -10%: {taxa_c2:.2f}%
        - Redução: {taxa_original - taxa_c2:.2f}% (ou {((taxa_original - taxa_c2)/taxa_original)*100:.1f}%)
        """)
