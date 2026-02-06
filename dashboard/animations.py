"""
✨ Módulo de Animações Lottie para o Dashboard
Oferece loading spinners, success animations, etc.
"""

import streamlit as st
import requests
import json

# ============================================================================
# URLS DE ANIMAÇÕES LOTTIE (De LottieFiles.com - Free)
# ============================================================================

LOTTIE_ANIMATIONS = {
    # Loading
    "loading": "https://lottie.host/e0d83766-1a4c-4ab0-bfce-6b5b47fa49f3/LOKqHazQkT.json",
    "loading_bars": "https://lottie.host/f1c22ae2-31ca-4da2-9f38-a8ab29c8c2f9/MZW8g0oq0e.json",
    "loading_spinner": "https://lottie.host/d2d3a31c-db3b-44a0-ba5a-70249f0186f3/RzuYvCMb7v.json",
    
    # Success
    "success": "https://lottie.host/6bfcc899-c0f8-44c2-b07e-cd0beb0c0f6f/W5l19UDSTM.json",
    "success_checkmark": "https://lottie.host/1c4f5149-2998-4c5a-b3f7-0ba3e3a81ff3/yQzDqXLPKn.json",
    "success_confetti": "https://lottie.host/e124e7cf-f32a-4df1-a0eb-44903a3e34ef/eM9V6cFKfH.json",
    
    # Error
    "error": "https://lottie.host/b59e4e3c-b3c5-4fb4-8fdf-9f3d87a7c6cf/vGPbVp5Gho.json",
    "error_sad": "https://lottie.host/4a8f05c6-eef3-44b0-b13a-40e35e72d74c/gWdL3G4WLe.json",
    
    # Others
    "data_analysis": "https://lottie.host/1f9d7a4f-2f0c-446e-a47b-0c6b8e4c0e5d/abc123.json",
    "chart_growth": "https://lottie.host/7d3f3c3c-3c3c-3c3c-3c3c-3c3c3c3c3c3c/abc456.json",
}

# ============================================================================
# FUNÇÃO PARA CARREGAR ANIMAÇÕES LOTTIE
# ============================================================================

def load_lottie_url(url: str):
    """
    Carrega animação Lottie de uma URL
    
    Args:
        url: URL da animação Lottie
        
    Returns:
        dict: JSON da animação ou None se falhar
    """
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        st.warning(f"⚠️ Não foi possível carregar animação: {e}")
    return None


def load_lottie_local(filepath: str):
    """
    Carrega animação Lottie de arquivo local
    
    Args:
        filepath: Caminho para arquivo JSON Lottie
        
    Returns:
        dict: JSON da animação
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Não foi possível carregar arquivo: {e}")
    return None


# ============================================================================
# COMPONENTES COM ANIMAÇÕES
# ============================================================================

def show_loading_animation(text: str = "Carregando..."):
    """
    Mostra animação de loading com texto
    
    Args:
        text: Texto a exibir durante loading
    """
    from streamlit_lottie import st_lottie
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        animation = load_lottie_url(LOTTIE_ANIMATIONS["loading_spinner"])
        if animation:
            st_lottie(animation, height=200, key="loading")
    
    with col2:
        st.markdown(f"""
        <div style="display: flex; align-items: center; height: 200px;">
            <h3 style="color: #3B82F6;">{text}</h3>
        </div>
        """, unsafe_allow_html=True)


def show_success_animation(message: str = "Sucesso!", subtitle: str = ""):
    """
    Mostra animação de sucesso
    
    Args:
        message: Mensagem principal
        subtitle: Subtítulo/descrição
    """
    from streamlit_lottie import st_lottie
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        animation = load_lottie_url(LOTTIE_ANIMATIONS["success_confetti"])
        if animation:
            st_lottie(animation, height=250, key="success")
    
    with col2:
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; justify-content: center; height: 250px;">
            <h2 style="color: #10B981; margin: 0;">✅ {message}</h2>
            {f'<p style="color: #CBD5E1;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)


def show_error_animation(message: str = "Erro!", subtitle: str = ""):
    """
    Mostra animação de erro
    
    Args:
        message: Mensagem de erro
        subtitle: Detalhes do erro
    """
    from streamlit_lottie import st_lottie
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        animation = load_lottie_url(LOTTIE_ANIMATIONS["error"])
        if animation:
            st_lottie(animation, height=250, key="error")
    
    with col2:
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; justify-content: center; height: 250px;">
            <h2 style="color: #EF4444; margin: 0;">❌ {message}</h2>
            {f'<p style="color: #CBD5E1;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)


def show_data_analysis_animation():
    """Mostra animação de análise de dados"""
    from streamlit_lottie import st_lottie
    
    animation = load_lottie_url(LOTTIE_ANIMATIONS["loading"])
    if animation:
        st_lottie(animation, height=300, key="data_analysis")


# ============================================================================
# PROGRESS BAR COM ANIMAÇÃO
# ============================================================================

def animated_progress_bar(progress: float, label: str = "Progresso"):
    """
    Barra de progresso customizada com animação
    
    Args:
        progress: Valor de 0 a 1 (0% a 100%)
        label: Rótulo da barra
    """
    percentage = min(max(progress, 0), 1)
    percent_display = percentage * 100
    
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <p style="color: #CBD5E1; font-size: 0.9em; margin-bottom: 8px;">
            {label}: <strong style="color: #3B82F6;">{percent_display:.0f}%</strong>
        </p>
        <div style="
            width: 100%;
            height: 8px;
            background-color: #334155;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
        ">
            <div style="
                width: {percentage * 100}%;
                height: 100%;
                background: linear-gradient(90deg, #3B82F6 0%, #06B6D4 100%);
                border-radius: 10px;
                animation: progress 0.5s ease-out;
                box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
            "></div>
        </div>
    </div>
    <style>
        @keyframes progress {{
            from {{ width: 0; }}
        }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# CARDS COM ANIMAÇÕES
# ============================================================================

def animated_metric_card(
    title: str,
    value: str,
    change: str = "",
    color: str = "primary",
    icon: str = "📊"
):
    """
    Card de métrica com animação ao hover
    
    Args:
        title: Título da métrica
        value: Valor
        change: Mudança (ex: "+5%")
        color: Cor (primary, success, warning, danger)
        icon: Ícone/emoji
    """
    color_map = {
        'primary': '#3B82F6',
        'success': '#10B981',
        'warning': '#F59E0B',
        'danger': '#EF4444',
    }
    
    border_color = color_map.get(color, '#3B82F6')
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-left: 4px solid {border_color};
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
            <div style="font-size: 2.5em;">{icon}</div>
            <span style="color: {border_color}; font-size: 0.85em; font-weight: 600;">{change}</span>
        </div>
        <div style="color: #CBD5E1; font-size: 0.9em; margin-bottom: 8px;">{title}</div>
        <div style="color: {border_color}; font-size: 2.2em; font-weight: 700;">{value}</div>
    </div>
    
    <style>
        div:hover {{
            transform: translateY(-4px) !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4) !important;
            border-left-color: {border_color} !important;
        }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# TIMELINE ANIMADA
# ============================================================================

def animated_timeline(events: list):
    """
    Timeline animada com eventos
    
    Args:
        events: Lista de dicts com keys: {'year', 'title', 'description', 'icon'}
    """
    st.markdown("""
    <style>
        .timeline {
            position: relative;
            padding: 20px 0;
        }
        
        .timeline-item {
            margin: 20px 0;
            padding-left: 40px;
            border-left: 3px solid #475569;
            animation: slideIn 0.5s ease-out;
        }
        
        .timeline-marker {
            position: absolute;
            left: -12px;
            top: 20px;
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%);
            border: 3px solid #0F172A;
            border-radius: 50%;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    for i, event in enumerate(events):
        st.markdown(f"""
        <div class="timeline">
            <div class="timeline-item">
                <div class="timeline-marker" style="animation-delay: {i*0.1}s;"></div>
                <div style="color: #3B82F6; font-weight: 700; font-size: 1.1em; margin-bottom: 4px;">
                    {event.get('icon', '📌')} {event.get('year', '')}
                </div>
                <div style="color: #F1F5F9; font-weight: 600; margin-bottom: 4px;">
                    {event.get('title', '')}
                </div>
                <div style="color: #CBD5E1; font-size: 0.95em;">
                    {event.get('description', '')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
