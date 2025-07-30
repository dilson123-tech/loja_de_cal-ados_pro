from fastapi import FastAPI
from app import database, models  # ✅ isso aqui está ok agora
from app.routes.produto_routes import router as produto_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.venda_routes import router as venda_router



from app.database.session import engine
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sistema de Controle - Loja de Calçados",
    description="API para gerenciamento de produtos da loja física",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mensagem": "API da Loja de Calçados rodando com sucesso!"}

app.include_router(produto_router, prefix="/api", tags=["Produtos"])
app.include_router(venda_router, prefix="/api/vendas", tags=["Vendas"])



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://127.0.0.1:5500"] se quiser restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
