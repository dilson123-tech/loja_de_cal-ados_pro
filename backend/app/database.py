from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexão com banco SQLite local
DATABASE_URL = "sqlite:///./loja.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Essa função é o que estava faltando
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
