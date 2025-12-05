from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class MotherSchema(BaseModel):
    """
    Schema Pydantic completo para validar o JSON de entrada do frontend.
    """
    # Datas e Identificação
    dataEnvio: str
    nomeCompleto: str
    dataNascimento: str
    idade: str
    cpf: str
    rg: str
    estadoCivil: str

    # Contato e Endereço
    telefone: str
    email: str
    cep: str
    estado: str
    endereco: str
    numero: str
    complemento: Optional[str] = None # Campo opcional
    bairro: str
    cidade: str

    # Situação Familiar
    moraCom: str
    numPessoas: str
    numCriancas: str

    # Gestação e Saúde
    statusGestacao: str
    mesesGestacao: Optional[str] = None # Pode não se aplicar se statusGestacao != 'gravida'
    preNatal: str
    localPreNatal: Optional[str] = None # Campo opcional
    dataParto: Optional[str] = None # Campo opcional
    medicamento: str
    qualMedicamento: Optional[str] = None # Campo opcional
    postoSaude: str
    acompanhamento: str
    programaSocial: str

    # Trabalho e Moradia
    trabalho: str
    fonteRenda: str
    rendaMensal: str
    tipoMoradia: str
    materialCasa: str
    servicos: List[str] # Lista de strings (será serializada para DB)

    # Suporte e História
    ajuda: List[str] # Lista de strings (será serializada para DB)
    apoioPessoal: str
    instagramHandle: Optional[str] = None # Campo opcional
    instagramPublicCheck: str
    historia: str
    novoItem: Optional[str] = None # Campo opcional

    # Nível de Urgência
    urgencyScore: int
    urgencyLevel: int = Field(default=0) # Mantendo o campo, com default