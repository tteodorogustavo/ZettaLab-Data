# Copilot Instructions - ZettaLab Data Analysis

## Visão Geral do Projeto

Projeto de **Ciência de Dados Educacionais** que analisa correlações entre fatores socioeconômicos (deslocamento, saneamento) e desempenho escolar (evasão, repetência) de jovens de 10-17 anos por UF no Brasil. Dados de 2022 do IBGE, INEP e SNIS.

## Arquitetura de Dados

### Pipeline de Processamento
```
data/Raw/ → notebooks/clean-data.ipynb → data/Processed/ → notebooks/vizualizations.ipynb → data/vizualizations/
```

### Arquivos-Chave
| Arquivo | Propósito |
|---------|-----------|
| `data/Processed/dados_finais_analise.csv` | **DataFrame final** - fonte única para visualizações |
| `notebooks/clean-data.ipynb` | Limpeza: ffill, melt, tratamento de cabeçalhos multi-nível |
| `notebooks/extract-info.ipynb` | Profiling com YData |
| `notebooks/vizualizations.ipynb` | Merge final + geração de 9 gráficos |

## Convenções e Padrões

### Colunas Padronizadas (DataFrame Final)
- `UF` - Nome completo da Unidade Federativa (chave de merge)
- `Tempo_Deslocamento_Medio_Minutos` - Média ponderada pelo nº de pessoas
- `Indice_Saneamento_Basico` - Média entre coleta e tratamento de esgoto
- `Taxa_Evasao_Media`, `Taxa_Repetencia_Media` - Média entre EF e EM

### Transformações Críticas
```python
# Mapeamento de tempo de deslocamento para valores numéricos
tempo_map = {
    'Até cinco minutos': 2.5, 'Mais de cinco minutos até quinze minutos': 10,
    'Mais de quinze minutos até meia hora': 22.5, 'Mais de meia hora até uma hora': 45,
    'Mais de uma hora até duas horas': 90, 'Mais de quatro horas': 240
}

# Merge sempre por UF (nome completo, não sigla)
df_final = pd.merge(df1, df2, on='UF', how='inner')
```

### Estilo de Visualizações
- Biblioteca: **Seaborn** com estilo `whitegrid` e paleta `viridis`
- Figuras: `(12, 6)` padrão, `(14, 7)` para gráficos combinados
- Salvar em: `data/vizualizations/` com formato `Insight_{N}_{Descricao}.png`
- Sempre incluir anotação de UF em scatter plots

## Workflow de Desenvolvimento

### Executar Notebooks
```bash
# Instalar dependências
pip install -r requirements.txt

# Ordem de execução
1. clean-data.ipynb    # Gera arquivos em data/Processed/
2. extract-info.ipynb  # Opcional: profiling exploratório
3. vizualizations.ipynb # Gera gráficos e dados_finais_analise.csv
```

### Bibliotecas Utilizadas
- `pandas`, `numpy` - Manipulação de dados
- `ydata-profiling` - Análise exploratória (import como `ydata_profiling`)
- `seaborn`, `matplotlib` - Visualizações
- `pyarrow`, `openpyxl` - Leitura de formatos diversos

## Padrões de Código

### Leitura de Dados com Problemas de Formatação
```python
# Para CSVs do IBGE com cabeçalhos problemáticos
df = pd.read_csv(path, encoding='utf-8', skiprows=6, header=None, na_values=['-', '...'])
# Aplicar ffill() ANTES de dropna() para colunas mescladas
df[cols_agrupamento] = df[cols_agrupamento].ffill()
```

### Conversão UF Sigla → Nome
```python
uf_map = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 
    'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', # ... etc
}
```

## Notas Importantes

- **Granularidade**: Todos os dados são agregados por UF (27 estados)
- **Ano base**: 2022 para consistência temporal
- **Filtros padrão**: `localizacao == 'Total'` e `rede == 'Total'` para índices de ensino
- **Arredondamento**: `.round(2)` em todas as métricas finais
