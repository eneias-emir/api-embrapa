import requests
import os
from api_embrapa.appconfig import AppConfig


def url_to_csv_filename(url: str) -> str:
    return AppConfig.PATH_DATA + url.rsplit("/", 1)[1]


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
    result = {
        "Atividade": record[3],
        "Tipo": record[5],
        "Grupo": record[6],
        "Codigo": record[7],
        "Produto": record[8],
        "Ano": record[9],
        "Qtde": record[10],
    }

    # importacao e exportacao tem a coluna valor
    if record[2] == "opt_05" or record[2] == "opt_06":
        result["Valor"] = record[11]

    return result


def get_retorno_padrao_api(dados: list) -> dict:
    lista = []
    for record in dados:
        lista.append(get_dict_retorno_api(record))

    result = {"data": lista}

    return result
