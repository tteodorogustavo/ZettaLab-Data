"""
🗺️ Página 6 - Mapa do Brasil (Reestruturada com Tabs)
Análise Espacial de Evasão Escolar por Estado
"""

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

# Adicionar o diretório dashboard ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import *
from utils.mapa_helper import criar_mapa_brasil
from theme import apply_dark_theme, section_header

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Mapa - Evasão Escolar",
    page_icon="🗺️",
    layout="wide"
)

apply_dark_theme()

# ============================================================================
# TÍTULO E DESCRIÇÃO
# ============================================================================

st.title("🗺️ Mapa do Brasil - Análise Espacial")
st.markdown("""
Visualize a taxa de abandono escolar em cada estado do Brasil ao longo dos anos.
Os controles abaixo permitem explorar diferentes períodos (2018-2022) e analisar variações espaciais.
""")

# ============================================================================
# CARREGAR DADOS
# ============================================================================

@st.cache_data
def carregar_dados():
    df = pd.read_csv(DATA_FILE)
    return df

try:
    df = carregar_dados()
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

# ============================================================================
# SELETOR DE ANO GLOBAL
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### Ano")

with col2:
    # Slider para selecionar o ano
    ano_selecionado = st.slider(
        "Selecione o ano",
        min_value=min(ANOS_DISPONIVEIS),
        max_value=max(ANOS_DISPONIVEIS),
        value=max(ANOS_DISPONIVEIS),
        step=1,
        label_visibility="collapsed"
    )

with col3:
    # Informação do ano
    st.markdown(f"**{ano_selecionado}**")

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["🗺️ Mapa Interativo", "📊 Ranking de Estados", "📈 Tendência Temporal"])

# TAB 1: Mapa Interativo
with tab1:
    st.markdown("---")
    section_header("Visualização Espacial", "🗺️")
    
    try:
        # Criar mapa
        mapa = criar_mapa_brasil(df, ano_selecionado)
        
        # Exibir mapa no Streamlit
        map_data = st_folium(mapa, width=1200, height=600)
        
    except Exception as e:
        st.error(f"❌ Erro ao criar mapa: {e}")
        st.warning("Verifique se o arquivo GeoJSON está disponível em data/geojson/brasil_estados.geojson")
    
    # Estatísticas do ano
    st.markdown("---")
    section_header("Estatísticas do Ano", "📊")
    
    df_ano = df[df['Ano'] == ano_selecionado]
    
    if not df_ano.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            taxa_media = df_ano['Taxa_Abandono_Media'].mean()
            st.metric(
                "Taxa Média de Abandono",
                f"{taxa_media:.2f}%"
            )
        
        with col2:
            taxa_min = df_ano['Taxa_Abandono_Media'].min()
            estado_min = df_ano.loc[df_ano['Taxa_Abandono_Media'].idxmin(), 'UF']
            st.metric(
                "Taxa Mínima",
                f"{taxa_min:.2f}%",
                f"({estado_min})"
            )
        
        with col3:
            taxa_max = df_ano['Taxa_Abandono_Media'].max()
            estado_max = df_ano.loc[df_ano['Taxa_Abandono_Media'].idxmax(), 'UF']
            st.metric(
                "Taxa Máxima",
                f"{taxa_max:.2f}%",
                f"({estado_max})"
            )
        
        with col4:
            num_estados_alto_risco = (df_ano['Taxa_Abandono_Media'] > THRESHOLD_ALTO).sum()
            st.metric(
                "Estados em Alto Risco",
                f"{num_estados_alto_risco}",
                f"de {len(df_ano)}"
            )

# TAB 2: Ranking de Estados
with tab2:
    st.markdown("---")
    section_header("Dados Detalhados por Estado", "📊")
    
    # Preparar dados para exibição
    df_tabela = df[df['Ano'] == ano_selecionado][['UF', 'Taxa_Abandono_Media']].copy()
    df_tabela = df_tabela.sort_values('Taxa_Abandono_Media', ascending=False).reset_index(drop=True)
    df_tabela.columns = ['Estado', 'Taxa (%)']
    df_tabela.index = df_tabela.index + 1  # Começar ranking em 1
    
    # Definir cores baseado na taxa
    def colorir_risco(val):
        if val <= THRESHOLD_BAIXO:
            return 'background-color: #10B981; color: white'  # Verde
        elif val <= THRESHOLD_ALTO:
            return 'background-color: #F59E0B; color: white'  # Amarelo
        else:
            return 'background-color: #EF4444; color: white'  # Vermelho
    
    # Exibir tabela com ranking
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Ranking de Estados")
        st.dataframe(
            df_tabela.style.format({'Taxa (%)': '{:.2f}%'}).applymap(
                colorir_risco,
                subset=['Taxa (%)']
            ),
            use_container_width=True,
            height=500
        )
    
    with col2:
        st.markdown("### Legenda")
        st.markdown("🟢 **Baixo** (≤ 1.0%)")
        st.markdown("🟡 **Médio** (1.0% - 3.0%)")
        st.markdown("🔴 **Alto** (> 3.0%)")
        
        st.markdown("---")
        st.markdown("### Thresholds")
        st.markdown("""
        - **Meta PNE**: 1.0%
        - **Crise**: 3.0% (3x a meta)
        """)
    
    # Gráfico de distribuição
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histograma
        fig_hist = go.Figure(data=[
            go.Histogram(
                x=df[df['Ano'] == ano_selecionado]['Taxa_Abandono_Media'],
                nbinsx=10,
                marker_color='#3B82F6',
                name='Taxa de Abandono'
            )
        ])
        
        fig_hist.update_layout(
            title=f'Distribuição de Taxa de Abandono ({ano_selecionado})',
            xaxis_title='Taxa (%)',
            yaxis_title='Número de Estados',
            height=400
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Box plot
        fig_box = go.Figure(data=[
            go.Box(
                y=df[df['Ano'] == ano_selecionado]['Taxa_Abandono_Media'],
                name='Taxa de Abandono',
                marker_color='#06B6D4'
            )
        ])
        
        fig_box.update_layout(
            title=f'Distribuição de Taxa de Abandono ({ano_selecionado})',
            yaxis_title='Taxa (%)',
            height=400
        )
        
        st.plotly_chart(fig_box, use_container_width=True)

# TAB 3: Tendência Temporal
with tab3:
    st.markdown("---")
    section_header("Evolução Temporal (2018-2022)", "📈")
    
    df_temporal = df.groupby('Ano')['Taxa_Abandono_Media'].agg(['mean', 'min', 'max', 'std']).reset_index()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = go.Figure()
        
        # Linha de média
        fig.add_trace(go.Scatter(
            x=df_temporal['Ano'],
            y=df_temporal['mean'],
            mode='lines+markers',
            name='Média Nacional',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        
        # Máximo
        fig.add_trace(go.Scatter(
            x=df_temporal['Ano'],
            y=df_temporal['max'],
            mode='lines',
            name='Máximo',
            line=dict(color='#EF4444', dash='dash', width=2)
        ))
        
        # Mínimo
        fig.add_trace(go.Scatter(
            x=df_temporal['Ano'],
            y=df_temporal['min'],
            mode='lines',
            name='Mínimo',
            line=dict(color='#10B981', dash='dash', width=2),
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        
        # Thresholds
        fig.add_hline(y=THRESHOLD_BAIXO, line_dash="dot", 
                     line_color="gray", annotation_text="Meta PNE (1.0%)")
        fig.add_hline(y=THRESHOLD_ALTO, line_dash="dot", 
                     line_color="red", annotation_text="Crise (3.0%)")
        
        fig.update_layout(
            title="Taxa de Abandono Escolar no Brasil",
            xaxis_title="Ano",
            yaxis_title="Taxa (%)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Insights")
        
        # Calcular variações
        anos = sorted(df['Ano'].unique())
        taxa_inicial = df[df['Ano'] == anos[0]]['Taxa_Abandono_Media'].mean()
        taxa_final = df[df['Ano'] == anos[-1]]['Taxa_Abandono_Media'].mean()
        variacao = taxa_final - taxa_inicial
        variacao_pct = (variacao / taxa_inicial) * 100
        
        if variacao > 0:
            direcao = "📈 Aumentou"
            cor = "#EF4444"
        else:
            direcao = "📉 Diminuiu"
            cor = "#10B981"
        
        st.markdown(f"""
        **Taxa Média {anos[0]}**: {taxa_inicial:.2f}%  
        **Taxa Média {anos[-1]}**: {taxa_final:.2f}%  
        **Variação**: {direcao} {abs(variacao_pct):.1f}%
        """)
        
        st.markdown("---")
        
        # Distribuição de risco
        df_ano = df[df['Ano'] == ano_selecionado]
        baixo = (df_ano['Taxa_Abandono_Media'] <= THRESHOLD_BAIXO).sum()
        medio = ((df_ano['Taxa_Abandono_Media'] > THRESHOLD_BAIXO) & 
                (df_ano['Taxa_Abandono_Media'] <= THRESHOLD_ALTO)).sum()
        alto = (df_ano['Taxa_Abandono_Media'] > THRESHOLD_ALTO).sum()
        
        st.markdown(f"""
        **Distribuição ({ano_selecionado})**
        
        - 🟢 Baixo: {baixo}
        - 🟡 Médio: {medio}
        - 🔴 Alto: {alto}
        """)

# Notas Importantes
st.markdown("---")
st.info("""
### ℹ️ Notas Importantes

1. **Dados Históricos**: Visualização de 2018-2022 baseada em dados reais
2. **Granularidade**: Análise em nível estadual (não municipal)
3. **Thresholds**: Baseados em meta PNE (1%) e crise (3%)
4. **Interpretação**: Cores indicam risco relativo à meta nacional

Para análise detalhada de um estado específico, visite a página **Análise de Estados**.
""")
