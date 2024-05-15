import requests
import os
from api_embrapa.appconfig import AppConfig
from api_embrapa.embrapa_csv_params import EmbrapaCsvParams
from api_embrapa.model_resp_api import (
    RespApi,
    RespApiImportacaoExportacao,
    ItensRespApi,
)


def url_to_csv_filename(url: str) -> str:
    path = AppConfig.PATH_DATA
    if path[-1] != "/":
        path = path + "/"

    return path + url.rsplit("/", 1)[1]


def download_csv(url: str) -> None:
    file_name = url_to_csv_filename(url)
    print(url)
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the content of the response to a local CSV file
        with open(file_name, "wb") as f:
            f.write(response.content)
        print("CSV file downloaded successfully")
    else:
        print("Failed to download CSV file. Status code:", response.status_code)


def database_file_exists() -> bool:
    db_file_name = AppConfig.DATABASE_NAME + AppConfig.DATABASE_EXTENSION
    working_dir = AppConfig.PATH_DATA
    db_file = os.path.join(working_dir, db_file_name)
    if not os.path.exists(db_file):
        return False
    else:
        return True


def get_dict_retorno_api(record: list) -> dict:
    if (
        record[2] == EmbrapaCsvParams.OPT_IMPORTACAO
        or record[2] == EmbrapaCsvParams.OPT_EXPORTACAO
    ):
        resp = RespApiImportacaoExportacao(
            atividade=record[3], tipo=record[5], pais=record[8], itens=[]
        )
    else:
        resp = RespApi(
            atividade=record[3],
            grupo=record[6],
            codigo=record[7],
            produto=record[8],
            itens=[],
        )

        if record[5] != "":
            resp.tipo = record[5]

    for item in record[9]:
        reg = ItensRespApi(ano=int(item[0]), qtde=0)
        if item[1] != "":
            reg.qtde = int(item[1])

        # importacao e exportacao tem a coluna valor
        if (
            record[2] == EmbrapaCsvParams.OPT_IMPORTACAO
            or record[2] == EmbrapaCsvParams.OPT_EXPORTACAO
        ):
            if item[2] != "":
                reg.valor = item[2]
            else:
                reg.valor = 0
        else:
            reg.valor = None

        resp.itens.append(reg)

    return resp


def get_retorno_padrao_api(dados: list) -> dict:
    lista = []
    for record in dados:
        lista.append(get_dict_retorno_api(record))

    # result = {"data": lista}
    result = lista

    return result
