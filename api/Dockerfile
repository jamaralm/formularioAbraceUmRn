# Usa uma imagem base Python slim
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Define variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY ./app /app/app

# Comando padrão para iniciar a aplicação
# Ele será sobrescrito pelo docker-compose para aguardar o DB
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]