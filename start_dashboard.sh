#!/bin/bash

# Script para iniciar o Dashboard Streamlit

echo "Iniciando Dashboard..."
echo "===================="
echo ""

# Verificar se está na raiz do projeto
if [ ! -f "dashboard/app.py" ]; then
    echo "Erro: Execute este script da raiz do projeto"
    echo "Exemplo: cd /home/teodoro/Documents/ZettaLab/ZettaLab-Data"
    exit 1
fi

# Ativar venv
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Ambiente virtual ativado"
else
    echo "Erro: Ambiente virtual não encontrado"
    exit 1
fi

# Iniciar dashboard
echo ""
echo "Iniciando Streamlit..."
echo ""
echo "O dashboard abrirá em: http://localhost:8501"
echo ""
echo "Para parar, pressione Ctrl+C"
echo ""

streamlit run dashboard/app.py
