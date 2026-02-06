"""
📑 Módulo de Tabs Customizadas para o Dashboard
Oferece tabs com estilos do tema Dark Mode
"""

import streamlit as st
from theme import COLORS

# ============================================================================
# TABS CUSTOMIZADAS COM THEME
# ============================================================================

def custom_tabs(tabs_dict: dict, default_tab: int = 0):
    """
    Cria tabs customizadas com tema Dark Mode
    
    Args:
        tabs_dict: Dict com {'tab_name': tab_content}
        default_tab: Índice da aba padrão
        
    Returns:
        str: Nome da aba selecionada
    """
    
    # CSS para tabs customizadas
    st.markdown("""
    <style>
        .custom-tabs-container {
            display: flex;
            border-bottom: 2px solid #475569;
            margin-bottom: 20px;
            gap: 0;
            overflow-x: auto;
        }
        
        .custom-tab {
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: transparent;
            color: #CBD5E1;
            font-weight: 600;
            font-size: 0.95em;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
        }
        
        .custom-tab:hover {
            color: #3B82F6;
            background-color: rgba(59, 130, 246, 0.1);
        }
        
        .custom-tab.active {
            color: #3B82F6;
            border-bottom-color: #3B82F6;
            background: linear-gradient(180deg, rgba(59, 130, 246, 0.1) 0%, transparent 100%);
        }
        
        .tab-content {
            animation: fadeIn 0.3s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Se não existe session state para tabs, cria
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = default_tab
    
    # Criar buttons para tabs
    tab_names = list(tabs_dict.keys())
    cols = st.columns(len(tab_names))
    
    for i, (col, tab_name) in enumerate(zip(cols, tab_names)):
        with col:
            if st.button(
                tab_name,
                key=f"tab_{i}",
                use_container_width=True,
                type="primary" if st.session_state.active_tab == i else "secondary"
            ):
                st.session_state.active_tab = i
    
    st.markdown("---")
    
    # Exibir conteúdo da aba ativa
    active_tab_name = tab_names[st.session_state.active_tab]
    tab_content = tabs_dict[active_tab_name]
    
    st.markdown(f'<div class="tab-content">', unsafe_allow_html=True)
    
    # Se o conteúdo é uma função, executar
    if callable(tab_content):
        tab_content()
    else:
        st.write(tab_content)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return active_tab_name


def simple_tabs(tabs_list: list):
    """
    Cria tabs simples e elegantes (usa st.tabs nativo com styling)
    
    Args:
        tabs_list: Lista de tuples (tab_name, tab_content_function)
        
    Returns:
        None
    """
    
    tab_names = [name for name, _ in tabs_list]
    tabs = st.tabs(tab_names)
    
    for tab, (_, content_func) in zip(tabs, tabs_list):
        with tab:
            if callable(content_func):
                content_func()
            else:
                st.write(content_func)


def metric_tabs(metrics_dict: dict):
    """
    Tabs especializadas para exibir métricas
    
    Args:
        metrics_dict: Dict com {'tab_name': {'label': valor, 'icon': emoji, 'color': cor}}
    """
    
    tab_names = list(metrics_dict.keys())
    tabs = st.tabs(tab_names)
    
    for tab, tab_name in zip(tabs, tab_names):
        with tab:
            metrics = metrics_dict[tab_name]
            
            # Exibir métricas em colunas
            cols = st.columns(len(metrics))
            
            for col, (metric_name, metric_info) in zip(cols, metrics.items()):
                with col:
                    icon = metric_info.get('icon', '📊')
                    value = metric_info.get('valor', 'N/A')
                    color = metric_info.get('color', 'primary')
                    
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
                        border-radius: 8px;
                        padding: 16px;
                        text-align: center;
                    ">
                        <div style="font-size: 2em; margin-bottom: 8px;">{icon}</div>
                        <div style="color: {COLORS['text_muted']}; font-size: 0.85em; margin-bottom: 4px;">{metric_name}</div>
                        <div style="color: {border_color}; font-size: 1.8em; font-weight: bold;">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)


# ============================================================================
# ACCORDION CUSTOMIZADO
# ============================================================================

def custom_accordion(items: list):
    """
    Accordion customizado com tema
    
    Args:
        items: Lista de dicts {'title': str, 'content': str ou callable}
    """
    
    for i, item in enumerate(items):
        title = item.get('title', 'Item')
        content = item.get('content', '')
        icon = item.get('icon', '📌')
        
        with st.expander(f"{icon} {title}", expanded=i == 0):
            if callable(content):
                content()
            else:
                st.markdown(content)
