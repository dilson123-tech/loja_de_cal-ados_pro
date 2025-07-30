from sqlalchemy.orm import Session
from app.models.venda_model import Venda
from app.models.produto_model import Produto
from app.schemas.venda_schema import VendaCreate
from fastapi import HTTPException

def registrar_venda(db: Session, venda_data: VendaCreate):
    produto = db.query(Produto).filter(Produto.id == venda_data.produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    if produto.quantidade < venda_data.quantidade_vendida:
        raise HTTPException(status_code=400, detail="Quantidade em estoque insuficiente.")

    valor_total = produto.preco * venda_data.quantidade_vendida

    nova_venda = Venda(
        produto_id=venda_data.produto_id,
        quantidade_vendida=venda_data.quantidade_vendida,
        valor_total=valor_total
    )

    produto.quantidade -= venda_data.quantidade_vendida  # Atualiza o estoque

    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)

    return nova_venda
