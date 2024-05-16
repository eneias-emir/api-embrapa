from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from webapp.database_config import Base, engine, get_db

from webapp.producao import producao_api
from webapp.scraping_embrapa_service import get_csv_url_list

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/api/sync/importar")
def importar_producao_csv(db: Session = Depends(get_db)):
    return get_csv_url_list(db)

# Registro das rotas
app.include_router(producao_api.router)
