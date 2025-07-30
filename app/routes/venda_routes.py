from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.controllers.venda_controller import registrar_venda
from app.schemas.venda_schema import VendaCreate, VendaResponse
from app import models
from datetime import datetime

router = APIRouter(tags=["Vendas"])


@router.get("/resumo")
def resumo_vendas(db: Session = Depends(get_db)):
    vendas = db.query(models.Venda).all()
    total_vendas = len(vendas)
    total_arrecadado = sum(v.valor for v in vendas)

    resumo = {
        "total_vendas": total_vendas,
        "total_arrecadado": total_arrecadado,
        "vendas": [
            {
                "id": v.id,
                "produto": v.nome_produto,
                "valor": v.valor,
                "data": v.data_venda.strftime("%d/%m/%Y %H:%M:%S")
            }
            for v in vendas
        ]
    }
    return resumo

@router.post("/", response_model=VendaResponse, status_code=201)
def criar_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    return registrar_venda(db, venda)
