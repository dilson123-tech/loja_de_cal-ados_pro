from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int
    criado_em: datetime

    class Config:
        orm_mode = True
