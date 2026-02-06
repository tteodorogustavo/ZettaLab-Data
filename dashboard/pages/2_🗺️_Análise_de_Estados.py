"""
Página 2: Análise por Estado (Reestruturada com Tabs e Dark Mode)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
from streamlit_folium import st_folium

sys.path.append(str(Path(__file__).parent.parent))
from config import *
from utils.mapa_helper import criar_mapa_estado_destaque
from theme import apply_dark_theme, section_header, stat_card

st.set_page_config(page_title="Análise de Estados", page_icon="🗺️", layout="wide")
apply_dark_theme()

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

st.title("🗺️ Análise por Estado")

# Seletor global
col1, col2 = st.columns([1, 2])

with col1:
    estado_uf = st.selectbox("Selecione um Estado:", sorted(df['UF'].unique()), key='estado_select')
    estado_nome = estado_uf

with col2:
    anos_range = st.slider("Período:", min_value=2018, max_value=2022, value=(2018, 2022))

# Filtrar dados
df_estado = df[(df['UF'] == estado_uf) & 
              (df['Ano'] >= anos_range[0]) & (df['Ano'] <= anos_range[1])].copy()

if df_estado.empty:
    st.error("❌ Sem dados para este período")
else:
    # Renderizar diferentes tabs
    def render_visao_geral():
        """Tab 1: Visão Geral"""
        section_header("Visão Geral do Estado", "🔍")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        ultima_taxa = df_estado.iloc[-1]['Taxa_Abandono_Media']
        media_taxa = df_estado['Taxa_Abandono_Media'].mean()
        renda = df_estado.iloc[-1]['Renda_Per_Capita']
        
        with col1:
            stat_card("Taxa 2022", f"{ultima_taxa:.2f}%", "📊", "#3B82F6")
        with col2:
            stat_card("Média Período", f"{media_taxa:.2f}%", "📈", "#06B6D4")
        with col3:
            stat_card("Renda Per Capita", f"R$ {renda:,.0f}", "💰", "#10B981")
        with col4:
            classe = "Alto" if ultima_taxa > THRESHOLD_ALTO else ("Médio" if ultima_taxa > THRESHOLD_BAIXO else "Baixo")
            cor = "#EF4444" if classe == "Alto" else "#F59E0B" if classe == "Médio" else "#10B981"
            stat_card("Classe Risco", classe, "⚠️", cor)
        
        st.markdown("---")
        
        # Mapa do estado
        st.markdown("### 📍 Localização do Estado")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            try:
                mapa_pequeno = criar_mapa_estado_destaque(df, 2022, estado_nome)
                st_folium(mapa_pequeno, width=350, height=350)
            except Exception as e:
                st.warning(f"Não foi possível exibir o mapa: {e}")
        
        with col2:
             st.markdown(f"""
             #### {estado_nome}
             
             Este mapa mostra a localização de **{estado_nome}** em relação ao restante do Brasil.
             
             A página "🗺️ Mapa do Brasil" oferece uma visualização interativa completa 
             de todos os estados com zoom temporal e exploração detalhada.
             
             **Funcionalidades Disponíveis:**
             - Estados podem ser clicados para visualizar detalhes específicos
             - Zoom e pan para explorar regiões de interesse
             - Controle temporal permite visualizar evolução dos dados de 2018 a 2022
             """)

    def render_serie_temporal():
        """Tab 2: Série Temporal"""
        section_header("Série Temporal - Taxa de Abandono", "📈")
        
        fig = go.Figure()
        
        # Linha principal
        fig.add_trace(go.Scatter(
            x=df_estado['Ano'], 
            y=df_estado['Taxa_Abandono_Media'],
            mode='lines+markers', 
            name='Taxa Abandono',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        
        # Thresholds
        fig.add_hline(y=THRESHOLD_BAIXO, line_dash="dash", line_color="green", 
                     annotation_text="Meta PNE (1.0%)")
        fig.add_hline(y=THRESHOLD_ALTO, line_dash="dash", line_color="red",
                     annotation_text="Nível Crítico (3.0%)")
        
        fig.update_layout(
            title=f"Evolução - {estado_nome}",
            xaxis_title="Ano",
            yaxis_title="Taxa (%)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def render_indicadores():
        """Tab 3: Indicadores Socioeconômicos"""
        section_header("Indicadores Socioeconômicos - Última Observação", "📊")
        
        ultima_obs = df_estado.iloc[-1]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💡 Desenvolvimento Humano")
            st.info(f"""
            **IDHM**: {ultima_obs['IDHM']:.3f}
            (0=baixíssimo, 1=muito alto)
            
            **PIB Total**: R$ {ultima_obs['PIB_Total_MilReais']:,.0f}M
            
            **Renda Per Capita**: R$ {ultima_obs['Renda_Per_Capita']:,.0f}
            """)
        
        with col2:
            st.markdown("#### 📉 Mercado de Trabalho")
            st.info(f"""
            **Taxa de Desemprego**: {ultima_obs['Taxa_Desemprego']:.2f}%
            
            **Taxa de Gravidez Adolescente**: {ultima_obs['Taxa_Gravidez_Adolescente']:.2f}%
            
            **Índice de Gini**: {ultima_obs['Indice_Gini']:.3f}
            (0=igualdade, 1=desigualdade máxima)
            """)
        
        st.markdown("---")
        
        # Radar chart
        fig = go.Figure(data=go.Scatterpolar(
            r=[ultima_obs['Taxa_Gravidez_Adolescente'], 
               ultima_obs['Renda_Per_Capita']/1000, 
               ultima_obs['Taxa_Desemprego'], 
               ultima_obs['IDHM']*100, 
               ultima_obs['Indice_Gini']*100],
            theta=['Gravidez Adol.', 'Renda (R$ mil)', 'Desemprego', 'IDHM', 'Gini'],
            fill='toself',
            name=estado_nome,
            marker=dict(color='#3B82F6')
        ))
        
        fig.update_layout(
            title=f"Perfil Socioeconômico - {estado_nome}",
            height=400,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def render_comparacao():
        """Tab 4: Comparação com Brasil"""
        section_header("Comparação: Estado vs Brasil", "🔄")
        
        ultima_taxa_estado = df_estado.iloc[-1]['Taxa_Abandono_Media']
        ano_atual = df_estado.iloc[-1]['Ano']
        media_brasil = df[df['Ano'] == ano_atual]['Taxa_Abandono_Media'].mean()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Comparação 2022")
            fig = go.Figure(data=[
                go.Bar(name=estado_nome, 
                      x=[estado_nome], 
                      y=[ultima_taxa_estado], 
                      marker_color='#3B82F6',
                      text=[f'{ultima_taxa_estado:.2f}%'],
                      textposition='auto'),
                go.Bar(name='Média Brasil', 
                      x=['Brasil'], 
                      y=[media_brasil], 
                      marker_color='#06B6D4',
                      text=[f'{media_brasil:.2f}%'],
                      textposition='auto')
            ])
            
            fig.update_layout(title="Taxa de Abandono", height=400, barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Análise Comparativa")
            diferenca = ultima_taxa_estado - media_brasil
            diferenca_pct = (diferenca / media_brasil) * 100
            
            if diferenca > 0:
                st.error(f"""
                **{estado_nome} está ACIMA da média**
                
                - Diferença: **+{diferenca:.2f} p.p.**
                - Variação relativa: **+{diferenca_pct:.1f}%**
                
                ⚠️ Este estado tem uma taxa de abandono mais alta que a média brasileira.
                """)
            elif diferenca < 0:
                st.success(f"""
                **{estado_nome} está ABAIXO da média**
                
                - Diferença: **{diferenca:.2f} p.p.**
                - Variação relativa: **{diferenca_pct:.1f}%**
                
                ✅ Este estado tem uma taxa de abandono mais baixa que a média brasileira.
                """)
            else:
                st.info(f"""
                **{estado_nome} está NA MÉDIA**
                
                - Taxa é aproximadamente igual à média brasileira
                """)

    # Criar tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Visão Geral", "📈 Série Temporal", "📊 Indicadores", "🔄 Comparação"])
    
    with tab1:
        render_visao_geral()
    
    with tab2:
        render_serie_temporal()
    
    with tab3:
        render_indicadores()
    
    with tab4:
        render_comparacao()
