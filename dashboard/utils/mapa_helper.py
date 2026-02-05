"""
🗺️ Utilitários para criação de mapas Folium
Desafio 2 - Ciência e Governança de Dados
"""

import json
import os
import folium
from folium import plugins
import pandas as pd
import numpy as np
from pathlib import Path


# Constantes
GEOJSON_PATH = Path(__file__).parent.parent.parent / 'data' / 'geojson' / 'brasil_estados.geojson'
MAPA_BRASIL_CENTER = [-10.3910, -51.9253]  # Centro do Brasil


def obter_geojson():
    """Carrega o GeoJSON do Brasil (arquivo local)"""
    if not GEOJSON_PATH.exists():
        raise FileNotFoundError(f"GeoJSON não encontrado em {GEOJSON_PATH}")
    
    with open(GEOJSON_PATH, 'r', encoding='utf-8') as f:
        geojson = json.load(f)
    
    return geojson


def mapear_cor_risco(valor, threshold_baixo=0.01, threshold_alto=0.03):
    """
    Mapeia valor de taxa de abandono para cor de risco
    
    Args:
        valor: Taxa de abandono (em decimal, ex: 0.018 = 1.8%)
        threshold_baixo: Limite entre Baixo e Médio (padrão 1%)
        threshold_alto: Limite entre Médio e Alto (padrão 3%)
    
    Returns:
        tuple: (cor_hex, classe_risco)
    """
    if valor <= threshold_baixo:
        return '#6BCB77', 'Baixo'  # Verde
    elif valor <= threshold_alto:
        return '#FFD93D', 'Médio'  # Amarelo
    else:
        return '#FF6B6B', 'Alto'   # Vermelho


def normalizar_nome_estado(nome):
    """Normaliza nomes de estados para matching com GeoJSON"""
    # Mapa de conversões (nomes no CSV vs nomes no GeoJSON)
    mapa_conversao = {
        'Acre': 'Acre',
        'Alagoas': 'Alagoas',
        'Amapá': 'Amapá',
        'Amazonas': 'Amazonas',
        'Bahia': 'Bahia',
        'Ceará': 'Ceará',
        'Distrito Federal': 'Distrito Federal',
        'Espírito Santo': 'Espírito Santo',
        'Goiás': 'Goiás',
        'Maranhão': 'Maranhão',
        'Mato Grosso': 'Mato Grosso',
        'Mato Grosso do Sul': 'Mato Grosso do Sul',
        'Minas Gerais': 'Minas Gerais',
        'Pará': 'Pará',
        'Paraíba': 'Paraíba',
        'Paraná': 'Paraná',
        'Pernambuco': 'Pernambuco',
        'Piauí': 'Piauí',
        'Rio de Janeiro': 'Rio de Janeiro',
        'Rio Grande do Norte': 'Rio Grande do Norte',
        'Rio Grande do Sul': 'Rio Grande do Sul',
        'Rondônia': 'Rondônia',
        'Roraima': 'Roraima',
        'Santa Catarina': 'Santa Catarina',
        'São Paulo': 'São Paulo',
        'Sergipe': 'Sergipe',
        'Tocantins': 'Tocantins'
    }
    
    return mapa_conversao.get(nome, nome)


def criar_mapa_brasil(df, ano, altura='500px', largura='100%'):
    """
    Cria mapa interativo do Brasil com dados de abandono escolar
    
    Args:
        df: DataFrame com colunas ['Estado', 'Taxa_Abandono_Media', 'Ano']
        ano: Ano a ser visualizado
        altura: Altura do mapa em pixels
        largura: Largura do mapa
    
    Returns:
        folium.Map: Mapa interativo
    """
    
    # Filtrar dados do ano
    df_ano = df[df['Ano'] == ano].copy()
    
    if df_ano.empty:
        raise ValueError(f"Dados não encontrados para o ano {ano}")
    
    # Carregar GeoJSON
    geojson = obter_geojson()
    
    # Criar mapa base
    mapa = folium.Map(
        location=MAPA_BRASIL_CENTER,
        zoom_start=4,
        tiles='OpenStreetMap',
        prefer_canvas=True
    )
    
    # Criar dicionário para lookup rápido
    df_dict = {}
    for _, row in df_ano.iterrows():
        estado_norm = normalizar_nome_estado(row['Estado'])
        df_dict[estado_norm] = {
            'taxa': row['Taxa_Abandono_Media'],
            'estado': row['Estado'],
            'uf': row.get('UF', '')
        }
    
    # Adicionar features do GeoJSON
    for feature in geojson['features']:
        props = feature['properties']
        nome_estado = props.get('name', '')
        
        # Buscar dados do estado
        dados_estado = df_dict.get(nome_estado)
        
        if dados_estado:
            taxa = dados_estado['taxa']
            cor, classe = mapear_cor_risco(taxa)
        else:
            # Estado sem dados no ano
            taxa = None
            cor = '#cccccc'
            classe = 'Sem dados'
        
        # Criar popup
        if taxa is not None:
            popup_text = f"""
            <b>{nome_estado}</b><br>
            Taxa de Abandono: {taxa*100:.2f}%<br>
            Classificação: {classe}<br>
            Ano: {ano}
            """
        else:
            popup_text = f"<b>{nome_estado}</b><br>Sem dados para {ano}"
        
        # Adicionar GeoJSON feature ao mapa
        folium.GeoJson(
            feature,
            style_function=lambda x, cor=cor: {
                'fillColor': cor,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=folium.Tooltip(f"{nome_estado}<br>Taxa: {taxa*100:.2f}%" if taxa else nome_estado)
        ).add_to(mapa)
    
    # Adicionar legenda
    legenda_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 10px; width: 200px; height: 180px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p style="margin-top: 0; font-weight: bold;">Classificação de Risco</p>
    <p><span style="background-color: #6BCB77; padding: 3px 8px; border-radius: 3px;"></span> Baixo (≤ 1.0%)</p>
    <p><span style="background-color: #FFD93D; padding: 3px 8px; border-radius: 3px;"></span> Médio (1.0% - 3.0%)</p>
    <p><span style="background-color: #FF6B6B; padding: 3px 8px; border-radius: 3px;"></span> Alto (> 3.0%)</p>
    <p><span style="background-color: #cccccc; padding: 3px 8px; border-radius: 3px;"></span> Sem dados</p>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    return mapa


def criar_mapa_estado_destaque(df, ano, estado_selecionado, altura='300px', largura='100%'):
    """
    Cria mapa pequeno com destaque de um estado específico
    
    Args:
        df: DataFrame com dados
        ano: Ano a ser visualizado
        estado_selecionado: Nome do estado a destacar
        altura: Altura do mapa
        largura: Largura do mapa
    
    Returns:
        folium.Map: Mapa pequeno com destaque
    """
    
    # Filtrar dados
    df_ano = df[df['Ano'] == ano].copy()
    
    # Criar mapa base (zoom maior para estado)
    mapa = folium.Map(
        location=MAPA_BRASIL_CENTER,
        zoom_start=4,
        tiles='OpenStreetMap',
        prefer_canvas=True
    )
    
    # Criar dicionário para lookup
    df_dict = {}
    for _, row in df_ano.iterrows():
        estado_norm = normalizar_nome_estado(row['Estado'])
        df_dict[estado_norm] = {
            'taxa': row['Taxa_Abandono_Media'],
            'estado': row['Estado']
        }
    
    # Carregar GeoJSON
    geojson = obter_geojson()
    
    # Adicionar estados e destacar selecionado
    for feature in geojson['features']:
        props = feature['properties']
        nome_estado = props.get('name', '')
        
        dados_estado = df_dict.get(nome_estado)
        
        if dados_estado:
            taxa = dados_estado['taxa']
            cor, classe = mapear_cor_risco(taxa)
        else:
            taxa = None
            cor = '#cccccc'
            classe = 'Sem dados'
        
        # Destacar estado selecionado com borda mais grossa
        if nome_estado == estado_selecionado:
            peso = 3
            opacidade = 0.8
        else:
            peso = 1
            opacidade = 0.6
        
        popup_text = f"<b>{nome_estado}</b>"
        if taxa is not None:
            popup_text += f"<br>Taxa: {taxa*100:.2f}%"
        
        folium.GeoJson(
            feature,
            style_function=lambda x, cor=cor, peso=peso, opacidade=opacidade: {
                'fillColor': cor,
                'color': 'black',
                'weight': peso,
                'fillOpacity': opacidade
            },
            popup=folium.Popup(popup_text, max_width=200)
        ).add_to(mapa)
    
    return mapa
