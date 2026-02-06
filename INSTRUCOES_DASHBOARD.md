# Instruções para Usar o Dashboard

## Resolução do Erro de Caminhos

O erro "No such file or directory: '../data/Processed/dados_modelo_final.csv'" foi corrigido atualizando o `dashboard/config.py` para usar **caminhos absolutos** baseados no diretório do projeto.

**Alteração realizada**: 
- Antes: Caminhos relativos (`../data/...`)
- Depois: Caminhos absolutos usando `Path(__file__).parent.parent`

## Como Executar o Dashboard

### 1. Abra um terminal na raiz do projeto

```bash
cd /home/teodoro/Documents/ZettaLab/ZettaLab-Data
```

### 2. Ative o ambiente virtual

```bash
source venv/bin/activate
```

### 3. Inicie o dashboard

```bash
streamlit run dashboard/app.py
```

### 4. Acesse o dashboard

O Streamlit abrirá automaticamente no navegador. Se não abrir, acesse:
- Local: http://localhost:8501
- IP da rede: http://192.168.x.x:8501

## Estrutura do Dashboard

O dashboard contém 6 páginas acessíveis no menu lateral:

### Página 1: Início
- KPIs principais
- Visão geral dos dados
- Filtros por período e estado

### Página 2: Análise de Estados
- Série histórica por estado (2018-2022)
- Mapa Folium com destaque do estado
- Comparação com média nacional

### Página 3: Predições Futuras
- Previsões para 2023-2025 usando XGBoost
- Cenários "E se..." (simulação de políticas)
- Gráficos interativos

### Página 4: SHAP Analysis
- Interpretabilidade do modelo
- Feature importance global
- Análise de casos específicos
- Dependence plots

### Página 5: Conclusões
- Resumo das descobertas
- Fatores socioeconômicos críticos
- Recomendações por região
- Limitações da análise

### Página 6: Mapa Brasil Interativo
- Mapa coroplético do Brasil
- Slider temporal (2018-2022)
- Visualização de risco por UF
- Ranking de estados

## Verificação de Funcionamento

Se o dashboard ainda apresentar problemas, execute o teste:

```bash
python << 'TESTE'
import sys
sys.path.insert(0, 'dashboard')
from config import DATA_FILE, MODEL_FILE, GEOJSON_PATH
import os

print("Verificando arquivos necessários:")
print(f"Dados: {os.path.exists(DATA_FILE)} - {DATA_FILE}")
print(f"Modelo: {os.path.exists(MODEL_FILE)} - {MODEL_FILE}")
print(f"GeoJSON: {os.path.exists(GEOJSON_PATH)} - {GEOJSON_PATH}")
TESTE
```

## Requisitos

- Python 3.9+
- Dependências instaladas (requirements.txt)
- Dataset em `data/Processed/dados_modelo_final.csv`
- Modelo em `models/xgboost_otimizado.pkl`
- GeoJSON em `data/geojson/brasil_estados.geojson`

## Troubleshooting

### "Erro ao carregar dados"
1. Verifique se está na raiz do projeto
2. Confirme que os arquivos existem
3. Teste o script de verificação acima

### Dashboard lento
1. É normal na primeira carga (cache)
2. Atualizações posteriores são mais rápidas
3. Reduza o período no filtro se necessário

### Mapa não carrega
1. Verifique se o GeoJSON existe
2. Pode demorar alguns segundos
3. Atualize a página (F5)

## Contato

Para problemas, consulte o README.md principal do projeto.
