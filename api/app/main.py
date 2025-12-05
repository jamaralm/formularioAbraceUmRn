import os
import json

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from pydantic import BaseModel
# Importa apenas o que é necessário e a função get_db
from .database import engine, Base, MotherModel, get_db
from .models import MotherSchema
from .services import create_mother

app = FastAPI(title="Abrace um RN API")

# Se o erro de importação persistir, mude para 'from database import ...' 
# e certifique-se de que database.py está na mesma pasta.

# --- Endpoints ---

@app.get("/", status_code=status.HTTP_200_OK)
def read_root(db: Session = Depends(get_db)):
    """
    Lista todas as mães cadastradas, retornando um resumo dos campos chave.
    """
    motherList = db.query(MotherModel).all()

    if not motherList:
        return {"Mother List": "No mothers found."}

    responseList = [
        {
            "id": mother.id, 
            "nomeCompleto": mother.name, 
            "statusGestacao": mother.statusGestacao, 
            "urgencyScore": mother.urgencyScore,
            "cidade": mother.cidade,
            "telefone": mother.telefone,
            "dataEnvio": mother.dataEnvio
        } 
        for mother in motherList
    ]
    return {"Mother List": responseList}

@app.get("/mother/{mother_id}", status_code=status.HTTP_200_OK)
def read_mother(mother_id: int, db: Session = Depends(get_db)):
    """
    Obtém TODOS os detalhes de uma mãe específica pelo ID, 
    incluindo a desserialização dos campos de lista (servicos, ajuda).
    """
    mother = db.query(MotherModel).filter(MotherModel.id == mother_id).first()

    if not mother:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mother with ID {mother_id} not found."
        )

    mother_dict = mother.__dict__
    mother_dict.pop('_sa_instance_state', None)
    
    mother_dict['nomeCompleto'] = mother_dict.pop('name')

    # Desserializa os campos de lista (JSON string -> Python List)
    try:
        if mother_dict.get('servicos') and isinstance(mother_dict['servicos'], str):
            mother_dict['servicos'] = json.loads(mother_dict['servicos'])
    except json.JSONDecodeError:
        print(f"Erro ao desserializar 'servicos' para a mãe {mother_id}")
        mother_dict['servicos'] = []
        
    try:
        if mother_dict.get('ajuda') and isinstance(mother_dict['ajuda'], str):
            mother_dict['ajuda'] = json.loads(mother_dict['ajuda'])
    except json.JSONDecodeError:
        print(f"Erro ao desserializar 'ajuda' para a mãe {mother_id}")
        mother_dict['ajuda'] = []

    return mother_dict

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
def form_submit(data: MotherSchema, db: Session = Depends(get_db)):
    """
    Endpoint para submissão de formulários e criação de MotherModel.
    Agora usa MotherSchema para validação automática do corpo da requisição.
    """

    try:
        # A função create_mother recebe o objeto Pydantic validado
        db_mother = create_mother(data)
    except Exception as e:
        # Se houver um erro durante a criação/persistência no DB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Erro ao processar o formulário ou salvar no banco de dados: {e}"
        )

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