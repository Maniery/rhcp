#!/bin/bash

# definicao das portas dos servidores
PORTA_DASHBOARD_HTTP=8888
PORTA_SERVIDOR_RHCP=8000

function finalizar {
    echo "Finalizando Dashboard HTTP..."
    kill -15 "$PID_HTTP"
    echo "Finalizando Servidor RHCP..."
    kill -15 $PID_RHCP
    echo "Finalizando serviço geral..."
    exit 0
}

# capturando o ctrl+c
trap finalizar SIGINT SIGTERM

# Rodando o dashboard HTTP para o site
python3 -m http.server "$PORTA_DASHBOARD_HTTP" &
# obtendo o seu PID
PID_HTTP=$!

echo "Dashboard HTTP rodando com PID $PID_HTTP"

# Rodando o servidor RHCP
python3 servidor.py $PORTA_SERVIDOR_RHCP &
# obtendo o seu PID
PID_RHCP=$!

echo "Servidor RHCP rodando com PID $$"

while true;
do
    sleep 1
done
