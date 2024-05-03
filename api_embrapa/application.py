from contextlib import asynccontextmanager
from starlette.background import BackgroundTasks
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api_embrapa.appconfig import AppConfig
from api_embrapa.routes import inventory
from api_embrapa.scrapping import ScrapingEmbrapa
from api_embrapa.utils import download_csv, database_file_exists
from api_embrapa.LoadData import LoadData


def atualizar_dados() -> None:
    print("Executando atualização de dados...")
    scraping_embrapa = ScrapingEmbrapa()
    lista = scraping_embrapa.get_lista_url_csv()
    # f = open('./lista_csv.json')
    # lista = json.load(f)

    for obj_url in lista:
        print("obj_url:", obj_url["url"])
        download_csv(obj_url["url"])

    load = LoadData()
    load.load_csv_to_database(lista)

    print(" atualização de dados concluída.")


@asynccontextmanager
async def startup_event(app: FastAPI):
    print("Executando rotinas de inicialização...")
    if not database_file_exists():
        background_tasks = BackgroundTasks()
        background_tasks.add_task(atualizar_dados)
        await background_tasks()

    yield


def add_middleware(app: FastAPI) -> None:
    """Add FastAPI middlewares to the main application.

    :param app: The FastAPI instance used.
    """
    app.add_middleware(
        SessionMiddleware,
        secret_key=AppConfig.API_EMBRAPRA_SESSION_SECRET_KEY,
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _create_app() -> FastAPI:
    """Create the initial FastAPI application."""
    app = FastAPI(lifespan=startup_event)

    app.include_router(router=inventory.router, prefix="/api/v1")

    add_middleware(app)

    return app


def start_api():
    config = uvicorn.Config(
        _create_app(),
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
    server = uvicorn.Server(config)
    server.run()
