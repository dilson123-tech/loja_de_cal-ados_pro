from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.produto_model import ProdutoModel as Produto
from app.models.venda_model import Venda
from app.schemas.venda_schema import VendaCreate, VendaResponse
from app import models

router = APIRouter()  # ✅ ESSA LINHA TEM QUE EXISTIR e vir aqui



@router.get("/resumo")
def resumo_vendas(db: Session = Depends(get_db)):
    vendas = db.query(models.Venda).all()
    total_vendas = len(vendas)
    total_arrecadado = sum(v.valor_total for v in vendas)

    resumo = {
        "total_vendas": total_vendas,
        "total_arrecadado": total_arrecadado,
        "vendas": [
            {
                "id": v.id,
                "produto": v.produto.nome if v.produto else "Desconhecido",
                "valor": v.valor_total,
                "data": v.criado_em.strftime("%d/%m/%Y %H:%M")
            }
            for v in vendas
        ]
    }
    return resumo

@router.post("/", response_model=VendaResponse, status_code=201)
def criar_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    if not venda.itens:
        raise HTTPException(status_code=400, detail="Nenhum produto informado")

    total_calculado = 0

    for item in venda.itens:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if not produto:
            raise HTTPException(
                status_code=404,
                detail=f"Produto ID {item.produto_id} não encontrado"
            )
        total_calculado += produto.preco * item.quantidade

    nova_venda = Venda(
    cliente_nome=venda.cliente.nome,
    cliente_cpf=venda.cliente.cpf,
    cliente_endereco=venda.cliente.endereco,
    forma_pagamento=venda.pagamento.forma,
    valor_total=total_calculado
)


    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)

    return VendaResponse(
        id=nova_venda.id,
        produto_id=None,  # Se não usa mais, remova do schema
        quantidade=None,  # Se não usa mais, remova do schema
        valor_total=nova_venda.valor_total,
        cliente_nome=nova_venda.cliente_nome,
        cliente_cpf=nova_venda.cliente_cpf,
        cliente_endereco=nova_venda.cliente_endereco,
        forma_pagamento=nova_venda.forma_pagamento,
        criado_em=nova_venda.criado_em,
        produto_nome="Múltiplos produtos"
    )

