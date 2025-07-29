from fastapi import FastAPI
from app import database, models  # ✅ isso aqui está ok agora
from app.routes.produto_routes import router as produto_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Sistema de Controle - Loja de Calçados",
    description="API para gerenciamento de produtos da loja física",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mensagem": "API da Loja de Calçados rodando com sucesso!"}

app.include_router(produto_router, prefix="/api", tags=["Produtos"])
