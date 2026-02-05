# 📊 Dashboard Interativo - Análise de Evasão Escolar

## 🎯 Objetivo

Dashboard interativo que apresenta análise rigorosa de como fatores socioeconômicos impactam a evasão escolar no Brasil, utilizando Machine Learning (XGBoost) e metodologia CRISP-DM.

## 📁 Estrutura

```
dashboard/
├── app.py                    # Página principal
├── config.py                 # Configurações e constantes
├── pages/
│   ├── 1_inicio.py          # KPIs e visão geral
│   ├── 2_analise_estados.py # Análise por estado + mapa pequeno
│   ├── 3_predicoes.py       # Predições futuras
│   ├── 4_shap_analysis.py   # Interpretabilidade
│   ├── 5_conclusoes.py      # Storytelling de dados
│   └── 6_mapa_brasil.py     # Mapa interativo do Brasil
├── utils/
│   └── mapa_helper.py       # Funções auxiliares para mapas Folium
└── README.md                 # Este arquivo
```

## 🚀 Como Executar

### 1. Instalar dependências (na raiz do projeto)

```bash
# Na raiz do projeto
pip install -r requirements.txt
```

### 2. Rodar o dashboard

```bash
# A partir da raiz do projeto
streamlit run dashboard/app.py
```

O dashboard será aberto em `http://localhost:8501`

## 📖 Páginas do Dashboard

### 1️⃣ **Início** (Página Principal)
- KPIs gerais (taxa média, estados críticos, etc)
- Distribuição de risco (2022)
- Top 5 estados com maior risco
- Tendência temporal (2018-2022)
- Informações sobre metodologia e modelo

### 2️⃣ **Análise de Estados**
- Selecionar estado específico
- **Mapa pequeno** com localização espacial do estado
- Série temporal de abandono
- Indicadores socioeconômicos
- Comparação com média Brasil

### 3️⃣ **Predições**
- Prever taxas de abandono para 2023-2025
- Análise de cenários "E se..."
  - E se IDHM melhorasse em 5%?
  - E se desemprego caísse em 10%?
- Visualizar impacto de mudanças

### 4️⃣ **SHAP Analysis**
- Importância global das variáveis
- Análise individual por estado
- Gráficos de dependência parcial
- Entender como modelo faz predições

### 5️⃣ **Conclusões**
- Storytelling de dados
- Descobertas principais
- Validação temporal
- Capacidade preditiva
- Limitações e próximas investigações

### 6️⃣ **Mapa do Brasil** ⭐ NOVO
- **Visualização interativa do Brasil** com todos os 27 estados
- **Slider temporal**: Explore dados de 2018-2022
- **Cores por risco**: Verde (Baixo) → Amarelo (Médio) → Vermelho (Alto)
- **Interatividade**: 
  - Passe o mouse para ver taxa de abandono
  - Clique para detalhes completos
  - Zoom e pan para exploração
- **Estatísticas**: Taxa média, mínima e máxima por ano
- **Tabela detalhada**: Todos os estados ordenados por risco
- **Análise temporal**: Evolução 2018-2022 com tendências

## 🔧 Configurações

Edite `config.py` para customizar:

```python
# Thresholds de risco
THRESHOLD_BAIXO = 0.01     # 1.0% - Meta PNE
THRESHOLD_ALTO = 0.03      # 3.0% - Crise (3x meta)

# Cores por classe
CORES_RISCO = {
    'Baixo': '#6BCB77',
    'Médio': '#FFD93D',
    'Alto': '#FF6B6B'
}
```

## 📊 Dados Utilizados

- **Fonte**: `../data/Processed/dados_modelo_final.csv`
- **Período**: 2018-2022
- **Unidades**: 27 UFs
- **Registros**: 135 (27 UFs × 5 anos)
- **Variáveis**: 8 (2 target + 6 features)

## 🤖 Modelo

- **Tipo**: XGBoost Regressor
- **Arquivo**: `../models/xgboost_otimizado.pkl`
- **Performance**: R² = 0.510
- **Validação**: 5-fold cross-validation

## 🎨 Tecnologias

- **Frontend**: Streamlit
- **Visualizações**: Plotly
- **Mapas**: Folium + Streamlit-Folium
- **Dados Geográficos**: GeoPandas, GeoJSON
- **ML**: XGBoost
- **Dados**: Pandas, NumPy
- **Interpretabilidade**: SHAP

## 🗺️ Dados Geográficos

- **GeoJSON**: `../data/geojson/brasil_estados.geojson`
- **Formato**: 27 estados do Brasil em formato GeoJSON
- **Source**: Baixado de repositório público e salvo localmente
- **Funcionalidades**: 
  - Colorização por tema (risco)
  - Tooltips interativas
  - Popups com detalhes
  - Zoom e pan interativo

## 📝 Notas Importantes

1. **Dados Históricos**: Dashboard usa dados 2018-2022
2. **Predições**: Baseadas em modelo treinado (R² = 0.51)
3. **Incerteza**: 49% da variância não é explicada pelo modelo
4. **Granularidade**: Dados de nível estadual (não municipal)

## 🔗 Links Úteis

- Notebook 04: Modelagem de Regressão
- Notebook 05: Avaliação SHAP
- Notebook 08: Otimização de Hiperparâmetros
- README Desafio 2: Documentação Completa

## 👨‍💻 Desenvolvedor

Gustavo Teodoro  
Desafio 2 - Ciência e Governança de Dados (Zetta Lab)  
Fevereiro/2026

---

**Status**: ✅ Completo e Funcional
