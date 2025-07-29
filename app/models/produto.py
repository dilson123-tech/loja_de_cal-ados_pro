# app/models/produto_model.py

from sqlalchemy import Column, Integer, String, Float
from app.database import Base




class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, default=0)
