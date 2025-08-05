from pydantic import BaseModel
from datetime import datetime
from typing import List

# Já existentes
class ClienteSchema(BaseModel):
    nome: str
    cpf: str
    endereco: str

class PagamentoSchema(BaseModel):
    forma: str
    numero_cartao: str = ""
    validade: str = ""
    cvv: str = ""

class ItemVenda(BaseModel):
    produto_id: int
    quantidade: int

class VendaCreate(BaseModel):
    cliente: ClienteSchema
    pagamento: PagamentoSchema
    itens: List[ItemVenda]
    total: float  # esse pode ser ignorado internamente

class VendaResponse(BaseModel):
    id: int
    produto_id: int | None = None
    quantidade: int | None = None
    valor_total: float
    cliente_nome: str
    cliente_cpf: str
    cliente_endereco: str
    forma_pagamento: str
    criado_em: datetime
    produto_nome: str

    class Config:
        from_attributes = True

# ✅ NOVO: Subschema para o histórico de itens da venda
class ItemVendaOut(BaseModel):
    produto_id: int
    nome_produto: str
    preco_unitario: float
    quantidade: int
    subtotal: float

    class Config:
        from_attributes = True

# ✅ NOVO: Schema de saída para o histórico completo de vendas
class VendaOut(BaseModel):
    id: int
    cliente_nome: str
    cliente_cpf: str
    cliente_endereco: str
    forma_pagamento: str
    valor_total: float
    criado_em: datetime
    itens: List[ItemVendaOut]

    class Config:
        from_attributes = True
