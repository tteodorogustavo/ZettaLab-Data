"""
Página 4: SHAP Analysis - Interpretabilidade (Reestruturada com Tabs e 3D)
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
from theme import apply_dark_theme, section_header

st.set_page_config(page_title="SHAP Analysis", page_icon="🔬", layout="wide")
apply_dark_theme()

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

st.title("🔬 Análise SHAP - Interpretabilidade do Modelo")

st.markdown("""
SHAP (SHapley Additive exPlanations) utiliza teoria dos jogos para explicar 
as predições do modelo de forma matematicamente rigorosa.
""")

# Dados de importância SHAP
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

def render_importancia_global():
    """Tab 1: Importância Global"""
    section_header("Importância Global das Variáveis", "🎯")
    
    st.markdown("""
    Estas são as variáveis que **mais influenciam** as predições de abandono escolar.
    Os valores indicam quanto cada variável afeta o resultado final.
    """)
    
    col1, col2 = st.columns([1.2, 1.8])
    
    with col1:
        st.markdown("**Tabela de Importância**")
        st.dataframe(df_importance.style.format({
            'SHAP Value': '{:.3f}',
            'Importância (%)': '{:.1f}%'
        }), use_container_width=True, height=400)
    
    with col2:
        fig = go.Figure(data=[
            go.Bar(
                y=df_importance.sort_values('SHAP Value')['Variável'],
                x=df_importance.sort_values('SHAP Value')['Importância (%)'],
                orientation='h',
                marker=dict(
                    color=df_importance.sort_values('SHAP Value')['Importância (%)'],
                    colorscale='Blues',
                    showscale=True
                ),
                text=df_importance.sort_values('SHAP Value')['Importância (%)'].apply(lambda x: f'{x:.1f}%'),
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title='Importância de Cada Variável',
            xaxis_title='Importância (%)',
            yaxis_title='Variável',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Interpretação
    section_header("Interpretação dos Achados", "📖")
     
    st.markdown("""
    ### 🔴 Achado Principal: Gravidez Adolescente (63.5%)
     
    A análise SHAP indica que **gravidez adolescente é o fator mais importante** 
    para explicar variações em evasão escolar entre estados.
     
    **Contexto Técnico:**
    - SHAP valores medem importância das features no modelo de predição
    - Isto representa ASSOCIAÇÃO observada, não causalidade estabelecida
    - Ambas (gravidez adolescente e evasão) podem resultar de vulnerabilidade social comum
     
    **Possíveis Mecanismos** (requerem confirmação em pesquisa adicional):
    - Impacto direto: Gravidez interrompe trajetória educacional
    - Fator comum: Pobreza e oportunidades limitadas predispõem ambos os eventos
     
    ---
     
    ### 💰 Achado 2: Renda Per Capita (15.2%)
     
    Renda mais baixa apresenta forte associação com maior evasão.
     
    **Possível Mecanismo**: Pobreza → necessidade de trabalhar → abandono escolar
     
    **Nota Importante**: Correlação não implica causalidade direta.
     
    ---
     
    ### 💼 Achado 3: Desemprego (12.1%)
     
    Taxa de desemprego elevada mostra associação com maior evasão.
     
    **Possível Mecanismo**: Desemprego dos pais → insegurança financeira → menor investimento em educação
     
    **Nota Importante**: Pode haver relação indireta através de renda/estabilidade financeira.
    """)

def render_perfil_estado():
    """Tab 2: Perfil por Estado"""
    section_header("Importância Individual por Estado", "🎯")
    
    estado = st.selectbox("Selecione um Estado para análise:", sorted(df['UF'].unique()), key='shap_estado')
    
    df_estado = df[df['UF'] == estado].tail(1)
    
    if not df_estado.empty:
        obs = df_estado.iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Estado**: {estado}
            
            **Ano**: {int(obs['Ano'])}
            
            **Taxa de Abandono**: {obs['Taxa_Abandono_Media']:.2f}%
            """)
        
        with col2:
            # Radar chart dos indicadores
            fig = go.Figure(data=go.Scatterpolar(
                r=[obs['Taxa_Gravidez_Adolescente'], 
                   obs['Renda_Per_Capita']/1000, 
                   obs['Taxa_Desemprego'], 
                   obs['IDHM']*100, 
                   obs['Indice_Gini']*100],
                theta=['Gravidez Adol.', 'Renda (R$ mil)', 'Desemprego', 'IDHM', 'Gini'],
                fill='toself',
                name=estado,
                marker=dict(color='#3B82F6')
            ))
            
            fig.update_layout(
                title=f"Perfil Socioeconômico - {estado}",
                height=400,
                font=dict(size=11)
            )
            
            st.plotly_chart(fig, use_container_width=True)

def render_dependencia():
    """Tab 3: Análise de Dependência"""
    section_header("Análise de Dependência - Como cada Variável Afeta Evasão?", "📊")
    
    variavel_selecionada = st.selectbox(
        "Escolha uma variável para análise:",
        ['Taxa_Gravidez_Adolescente', 'Renda_Per_Capita', 'Taxa_Desemprego', 'IDHM'],
        key='shap_var'
    )
    
    # Gráfico de dispersão
    if variavel_selecionada == 'Taxa_Gravidez_Adolescente':
        fig = px.scatter(df, x='Taxa_Gravidez_Adolescente', y='Taxa_Abandono_Media',
                        color='Taxa_Abandono_Media', size='Renda_Per_Capita',
                        hover_name='UF', title='Relação: Gravidez Adolescente → Evasão',
                        color_continuous_scale='RdYlGn_r', size_max=30)
    
    elif variavel_selecionada == 'Renda_Per_Capita':
        fig = px.scatter(df, x='Renda_Per_Capita', y='Taxa_Abandono_Media',
                        color='Taxa_Abandono_Media', size='Taxa_Gravidez_Adolescente',
                        hover_name='UF', title='Relação: Renda Per Capita → Evasão',
                        color_continuous_scale='RdYlGn_r', size_max=30)
    
    elif variavel_selecionada == 'Taxa_Desemprego':
        fig = px.scatter(df, x='Taxa_Desemprego', y='Taxa_Abandono_Media',
                        color='Taxa_Abandono_Media', size='Renda_Per_Capita',
                        hover_name='UF', title='Relação: Desemprego → Evasão',
                        color_continuous_scale='RdYlGn_r', size_max=30)
    
    else:  # IDHM
        fig = px.scatter(df, x='IDHM', y='Taxa_Abandono_Media',
                        color='Taxa_Abandono_Media', size='Taxa_Gravidez_Adolescente',
                        hover_name='UF', title='Relação: IDHM → Evasão',
                        color_continuous_scale='RdYlGn_r', size_max=30)
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    ✅ **Interpretação**:
    - Pontos à esquerda = variável baixa → normalmente menos evasão
    - Pontos vermelhos = maior evasão
    - Tamanho dos pontos = importância de outra variável
    - Padrão visual mostra a relação entre variáveis
    """)

def render_grafico_3d():
    """Tab 4: Visualização 3D Multidimensional"""
    section_header("Análise 3D Multidimensional", "📊")
    
    st.markdown("""
    Visualize como três variáveis importantes se relacionam simultaneamente:
    - **Eixo X**: Taxa de Gravidez Adolescente
    - **Eixo Y**: Renda Per Capita
    - **Eixo Z**: Taxa de Abandono
    
    O tamanho dos pontos representa Desemprego, e a cor representa IDHM.
    """)
    
    # Criar scatter 3D
    fig = go.Figure(data=[go.Scatter3d(
        x=df['Taxa_Gravidez_Adolescente'],
        y=df['Renda_Per_Capita'],
        z=df['Taxa_Abandono_Media'],
        mode='markers',
        marker=dict(
            size=5,
            color=df['IDHM'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="IDHM")
        ),
        text=[f"UF: {uf}<br>Gravidez: {g:.2f}%<br>Renda: R$ {r:.0f}<br>Abandono: {a:.2f}%<br>Desemprego: {d:.2f}%" 
              for uf, g, r, a, d in zip(df['UF'], df['Taxa_Gravidez_Adolescente'], 
                                         df['Renda_Per_Capita'], df['Taxa_Abandono_Media'],
                                         df['Taxa_Desemprego'])],
        hoverinfo='text'
    )])
    
    fig.update_layout(
        title='Relação Multidimensional (SHAP)',
        scene=dict(
            xaxis_title='Gravidez Adolescente (%)',
            yaxis_title='Renda Per Capita (R$)',
            zaxis_title='Taxa de Abandono (%)'
        ),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Criar tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Importância Global", "👤 Perfil Estado", "📊 Dependência", "📈 3D Multidimensional"])

with tab1:
    render_importancia_global()

with tab2:
    render_perfil_estado()

with tab3:
    render_dependencia()

with tab4:
    render_grafico_3d()

st.markdown("---")

st.warning("""
⚠️ **Disclaimer Técnico Importante**

**SHAP Valores Medem Importância, Não Causalidade:**
- Os valores SHAP indicam a importância de cada feature para o modelo fazer suas predições
- Isto não equivale a estabelecer relações causais no mundo real
- A correlação forte observada pode indicar:
  1. Relação causal direta (gravidez → evasão)
  2. Causalidade reversa (evasão → gravidez)
  3. Ambas causadas por fator comum não observado (vulnerabilidade social)

**Para confirmar mecanismos causais seria necessário:**
- Pesquisa qualitativa ou etnográfica
- Estudos experimentais ou quasi-experimentais
- Análise de séries temporais com defasagens apropriadas
- Validação em diferentes contextos geográficos

A análise SHAP é excelente para **identificar padrões importantes**, 
mas pesquisa adicional é necessária para **entender por quê** esses padrões existem.
""")
