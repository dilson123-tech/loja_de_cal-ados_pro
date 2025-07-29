from app.database import Base, engine
from app.models.app.models import Produto



print("Criando o banco de dados...")
Base.metadata.create_all(bind=engine)
print("Banco criado com sucesso!")
