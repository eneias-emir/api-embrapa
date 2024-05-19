from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from webapp.database import Base, engine, get_db
from webapp.api import router
from webapp.scrapping import import_csv_to_base

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/api/importar-csv")
def importar_csv(db: Session = Depends(get_db)):
    """
    Importar CSV para o Banco de Dados

    Esta função faz o scraping dos dados do site da Embrapa e importa esses dados para o banco de dados.

    Args:
    - db (Session): Sessão do banco de dados obtida através do Depends(get_db).

    Returns:
    - dict: Resultado da importação dos dados.
    """
    return import_csv_to_base(db)

# Registro das rotas
app.include_router(router)
