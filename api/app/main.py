import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from .database import MotherModel, Base

app = FastAPI(title="Backend Social Mothers")

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(bind=engine)

class Mother(BaseModel):
    name: str
    statusGestacao: str
    urgencyLevel: int = 0

def create_mother(db: Session, mother: MotherModel):
    db_mother = MotherModel(name=mother.name, statusGestacao=mother.statusGestacao, urgencyLevel=mother.urgencyLevel)
    db.add(db_mother)
    db.commit()
    db.refresh(db_mother)
    return db_mother

@app.get("/")
def read_root():
    motherList = session.query(MotherModel).all()

    if not motherList:
        return {"Mother List": "No mothers found."}

    resposeList = [
        {"name": mother.name, "statusGestacao": mother.statusGestacao, "urgencyLevel": mother.urgencyLevel} for mother in motherList
    ]
    return {"Mother List": resposeList}

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
        raise HTTPException(status_code=500, detail=f"Could not connect to database: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.post("/formSubmit")
def form_submit(data: dict):
    """
    Endpoint para submissão de formulários.
    """

    nomeCompleto = data.get("nomeCompleto")
    statusGestacao = data.get("statusGestacao") 

    newMother = Mother(name=nomeCompleto, statusGestacao=statusGestacao)

    create_mother(Session(bind=engine), MotherModel(**newMother.dict()))

    return {"message": "Form submitted successfully!", "data": data}