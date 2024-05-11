import requests
import os
from api_embrapa.appconfig import AppConfig
from api_embrapa.embrapa_csv_params import EmbrapaCsvParams


def url_to_csv_filename(url: str) -> str:
    path = AppConfig.PATH_DATA
    if path[-1] != '/':
        path = path + '/'

    return path + url.rsplit("/", 1)[1]

def download_csv(url: str) -> None:
    file_name = url_to_csv_filename(url)

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
    #print(record)
    result = {
        "atividade": record[3],
        "tipo": record[5],
        "grupo": record[6],
        "codigo": record[7],
        "produto": record[8],
        "itens": []
    }

    for item in record[9]:
        reg = {"ano": item[0], "qtde": item[1]}
        # importacao e exportacao tem a coluna valor
        if record[2] == EmbrapaCsvParams.OPT_IMPORTACAO or record[2] == EmbrapaCsvParams.OPT_EXPORTACAO:
            reg["Valor"] = item[2]

        result["itens"].append(reg)


    return result


def get_retorno_padrao_api(dados: list) -> dict:
    lista = []
    for record in dados:
        lista.append(get_dict_retorno_api(record))

    # result = {"data": lista}
    result = lista

    return result
