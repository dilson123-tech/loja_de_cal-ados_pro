from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    valor_total = Column(Float)
    cliente_nome = Column(String)
    cliente_cpf = Column(String)
    cliente_endereco = Column(String)
    forma_pagamento = Column(String)
    criado_em = Column(DateTime, default=datetime.utcnow)

    itens = relationship("ItemVenda", back_populates="venda")  # 👈 em string
