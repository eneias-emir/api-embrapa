from typing import Union
from fastapi import FastAPI

from ScrapingEmbrapa import ScrapingEmbrapa

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/lista_urls_csv")
def read_lista_urls_csv():
    scraping_embrapa = ScrapingEmbrapa()
    lista = scraping_embrapa.get_lista_url_csv()

    return lista


@app.get("/lista_producao")
def get_lista_producao():
    return {"lista": "produção"}


@app.get("/lista_processamento")
def get_lista_processamento():
    return {"lista": "processamento"}


@app.get("/lista_comercializacao")
def get_lista_comercializacao():
    return {"lista": "comercialização"}


@app.get("/lista_importacao")
def get_lista_importacao():
    return {"lista": "importação"}


@app.get("/lista_exportacao")
def get_lista_exportacao():
    return {"lista": "exportação"}
