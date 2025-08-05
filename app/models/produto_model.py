from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    itens = relationship("ItemVenda", back_populates="produto")  # 👈 em string, sem importar direto
