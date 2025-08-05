from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
from app.models.produto_model import ProdutoModel


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False)
    cliente_nome = Column(String, nullable=False)
    cliente_cpf = Column(String, nullable=False)
    cliente_endereco = Column(String, nullable=False)
    forma_pagamento = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

produto = relationship("ProdutoModel")

from sqlalchemy.orm import relationship
from app.models.produto_model import ProdutoModel

# ...

class Venda(Base):
    __tablename__ = "vendas"

    # ... seus campos já existentes

    produto = relationship("ProdutoModel", backref="vendas")
