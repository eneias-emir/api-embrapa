#!/bin/bash

# Iniciar o serviço principal com 4 trabalhadores
python3 -m uvicorn webapp.main:app --host 0.0.0.0 --port 8000 --workers 4

# Executar o comando fornecido em CMD
exec "$@"
