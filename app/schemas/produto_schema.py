from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    quantidade: int

    class Config:
        from_attributes = True  # ✅ agora tá dentro da classe ProdutoOut

class MensagemResponse(BaseModel):
    mensagem: str
