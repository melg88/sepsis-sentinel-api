#!/bin/bash

# Inicia a API FastAPI em segundo plano
echo "Iniciando a API FastAPI..."
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# Inicia a aplicação Streamlit em primeiro plano
echo "Iniciando o Frontend Streamlit..."
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0