from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from webapp.database import Base, engine, get_db
from webapp.api import router
from webapp.scrapping import import_csv_to_base

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/api/sync/importar")
def importar_producao_csv(db: Session = Depends(get_db)):
    return import_csv_to_base(db)


# Registro das rotas
app.include_router(router)
