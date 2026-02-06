# 🎨 Guia Visual do Dashboard - Dark Mode Moderno

## Overview

O dashboard agora utiliza um **tema Dark Mode Moderno** com componentes visuais customizados que melhoram significativamente a experiência do usuário.

## Bibliotecas Instaladas

```bash
streamlit-extras          # Componentes adicionais para Streamlit
streamlit-option-menu     # Menu customizado
streamlit-lottie          # Animações Lottie (opcional)
```

## Paleta de Cores

### Cores Primárias
- **Azul Escuro**: `#1E3A8A` - Cor principal
- **Azul Claro**: `#3B82F6` - Destaque
- **Ciano**: `#06B6D4` - Secundária

### Cores de Status
- **Verde**: `#10B981` - Sucesso
- **Amarelo/Laranja**: `#F59E0B` - Aviso
- **Vermelho**: `#EF4444` - Erro/Perigo
- **Ciano**: `#06B6D4` - Informação

### Cores Neutras (Dark Mode)
- **Background**: `#0F172A` - Fundo principal
- **Surface**: `#1E293B` - Cards e containers
- **Texto**: `#F1F5F9` - Texto claro
- **Border**: `#475569` - Bordas

## Componentes Visuais

### 1. Stat Card
Card customizado para exibir estatísticas com ícone, label, valor e cor.

**Uso:**
```python
from theme import stat_card

stat_card(
    label="Taxa Média Abandono",
    value="1.78%",
    icon="📈",
    color="warning"  # 'primary', 'success', 'warning', 'danger', 'info'
)
```

**Cores disponíveis:** primary, success, warning, danger, info

### 2. Section Header
Header de seção com gradiente e ícone.

**Uso:**
```python
from theme import section_header

section_header("Distribuição de Risco (2022)", "📊")
```

**Resultado:** Header com fundo gradiente azul-ciano

### 3. Info Box
Box para informações gerais.

**Uso:**
```python
from theme import info_box

info_box(
    text="Todos os estados foram analisados entre 2018-2022",
    title="ℹ️ Informação"
)
```

### 4. Success Box
Box para mensagens de sucesso.

**Uso:**
```python
from theme import success_box

success_box(
    text="A análise foi concluída com sucesso!",
    title="✅ Sucesso"
)
```

### 5. Warning Box
Box para aviso e alertas.

**Uso:**
```python
from theme import warning_box

warning_box(
    text="Por que as predições são linhas retas?",
    title="⚠️ Importante"
)
```

## Estilos CSS Aplicados

### Títulos
- **H1**: Gradiente azul-ciano, 2.5em
- **H2**: Azul claro com linha esquerda, 1.8em
- **H3**: Azul claro, 1.3em

### Métricas
- Background gradiente
- Border esquerdo colorido
- Hover effect com elevação
- Shadow animado

### Botões
- Gradiente azul
- Shadow com cor azul
- Hover com elevação (-2px)
- Transição suave (0.3s)

### Dataframes
- Background escuro
- Header com cor azul
- Hover nas linhas
- Border sutil

### Alerts
- Info: Ciano
- Success: Verde
- Warning: Amarelo
- Error: Vermelho

## Como Usar o Tema

### No arquivo principal (app.py):

```python
from theme import apply_dark_theme, section_header, stat_card

# No início do arquivo, após st.set_page_config()
apply_dark_theme()

# Usar na seção de KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    stat_card("Métrica 1", "Valor", "📊", "success")

with col2:
    stat_card("Métrica 2", "Valor", "📈", "warning")

# Usar para headers de seção
section_header("Seção Principal", "📊")

# Usar para mensagens customizadas
success_box("Operação concluída!", "✅ Sucesso")
warning_box("Atenção: alguns dados podem estar desatualizados", "⚠️ Aviso")
info_box("Isso é uma informação importante", "ℹ️ Informação")
```

### Nas páginas secundárias:

Cada página de seção (pages/*.py) pode importar:

```python
from dashboard.theme import (
    apply_dark_theme, 
    section_header, 
    stat_card,
    success_box,
    warning_box,
    info_box
)
```

## Recursos Visuais

### Gradientes
- **Azul→Ciano**: Headers principais
- **Verde**: Status positivo
- **Laranja**: Avisos
- **Vermelho**: Erros

### Animações CSS
- Buttons: Elevação ao hover
- Cards: Elevação + sombra ao hover
- Links: Mudança de cor ao hover

### Efeitos
- Border radius: 8-12px (arredondado)
- Shadows: 0 4px 20px rgba(0,0,0,0.3)
- Transitions: 0.3s ease

## Scrollbar Customizado

O scrollbar foi customizado para combinar com o tema:
- Track: Cor de surface
- Thumb: Azul primário
- Hover: Azul claro

## Estrutura de Pastas

```
dashboard/
├── app.py                    # Arquivo principal (com tema integrado)
├── theme.py                  # ✨ Novo arquivo de temas
├── config.py                 # Configurações
├── pages/
│   ├── 1_inicio.py
│   ├── 2_analise_estados.py
│   ├── 3_predicoes.py
│   ├── 4_shap_analysis.py
│   ├── 5_conclusoes.py
│   └── 6_mapa_brasil.py
└── utils/
    └── mapa_helper.py
```

## Customizações Futuras

Para customizar ainda mais, você pode:

1. **Modificar paleta de cores** em `theme.py` na seção `COLORS`
2. **Criar novos componentes** com funções customizadas
3. **Ajustar CSS** na variável `DARK_MODE_CSS`
4. **Usar gradientes custom** nos componentes

## Performance

O CSS é aplicado uma única vez no carregamento:
- ✅ Sem impacto negativo na performance
- ✅ Todos os navegadores modernos suportam
- ✅ Responsivo em mobile e desktop

## Compatibilidade

- ✅ Streamlit 1.0+
- ✅ Todos os navegadores modernos
- ✅ Dark mode automático (segue preferência do SO)
- ✅ Funciona com todos os componentes do Streamlit

## Exemplos de Uso

### Página de Análises
```python
st.set_page_config(page_title="Análise", page_icon="📊", layout="wide")
apply_dark_theme()

section_header("Análise de Dados", "📊")

col1, col2 = st.columns(2)
with col1:
    stat_card("Total de Registros", "135", "📋", "info")
with col2:
    stat_card("Taxa Média", "1.78%", "📈", "warning")

st.markdown("---")

# Seu conteúdo aqui
```

### Página com Mensagens
```python
apply_dark_theme()

section_header("Resultados", "✨")

if sucesso:
    success_box(
        "Análise concluída com 95% de precisão!",
        "✅ Análise Sucesso"
    )
else:
    warning_box(
        "Alguns dados faltam. Verifique a fonte.",
        "⚠️ Aviso de Qualidade"
    )

info_box(
    "Este dashboard atualiza dados a cada execução",
    "ℹ️ Atualização"
)
```

## Próximas Melhorias

Possíveis adições:
- [ ] Tema claro alternativo
- [ ] Seletor de tema no sidebar
- [ ] Animações Lottie para loading
- [ ] Menu de navegação customizado com `streamlit-option-menu`
- [ ] Ícones SVG customizados
- [ ] Dark/Light mode toggle

---

**Versão**: 1.0  
**Última atualização**: Feb 5, 2026  
**Autor**: Dashboard Team
