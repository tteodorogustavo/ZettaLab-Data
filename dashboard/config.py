# Configurações do Dashboard

import os
from pathlib import Path

# Diretório raiz do projeto (um nível acima de dashboard)
PROJECT_ROOT = Path(__file__).parent.parent

# Diretórios
DATA_DIR = PROJECT_ROOT / 'data' / 'Processed'
MODELS_DIR = PROJECT_ROOT / 'models'
REPORTS_DIR = PROJECT_ROOT / 'reports'

# Arquivo de dados
DATA_FILE = str(DATA_DIR / 'dados_modelo_final.csv')
MODEL_FILE = str(MODELS_DIR / 'xgboost_otimizado.pkl')

# Constantes
RANDOM_STATE = 42
ANOS_DISPONIVEIS = [2018, 2019, 2020, 2021, 2022]
ANOS_PREDICAO = [2023, 2024, 2025]

# Thresholds de Risco
THRESHOLD_BAIXO = 1.0       # 1.0% - Meta PNE
THRESHOLD_ALTO = 3.0        # 3.0% - 3x meta (crise)

# Cores por classe de risco
CORES_RISCO = {
    'Baixo': '#6BCB77',      # Verde
    'Médio': '#FFD93D',      # Amarelo
    'Alto': '#FF6B6B'        # Vermelho
}

# Títulos e descrições
TITULO_PRINCIPAL = "📊 Dashboard - Análise de Evasão Escolar"
SUBTITULO = "Impactos Socioeconômicos no Desempenho Escolar Brasileiro (2018-2022)"
DESCRICAO = """
**Desafio 2 - Ciência e Governança de Dados (Zetta Lab)**

Este dashboard apresenta uma análise rigorosa de como fatores socioeconômicos 
impactam a evasão escolar no Brasil, utilizando metodologia CRISP-DM e técnicas 
de Machine Learning (XGBoost) para previsão e interpretação.
"""

# Features para o modelo
FEATURES = ['Ano', 'IDHM', 'Taxa_Desemprego', 'Renda_Per_Capita', 
            'Indice_Gini_x', 'Taxa_Gravidez_Adolescente_x', 'PIB_Total_MilReais_x']

# Nomes legíveis das features
FEATURE_NAMES = {
    'Ano': 'Ano',
    'IDHM': 'Índice de Desenvolvimento Humano',
    'Taxa_Desemprego': 'Taxa de Desemprego (%)',
    'Renda_Per_Capita': 'Renda Per Capita (R$)',
    'Indice_Gini_x': 'Índice de Gini',
    'Taxa_Gravidez_Adolescente_x': 'Taxa de Gravidez Adolescente (%)',
    'PIB_Total_MilReais_x': 'PIB (Milhões R$)',
    'Taxa_Abandono_Media': 'Taxa de Abandono Escolar (%)',
    'Taxa_Reprovacao_Media': 'Taxa de Reprovação (%)'
}

# Configurações de Mapa
GEOJSON_PATH = str(PROJECT_ROOT / 'data' / 'geojson' / 'brasil_estados.geojson')
MAPA_BRASIL_CENTER = [-10.3910, -51.9253]  # Centro do Brasil
MAPA_ZOOM_INICIAL = 4
MAPA_ALTURA_GRANDE = '600px'
MAPA_ALTURA_PEQUENO = '300px'
