from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.produto_schema import ProdutoCreate, ProdutoOut, MensagemResponse
from app.services import produto_service  # 🔥 novo import

router = APIRouter()

# 📌 Criar produto
@router.post("/produtos", response_model=ProdutoOut, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return produto_service.criar_produto(db, produto)

# 📌 Listar produtos
@router.get("/produtos", response_model=list[ProdutoOut])
def listar_produtos(db: Session = Depends(get_db)):
    return produto_service.listar_produtos(db)

# 📌 Buscar por ID
@router.get("/produtos/{produto_id}", response_model=ProdutoOut)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = produto_service.buscar_produto(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# 📌 Atualizar
@router.put("/produtos/{produto_id}", response_model=ProdutoOut)
def atualizar_produto(produto_id: int, produto: ProdutoCreate, db: Session = Depends(get_db)):
    produto_atualizado = produto_service.atualizar_produto(db, produto_id, produto)
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="Produto não encontrado para atualizar")
    return produto_atualizado

# 📌 Deletar
@router.delete("/produtos/{produto_id}", response_model=MensagemResponse)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto_deletado = produto_service.deletar_produto(db, produto_id)
    if not produto_deletado:
        raise HTTPException(status_code=404, detail="Produto não encontrado para deletar")
    
    return {"mensagem": "Produto deletado com sucesso!"}



