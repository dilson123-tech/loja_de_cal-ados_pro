# create_db.py

from app.database.session import engine, Base
from app.models import produto_model, venda_model, item_venda_model

print("🔨 Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")
