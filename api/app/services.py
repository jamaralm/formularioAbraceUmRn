import json

from .database import get_db, MotherModel
from .models import MotherSchema

db = get_db()

def create_mother(mother_data: MotherSchema):
    """
    Cria um registro MotherModel no banco de dados a partir do schema Pydantic.
    Lida com a serialização de listas para JSON string.
    """
    # Converte o Pydantic model para um dicionário
    mother_dict = mother_data.model_dump()

    # Renomeia 'nomeCompleto' para 'name' (para manter a convenção da sua Model)
    mother_dict['name'] = mother_dict.pop('nomeCompleto')
    
    # Serializa listas para string JSON para persistir na coluna String do DB
    if 'servicos' in mother_dict and isinstance(mother_dict['servicos'], list):
        mother_dict['servicos'] = json.dumps(mother_dict['servicos'])
    
    if 'ajuda' in mother_dict and isinstance(mother_dict['ajuda'], list):
        mother_dict['ajuda'] = json.dumps(mother_dict['ajuda'])

    # Cria a instância do modelo SQLAlchemy
    db_mother = MotherModel(**mother_dict)
    
    # Persistência
    try:
        db.add(db_mother)
        db.commit()
        db.refresh(db_mother)
        return db_mother
    except Exception as e:
        db.rollback()
        print(f"Erro ao salvar no banco de dados: {e}")
        raise