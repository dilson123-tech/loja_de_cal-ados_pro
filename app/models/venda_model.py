# app/models/venda_model.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade_vendida = Column(Integer)
    valor_total = Column(Float)
    data_venda = Column(DateTime, default=datetime.utcnow)

    produto = relationship("Produto")
