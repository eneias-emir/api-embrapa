from fastapi import FastAPI

from app.database_config import Base, engine
from app.report import report_api
from app.report_item import report_item_api
from app.producao import producao_api

app = FastAPI()
#asyncio.run(create_db())
Base.metadata.create_all(bind=engine)
# Registro das rotas
app.include_router(report_api.router)
app.include_router(report_item_api.router)
app.include_router(producao_api.router)


