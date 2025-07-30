from sqlalchemy.orm import Session
from app.models.produto_model import Produto
from app.schemas.produto_schema import ProdutoCreate

# 🔨 Criar produto
def criar_produto(db: Session, produto_data: ProdutoCreate):
    novo_produto = Produto(**produto_data.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

# 📦 Listar todos os produtos
def listar_produtos(db: Session):
    return db.query(Produto).all()

# 🔍 Buscar produto por ID
def buscar_produto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()

# 🛠️ Atualizar produto
def atualizar_produto(db: Session, produto_id: int, produto_data: ProdutoCreate):
    produto = buscar_produto(db, produto_id)
    if produto:
        for key, value in produto_data.dict().items():
            setattr(produto, key, value)
        db.commit()
        db.refresh(produto)
    return produto

# ❌ Deletar produto
def deletar_produto(db: Session, produto_id: int):
    produto = buscar_produto(db, produto_id)
    if produto:
        db.delete(produto)
        db.commit()
    return produto
