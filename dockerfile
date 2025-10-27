# Dockerfile Simples - Integra Maker
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 5002

# Comando para executar

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app", "--workers", "3"]