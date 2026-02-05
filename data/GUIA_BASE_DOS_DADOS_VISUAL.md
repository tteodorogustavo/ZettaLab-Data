# GUIA VISUAL - BASE DOS DADOS (EDUCAÇÃO)

## 🔍 O QUE VOCÊ ESTÁ VENDO NA PÁGINA

Na página `https://basedosdados.org/search?theme=education&page=1`, você verá uma lista de **conjuntos de dados** (datasets).

---

## ✅ CONJUNTO DE DADOS CORRETO

### Procure por este card na página:

```
┌─────────────────────────────────────────────────────────┐
│ 📊 INEP - Indicadores Educacionais                     │
│                                                         │
│ Organização: INEP                                      │
│ Tema: Educação                                         │
│                                                         │
│ [Acessar]  [Visualizar tabelas]                        │
└─────────────────────────────────────────────────────────┘
```

**URL Direta:** `https://basedosdados.org/dataset/br-inep-indicadores-educacionais`

---

## 📋 PASSO A PASSO VISUAL

### Passo 1: Encontre o Card
Na página de resultados, procure o card com:
- **Título**: "INEP - Indicadores Educacionais" ou "br_inep_indicadores_educacionais"
- **Ícone**: 📊 (gráfico)
- **Tema**: Educação

### Passo 2: Clique em "Acessar" ou no Título
Isso abrirá a página do dataset com todas as tabelas disponíveis.

### Passo 3: Escolha a Tabela Correta

Você verá uma lista de tabelas. Procure por:

```
✅ TABELA CORRETA: "Taxa de Transição" ou "taxa_transicao"

O que está tabela contém:
├── taxa_evasao_ef        (Evasão no Ensino Fundamental)
├── taxa_evasao_em        (Evasão no Ensino Médio)
├── taxa_repetencia_ef    (Repetência no Ensino Fundamental)
├── taxa_repetencia_em    (Repetência no Ensino Médio)
├── taxa_promocao_ef      (Promoção no Ensino Fundamental)
├── taxa_promocao_em      (Promoção no Ensino Médio)
├── sigla_uf              (Sigla da UF - ex: SP, RJ)
├── id_municipio          (Código do município)
├── ano                   (Ano de referência)
└── E outras colunas...
```

**⚠️ ATENÇÃO:** Não confunda com:
- ❌ "taxa_aprovacao" (taxa de aprovação - diferente!)
- ❌ "matricula" (dados de matrícula)
- ❌ "docente" (dados de professores)

---

## 📥 COMO FAZER O DOWNLOAD

### Opção 1: Download Direto (Mais Simples)

1. Na página da tabela `taxa_transicao`, procure o botão **"Download"** ou **"Baixar dados"**
2. Configure os filtros:
   ```
   Ano: 2018, 2019, 2020, 2021, 2022
   Rede: Total (ou deixe todos)
   Localização: Total (ou deixe todos)
   ```
3. Clique em **"Download CSV"**
4. Salve como: `indicadores_educacionais_2018_2022.csv`

### Opção 2: Query SQL (Mais Flexível)

1. Clique em **"Consultar dados"** ou **"Query SQL"**
2. Cole esta query:

```sql
SELECT 
    sigla_uf,
    ano,
    rede,
    localizacao,
    taxa_evasao_ef,
    taxa_evasao_em,
    taxa_repetencia_ef,
    taxa_repetencia_em
FROM `basedosdados.br_inep_indicadores_educacionais.taxa_transicao`
WHERE ano BETWEEN 2018 AND 2022
  AND rede = 'Total'
  AND localizacao = 'Total'
ORDER BY sigla_uf, ano
```

3. Clique em **"Executar"** ou **"Run"**
4. Baixe o resultado em CSV

---

## 🎯 FILTROS IMPORTANTES

### Quando for baixar, configure:

| Filtro | Valor | Por quê? |
|--------|-------|----------|
| **Ano** | 2018, 2019, 2020, 2021, 2022 | Período do estudo |
| **Rede** | Total | Público + Privado |
| **Localização** | Total | Rural + Urbana |
| **Etapa** | Deixar todas | EF + EM |

---

## 📊 ESTRUTURA ESPERADA DO ARQUIVO

O CSV baixado deve ter estas colunas:

```csv
sigla_uf,ano,rede,localizacao,taxa_evasao_ef,taxa_evasao_em,taxa_repetencia_ef,taxa_repetencia_em
SP,2022,Total,Total,1.2,1.4,0.8,0.9
RJ,2022,Total,Total,2.1,3.4,1.5,2.1
MG,2022,Total,Total,1.8,2.2,1.2,1.4
...
```

**Esperamos:** 135 linhas (27 UFs x 5 anos)

---

## 🔗 LINKS DIRETOS (TENTE ESTES)

Se a busca não funcionar, tente acessar diretamente:

1. **Dataset geral:**
   `https://basedosdados.org/dataset/br-inep-indicadores-educacionais`

2. **Tabela específica (taxa_transicao):**
   `https://basedosdados.org/dataset/br-inep-indicadores-educacionais?table=taxa_transicao`

3. **Query SQL direta:**
   `https://basedosdados.org/dataset/br-inep-indicadores-educacionais?table=taxa_transicao&query`

---

## ❌ SE DER ERRO

### Erro comum: "Necessário autenticação Google Cloud"

**Solução:**
1. Crie uma conta gratuita no Google Cloud (12 meses grátis)
2. Ou use o **modo de download direto** (não precisa de autenticação)

### Erro comum: "Dados muito grandes"

**Solução:**
- Use filtros mais específicos (ano por ano)
- Ou baixe apenas os dados de UF (agregue por estado, não município)

---

## ✅ CHECKLIST DE VERIFICAÇÃO

Depois de baixar, verifique:

- [ ] Arquivo tem extensão `.csv`
- [ ] Nome do arquivo: `indicadores_educacionais_2018_2022.csv`
- [ ] Colunas incluem: sigla_uf, ano, taxa_evasao_ef, taxa_evasao_em
- [ ] Período: 2018 até 2022
- [ ] Quantidade de linhas: ~135 (27 UFs x 5 anos)
- [ ] Valores não estão vazios (poucos NaN)

---

## 🆘 ALTERNATIVA SE BASE DOS DADOS NÃO FUNCIONAR

### Opção B: Site Oficial do INEP

1. Acesse: `https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais`
2. Procure: "Taxas de Rendimento (Fluxo)"
3. Baixe: `taxas_transicao_2018_2022.xlsx`
4. Converta para CSV se necessário

---

## 📞 PRECISA DE MAIS AJUDA?

Se não conseguir encontrar, me envie:
1. Screenshot da página que você está vendo
2. URL exata onde você está
3. Descrição do que aparece na tela

Assim posso te guiar melhor! 🎯
