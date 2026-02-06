"""
🎨 Módulo de Temas e Estilos para o Dashboard
Oferece temas modernos com Dark Mode
"""

import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

# ============================================================================
# CORES DO TEMA DARK MODE MODERNO
# ============================================================================

COLORS = {
    # Cores primárias
    'primary': '#1E3A8A',        # Azul escuro profissional
    'primary_light': '#3B82F6',  # Azul claro
    'primary_dark': '#1E40AF',   # Azul mais escuro
    
    # Cores de status
    'success': '#10B981',         # Verde
    'warning': '#F59E0B',         # Amarelo/Laranja
    'danger': '#EF4444',          # Vermelho
    'info': '#06B6D4',            # Ciano
    
    # Cores neutras (Dark mode)
    'bg_dark': '#0F172A',         # Background muito escuro
    'bg_darker': '#020617',       # Background quase preto
    'surface': '#1E293B',         # Surface cards
    'surface_light': '#334155',   # Surface lighter
    'border': '#475569',          # Borders
    'text': '#F1F5F9',            # Texto claro
    'text_muted': '#CBD5E1',      # Texto muted
    
    # Gradientes
    'gradient_blue': 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
    'gradient_green': 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
    'gradient_orange': 'linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)',
}

# ============================================================================
# CSS CUSTOMIZADO - DARK MODE MODERNO
# ============================================================================

DARK_MODE_CSS = f"""
    <style>
        /* Root variables */
        :root {{
            --primary-color: {COLORS['primary']};
            --primary-light: {COLORS['primary_light']};
            --success-color: {COLORS['success']};
            --warning-color: {COLORS['warning']};
            --danger-color: {COLORS['danger']};
            --info-color: {COLORS['info']};
        }}
        
        /* ============= BACKGROUND ============= */
        body {{
            background-color: {COLORS['bg_dark']};
            color: {COLORS['text']};
        }}
        
        /* ============= TÍTULOS ============= */
        h1 {{
            color: {COLORS['text']};
            font-size: 2.5em;
            font-weight: 800;
            margin-bottom: 20px;
            background: linear-gradient(135deg, {COLORS['primary_light']} 0%, {COLORS['info']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        h2 {{
            color: {COLORS['primary_light']};
            font-size: 1.8em;
            font-weight: 700;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid {COLORS['primary']};
            padding-left: 15px;
        }}
        
        h3 {{
            color: {COLORS['primary_light']};
            font-size: 1.3em;
            font-weight: 600;
        }}
        
        /* ============= MARKDOWN ============= */
        [data-testid="stMarkdownContainer"] {{
            line-height: 1.7;
            color: {COLORS['text']};
        }}
        
        /* ============= MÉTRICAS ============= */
        [data-testid="metric"] {{
            background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['surface_light']} 100%);
            border: 1px solid {COLORS['border']};
            border-left: 4px solid {COLORS['primary_light']};
            border-radius: 12px;
            padding: 20px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }}
        
        [data-testid="metric"]:hover {{
            border-left-color: {COLORS['success']};
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        }}
        
        /* ============= BOTÕES ============= */
        button {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        }}
        
        button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5) !important;
        }}
        
        button:active {{
            transform: translateY(0) !important;
        }}
        
        /* ============= INPUTS ============= */
        [data-testid="stSelectbox"],
        [data-testid="stNumberInput"],
        [data-testid="stSlider"],
        [data-testid="stTextInput"] {{
            border-radius: 8px !important;
        }}
        
        /* ============= DATAFRAMES ============= */
        [data-testid="stDataFrame"] {{
            border: 1px solid {COLORS['border']} !important;
            border-radius: 8px !important;
            background-color: {COLORS['surface']} !important;
        }}
        
        [data-testid="stDataFrame"] thead {{
            background-color: {COLORS['primary']} !important;
            color: white !important;
        }}
        
        [data-testid="stDataFrame"] tbody tr {{
            border-color: {COLORS['border']} !important;
        }}
        
        [data-testid="stDataFrame"] tbody tr:hover {{
            background-color: {COLORS['surface_light']} !important;
        }}
        
        /* ============= ALERTS ============= */
        [data-testid="stAlert"] {{
            border-radius: 8px !important;
            border: 1px solid {COLORS['border']} !important;
            padding: 16px !important;
        }}
        
        /* Info */
        .st-emotion-cache-qg31p5 {{
            background-color: rgba(6, 182, 212, 0.1) !important;
            border-left: 4px solid {COLORS['info']} !important;
        }}
        
        /* Success */
        .st-emotion-cache-1222qye {{
            background-color: rgba(16, 185, 129, 0.1) !important;
            border-left: 4px solid {COLORS['success']} !important;
        }}
        
        /* Warning */
        .st-emotion-cache-yqstza {{
            background-color: rgba(245, 158, 11, 0.1) !important;
            border-left: 4px solid {COLORS['warning']} !important;
        }}
        
        /* Error */
        .st-emotion-cache-ymdysj {{
            background-color: rgba(239, 68, 68, 0.1) !important;
            border-left: 4px solid {COLORS['danger']} !important;
        }}
        
        /* ============= SIDEBAR ============= */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['bg_darker']} 0%, {COLORS['surface']} 100%);
            border-right: 1px solid {COLORS['border']};
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            color: {COLORS['text']};
        }}
        
        /* ============= SEPARADORES ============= */
        hr {{
            border-color: {COLORS['border']} !important;
            margin: 30px 0 !important;
        }}
        
        /* ============= LINKS ============= */
        a {{
            color: {COLORS['primary_light']} !important;
            text-decoration: none;
            transition: all 0.3s ease;
        }}
        
        a:hover {{
            color: {COLORS['success']} !important;
            text-decoration: underline;
        }}
        
        /* ============= SCROLLBAR ============= */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {COLORS['surface']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['primary']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['primary_light']};
        }}
        
        /* ============= CUSTOM CLASSES ============= */
        .gradient-text {{
            background: linear-gradient(135deg, {COLORS['primary_light']} 0%, {COLORS['info']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: bold;
        }}
        
        .card {{
            background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['surface_light']} 100%);
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}
        
        .card:hover {{
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
            transform: translateY(-4px);
            transition: all 0.3s ease;
        }}
    </style>
"""

# ============================================================================
# FUNÇÕES DE APLICAÇÃO DO TEMA
# ============================================================================

def apply_dark_theme():
    """Aplica o tema Dark Mode ao Streamlit"""
    st.markdown(DARK_MODE_CSS, unsafe_allow_html=True)


def section_header(title: str, icon: str = "📊"):
    """
    Cria um header de seção customizado com ícone
    
    Args:
        title: Título da seção
        icon: Emoji ou ícone
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_light']} 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    ">
        <h2 style="
            color: white;
            margin: 0;
            border-left: none;
            padding-left: 0;
            font-size: 1.6em;
        ">{icon} {title}</h2>
    </div>
    """, unsafe_allow_html=True)


def stat_card(label: str, value: str, icon: str = "📊", color: str = "primary"):
    """
    Cria um card de estatística customizado
    
    Args:
        label: Rótulo da estatística
        value: Valor a exibir
        icon: Emoji/ícone
        color: Cor da borda ('primary', 'success', 'warning', 'danger')
    """
    color_map = {
        'primary': COLORS['primary_light'],
        'success': COLORS['success'],
        'warning': COLORS['warning'],
        'danger': COLORS['danger'],
        'info': COLORS['info'],
    }
    
    border_color = color_map.get(color, COLORS['primary_light'])
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['surface_light']} 100%);
        border-left: 4px solid {border_color};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    ">
        <div style="font-size: 2em; margin-bottom: 10px;">{icon}</div>
        <div style="color: {COLORS['text_muted']}; font-size: 0.9em; margin-bottom: 5px;">{label}</div>
        <div style="color: {border_color}; font-size: 2em; font-weight: bold;">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def success_box(text: str, title: str = "✅ Sucesso"):
    """Box de sucesso customizado"""
    st.markdown(f"""
    <div style="
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 4px solid {COLORS['success']};
        border: 1px solid {COLORS['success']};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    ">
        <strong style="color: {COLORS['success']};">{title}</strong><br>
        <span style="color: {COLORS['text']};">{text}</span>
    </div>
    """, unsafe_allow_html=True)


def warning_box(text: str, title: str = "⚠️ Aviso"):
    """Box de aviso customizado"""
    st.markdown(f"""
    <div style="
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid {COLORS['warning']};
        border: 1px solid {COLORS['warning']};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    ">
        <strong style="color: {COLORS['warning']};">{title}</strong><br>
        <span style="color: {COLORS['text']};">{text}</span>
    </div>
    """, unsafe_allow_html=True)


def info_box(text: str, title: str = "ℹ️ Informação"):
    """Box de informação customizado"""
    st.markdown(f"""
    <div style="
        background-color: rgba(6, 182, 212, 0.1);
        border-left: 4px solid {COLORS['info']};
        border: 1px solid {COLORS['info']};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    ">
        <strong style="color: {COLORS['info']};">{title}</strong><br>
        <span style="color: {COLORS['text']};">{text}</span>
    </div>
    """, unsafe_allow_html=True)
