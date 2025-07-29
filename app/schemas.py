from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade: int  # <- nome igual ao model

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True

class MensagemResponse(BaseModel):
    mensagem: str
