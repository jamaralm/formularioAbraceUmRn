import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from pydantic import BaseModel
# Importa apenas o que é necessário e a função get_db
from .database import engine, Base, MotherModel, get_db

app = FastAPI(title="Backend Social Mothers")

# Se o erro de importação persistir, mude para 'from database import ...' 
# e certifique-se de que database.py está na mesma pasta.

# --- Pydantic Model (O que entra na API) ---
class MotherBase(BaseModel):
    name: str
    statusGestacao: str
    urgencyLevel: int = 0

# --- Lógica de Criação (Serviço) ---
def create_mother(db: Session, mother_data: MotherBase):
    db_mother = MotherModel(**mother_data.dict())
    db.add(db_mother)
    db.commit()
    db.refresh(db_mother)
    return db_mother

# --- Endpoints ---

@app.get("/", status_code=status.HTTP_200_OK)
def read_root(db: Session = Depends(get_db)):
    """
    Lista todas as mães cadastradas.
    """
    motherList = db.query(MotherModel).all()

    if not motherList:
        return {"Mother List": "No mothers found."}

    resposeList = [
        {"name": mother.name, "statusGestacao": mother.statusGestacao, "urgencyLevel": mother.urgencyLevel} 
        for mother in motherList
    ]
    return {"Mother List": resposeList}

@app.get("/mother/{mother_id}", status_code=status.HTTP_200_OK)
def read_mother(mother_id: int, db: Session = Depends(get_db)):
    """
    Obtém detalhes de uma mãe específica pelo ID.
    """
    mother = db.query(MotherModel).filter(MotherModel.id == mother_id).first()

    if not mother:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mother with ID {mother_id} not found."
        )

    return {
        "name": mother.name,
        "statusGestacao": mother.statusGestacao,
        "urgencyLevel": mother.urgencyLevel
    }

@app.delete("/mother/{mother_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mother(mother_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma mãe específica pelo ID.
    """
    mother = db.query(MotherModel).filter(MotherModel.id == mother_id).first()

    if not mother:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mother with ID {mother_id} not found."
        )

    db.delete(mother)
    db.commit()
    return

@app.post("/formSubmit", status_code=status.HTTP_201_CREATED)
def form_submit(data: dict, db: Session = Depends(get_db)):
    """
    Endpoint para submissão de formulários e criação de MotherModel.
    """

    # Validação Básica
    nomeCompleto = data.get("nomeCompleto")
    statusGestacao = data.get("statusGestacao") 
    
    if not nomeCompleto or not statusGestacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campos 'nomeCompleto' e 'statusGestacao' são obrigatórios."
        )

    # Cria o modelo Pydantic para validação e passagem de dados
    try:
        newMotherData = MotherBase(name=nomeCompleto, statusGestacao=statusGestacao)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro de validação de dados: {e}")

    # Cria o registro no banco de dados usando a sessão injetada
    db_mother = create_mother(db, newMotherData)

    return {"message": "Form submitted successfully!", "mother_id": db_mother.id}

# --- Health Check ---
@app.get("/db-status")
def get_db_status():
    """
    Verifica a conexão com o banco de dados.
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() == 1:
                return {"db_status": "Connected to PostgreSQL successfully!"}
            else:
                return {"db_status": "Connection test failed."}
    except OperationalError as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not connect to database.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")