from sqlalchemy.orm import Session
from app.models import Produto
from app.schemas import ProdutoCreate

# CRIAR um novo produto
def criar_produto(db: Session, produto: ProdutoCreate):
    novo_produto = Produto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

# LISTAR todos os produtos
def listar_produtos(db: Session):
    return db.query(Produto).all()

# BUSCAR produto por ID
def buscar_produto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()

# ATUALIZAR produto
def atualizar_produto(db: Session, produto_id: int, dados: ProdutoCreate):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        for key, value in dados.dict().items():
            setattr(produto, key, value)
        db.commit()
        db.refresh(produto)
    return produto

# DELETAR produto
def deletar_produto(db: Session, produto_id: int):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
    return produto
