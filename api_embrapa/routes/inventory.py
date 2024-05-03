from fastapi import APIRouter, Request

from api_embrapa.scrapping import ScrapingEmbrapa
from api_embrapa.database import db
from api_embrapa.utils import get_retorno_padrao_api

router = APIRouter(prefix="/inventory")


@router.get("/")
def root(request: Request):
    endpoints = [
        f"{request.url}{endpoint}"
        for endpoint in [
            "production",
            "processing",
            "comercialization",
            "imports",
            "exports",
            "all",
        ]
    ]
    return {
        "name": "API Embrapa",
        "description": "Banco de dados de uva, vinho e derivados - Embrapa Uva e Vinho",
        "endpoints": endpoints,
    }


@router.get("/all_csvs")
def all_csvs():
    scraping_embrapa = ScrapingEmbrapa()
    lista = scraping_embrapa.get_lista_url_csv()

    return lista


@router.get("/production")
def production():
    dados = db.consultar(opt="opt_02")

    result = get_retorno_padrao_api(dados)

    return result


@router.get("/processing")
def processing():
    dados = db.consultar(opt="opt_03")
    result = get_retorno_padrao_api(dados)

    return result


@router.get("/comercialization")
def comercialization():
    dados = db.consultar(opt="opt_04")
    result = get_retorno_padrao_api(dados)

    return result


@router.get("/imports")
def imports():
    dados = db.consultar(opt="opt_05")
    result = get_retorno_padrao_api(dados)

    return result


@router.get("/exports")
def exports():
    dados = db.consultar(opt="opt_06")
    result = get_retorno_padrao_api(dados)

    return result
