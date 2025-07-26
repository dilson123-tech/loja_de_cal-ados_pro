from fastapi import FastAPI
from app import models, database
from app.controllers import router as produto_router

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=database.engine)

# Instância principal da aplicação
app = FastAPI(
    title="Sistema de Controle - Loja de Calçados",
    description="API para gerenciamento de produtos da loja física",
    version="1.0.0"
)

# Rota de teste inicial (opcional)
@app.get("/")
def read_root():
    return {"mensagem": "API da Loja de Calçados rodando com sucesso!"}

# Inclui as rotas do sistema
app.include_router(produto_router, prefix="/api", tags=["Produtos"])
