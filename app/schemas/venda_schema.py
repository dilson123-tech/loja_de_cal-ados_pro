from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VendaCreate(BaseModel):
    produto_id: int
    quantidade_vendida: int


class VendaResponse(BaseModel):
    id: int
    produto_id: int
    quantidade_vendida: int
    valor_total: float
    data_venda: datetime


    class Config:
        orm_mode = True
