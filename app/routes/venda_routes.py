from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.venda_model import Venda
from app.models.produto_model import ProdutoModel
from app.models.item_venda_model import ItemVenda
from app.schemas.venda_schema import VendaCreate, VendaResponse

router = APIRouter()


# 📌 Criar nova venda
# 📌 Criar nova venda
@router.post("/", response_model=VendaResponse, status_code=201)
def criar_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    if not venda.itens:
        raise HTTPException(status_code=400, detail="Nenhum produto informado")

    total_calculado = 0
    for item in venda.itens:
        produto = db.query(ProdutoModel).filter(ProdutoModel.id == item.produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto ID {item.produto_id} não encontrado")
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

    # ✅ Adiciona os itens da venda na tabela itens_venda
    for item in venda.itens:
        novo_item = ItemVenda(
            produto_id=item.produto_id,
            venda_id=nova_venda.id,
            quantidade=item.quantidade
        )
        db.add(novo_item)

    db.commit()

    return VendaResponse(
        id=nova_venda.id,
        produto_id=None,
        quantidade=None,
        valor_total=nova_venda.valor_total,
        cliente_nome=nova_venda.cliente_nome,
        cliente_cpf=nova_venda.cliente_cpf,
        cliente_endereco=nova_venda.cliente_endereco,
        forma_pagamento=nova_venda.forma_pagamento,
        criado_em=nova_venda.criado_em,
        produto_nome="Múltiplos produtos"
    )



# 📌 Resumo geral das vendas
from collections import Counter

@router.get("/resumo")
def resumo_vendas(db: Session = Depends(get_db)):
    try:
        vendas = db.query(Venda).all()

        # 💡 Resumo
        total_arrecadado = sum(v.valor_total for v in vendas)
        total_vendas = len(vendas)

        formas_pagamento = [v.forma_pagamento for v in vendas]
        forma_mais_usada = Counter(formas_pagamento).most_common(1)
        forma_mais_usada = forma_mais_usada[0][0] if forma_mais_usada else None

        # 💡 Vendas resumidas
        vendas_resumo = [
    {
        "cliente": v.cliente_nome,
        "produto": "Múltiplos produtos",
        "valor": v.valor_total,
        "forma_pagamento": v.forma_pagamento,
        "data": v.criado_em.strftime("%d/%m/%Y %H:%M")
    } for v in vendas
]


        return {
            "total_vendas": float(total_arrecadado or 0),
            "quantidade_total": int(total_vendas or 0),
            "forma_pagamento_mais_usada": forma_mais_usada or "-",
            "vendas": vendas_resumo or []
        }

    except Exception as e:
        print("⚠️ ERRO NA ROTA /resumo:", e)
        raise HTTPException(status_code=500, detail=str(e))


# 📌 Histórico completo com detalhes por item
@router.get("/historico", response_model=list[VendaResponse])
def listar_historico(db: Session = Depends(get_db)):
    vendas = db.query(Venda).all()

    resposta = []
    for venda in vendas:
        for item in venda.itens:
            produto = db.query(ProdutoModel).filter(ProdutoModel.id == item.produto_id).first()
            resposta.append(
                VendaResponse(
                    id=venda.id,
                    produto_id=item.produto_id,
                    quantidade=item.quantidade,
                    valor_total=venda.valor_total,
                    cliente_nome=venda.cliente_nome,
                    cliente_cpf=venda.cliente_cpf,
                    cliente_endereco=venda.cliente_endereco,
                    forma_pagamento=venda.forma_pagamento,
                    criado_em=venda.criado_em,
                    produto_nome=produto.nome if produto else "Produto não encontrado"
                )
            )
    return resposta
