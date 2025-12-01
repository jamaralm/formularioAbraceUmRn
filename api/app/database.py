import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Configuração do Engine
engine = create_engine(DATABASE_URL)

# Definição da Base
Base = declarative_base()

# Definição do Modelo do SQLAlchemy
class MotherModel(Base):
    __tablename__ = "mothers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    statusGestacao = Column(String)
    urgencyLevel = Column(Integer, default=0)

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# Configuração da Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função de Dependência
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()