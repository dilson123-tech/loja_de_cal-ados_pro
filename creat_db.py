from app.database import engine
from app.models import Produto, Venda
from app.models import Base



print("Criando o banco de dados...")
Base.metadata.create_all(bind=engine)
print("Banco criado com sucesso!")



