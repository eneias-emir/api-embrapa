from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, configure_mappers

# URL do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# URL do banco de dados PostgreSQL (exemplo)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Criando a engine do SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Criando uma sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarando uma base para os modelos
Base = declarative_base()

# Configurando mapeamentos
configure_mappers()

def get_db():
    """
    Função para retornar uma instância de sessão do banco de dados.

    Returns:
        Session: Instância de sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
