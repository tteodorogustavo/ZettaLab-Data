"""
Página 3: Predições Futuras (Reestruturada com Tabs, 3D e Dark Mode)
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
from theme import apply_dark_theme, section_header, stat_card
from advanced_charts import scatter_3d

st.set_page_config(page_title="Predições", page_icon="🔮", layout="wide")
apply_dark_theme()

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

st.markdown("""
Este módulo utiliza o modelo XGBoost treinado para explorar predições de evasão escolar 
em cenários futuros. **Importante**: As predições assumem que os indicadores socioeconômicos 
se mantêm constantes nos próximos anos. Para previsões realistas com mudanças nos indicadores, 
use a aba "Cenários" abaixo.
""")

st.info("""
⚠️ **Notas Importantes:**

- **Correlação ≠ Causalidade**: Os padrões observados representam associações. 
  A verdadeira causalidade entre mudanças em indicadores e evasão requer pesquisa adicional.

- **Horizonte de Validade**: Predições são mais confiáveis para 1-2 anos à frente. 
  Períodos mais distantes têm incerteza maior.

- **Dados Estaduais**: Análise usa dados agregados por estado (27 observações por ano). 
  Padrões podem variar significativamente em nível municipal ou escolar.
""")

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
    pred_obs = ultima_obs.copy()
    pred_obs['Ano'] = ano
    
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

# Tabs
def render_predicoes():
    """Tab 1: Predições Básicas"""
    section_header("Tabela de Predições", "📋")
    
    st.dataframe(df_pred.style.format({
        'Taxa Abandono Predita': '{:.2f}%',
        'IDHM': '{:.3f}',
        'Desemprego': '{:.2f}%',
        'Renda': 'R$ {:.0f}'
    }), use_container_width=True)
    
    st.markdown("---")
    
    # Gráfico: Histórico + Predições
    st.markdown("### 📈 Série Histórica + Predições")
    
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
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_pred_plot['Ano'], y=df_pred_plot['Taxa'],
        mode='lines+markers', name='Predição',
        line=dict(color='#F59E0B', width=3, dash='dash'),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(245, 158, 11, 0.15)'
    ))
    
    fig.add_hline(y=THRESHOLD_BAIXO, line_dash="dot", line_color="green",
                 annotation_text="Meta PNE")
    fig.add_hline(y=THRESHOLD_ALTO, line_dash="dot", line_color="red",
                 annotation_text="Crítico")
    
    fig.update_layout(
        title=f"Predição para {estado}",
        xaxis_title="Ano",
        yaxis_title="Taxa de Abandono (%)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_grafico_3d():
    """Tab 2: Visualização 3D"""
    section_header("Análise 3D de Predições", "📊")
    
    st.markdown("""
    Visualize as predições em 3D considerando múltiplas dimensões:
    - **Eixo X**: Ano
    - **Eixo Y**: Taxa de Abandono (%)
    - **Eixo Z**: Desemprego (%)
    """)
    
    # Preparar dados para scatter 3D
    df_plot = pd.concat([
        df[df['UF'] == estado][['Ano', 'Taxa_Abandono_Media', 'Taxa_Desemprego']].rename(
            columns={'Taxa_Abandono_Media': 'Taxa', 'Taxa_Desemprego': 'Desemprego'}
        ).assign(Tipo='Histórico'),
        df_pred[['Ano', 'Taxa Abandono Predita', 'Desemprego']].rename(
            columns={'Taxa Abandono Predita': 'Taxa'}
        ).assign(Tipo='Predição')
    ])
    
    fig = go.Figure()
    
    # Histórico
    df_hist_plot = df_plot[df_plot['Tipo'] == 'Histórico']
    fig.add_trace(go.Scatter3d(
        x=df_hist_plot['Ano'],
        y=df_hist_plot['Taxa'],
        z=df_hist_plot['Desemprego'],
        mode='markers+lines',
        name='Histórico',
        marker=dict(size=8, color='#3B82F6'),
        line=dict(color='#3B82F6', width=4)
    ))
    
    # Predição
    df_pred_plot = df_plot[df_plot['Tipo'] == 'Predição']
    fig.add_trace(go.Scatter3d(
        x=df_pred_plot['Ano'],
        y=df_pred_plot['Taxa'],
        z=df_pred_plot['Desemprego'],
        mode='markers+lines',
        name='Predição',
        marker=dict(size=8, color='#F59E0B'),
        line=dict(color='#F59E0B', width=4, dash='dash')
    ))
    
    fig.update_layout(
        title=f"Análise 3D - {estado}",
        scene=dict(
            xaxis_title="Ano",
            yaxis_title="Taxa de Abandono (%)",
            zaxis_title="Desemprego (%)"
        ),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_cenarios():
    """Tab 3: Cenários e Simulações"""
    section_header("Análise de Cenários - 'E se...'", "🎯")
    
    st.markdown("""
    Use os cenários abaixo para explorar **como mudanças em indicadores socioeconômicos**
    poderiam impactar a taxa de evasão escolar no futuro.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
         st.info("""
         **Cenário 1: Melhoria em Desenvolvimento Humano**
         
         Simula um aumento de 5% no Índice de Desenvolvimento Humano (IDHM).
         
         Possíveis mecanismos:
         - Melhorias em educação de base
         - Aumento de acesso a serviços de saúde
         - Maior segurança e estabilidade social
         """)
         
         if st.button("Simular Cenário 1 - IDHM +5%"):
             pred_cenario1 = ultima_obs.copy()
             pred_cenario1['IDHM'] = min(1.0, pred_cenario1['IDHM'] * 1.05)  # IDHM capped at 1.0
             pred_cenario1['Ano'] = 2025
             
             features_c1 = pred_cenario1[FEATURES].values.reshape(1, -1)
             taxa_c1 = model.predict(features_c1)[0]
             taxa_original = df_pred.iloc[-1]['Taxa Abandono Predita']
             reducao_pct = ((taxa_original - taxa_c1)/taxa_original)*100
             
             if taxa_original > taxa_c1:
                 st.success(f"""
                 **Simulação: Impacto da Melhoria de IDHM (5%)**
                 
                 - Taxa Atual (2025): **{taxa_original:.2f}%**
                 - Taxa Simulada com IDHM +5%: **{taxa_c1:.2f}%**
                 - **Redução em pontos percentuais**: {taxa_original - taxa_c1:.3f}
                 - **Melhoria relativa**: {reducao_pct:.2f}%
                 
                 Nota: Este resultado é baseado em padrões observados nos dados.
                 Mudanças reais dependem de múltiplos fatores e políticas implementadas.
                 """)
             else:
                 st.warning(f"""
                 Neste cenário, o IDHM não é o fator limitante para a redução de evasão. 
                 A taxa é mais influenciada por outros fatores (desemprego, renda, taxa de gravidez adolescente).
                 """)
    
     with col2:
         st.info("""
         **Cenário 2: Redução do Desemprego**
         
         Simula uma redução de 10% na taxa de desemprego.
         
         Possíveis mecanismos:
         - Maior estabilidade financeira para famílias
         - Menos necessidade de crianças trabalhar
         - Maior capacidade de investir em educação
         """)
         
         if st.button("Simular Cenário 2 - Desemprego -10%"):
             pred_cenario2 = ultima_obs.copy()
             pred_cenario2['Taxa_Desemprego'] = pred_cenario2['Taxa_Desemprego'] * 0.90
             pred_cenario2['Ano'] = 2025
             
             features_c2 = pred_cenario2[FEATURES].values.reshape(1, -1)
             taxa_c2 = model.predict(features_c2)[0]
             taxa_original = df_pred.iloc[-1]['Taxa Abandono Predita']
             reducao_pct = ((taxa_original - taxa_c2)/taxa_original)*100
             
             if taxa_original > taxa_c2:
                 st.success(f"""
                 **Simulação: Impacto da Redução de Desemprego (10%)**
                 
                 - Taxa Atual (2025): **{taxa_original:.2f}%**
                 - Taxa Simulada com Desemprego -10%: **{taxa_c2:.2f}%**
                 - **Redução em pontos percentuais**: {taxa_original - taxa_c2:.3f}
                 - **Melhoria relativa**: {reducao_pct:.2f}%
                 
                 Nota: Este resultado é baseado em padrões observados nos dados.
                 Mudanças reais dependem de múltiplos fatores e políticas implementadas.
                 """)
             else:
                 st.warning(f"""
                 Neste cenário, o desemprego não é o fator limitante para a redução de evasão. 
                 A taxa é mais influenciada por outros fatores (renda, taxa de gravidez adolescente).
                 """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
     with col1:
         st.info("""
         **Cenário 3: Aumento de Renda Per Capita**
         
         Simula um aumento de 15% na renda per capita.
         
         Possíveis mecanismos:
         - Redução de pobreza extrema
         - Maior poder de compra das famílias
         - Capacidade das famílias manter filhos na escola
         """)
         
         if st.button("Simular Cenário 3 - Renda +15%"):
             pred_cenario3 = ultima_obs.copy()
             pred_cenario3['Renda_Per_Capita'] = pred_cenario3['Renda_Per_Capita'] * 1.15
             pred_cenario3['Ano'] = 2025
             
             features_c3 = pred_cenario3[FEATURES].values.reshape(1, -1)
             taxa_c3 = model.predict(features_c3)[0]
             taxa_original = df_pred.iloc[-1]['Taxa Abandono Predita']
             reducao_pct = ((taxa_original - taxa_c3)/taxa_original)*100
             
             if taxa_original > taxa_c3:
                 st.success(f"""
                 **Simulação: Impacto do Aumento de Renda (15%)**
                 
                 - Taxa Atual (2025): **{taxa_original:.2f}%**
                 - Taxa Simulada com Renda +15%: **{taxa_c3:.2f}%**
                 - **Redução em pontos percentuais**: {taxa_original - taxa_c3:.3f}
                 - **Melhoria relativa**: {reducao_pct:.2f}%
                 
                 Nota: Este resultado é baseado em padrões observados nos dados.
                 Mudanças reais dependem de múltiplos fatores e políticas implementadas.
                 """)
             else:
                 st.warning(f"""
                 Neste cenário, a renda não é o fator limitante para a redução de evasão. 
                 A taxa é mais influenciada por outros fatores.
                 """)
    
     with col2:
         st.warning("""
         **⚠️ Notas Técnicas sobre as Predições Base**
         
         As predições sem modificação de cenários aparecem como retas (constantes) porque:
         
         1. **Assumção de estabilidade**: Indicadores socioeconômicos são mantidos 
            nos mesmos níveis de 2022
         
         2. **Influência limitada do tempo**: Com apenas 5 anos de dados históricos (2018-2022), 
            o componente temporal isolado tem influência reduzida nas predições
         
         3. **Fatores dominantes**: Variáveis como taxa de gravidez adolescente, renda e 
            desemprego dominam o modelo muito mais que mudanças anuais
         
         **Validez das predições**: 
         - Confiável para 1-2 anos à frente
         - Diminui para períodos mais distantes
         
         **Para explorar impactos reais**, use os cenários acima que modificam indicadores.
         """)

# Criar tabs
tab1, tab2, tab3 = st.tabs(["📋 Predições", "📊 Gráfico 3D", "🎯 Cenários"])

with tab1:
    render_predicoes()

with tab2:
    render_grafico_3d()

with tab3:
    render_cenarios()
