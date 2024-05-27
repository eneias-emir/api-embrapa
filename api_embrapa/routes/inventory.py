from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer

from api_embrapa.scrapping import ScrapingEmbrapa
from api_embrapa.db.database_raw import db
from api_embrapa.utils import get_retorno_padrao_api
from api_embrapa.model_resp_api import (
    RespApi,
    RespApiImportacaoExportacao,
    ApiDescription,
    ItemCsvList,
)

from api_embrapa.embrapa_csv_params import EmbrapaCsvParams

router = APIRouter(prefix="/inventory", tags=['inventory'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_data(opt: str, year: int) -> list[RespApi]:
    dados = db.consultar(opt=opt, year=year)

    result = get_retorno_padrao_api(dados)

    return result



@router.get("/", response_model=ApiDescription)
def root(request: Request):
    endpoints = [
        f"{request.url}{endpoint}"
        for endpoint in [
            "production",
            "processing",
            "comercialization",
            "imports",
            "exports",
            "all_csvs",
        ]
    ]
    return {
        "name": "API Embrapa",
        "description": "Banco de dados de uva, vinho e derivados - Embrapa Uva e Vinho",
        "endpoints": endpoints,
    }


@router.get("/all_csvs", response_model=list[ItemCsvList])
def all_csvs(token: Annotated[str, Depends(oauth2_scheme)]):
    scraping_embrapa = ScrapingEmbrapa()
    lista = scraping_embrapa.get_lista_url_csv()

    return lista


@router.get("/production", response_model=list[RespApi])
def production(token: Annotated[str, Depends(oauth2_scheme)]):
    return get_data(opt=EmbrapaCsvParams.OPT_PRODUCAO, year=0)

@router.get("/production/{year}", response_model=list[RespApi])
def production(token: Annotated[str, Depends(oauth2_scheme)], year: int):
    return get_data(opt=EmbrapaCsvParams.OPT_PRODUCAO, year=year)


@router.get("/processing", response_model=list[RespApi])
def processing(token: Annotated[str, Depends(oauth2_scheme)]):
    return get_data(opt=EmbrapaCsvParams.OPT_PROCESSAMENTO, year=0)

@router.get("/processing/{year}", response_model=list[RespApi])
def processing(token: Annotated[str, Depends(oauth2_scheme)], year: int):
    return get_data(opt=EmbrapaCsvParams.OPT_PROCESSAMENTO, year=year)


@router.get("/comercialization", response_model=list[RespApi])
def comercialization(token: Annotated[str, Depends(oauth2_scheme)]):
    return get_data(opt=EmbrapaCsvParams.OPT_COMERCIALIZACAO, year=0)

@router.get("/comercialization/{year}", response_model=list[RespApi])
def comercialization(token: Annotated[str, Depends(oauth2_scheme)], year: int):
    return get_data(opt=EmbrapaCsvParams.OPT_COMERCIALIZACAO, year=year)


@router.get("/imports", response_model=list[RespApiImportacaoExportacao])
def imports(token: Annotated[str, Depends(oauth2_scheme)]):
    return get_data(opt=EmbrapaCsvParams.OPT_IMPORTACAO, year=0)

@router.get("/imports/{year}", response_model=list[RespApiImportacaoExportacao])
def imports(token: Annotated[str, Depends(oauth2_scheme)], year: int):
    return get_data(opt=EmbrapaCsvParams.OPT_IMPORTACAO, year=year)


@router.get("/exports", response_model=list[RespApiImportacaoExportacao])
def exports(token: Annotated[str, Depends(oauth2_scheme)]):
    return get_data(opt=EmbrapaCsvParams.OPT_EXPORTACAO, year=0)

@router.get("/exports/{year}", response_model=list[RespApiImportacaoExportacao])
def exports(token: Annotated[str, Depends(oauth2_scheme)], year: int):
    return get_data(opt=EmbrapaCsvParams.OPT_EXPORTACAO, year=year)

