from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    venda_id = Column(Integer, ForeignKey("vendas.id"))
    quantidade = Column(Integer, nullable=False)

    produto = relationship("ProdutoModel", back_populates="itens")
    venda = relationship("Venda", back_populates="itens")  # 👈 também em string
