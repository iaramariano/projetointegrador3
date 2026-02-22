#!/bin/sh

# O set -e garante que o script irá parar se algum comando falhar
set -e

# Testando a conexão de rede
echo "--- INICIANDO TESTE DE CONEXÃO ---"
curl -v "https://${AWS_S3_ENDPOINT_URL}"
echo "---TESTE FINALIZADO---"

echo "--- VERIFICANDO VARIÁVEIS DE AMBIENTE ANTES DE INICIAR ---"
echo "AWS_STORAGE_BUCKET_NAME: ${AWS_STORAGE_BUCKET_NAME}"
echo "AWS_S3_ENDPOINT_URL: ${AWS_S3_ENDPOINT_URL}"
echo "AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}"

if [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "AWS_SECRET_ACCESS_KEY: [ESTÁ DEFINIDA]"
else
    echo "AWS_SECRET_ACCESS_KEY: [!!!!NÃO FOI ENCONTRADA!!!!]"
fi
echo "--- FIM DA VERIFICAÇÃO ---"

# Executa as migrações do banco de dados
echo "Aplicando migrações do banco de dados..."
python manage.py migrate --no-input

# Coleta os arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input --clear

# Inicia o servidor Gunicorn
echo "Iniciando o servidor Gunicorn..."
gunicorn project.wsgi:application --bind 0.0.0.0:8000 --timeout 120
