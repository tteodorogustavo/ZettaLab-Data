"""
🎯 Módulo de Menu de Navegação Customizado
Oferece menu elegante com streamlit-option-menu
"""

import streamlit as st
from streamlit_option_menu import option_menu
from theme import COLORS

# ============================================================================
# MENU HORIZONTAL NO TOPO
# ============================================================================

def create_top_menu(
    options: list,
    icons: list = None,
    menu_icon: str = "menu-button-wide",
    default_index: int = 0,
    orientation: str = "horizontal"
):
    """
    Cria menu horizontal customizado no topo
    
    Args:
        options: Lista de nomes das opções
        icons: Lista de ícones (mesmo tamanho de options)
        menu_icon: Ícone do menu
        default_index: Índice padrão
        orientation: 'horizontal' ou 'vertical'
        
    Returns:
        str: Opção selecionada
    """
    
    if icons is None:
        icons = ["house"] * len(options)
    
    selected = option_menu(
        menu_title=None,
        options=options,
        icons=icons,
        menu_icon=menu_icon,
        default_index=default_index,
        orientation=orientation,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#0F172A",
                "border-bottom": f"2px solid {COLORS['border']}"
            },
            "icon": {
                "color": COLORS['primary_light'],
                "font-size": "24px"
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "center",
                "margin": "0px",
                "padding": "10px 20px",
                "color": COLORS['text'],
                "--hover-color": COLORS['surface_light']
            },
            "nav-link-selected": {
                "background-color": COLORS['primary'],
                "color": "white",
                "font-weight": "bold"
            }
        }
    )
    
    return selected


# ============================================================================
# MENU VERTICAL NA SIDEBAR
# ============================================================================

def create_sidebar_menu(
    options: list,
    icons: list = None,
    menu_icon: str = "list",
    default_index: int = 0
):
    """
    Cria menu vertical na sidebar
    
    Args:
        options: Lista de opções
        icons: Lista de ícones
        menu_icon: Ícone do menu principal
        default_index: Índice padrão
        
    Returns:
        str: Opção selecionada
    """
    
    if icons is None:
        icons = ["circle-fill"] * len(options)
    
    with st.sidebar:
        st.markdown(f"""
        <div style="
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid {COLORS['border']};
            margin-bottom: 10px;
        ">
            <h2 style="color: {COLORS['primary_light']}; margin: 0;">
                📊 Dashboard
            </h2>
            <p style="color: {COLORS['text_muted']}; margin: 5px 0 0 0;">
                Evasão Escolar
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            menu_icon=menu_icon,
            default_index=default_index,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent"
                },
                "icon": {
                    "color": COLORS['primary_light'],
                    "font-size": "20px"
                },
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "5px 0",
                    "padding": "12px 20px",
                    "border-radius": "8px",
                    "color": COLORS['text'],
                    "--hover-color": COLORS['surface_light']
                },
                "nav-link-selected": {
                    "background-color": COLORS['primary'],
                    "color": "white",
                    "font-weight": "bold",
                    "border-radius": "8px"
                }
            }
        )
    
    return selected


# ============================================================================
# MENU DROPDOWN
# ============================================================================

def create_dropdown_menu(
    label: str,
    options: list,
    icons: list = None,
    key: str = None,
    default: int = 0
):
    """
    Cria menu dropdown (selectbox) customizado
    
    Args:
        label: Rótulo do menu
        options: Lista de opções
        icons: Ícones (opcional)
        key: Chave única para session state
        default: Índice padrão
        
    Returns:
        str: Opção selecionada
    """
    
    if icons is None:
        icons = ["•"] * len(options)
    
    # Criar labels com ícones
    labels_with_icons = [f"{icon} {opt}" for icon, opt in zip(icons, options)]
    
    selected_index = st.selectbox(
        label,
        range(len(options)),
        format_func=lambda x: labels_with_icons[x],
        key=key
    )
    
    return options[selected_index]


# ============================================================================
# BREADCRUMB NAVIGATION
# ============================================================================

def create_breadcrumb(items: list):
    """
    Cria breadcrumb de navegação
    
    Args:
        items: Lista de dicts {'label': str, 'icon': str}
    """
    
    breadcrumb_html = '<div style="display: flex; align-items: center; gap: 10px; margin: 15px 0; color: #CBD5E1;">'
    
    for i, item in enumerate(items):
        label = item.get('label', '')
        icon = item.get('icon', '📌')
        is_active = item.get('active', i == len(items) - 1)
        
        color = COLORS['primary_light'] if is_active else COLORS['text_muted']
        
        breadcrumb_html += f"""
        <span style="
            display: flex;
            align-items: center;
            gap: 5px;
            color: {color};
            font-weight: {'bold' if is_active else 'normal'};
        ">
            {icon} {label}
        </span>
        """
        
        if i < len(items) - 1:
            breadcrumb_html += f'<span style="color: {COLORS["border"]}; font-size: 1.2em;">›</span>'
    
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


# ============================================================================
# NAVIGATION BUTTONS
# ============================================================================

def create_nav_buttons(prev_label: str = None, next_label: str = None):
    """
    Cria botões de navegação anterior/próximo
    
    Args:
        prev_label: Texto do botão anterior
        next_label: Texto do botão próximo
        
    Returns:
        tuple: (prev_clicked, next_clicked)
    """
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    prev_clicked = False
    next_clicked = False
    
    with col1:
        if prev_label and st.button(f"← {prev_label}", use_container_width=True):
            prev_clicked = True
    
    with col3:
        if next_label and st.button(f"{next_label} →", use_container_width=True):
            next_clicked = True
    
    return prev_clicked, next_clicked


# ============================================================================
# MENU COM SEARCH
# ============================================================================

def create_searchable_menu(
    options: list,
    icons: list = None,
    placeholder: str = "🔍 Buscar...",
    key: str = None
):
    """
    Cria menu com barra de busca
    
    Args:
        options: Lista de opções
        icons: Lista de ícones
        placeholder: Placeholder da busca
        key: Chave única
        
    Returns:
        str: Opção selecionada
    """
    
    if icons is None:
        icons = ["•"] * len(options)
    
    # Barra de busca
    search_term = st.text_input(placeholder, key=key)
    
    # Filtrar opções
    if search_term:
        filtered_options = [
            opt for opt in options 
            if search_term.lower() in opt.lower()
        ]
    else:
        filtered_options = options
    
    if filtered_options:
        selected_index = st.selectbox(
            "Selecione uma opção:",
            range(len(filtered_options)),
            format_func=lambda x: filtered_options[x],
            key=f"{key}_select" if key else None
        )
        return filtered_options[selected_index]
    else:
        st.warning(f"Nenhuma opção encontrada para '{search_term}'")
        return None
