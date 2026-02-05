# GUIA DE DOWNLOAD MANUAL - DADOS SOCIOECONÔMICOS

## 📋 CHECKLIST DE DOWNLOADS

- [x] IDHM (Atlas Brasil) - ✅ CONCLUÍDO → `data/Processed/idhm_2018_2022.csv`
- [ ] Taxa de Desemprego (IBGE SIDRA) - PRIORIDADE ALTA  
- [ ] Renda Per Capita (IBGE SIDRA) - PRIORIDADE MÉDIA

---

## 1️⃣ IDH - ATLAS BRASIL (PRIORIDADE ALTA)

### Site Oficial
🔗 **URL**: http://www.atlasbrasil.org.br/

### Passo a Passo:

#### Método 1: Download Direto (Mais Fácil)

1. **Acesse**: http://www.atlasbrasil.org.br/
2. **Clique em**: "Download de Dados" ou "Dados"
3. **Selecione**:
   - **Nível**: Unidades da Federação (UFs)
   - **Indicador**: IDH
   - **Ano**: Último disponível (2021 ou 2022)
4. **Formato**: CSV
5. **Salve como**: `data/Raw/idh_uf_2021.csv`

#### Método 2: Navegação pelo Mapa

1. **Acesse**: http://www.atlasbrasil.org.br/
2. **Clique**: "Consulta" ou "Mapa"
3. **Filtre**: 
   - Tema: IDH
   - Local: Estados
4. **Exporte**: Botão "Download" ou "Exportar"

#### Método 3: Alternativa - Atlas HDI (Global Data Lab)

Se Atlas Brasil não funcionar:
🔗 **URL**: https://globaldatalab.org/shdi/shdi/

1. Selecione: **Brazil**
2. Nível: **States** (UFs)
3. Baixe dados de IDH
4. Salve como: `data/Raw/idh_globaldatalab.csv`

### Estrutura Esperada:
```csv
UF,IDH,ano
São Paulo,0.806,2021
Rio de Janeiro,0.762,2021
Minas Gerais,0.774,2021
...
```

### ⚠️ IMPORTANTE:
- IDH é **atualizado a cada 2-3 anos** (não há variação anual)
- Use o valor mais recente (2021) para todos os anos (2018-2022)
- Na documentação, mencione: "IDH constante assumido para período"

---

## 2️⃣ TAXA DE DESEMPREGO - IBGE SIDRA (PRIORIDADE ALTA)

### 🔗 URL DIRETA (com filtros pré-configurados):

**COPIE E COLE NO NAVEGADOR:**
```
https://sidra.ibge.gov.br/tabela/4099
```

### Passo a Passo VISUAL:

#### PASSO 1: Acessar a tabela
- Abra o link acima
- Você verá a "Tabela 4099 - Taxa de desocupação..."

#### PASSO 2: Configurar VARIÁVEL
- Na seção "Variável", marque: **Taxa de desocupação**

#### PASSO 3: Configurar TERRITÓRIO  
- Clique em "Unidade da Federação"
- Clique em **"Selecionar todos"** (ou marque as 27 UFs)
- **NÃO** selecione Brasil (queremos só UFs)

#### PASSO 4: Configurar PERÍODO
- Clique em "Trimestre"
- Selecione APENAS os **4º trimestres**:
  - ✅ 4º trimestre 2018
  - ✅ 4º trimestre 2019
  - ✅ 4º trimestre 2020
  - ✅ 4º trimestre 2021
  - ✅ 4º trimestre 2022

#### PASSO 5: Baixar
1. Clique no botão **"Tabela"** (para visualizar)
2. Verifique se aparece uma tabela com 27 linhas (UFs) × 5 colunas (anos)
3. Clique em **"Download"** → **"CSV (BR)"**
4. Salve como: `desemprego_sidra.csv`
5. Mova para: `data/Raw/desemprego_sidra.csv`

### ⚠️ IMPORTANTE:
- Usamos 4º trimestre como representativo do ano
- PNAD Contínua: dados trimestrais desde 2012

### Estrutura Esperada:
```csv
Unidade da Federação,2018,2019,2020,2021,2022
São Paulo,12.5,11.8,14.2,13.1,10.5
Rio de Janeiro,15.2,14.8,16.5,15.2,12.8
...
```

### Alternativa: IPEADATA

Se IBGE SIDRA estiver com problemas:
🔗 **URL**: http://www.ipeadata.gov.br/

1. Busque: "Taxa de desemprego por UF"
2. Série: PAN12_TOTDES12
3. Exporte: Excel ou CSV
4. Salve como: `data/Raw/desemprego_ipea_2018_2022.xlsx`

---

## 3️⃣ RENDA PER CAPITA - IBGE SIDRA (PRIORIDADE MÉDIA)

> **Decisão**: Usar Renda Per Capita ao invés de Taxa de Pobreza.
> Justificativa: variável contínua, mais informativa para ML, correlação inversa com pobreza.

### 🔗 URL DIRETA:
```
https://sidra.ibge.gov.br/tabela/7531
```

### Passo a Passo VISUAL:

#### PASSO 1: Acessar a tabela 7531
- Abra o link acima

#### PASSO 2: Configurar VARIÁVEL
- Marque: **Rendimento médio mensal real domiciliar per capita, a preços médios do ano (Reais)**
- NÃO marque "Coeficiente de variação"

#### PASSO 3: Configurar TERRITÓRIO  
- Clique em "Unidade da Federação"
- Clique em **"Selecionar todos"** (27 UFs)
- NÃO selecione Brasil

#### PASSO 4: Configurar PERÍODO
- Selecione os anos:
  - ✅ 2018
  - ✅ 2019
  - ✅ 2020 (pode não ter - COVID afetou coleta)
  - ✅ 2021
  - ✅ 2022

#### PASSO 5: Baixar
1. Clique em **"Tabela"**
2. Verifique se aparece tabela com 27 UFs × anos
3. Clique em **"Download"** → **"CSV (BR)"**
4. Salve como: `renda_sidra.csv`
5. Mova para: `data/Raw/renda_sidra.csv`

### ⚠️ NOTA:
- Valores em Reais (R$) - preços médios do ano
- Renda baixa = proxy para pobreza alta (correlação inversa)
- Se 2020 não estiver disponível, usaremos interpolação

---

## 📁 ESTRUTURA ESPERADA NA PASTA RAW

Após todos os downloads:

```
data/Raw/
├── TX_REND_BRASIL_REGIOES_UFS_2018.xlsx  ✅ (já temos)
├── tx_rend_brasil_regioes_ufs_2019.xlsx   ✅ (já temos)
├── tx_rend_brasil_regioes_ufs_2020.xlsx   ✅ (já temos)
├── tx_rend_brasil_regioes_ufs_2021.xlsx   ✅ (já temos)
├── tx_rend_brasil_regioes_ufs_2022.xlsx   ✅ (já temos)
├── IDHM.xlsx                              ✅ (já temos - processado)
├── desemprego_sidra.csv                   ⏳ (baixar agora)
└── renda_sidra.csv                        ⏳ (baixar depois)
```

data/Processed/
├── indicadores_educacionais_2018_2022.csv ✅ (135 registros)
├── idhm_2018_2022.csv                     ✅ (135 registros)
└── dados_modelo_final.csv                 ⏳ (será criado após merge)

---

## 🔍 COMO VERIFICAR SE BAIXOU CORRETAMENTE

### Depois de baixar cada arquivo, verifique:

```bash
# Listar arquivos na pasta Raw
ls -lh data/Raw/

# Verificar conteúdo do CSV de IDH
head -10 data/Raw/idh_uf_2021.csv

# Verificar conteúdo do CSV de desemprego
head -10 data/Raw/desemprego_uf_2018_2022.csv

# Contar número de UFs (deve ser 27)
wc -l data/Raw/idh_uf_2021.csv
```

---

## ⚠️ DICAS IMPORTANTES

### 1. Nomenclatura de UFs
Certifique-se que os nomes das UFs estão no formato **completo** (ex: "São Paulo", não "SP") para facilitar o merge posterior.

### 2. Dados faltantes
Se algum ano específico não estiver disponível:
- **Desemprego**: Use interpolação linear entre anos vizinhos
- **Pobreza**: Use média do período mais próximo
- **IDH**: Use o valor mais recente para todos os anos

### 3. Formato dos dados
Prefira CSV quando possível. Se receber Excel (.xlsx), podemos converter facilmente:
```bash
python3 -c "import pandas as pd; df = pd.read_excel('arquivo.xlsx'); df.to_csv('arquivo.csv', index=False)"
```

---

## 📞 SE ENCONTRAR PROBLEMAS

| Problema | Solução |
|----------|---------|
| Site não carrega | Tente acesso em outro horário ou use VPN |
| Download falha | Tente formato diferente (CSV vs Excel) |
| Dados de 2022 não disponíveis | Use 2021 como proxy |
| UFs com nomes diferentes | Padronize manualmente (SP→São Paulo) |

---

## ✅ CHECKLIST FINAL

Após cada download, verifique:

- [ ] Arquivo salvo em `data/Raw/`
- [ ] Nome do arquivo segue padrão (ex: `idh_uf_2021.csv`)
- [ ] Arquivo contém 27 UFs (ou próximo disso)
- [ ] Dados estão no formato esperado (CSV ou Excel)
- [ ] Nenhum erro de leitura ao abrir

---

## 🚀 PRÓXIMO PASSO APÓS DOWNLOADS

Quando todos os arquivos estiverem baixados:

```bash
# Executar script de combinação
python scripts/01_combinar_dados_reais.py
```

Este script irá:
1. Ler todos os CSVs
2. Padronizar nomes das UFs
3. Fazer merge por UF e ano
4. Criar `data/Processed/dados_modelo_v2.csv` completo
5. Gerar relatório de qualidade dos dados

---

**Bons downloads! 📊**
