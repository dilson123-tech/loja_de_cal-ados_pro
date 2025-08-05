from sqlalchemy.orm import Session
from app.models.venda_model import Venda
from app.models.produto_model import Produto
from app.schemas.venda_schema import VendaCreate
from fastapi import HTTPException

def registrar_venda(db: Session, venda_data: VendaCreate):
    produto = db.query(Produto).filter(Produto.id == venda_data.produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    if produto.quantidade < venda_data.quantidade:
        raise HTTPException(status_code=400, detail="Quantidade em estoque insuficiente.")
    
    valor_total = produto.preco * venda_data.quantidade

    nova_venda = Venda(
        produto_id=venda_data.produto_id,
        quantidade=venda_data.quantidade,
        valor_total=valor_total,
        cliente_nome=venda_data.cliente_nome,
        cliente_cpf=venda_data.cliente_cpf,
        cliente_endereco=venda_data.cliente_endereco,
        forma_pagamento=venda_data.forma_pagamento,
    )

    produto.quantidade -= venda_data.quantidade

    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)

    return nova_venda
