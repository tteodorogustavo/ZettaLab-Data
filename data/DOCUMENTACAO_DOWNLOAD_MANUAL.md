
# GUIA DE DOWNLOAD MANUAL DE DADOS

## 1. DADOS EDUCACIONAIS (Evasão e Repetência) - 2018-2022

### Opção A: Base dos Dados (Recomendada)
1. Acesse: https://basedosdados.org/dataset/br-inep-indicadores-educacionais
2. Navegue até: taxa_transicao
3. Filtre: ano entre 2018 e 2022
4. Download: Clique em "Download" (formato CSV)
5. Salve em: data/Raw/indicadores_educacionais_2018_2022.csv

### Opção B: Site do INEP
1. Acesse: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais
2. Baixe: "Taxas de Transição (2018-2022)"
3. Salve em: data/Raw/taxas_transicao_2018_2022.xlsx

## 2. IDH (Índice de Desenvolvimento Humano)

### Atlas da Desigualdade
1. Acesse: http://www.atlasbrasil.org.br/
2. Clique: "Download de Dados"
3. Selecione: "IDH - Unidades da Federação"
4. Baixe o CSV
5. Salve em: data/Raw/idh_uf_2021.csv

### Atlas HDI (Alternativa)
1. Acesse: https://globaldatalab.org/shdi/shdi/
2. Filtre: Brazil, States
3. Baixe dados de 2018-2022
4. Salve em: data/Raw/shdi_brazil_states.csv

## 3. PIB PER CAPITA

### IBGE - SIDRA
1. Acesse: https://sidra.ibge.gov.br/tabela/5938
2. Selecione:
   - Período: 2018, 2019, 2020, 2021, 2022
   - Variável: Produto Interno Bruto per capita
   - Unidade de Federação: Todas
3. Clique: "Download" → CSV
4. Salve em: data/Raw/pib_per_capita_2018_2022.csv

### Base dos Dados
1. Acesse: https://basedosdados.org/dataset/br-ibge-pib
2. Tabela: municipio
3. Filtre: Ano entre 2018-2022
4. Agregue por UF
5. Salve em: data/Raw/pib_uf_2018_2022.csv

## 4. TAXA DE DESEMPREGO

### IBGE - PNADC
1. Acesse: https://sidra.ibge.gov.br/tabela/4099
2. Selecione:
   - Período: 2018-2022
   - Variável: Taxa de desocupação
   - Unidade da Federação: Todas
3. Download: CSV
4. Salve em: data/Raw/desemprego_uf_2018_2022.csv

### IPEADATA
1. Acesse: http://www.ipeadata.gov.br/
2. Busque: "Desemprego por UF"
3. Selecione série: PAN12_TOTDES12
4. Exporte: Excel ou CSV
5. Salve em: data/Raw/desemprego_ipea_2018_2022.csv

## 5. TAXA DE POBREZA

### IBGE - PNADC/SNIPC
1. Acesse: https://www.ibge.gov.br/estatisticas/sociais/populacao.html
2. Procure: "Síntese de Indicadores Sociais"
3. Download: Tabela de pobreza por UF
4. Salve em: data/Raw/pobreza_uf_2018_2022.csv

## ESTRUTURA ESPERADA DOS ARQUIVOS

### indicadores_educacionais.csv:
| sigla_uf | ano | taxa_evasao_ef | taxa_evasao_em | taxa_repetencia_ef | taxa_repetencia_em |
|----------|-----|----------------|----------------|-------------------|-------------------|
| SP       | 2022| 1.2            | 1.4            | 0.8               | 0.9               |
| RJ       | 2022| 2.1            | 3.4            | 1.5               | 2.1               |

### idh_uf.csv:
| UF           | ano | idh   |
|--------------|-----|-------|
| São Paulo    | 2021| 0.806 |
| Rio de Janeiro| 2021| 0.762 |

### pib_per_capita.csv:
| uf_sigla | ano | pib_per_capita |
|----------|-----|----------------|
| SP       | 2022| 56342.15       |
| RJ       | 2022| 51234.67       |

## COMBINAR OS DADOS

Após fazer todos os downloads, execute o script:
```bash
python notebooks/01_aquisicao_novos_dados_manual.py
```

Ou combine manualmente no notebook:
```python
import pandas as pd

# Carregar cada arquivo
educacao = pd.read_csv('data/Raw/indicadores_educacionais.csv')
idh = pd.read_csv('data/Raw/idh_uf.csv')
pib = pd.read_csv('data/Raw/pib_per_capita.csv')

# Fazer merges
combined = educacao.merge(idh, on=['UF', 'ano'])
combined = combined.merge(pib, on=['UF', 'ano'])

# Salvar
combined.to_csv('data/Processed/dados_modelo_v2.csv', index=False)
```

## OBSERVAÇÕES IMPORTANTES

1. **Consistência temporal**: Use sempre o mesmo período (2018-2022)
2. **Padronização de nomes**: Mantenha nomes completos das UFs (ex: "São Paulo", não "SP")
3. **Valores ausentes**: Documente qualquer gap nos dados
4. **Fontes**: Anote a URL e data de acesso de cada download

## PREENCHIMENTO ESTATÍSTICO (se necessário)

Se houver gaps pequenos (< 10% dos dados):
1. **Interpolação linear**: Para séries temporais contínuas
2. **Média móvel**: Suavizar variações abruptas
3. **Forward fill**: Para indicadores que não mudam drasticamente (ex: saneamento)
4. **Média regional**: Usar média de UFs similares

NUNCA use dados sintéticos sem documentar!
