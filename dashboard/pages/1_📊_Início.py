"""
Página 1: Início - KPIs e Visão Geral (Reestruturada com Tabs e Dark Mode)
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
from theme import apply_dark_theme, section_header, stat_card
from custom_tabs import custom_tabs

st.set_page_config(page_title="Início - Dashboard", page_icon="📊", layout="wide")
apply_dark_theme()

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

st.title("📊 Análise de Evasão Escolar - Visão Geral")
st.markdown("**Desafio 2 - Ciência e Governança de Dados (Zetta Lab)**")

# Preparar dados para tabs
def render_kpis():
    """Tab 1: KPIs Principais"""
    section_header("KPIs Principais", "📈")
    
    col1, col2, col3, col4 = st.columns(4)
    
    taxa_media = df['Taxa_Abandono_Media'].mean()
    n_criticos = (df[df['Ano'] == 2022]['Taxa_Abandono_Media'] > THRESHOLD_ALTO).sum()
    n_estados = df['UF'].nunique()
    r2_modelo = 0.510
    
    with col1:
        stat_card("Taxa Média (2018-2022)", f"{taxa_media:.2f}%", "📈", "#3B82F6")
    
    with col2:
        stat_card("Estados Críticos (2022)", f"{n_criticos}", "🚨", "#EF4444")
    
    with col3:
        stat_card("Total de UFs", f"{n_estados}", "🗺️", "#06B6D4")
    
    with col4:
        stat_card("R² Modelo", f"{r2_modelo:.3f}", "🤖", "#10B981")
    
    st.markdown("---")
    
    # Estatísticas detalhadas
    st.markdown("### 📊 Estatísticas Gerais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Taxa de Abandono Escolar (Brasil 2018-2022)**
        
        - **Mínima**: {df['Taxa_Abandono_Media'].min():.2f}% 
        - **Máxima**: {df['Taxa_Abandono_Media'].max():.2f}%
        - **Média**: {taxa_media:.2f}%
        - **Mediana**: {df['Taxa_Abandono_Media'].median():.2f}%
        - **Desvio Padrão**: {df['Taxa_Abandono_Media'].std():.2f}%
        """)
    
    with col2:
        st.warning(f"""
        **Estados em Situação Crítica (2022)**
        
        - **Alto Risco** (>3%): {n_criticos} estados
        - **Médio Risco** (1-3%): {((df[df['Ano'] == 2022]['Taxa_Abandono_Media'] > THRESHOLD_BAIXO) & (df[df['Ano'] == 2022]['Taxa_Abandono_Media'] <= THRESHOLD_ALTO)).sum()} estados
        - **Baixo Risco** (≤1%): {(df[df['Ano'] == 2022]['Taxa_Abandono_Media'] <= THRESHOLD_BAIXO).sum()} estados
        """)

def render_criticos():
    """Tab 2: Estados Críticos e Distribuição"""
    section_header("Estados Críticos", "🚨")
    
    df_2022 = df[df['Ano'] == 2022].copy()
    top10 = df_2022.nlargest(10, 'Taxa_Abandono_Media')[['UF', 'Taxa_Abandono_Media']].reset_index(drop=True)
    top10.columns = ['Estado', 'Taxa (%)']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Top 10 Estados com Maior Risco")
        st.dataframe(top10, use_container_width=True, height=400)
    
    with col2:
        st.markdown("### Distribuição de Risco (2022)")
        
        df_2022['Classe'] = pd.cut(
            df_2022['Taxa_Abandono_Media'],
            bins=[0, THRESHOLD_BAIXO, THRESHOLD_ALTO, float('inf')],
            labels=['Baixo', 'Médio', 'Alto']
        )
        
        dist = df_2022['Classe'].value_counts().sort_index()
        
        fig = go.Figure([go.Pie(
            labels=dist.index,
            values=dist.values,
            marker=dict(colors=['#10B981', '#F59E0B', '#EF4444']),
            textposition='inside',
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title="Distribuição por Classe de Risco",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_tendencia():
    """Tab 3: Tendência Temporal"""
    section_header("Tendência Temporal", "📉")
    
    tendencia = df.groupby('Ano')['Taxa_Abandono_Media'].agg(['mean', 'min', 'max', 'std']).reset_index()
    
    # Gráfico principal
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=tendencia['Ano'], 
        y=tendencia['mean'],
        mode='lines+markers', 
        name='Média',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.2)'
    ))
    
    # Adicionar range (min-max)
    fig.add_trace(go.Scatter(
        x=tendencia['Ano'], 
        y=tendencia['max'],
        mode='lines',
        name='Máximo',
        line=dict(color='#EF4444', dash='dash', width=2),
        showlegend=True
    ))
    
    fig.add_trace(go.Scatter(
        x=tendencia['Ano'], 
        y=tendencia['min'],
        mode='lines',
        name='Mínimo',
        line=dict(color='#10B981', dash='dash', width=2),
        fill='tonexty',
        fillcolor='rgba(16, 185, 129, 0.1)',
        showlegend=True
    ))
    
    # Thresholds
    fig.add_hline(y=THRESHOLD_BAIXO, line_dash="dot", line_color="green", 
                  annotation_text="Meta PNE (1.0%)")
    fig.add_hline(y=THRESHOLD_ALTO, line_dash="dot", line_color="red",
                  annotation_text="Nível Crítico (3.0%)")
    
    fig.update_layout(
        title="Evolução da Taxa de Abandono (2018-2022)",
        xaxis_title="Ano",
        yaxis_title="Taxa (%)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise textual
    st.markdown("---")
    st.markdown("### 📊 Análise da Série")
    
    col1, col2 = st.columns(2)
    
    with col1:
        variacao = tendencia.iloc[-1]['mean'] - tendencia.iloc[0]['mean']
        variacao_pct = (variacao / tendencia.iloc[0]['mean']) * 100
        
        if variacao > 0:
            st.error(f"📈 Tendência: **Crescente**\n\nA taxa média aumentou {abs(variacao_pct):.1f}% no período")
        elif variacao < 0:
            st.success(f"📉 Tendência: **Decrescente**\n\nA taxa média diminuiu {abs(variacao_pct):.1f}% no período")
        else:
            st.info(f"➡️ Tendência: **Estável**\n\nA taxa média manteve-se constante")
    
    with col2:
        volatilidade = tendencia['std'].mean()
        st.info(f"""
        **Volatilidade**
        
        - Desvio Padrão Médio: {volatilidade:.3f}%
        - Amplitude (Max-Min): {tendencia['max'].max() - tendencia['min'].min():.2f}%
        
        Interpretação: Indica variação entre estados em cada ano
        """)

def render_sobre():
    """Tab 4: Sobre o Projeto"""
    section_header("Sobre o Projeto", "ℹ️")
    
    with st.expander("📚 Metodologia CRISP-DM", expanded=False):
        st.markdown("""
        Este projeto segue rigorosamente a metodologia **CRISP-DM** (CRoss Industry Standard Process for Data Mining):
        
        1. **Entendimento do Negócio**: Definir o escopo da análise de evasão escolar
        2. **Entendimento dos Dados**: Explorar 135 registros (27 UFs × 5 anos)
        3. **Preparação dos Dados**: Consolidar múltiplas fontes em dataset íntegro
        4. **Modelagem**: Testar XGBoost, Random Forest, Regressão Linear
        5. **Avaliação**: SHAP analysis para interpretabilidade
        6. **Implantação**: Dashboard interativo para exploração
        """)
    
    with st.expander("🎯 Perguntas de Pesquisa", expanded=False):
        st.markdown("""
        Este dashboard responde às seguintes perguntas:
        
        - **P1**: Qual a magnitude da evasão escolar no Brasil?
        - **P2**: Quais fatores socioeconômicos mais influenciam evasão?
        - **P3**: Como as taxas variam entre estados?
        - **P4**: É possível prever evasão com base em indicadores?
        - **P5**: Quais estados precisam de intervenção urgente?
        """)
    
    with st.expander("🤖 Modelo de ML", expanded=False):
        st.markdown(f"""
        **XGBoost Regressor - Otimizado**
        
        - **Acurácia (R²)**: 0.510 (em dados não vistos)
        - **Baseline Linear**: 0.380 (comparação)
        - **RMSE**: 0.365% na taxa
        - **Validação**: 5-fold cross-validation
        - **Features**: {len(FEATURES)} variáveis socioeconômicas
        """)
    
     with st.expander("📖 Navegação do Dashboard", expanded=False):
         st.markdown("""
          **Páginas Disponíveis:**
          
          1. **📊 Início** (página atual)
             - KPIs gerais
             - Distribuição de risco
             - Tendência temporal
          
          2. **🗺️ Análise de Estados**
             - Exploração por UF
            - Indicadores socioeconômicos
            - Comparação estado vs Brasil
         
         3. **🔮 Predições Futuras**
            - Previsões 2023-2025
            - Análise de cenários
            - Simulações "E se..."
         
         4. **🔬 Análise SHAP**
            - Feature importance global
            - Análise por estado
            - Relações entre variáveis
         
         5. **📋 Conclusões**
            - Storytelling de dados
            - Descobertas principais
            - Limitações honestas
         
         6. **🗺️ Mapa do Brasil**
            - Visualização espacial
            - Série temporal interativa
            - Ranking de estados
         """)
     
     with st.expander("🔧 Metodologia Técnica Detalhada", expanded=False):
         st.markdown("""
         Para aprofundamento técnico sobre qualidade de dados, pré-processamento e tunning de hiperparâmetros:
         
         **Notebooks Disponíveis** (em `/notebooks/`):
         
         - **02_Preparacao_Dados.ipynb**
           - Qualidade de dados: limpeza, validação, tratamento de valores faltantes
           - Integração de múltiplas fontes (INEP, IBGE, Atlas Brasil)
           - Transformações e normalizações aplicadas
         
         - **04_modelagem_regressao.ipynb**
           - Comparação de 3 modelos: Linear Regression, Random Forest, XGBoost
           - Justificativa para seleção de XGBoost
           - Estratégia de validação (train 2018-2021, test 2022)
         
         - **08_otimizacao_hiperparametros.ipynb**
           - GridSearch para otimização de parâmetros XGBoost
           - Análise de sensibilidade
           - Validação cruzada temporal
         
         - **05_avaliacao_shap.ipynb**
           - Análise SHAP detalhada
           - Interpretabilidade do modelo
           - Validação de features importantes
         
         - **09_justificacao_thresholds_risco.ipynb**
           - Justificação científica dos thresholds (1.0% e 3.0%)
           - Análise de recall e precisão
           - Validação da estratégia híbrida
         
         Todos os notebooks são **reprodutíveis** com dados públicos.
         """)

# Criar tabs
tabs_dict = {
    "🎯 KPIs": render_kpis,
    "🚨 Críticos": render_criticos,
    "📉 Tendência": render_tendencia,
    "ℹ️ Sobre": render_sobre
}

# Usar custom_tabs para criar interface com 4 tabs
tab_choice = st.radio(
    "Selecione a visualização:",
    list(tabs_dict.keys()),
    horizontal=True,
    key="inicio_tabs"
)

# Renderizar conteúdo da tab selecionada
tabs_dict[tab_choice]()
