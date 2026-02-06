# Quick Start - Dashboard

## Iniciar o Dashboard em 3 passos

### 1. Navegue até o projeto
```bash
cd /home/teodoro/Documents/ZettaLab/ZettaLab-Data
```

### 2. Ative o ambiente virtual
```bash
source venv/bin/activate
```

### 3. Inicie o Streamlit
```bash
streamlit run dashboard/app.py
```

O navegador abrirá automaticamente em: **http://localhost:8501**

---

## O que é o Dashboard?

Um dashboard interativo com 6 páginas que analisa impactos socioeconômicos na evasão escolar brasileira.

### Páginas Disponíveis

| Página | Descrição |
|--------|-----------|
| **1. Início** | KPIs e visão geral dos dados |
| **2. Análise de Estados** | Série histórica por estado com mapa Folium |
| **3. Predições** | Previsões 2023-2025 e cenários "E se..." |
| **4. SHAP Analysis** | Interpretabilidade do modelo de ML |
| **5. Conclusões** | Descobertas principais e recomendações |
| **6. Mapa Brasil** | Mapa interativo com slider temporal |

---

## Principais Descobertas

- **Gravidez Adolescente**: 63.5% de importância no abandono escolar
- **Renda Per Capita**: 15.2% de importância
- **Desemprego**: 12.1% de impacto
- **7 Estados Críticos**: PA, BA, RR, AC, PB, RN, MA com >3% evasão

---

## Dados

- **Período**: 2018-2022
- **Granularidade**: 27 UFs (estados)
- **Total**: 135 registros
- **Features**: 6 variáveis socioeconômicas
- **Targets**: Taxa de abandono e reprovação

---

## Requisitos

- Python 3.9+
- Dependências em `requirements.txt`
- Dados em `data/Processed/dados_modelo_final.csv`
- Modelo em `models/xgboost_otimizado.pkl`

---

## Troubleshooting

**Dashboard lento na primeira carga?**
- Normal, é apenas o Streamlit fazendo cache de dados
- Recarregamentos posteriores são mais rápidos

**Mapa não aparece?**
- Aguarde alguns segundos
- Atualize a página (F5)
- Verifique se o GeoJSON existe em `data/geojson/brasil_estados.geojson`

**Erro ao carregar?**
- Verifique se está na raiz do projeto
- Confirme que o venv está ativado
- Consulte `INSTRUCOES_DASHBOARD.md` para mais detalhes

---

## Documentação Completa

Veja `README.md` para documentação detalhada do projeto, incluindo:
- Metodologia CRISP-DM
- Explicação dos dados e features
- Resultados da modelagem
- Limitações e recomendações futuras

---

**Criado**: 05 de Fevereiro de 2026  
**Última atualização**: 05 de Fevereiro de 2026
