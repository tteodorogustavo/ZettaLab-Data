"""
🗺️ Página 6 - Mapa do Brasil
Análise Espacial de Evasão Escolar por Estado
"""

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import st_folium
import sys
from pathlib import Path

# Adicionar o diretório dashboard ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import *
from utils.mapa_helper import criar_mapa_brasil

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Mapa - Evasão Escolar",
    page_icon="🗺️",
    layout="wide"
)

# ============================================================================
# TÍTULO E DESCRIÇÃO
# ============================================================================

st.title("🗺️ Mapa do Brasil - Análise Espacial")
st.markdown("""
Visualize a taxa de abandono escolar em cada estado do Brasil ao longo dos anos.
Use o controle deslizante abaixo para explorar diferentes períodos (2018-2022).
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
# SELETOR DE ANO
# ============================================================================

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
# MAPA INTERATIVO
# ============================================================================

st.markdown("---")
st.markdown("### Visualização Espacial")

try:
    # Criar mapa
    mapa = criar_mapa_brasil(df, ano_selecionado)
    
    # Exibir mapa no Streamlit
    map_data = st_folium(mapa, width=1200, height=600)
    
except Exception as e:
    st.error(f"❌ Erro ao criar mapa: {e}")
    st.warning("Verifique se o arquivo GeoJSON está disponível em data/geojson/brasil_estados.geojson")

# ============================================================================
# ESTATÍSTICAS DO ANO
# ============================================================================

st.markdown("---")
st.markdown("### Estatísticas do Ano")

df_ano = df[df['Ano'] == ano_selecionado]

if not df_ano.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        taxa_media = df_ano['Taxa_Abandono_Media'].mean()
        st.metric(
            "Taxa Média de Abandono",
            f"{taxa_media*100:.2f}%"
        )
    
    with col2:
        taxa_min = df_ano['Taxa_Abandono_Media'].min()
        estado_min = df_ano.loc[df_ano['Taxa_Abandono_Media'].idxmin(), 'Estado']
        st.metric(
            "Taxa Mínima",
            f"{taxa_min*100:.2f}%",
            f"({estado_min})"
        )
    
    with col3:
        taxa_max = df_ano['Taxa_Abandono_Media'].max()
        estado_max = df_ano.loc[df_ano['Taxa_Abandono_Media'].idxmax(), 'Estado']
        st.metric(
            "Taxa Máxima",
            f"{taxa_max*100:.2f}%",
            f"({estado_max})"
        )
    
    with col4:
        num_estados_alto_risco = (df_ano['Taxa_Abandono_Media'] > THRESHOLD_ALTO).sum()
        st.metric(
            "Estados em Alto Risco",
            f"{num_estados_alto_risco}",
            f"de {len(df_ano)}"
        )

# ============================================================================
# TABELA DE DADOS
# ============================================================================

st.markdown("---")
st.markdown("### Dados Detalhados por Estado")

# Preparar dados para exibição
df_tabela = df_ano[['Estado', 'Taxa_Abandono_Media']].copy()
df_tabela = df_tabela.sort_values('Taxa_Abandono_Media', ascending=False)
df_tabela['Taxa_Abandono_Media'] = df_tabela['Taxa_Abandono_Media'].apply(lambda x: f"{x*100:.2f}%")

# Definir cores baseado na taxa
def colorir_risco(val_str):
    val = float(val_str.rstrip('%')) / 100
    if val <= THRESHOLD_BAIXO:
        return 'background-color: #6BCB77'  # Verde
    elif val <= THRESHOLD_ALTO:
        return 'background-color: #FFD93D'  # Amarelo
    else:
        return 'background-color: #FF6B6B'  # Vermelho

# Exibir tabela
col1, col2 = st.columns([2, 1])

with col1:
    st.dataframe(
        df_tabela.rename(columns={
            'Estado': 'Estado',
            'Taxa_Abandono_Media': 'Taxa de Abandono'
        }),
        use_container_width=True,
        hide_index=True,
        height=400
    )

with col2:
    st.markdown("### Legenda")
    st.markdown("🟢 **Baixo** (≤ 1.0%)")
    st.markdown("🟡 **Médio** (1.0% - 3.0%)")
    st.markdown("🔴 **Alto** (> 3.0%)")
    st.markdown("⚪ **Sem dados**")
    
    st.markdown("---")
    st.markdown("### Metodologia")
    st.markdown("""
    Os thresholds foram definidos com base em:
    - **Meta PNE**: 1.0% (objetivo nacional)
    - **Crise**: 3.0% (3x a meta)
    
    Veja o Notebook 09 para análise detalhada.
    """)

# ============================================================================
# ANÁLISE TEMPORAL
# ============================================================================

st.markdown("---")
st.markdown("### Evolução Temporal (2018-2022)")

df_temporal = df.groupby('Ano')['Taxa_Abandono_Media'].agg(['mean', 'min', 'max'])

col1, col2 = st.columns(2)

with col1:
    import plotly.graph_objects as go
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_temporal.index,
        y=df_temporal['mean'] * 100,
        mode='lines+markers',
        name='Média Nacional',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10)
    ))
    fig.add_trace(go.Scatter(
        x=df_temporal.index,
        y=df_temporal['max'] * 100,
        mode='lines',
        name='Máximo',
        line=dict(color='#FF6B6B', dash='dash', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df_temporal.index,
        y=df_temporal['min'] * 100,
        mode='lines',
        name='Mínimo',
        line=dict(color='#6BCB77', dash='dash', width=2)
    ))
    
    # Adicionar linhas de threshold
    fig.add_hline(y=THRESHOLD_BAIXO*100, line_dash="dot", 
                  line_color="gray", annotation_text="Meta PNE (1.0%)")
    fig.add_hline(y=THRESHOLD_ALTO*100, line_dash="dot", 
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
    st.markdown("#### Insights")
    
    # Calcular variações
    anos = sorted(df['Ano'].unique())
    taxa_inicial = df[df['Ano'] == anos[0]]['Taxa_Abandono_Media'].mean()
    taxa_final = df[df['Ano'] == anos[-1]]['Taxa_Abandono_Media'].mean()
    variacao = taxa_final - taxa_inicial
    variacao_pct = (variacao / taxa_inicial) * 100
    
    if variacao > 0:
        direcao = "📈 Aumentou"
        cor = "#FF6B6B"
    else:
        direcao = "📉 Diminuiu"
        cor = "#6BCB77"
    
    st.markdown(f"""
    **Taxa Média {anos[0]}**: {taxa_inicial*100:.2f}%  
    **Taxa Média {anos[-1]}**: {taxa_final*100:.2f}%  
    **Variação**: {direcao} {abs(variacao_pct):.1f}%
    """)
    
    st.markdown("---")
    
    # Distribuição de risco
    baixo = (df_ano['Taxa_Abandono_Media'] <= THRESHOLD_BAIXO).sum()
    medio = ((df_ano['Taxa_Abandono_Media'] > THRESHOLD_BAIXO) & 
             (df_ano['Taxa_Abandono_Media'] <= THRESHOLD_ALTO)).sum()
    alto = (df_ano['Taxa_Abandono_Media'] > THRESHOLD_ALTO).sum()
    
    st.markdown(f"""
    **Distribuição de Risco ({ano_selecionado})**
    - 🟢 Baixo: {baixo} estados
    - 🟡 Médio: {medio} estados
    - 🔴 Alto: {alto} estados
    """)

st.markdown("---")
st.markdown("""
### Notas Importantes

1. **Dados Históricos**: Visualização de 2018-2022 baseada em dados reais
2. **Granularidade**: Análise em nível estadual (não municipal)
3. **Thresholds**: Baseados em meta PNE (1%) e crise (3%)
4. **Interpretação**: Cores indicam risco relativo à meta nacional

Para análise detalhada de um estado específico, visite a página **Análise de Estados**.
""")
