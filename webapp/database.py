import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, configure_mappers

# URL do banco de dados SQLite
engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})

if os.environ.get('DB_TYPE') == 'others':
    engine = create_engine(os.environ.get('DB_URL'))

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
