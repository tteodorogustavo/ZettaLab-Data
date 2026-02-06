"""
📊 Módulo de Gráficos Avançados - 3D e Heatmaps
Oferece visualizações 3D com Plotly e heatmaps com Folium
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium

# ============================================================================
# GRÁFICOS 3D COM PLOTLY
# ============================================================================

def scatter_3d(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    z_col: str,
    color_col: str = None,
    size_col: str = None,
    hover_data: list = None,
    title: str = "Gráfico 3D",
    height: int = 600
):
    """
    Cria gráfico 3D scatter com Plotly
    
    Args:
        df: DataFrame
        x_col: Coluna para eixo X
        y_col: Coluna para eixo Y
        z_col: Coluna para eixo Z
        color_col: Coluna para colorir pontos
        size_col: Coluna para tamanho dos pontos
        hover_data: Colunas para mostrar no hover
        title: Título do gráfico
        height: Altura do gráfico
    """
    
    fig = go.Figure(data=[go.Scatter3d(
        x=df[x_col],
        y=df[y_col],
        z=df[z_col],
        mode='markers',
        marker=dict(
            size=df[size_col] / df[size_col].max() * 8 if size_col else 6,
            color=df[color_col] if color_col else 'lightblue',
            colorscale='Viridis' if color_col else None,
            showscale=True if color_col else False,
            colorbar=dict(title=color_col) if color_col else None,
            opacity=0.8,
            line=dict(
                color='white',
                width=0.5
            )
        ),
        text=hover_data or df.columns.tolist(),
        hovertemplate='<b>%{text}</b><br>X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>'
    )])
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=x_col,
            yaxis_title=y_col,
            zaxis_title=z_col,
            bgcolor='#0F172A',
            xaxis=dict(
                backgroundcolor='#1E293B',
                gridcolor='#334155',
                showbackground=True,
                zerolinecolor='#475569'
            ),
            yaxis=dict(
                backgroundcolor='#1E293B',
                gridcolor='#334155',
                showbackground=True,
                zerolinecolor='#475569'
            ),
            zaxis=dict(
                backgroundcolor='#1E293B',
                gridcolor='#334155',
                showbackground=True,
                zerolinecolor='#475569'
            )
        ),
        paper_bgcolor='#0F172A',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9'),
        height=height,
        hovermode='closest'
    )
    
    return fig


def surface_3d(
    x_data: np.ndarray,
    y_data: np.ndarray,
    z_data: np.ndarray,
    title: str = "Superfície 3D",
    height: int = 600
):
    """
    Cria gráfico 3D de superfície
    
    Args:
        x_data: Array X
        y_data: Array Y
        z_data: Array Z (2D para superfície)
        title: Título
        height: Altura
    """
    
    fig = go.Figure(data=[go.Surface(
        x=x_data,
        y=y_data,
        z=z_data,
        colorscale='Viridis',
        showscale=True
    )])
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            bgcolor='#0F172A'
        ),
        paper_bgcolor='#0F172A',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9'),
        height=height
    )
    
    return fig


def bubble_3d(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    z_col: str,
    size_col: str,
    color_col: str = None,
    title: str = "Bubble 3D",
    height: int = 600
):
    """
    Cria gráfico 3D bubble (bolhas)
    
    Args:
        df: DataFrame
        x_col: Coluna X
        y_col: Coluna Y
        z_col: Coluna Z
        size_col: Coluna para tamanho das bolhas
        color_col: Coluna para cor
        title: Título
        height: Altura
    """
    
    size_normalized = df[size_col] / df[size_col].max() * 30
    
    fig = go.Figure(data=[go.Scatter3d(
        x=df[x_col],
        y=df[y_col],
        z=df[z_col],
        mode='markers',
        marker=dict(
            size=size_normalized,
            color=df[color_col] if color_col else 'lightblue',
            colorscale='Plasma' if color_col else None,
            showscale=True if color_col else False,
            opacity=0.7,
            line=dict(color='white', width=1),
            colorbar=dict(title=color_col) if color_col else None
        ),
        text=df.index,
        hovertemplate='<b>%{text}</b><br>' +
                     f'{x_col}: %{{x}}<br>' +
                     f'{y_col}: %{{y}}<br>' +
                     f'{z_col}: %{{z}}<extra></extra>'
    )])
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=x_col,
            yaxis_title=y_col,
            zaxis_title=z_col,
            bgcolor='#0F172A'
        ),
        paper_bgcolor='#0F172A',
        plot_bgcolor='#0F172A',
        font=dict(color='#F1F5F9'),
        height=height
    )
    
    return fig


# ============================================================================
# HEATMAPS COM FOLIUM
# ============================================================================

def create_heatmap(
    lat_list: list,
    lon_list: list,
    intensity_list: list,
    center_lat: float = None,
    center_lon: float = None,
    zoom_start: int = 6,
    title: str = "Heatmap",
    radius: int = 20,
    blur: int = 15
):
    """
    Cria mapa de calor com Folium
    
    Args:
        lat_list: Lista de latitudes
        lon_list: Lista de longitudes
        intensity_list: Lista de valores de intensidade
        center_lat: Latitude do centro do mapa
        center_lon: Longitude do centro do mapa
        zoom_start: Nível de zoom inicial
        title: Título
        radius: Raio do calor
        blur: Desfoque
        
    Returns:
        folium.Map: Mapa com heatmap
    """
    
    # Calcular centro se não fornecido
    if center_lat is None:
        center_lat = np.mean(lat_list)
    if center_lon is None:
        center_lon = np.mean(lon_list)
    
    # Criar mapa base
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap'
    )
    
    # Preparar dados para heatmap
    heat_data = [[lat, lon, intensity] 
                 for lat, lon, intensity in zip(lat_list, lon_list, intensity_list)]
    
    # Adicionar heatmap
    from folium.plugins import HeatMap
    HeatMap(heat_data, radius=radius, blur=blur, max_zoom=13).add_to(m)
    
    # Adicionar título
    title_html = f'''
             <div style="position: fixed; 
                     top: 10px; left: 50px; width: 300px; height: 60px; 
                     background-color: white; border:2px solid grey; z-index:9999; 
                     font-size:16px; font-weight: bold; padding: 10px">
             {title}
             </div>
             '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    return m


def create_choropleth_map(
    geojson: dict,
    data: pd.DataFrame,
    location_key: str,
    value_col: str,
    center_lat: float,
    center_lon: float,
    zoom_start: int = 6,
    colorscale: str = 'YlOrRd',
    title: str = "Mapa Coropleth"
):
    """
    Cria mapa coropleth (por região)
    
    Args:
        geojson: GeoJSON dict
        data: DataFrame com valores
        location_key: Chave para match no GeoJSON
        value_col: Coluna com valores
        center_lat: Latitude do centro
        center_lon: Longitude do centro
        zoom_start: Zoom
        colorscale: Escala de cores
        title: Título
        
    Returns:
        folium.Map: Mapa coropleth
    """
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap'
    )
    
    # Criar dicionário de valores
    values_dict = dict(zip(data[location_key], data[value_col]))
    
    # Adicionar choropleth
    folium.Choropleth(
        geo_data=geojson,
        name='choropleth',
        data=data,
        columns=[location_key, value_col],
        fill_color=colorscale,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=value_col
    ).add_to(m)
    
    return m


def create_marker_cluster_map(
    locations: list,
    values: list,
    location_names: list = None,
    center_lat: float = None,
    center_lon: float = None,
    zoom_start: int = 6,
    title: str = "Mapa de Clusters"
):
    """
    Cria mapa com clusters de marcadores
    
    Args:
        locations: Lista de [lat, lon]
        values: Lista de valores
        location_names: Nomes dos locais
        center_lat: Latitude do centro
        center_lon: Longitude do centro
        zoom_start: Zoom
        title: Título
        
    Returns:
        folium.Map: Mapa com clusters
    """
    
    if center_lat is None:
        center_lat = np.mean([loc[0] for loc in locations])
    if center_lon is None:
        center_lon = np.mean([loc[1] for loc in locations])
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap'
    )
    
    # Adicionar MarkerCluster
    from folium.plugins import MarkerCluster
    
    mc = MarkerCluster()
    
    for i, (loc, value) in enumerate(zip(locations, values)):
        name = location_names[i] if location_names else f"Local {i+1}"
        
        folium.Marker(
            location=loc,
            popup=f"{name}: {value:.2f}",
            tooltip=f"{name}: {value:.2f}"
        ).add_to(mc)
    
    mc.add_to(m)
    
    return m


# ============================================================================
# HELPERS PARA VISUALIZAÇÃO
# ============================================================================

def display_3d_chart(fig, use_container_width: bool = True):
    """Exibe gráfico 3D no Streamlit"""
    st.plotly_chart(fig, use_container_width=use_container_width)


def display_heatmap(m):
    """Exibe heatmap folium no Streamlit"""
    st_folium(m, width=700, height=500)
