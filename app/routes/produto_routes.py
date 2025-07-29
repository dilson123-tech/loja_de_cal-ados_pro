from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ProdutoCreate
from app.controllers import produto_controller
from app.database import get_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# Rota para criar um novo produto
@router.post("/", response_model=ProdutoCreate)
def criar(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return produto_controller.criar_produto(db, produto)

# Rota para listar todos os produtos
@router.get("/", response_model=list[ProdutoCreate])
def listar(db: Session = Depends(get_db)):
    return produto_controller.listar_produtos(db)

# Rota para buscar produto por ID
@router.get("/{produto_id}", response_model=ProdutoCreate)
def buscar(produto_id: int, db: Session = Depends(get_db)):
    produto = produto_controller.buscar_produto(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# Rota para atualizar produto
@router.put("/{produto_id}", response_model=ProdutoCreate)
def atualizar(produto_id: int, dados: ProdutoCreate, db: Session = Depends(get_db)):
    produto = produto_controller.atualizar_produto(db, produto_id, dados)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# Rota para deletar produto
@router.delete("/{produto_id}")
def deletar(produto_id: int, db: Session = Depends(get_db)):
    produto = produto_controller.deletar_produto(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"mensagem": "Produto deletado com sucesso"}
