from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# ✅ IMPORTAÇÕES DO BANCO E MODELOS
from app.database.session import engine, Base
from app.models.produto_model import ProdutoModel
from app.models.venda_model import Venda
from app.models.item_venda_model import ItemVenda

# ✅ CRIA AS TABELAS DEPOIS DE TODOS OS MODELOS ESTAREM IMPORTADOS
Base.metadata.create_all(bind=engine)

# ✅ CRIAÇÃO DA API
app = FastAPI(
    title="Sistema de Controle - Loja de Calçados",
    description="API para gerenciamento de produtos da loja física",
    version="1.0.0"
)

# ✅ ROTAS
from app.routes.produto_routes import router as produto_router
from app.routes.venda_routes import router as venda_router

app.include_router(produto_router, prefix="/api", tags=["Produtos"])
app.include_router(venda_router, prefix="/api/vendas", tags=["Vendas"])

# ✅ ROTA PRINCIPAL
@app.get("/")
def read_root():
    return {"mensagem": "API da Loja de Calçados rodando com sucesso!"}

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FRONTEND (estático)
app.mount(
    "/frontend",
    StaticFiles(directory=Path(__file__).parent.parent / "frontend"),
    name="frontend"
)

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent / "frontend/static"),
    name="static"
)
