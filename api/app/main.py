import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# 1. Configuração do FastAPI
app = FastAPI(title="Backend Social Mothers")

# 2. Configuração do Banco de Dados
# A URL de conexão é lida da variável de ambiente definida no docker-compose
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL)

# 3. Endpoint de Saúde (Health Check)
@app.get("/")
def read_root():
    return {"status": "Backend is running!"}

# 4. Endpoint de Teste do Banco de Dados
@app.get("/db-status")
def get_db_status():
    """
    Verifica a conexão com o banco de dados.
    """
    try:
        with engine.connect() as connection:
            # Executa uma consulta simples para testar a conexão
            result = connection.execute(text("SELECT 1"))
            # Se a conexão for bem-sucedida, retorna o status OK
            if result.scalar() == 1:
                return {"db_status": "Connected to PostgreSQL successfully!"}
            else:
                return {"db_status": "Connection test failed."}
    except OperationalError as e:
        # Se houver um erro operacional (ex: DB indisponível), retorna um erro 500
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Could not connect to database: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# **NOTA:** Por enquanto, este arquivo não tem modelos (models) nem rotas de criação (POST),
# apenas o necessário para rodar e testar a conexão básica.