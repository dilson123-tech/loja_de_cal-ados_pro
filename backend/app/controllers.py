from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()

@router.post("/produtos", response_model=schemas.ProdutoOut)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(database.get_db)):
    db_produto = models.Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.get("/produtos", response_model=list[schemas.ProdutoOut])
def listar_produtos(db: Session = Depends(database.get_db)):
    return db.query(models.Produto).all()

@router.get("/produtos/{produto_id}", response_model=schemas.ProdutoOut)
def buscar_produto(produto_id: int, db: Session = Depends(database.get_db)):
    produto = db.query(models.Produto).get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(database.get_db)):
    produto = db.query(models.Produto).get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"msg": "Produto deletado com sucesso"}
