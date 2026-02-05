# ⚙️ Configurações do Dashboard

import os

# Diretórios
DATA_DIR = '../data/Processed'
MODELS_DIR = '../models'
REPORTS_DIR = '../reports'

# Arquivo de dados
DATA_FILE = os.path.join(DATA_DIR, 'dados_modelo_final.csv')
MODEL_FILE = os.path.join(MODELS_DIR, 'xgboost_otimizado.pkl')

# Constantes
RANDOM_STATE = 42
ANOS_DISPONIVEIS = [2018, 2019, 2020, 2021, 2022]
ANOS_PREDICAO = [2023, 2024, 2025]

# Thresholds de Risco
THRESHOLD_BAIXO = 0.01     # 1.0% - Meta PNE
THRESHOLD_ALTO = 0.03      # 3.0% - 3x meta (crise)

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
            'Indice_Gini', 'Taxa_Gravidez_Adolescente', 'PIB_Total_MilReais']

# Nomes legíveis das features
FEATURE_NAMES = {
    'Ano': 'Ano',
    'IDHM': 'Índice de Desenvolvimento Humano',
    'Taxa_Desemprego': 'Taxa de Desemprego (%)',
    'Renda_Per_Capita': 'Renda Per Capita (R$)',
    'Indice_Gini': 'Índice de Gini',
    'Taxa_Gravidez_Adolescente': 'Taxa de Gravidez Adolescente (%)',
    'PIB_Total_MilReais': 'PIB (Milhões R$)',
    'Taxa_Abandono_Media': 'Taxa de Abandono Escolar (%)',
    'Taxa_Reprovacao_Media': 'Taxa de Reprovação (%)'
}
