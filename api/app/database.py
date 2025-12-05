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

# Função de Dependência
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Definição do Modelo do SQLAlchemy
class MotherModel(Base):
    """
    Modelo SQLAlchemy para a tabela 'mothers'.
    """
    __tablename__ = "mothers"
    
    # Colunas existentes
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # NomeCompleto
    statusGestacao = Column(String)
    urgencyLevel = Column(Integer, default=0) # Mantido

    # Novas colunas (todas como String para flexibilidade, exceto urgênciaScore)
    dataEnvio = Column(String)
    dataNascimento = Column(String)
    idade = Column(String)
    cpf = Column(String)
    rg = Column(String)
    estadoCivil = Column(String)

    telefone = Column(String)
    email = Column(String)
    cep = Column(String)
    estado = Column(String)
    endereco = Column(String)
    numero = Column(String)
    complemento = Column(String)
    bairro = Column(String)
    cidade = Column(String)

    moraCom = Column(String)
    numPessoas = Column(String)
    numCriancas = Column(String)

    mesesGestacao = Column(String)
    preNatal = Column(String)
    localPreNatal = Column(String)
    dataParto = Column(String)
    medicamento = Column(String)
    qualMedicamento = Column(String)
    postoSaude = Column(String)
    acompanhamento = Column(String)
    programaSocial = Column(String)

    trabalho = Column(String)
    fonteRenda = Column(String)
    rendaMensal = Column(String)
    tipoMoradia = Column(String)
    materialCasa = Column(String)
    servicos = Column(String) # Armazenará o JSON stringificado da lista

    ajuda = Column(String) # Armazenará o JSON stringificado da lista
    apoioPessoal = Column(String)
    instagramHandle = Column(String)
    instagramPublicCheck = Column(String)
    historia = Column(String)
    novoItem = Column(String)

    urgencyScore = Column(Integer)

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# Configuração da Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)