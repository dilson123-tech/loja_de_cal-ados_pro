from pydantic import BaseModel
from datetime import datetime

# Dados recebidos no POST
class VendaCreate(BaseModel):
    produto_id: int
    quantidade: int
    cliente_nome: str
    cliente_cpf: str
    cliente_endereco: str
    forma_pagamento: str

# Dados retornados no GET
class VendaResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    valor_total: float
    cliente_nome: str
    cliente_cpf: str
    cliente_endereco: str
    forma_pagamento: str
    criado_em: datetime
    produto_nome: str  # ← Novo campo! Vai puxar direto da relação

    class Config:
        orm_mode = True
