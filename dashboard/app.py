"""
📊 Dashboard Interativo - Análise de Evasão Escolar
Desafio 2 - Ciência e Governança de Dados (Zetta Lab)
"""

import streamlit as st
import pandas as pd
import numpy as np
from config import *
from theme import apply_dark_theme, section_header, stat_card, info_box, warning_box

# ============================================================================
# CONFIGURAÇÃO DO STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="Dashboard - Evasão Escolar",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar tema Dark Mode Moderno
apply_dark_theme()

# ============================================================================
# CARREGAMENTO DE DADOS
# ============================================================================

@st.cache_data
def load_data():
    """Carrega dados com cache para melhor performance"""
    return pd.read_csv(DATA_FILE)

@st.cache_resource
def load_model():
    """Carrega modelo XGBoost otimizado"""
    import pickle
    with open(MODEL_FILE, 'rb') as f:
        return pickle.load(f)

# Tentar carregar dados e modelo
try:
    df = load_data()
    model = load_model()
    dados_carregados = True
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {str(e)}")
    dados_carregados = False

# ============================================================================
# PÁGINA PRINCIPAL
# ============================================================================

def main():
    """Página inicial do dashboard"""
    
    # Título
    st.title(TITULO_PRINCIPAL)
    st.markdown(f"### {SUBTITULO}")
    st.markdown(DESCRICAO)
    
    if not dados_carregados:
        st.warning("⚠️ Não foi possível carregar os dados. Verifique os caminhos dos arquivos.")
        return
    
    st.markdown("---")
    
    # ===== KPIs NO TOPO =====
    st.markdown("")  # Espaçamento
    
    col1, col2, col3, col4 = st.columns(4)
    
    taxa_media = df['Taxa_Abandono_Media'].mean()
    n_estados = df['UF'].nunique()
    n_criticos = (df[df['Ano'] == 2022]['Taxa_Abandono_Media'] > THRESHOLD_ALTO).sum()
    r2_modelo = 0.510
    
    with col1:
        stat_card("Taxa Média Abandono", f"{taxa_media:.2f}%", "📈", "warning")
    
    with col2:
        stat_card("Estados Críticos (>3%)", f"{n_criticos}", "🚨", "danger")
    
    with col3:
        stat_card("Total de Estados", f"{n_estados}", "🗺️", "info")
    
    with col4:
        stat_card("Modelo R² Score", f"{r2_modelo:.3f}", "🤖", "success")
    
    st.markdown("---")
    
    # ===== DISTRIBUIÇÃO DE RISCO (2022) =====
    section_header("Distribuição de Risco (2022)", "📊")
    
    df_2022 = df[df['Ano'] == 2022].copy()
    df_2022['Classe_Risco'] = pd.cut(
        df_2022['Taxa_Abandono_Media'],
        bins=[0, THRESHOLD_BAIXO, THRESHOLD_ALTO, float('inf')],
        labels=['Baixo', 'Médio', 'Alto']
    )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Contagem por classe
        dist_risco = df_2022['Classe_Risco'].value_counts().sort_index()
        
        st.write("**Contagem por Classe:**")
        for classe, count in dist_risco.items():
            cor = CORES_RISCO[classe]
            st.write(f"<span style='color: {cor}'>●</span> **{classe}**: {count} estado(s)", 
                    unsafe_allow_html=True)
    
    with col2:
        # Gráfico de pizza
        import plotly.express as px
        fig = px.pie(
            values=dist_risco.values,
            names=dist_risco.index,
            color=dist_risco.index,
            color_discrete_map=CORES_RISCO,
            title="Distribuição de Estados por Risco"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ===== TOP 5 ESTADOS CRÍTICOS =====
    section_header("Top 5 Estados com Maior Risco (2022)", "🔴")
    
    top5 = df_2022.nlargest(5, 'Taxa_Abandono_Media')[['UF', 'Taxa_Abandono_Media']].copy()
    top5.columns = ['Estado', 'Taxa Abandono (%)']
    top5 = top5.reset_index(drop=True)
    top5.index = top5.index + 1
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(top5.style.format({'Taxa Abandono (%)': '{:.2f}%'}))
    
    with col2:
        # Gráfico de barras
        import plotly.graph_objects as go
        fig = go.Figure(data=[
            go.Bar(x=top5['Estado'], y=top5['Taxa Abandono (%)'],
                   marker=dict(color=top5['Taxa Abandono (%)'],
                             colorscale='Reds', showscale=False))
        ])
        fig.update_layout(
            title="Taxa de Abandono dos 5 Estados Críticos",
            xaxis_title="Estado",
            yaxis_title="Taxa de Abandono (%)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ===== TENDÊNCIA TEMPORAL =====
    section_header("Tendência Temporal (2018-2022)", "📉")
    
    tendencia = df.groupby('Ano')['Taxa_Abandono_Media'].agg(['mean', 'min', 'max']).reset_index()
    
    import plotly.graph_objects as go
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=tendencia['Ano'], y=tendencia['mean'],
        mode='lines+markers',
        name='Média',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=tendencia['Ano'], y=tendencia['max'],
        mode='lines',
        name='Máximo',
        line=dict(color='rgba(255, 0, 0, 0.2)', width=1),
        fill=None
    ))
    
    fig.add_trace(go.Scatter(
        x=tendencia['Ano'], y=tendencia['min'],
        mode='lines',
        name='Mínimo',
        line=dict(color='rgba(0, 255, 0, 0.2)', width=1),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title="Evolução da Taxa de Abandono Escolar",
        xaxis_title="Ano",
        yaxis_title="Taxa de Abandono (%)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ===== INFORMAÇÕES ADICIONAIS =====
    section_header("Sobre este Dashboard", "ℹ️")
    
    with st.expander("📖 Metodologia"):
        st.markdown("""
        **CRISP-DM (Cross Industry Standard Process for Data Mining)**
        
        Este dashboard apresenta resultados de análise estruturada em 6 fases:
        
        1. **Entendimento do Negócio**: Identificar agentes/fenômenos que causam evasão
        2. **Entendimento dos Dados**: Coletar 135 registros (27 UFs × 5 anos)
        3. **Preparação**: Consolidar variáveis socioeconômicas
        4. **Modelagem**: Treinar XGBoost com otimização de hiperparâmetros
        5. **Avaliação**: Validar modelo com SHAP analysis (R² = 0.510)
        6. **Implantação**: Dashboard interativo para exploração de insights
        """)
    
    with st.expander("🔧 Modelo Utilizado"):
        st.markdown(f"""
        **XGBoost (eXtreme Gradient Boosting)**
        
        - **Performance**: R² = 0.510 (explica 51% da variância)
        - **Hiperparâmetros Otimizados**: Encontrados via GridSearch com 5-fold CV
        - **Capacidade Preditiva**: Pode prever taxa de abandono com base em:
          - IDHM
          - Taxa de Desemprego
          - Renda Per Capita
          - Índice de Gini
          - Taxa de Gravidez Adolescente
          - PIB Total
        - **Vantagem**: Interpretável via SHAP (não é black-box)
        """)
    
    with st.expander("📊 Definições de Risco"):
        st.markdown(f"""
        **Thresholds de Classificação:**
        
        - **Baixo Risco**: Taxa ≤ {THRESHOLD_BAIXO:.1f}% (Meta do PNE)
        - **Médio Risco**: {THRESHOLD_BAIXO:.1f}% < Taxa ≤ {THRESHOLD_ALTO:.1f}%
        - **Alto Risco**: Taxa > {THRESHOLD_ALTO:.1f}% (3× a meta = Crise)
        
        Os thresholds foram definidos com base em:
        1. Análise estatística de percentis
        2. Alinhamento com meta do Plano Nacional de Educação
        3. Validação com dados 2018-2022
        """)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.header("⚙️ Configurações")
    
    st.markdown("---")
    st.subheader("📌 Navegação")
    st.markdown("""
    Use o menu ao lado para navegar entre as páginas:
    
    1. **Início** - Esta página (KPIs e visão geral)
    2. **Análise de Estados** - Explorar dados por UF
    3. **Predições** - Previsões para 2023-2025
    4. **SHAP Analysis** - Interpretabilidade do modelo
    5. **Conclusões** - Storytelling de dados
    """)
    
    st.markdown("---")
    st.subheader("ℹ️ Informações")
    st.info("""
    **Período de Dados**: 2018-2022  
    **Total de Registros**: 135 (27 UFs × 5 anos)  
    **Última Atualização**: Fevereiro 2026  
    **Modelo**: XGBoost Otimizado (R² = 0.510)
    """)
    
    st.markdown("---")
    st.subheader("🔗 Links Úteis")
    st.markdown("""
    - [📓 Notebook 04 - Modelagem](../notebooks/04_modelagem_regressao.ipynb)
    - [📓 Notebook 05 - SHAP Analysis](../notebooks/05_avaliacao_shap.ipynb)
    - [📓 Notebook 08 - Otimização](../notebooks/08_otimizacao_hiperparametros.ipynb)
    - [📄 README Desafio 2](../README_DESAFIO2_DRAFT.md)
    """)

# ============================================================================
# EXECUTAR
# ============================================================================

if __name__ == "__main__":
    main()
