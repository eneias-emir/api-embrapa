from starlette.background import BackgroundTasks
from fastapi import FastAPI, Request
from Database import Database


import json

from ScrapingEmbrapa import ScrapingEmbrapa
from utils import download_csv, database_file_exists
from LoadData import LoadData

app = FastAPI()
db = Database()

def get_dict_retorno_api(record: list) -> dict:
    result = {"Atividade": record[3],
             "Tipo": record[5],
             "Grupo": record[6],
             "Codigo": record[7],
             "Produto": record[8],
             "Ano": record[9],
             "Qtde": record[10]
             }

    # importacao e exportacao tem a coluna valor
    if record[2] == 'opt_05' or record[2] == 'opt_06':
        result["Valor"] = record[11]

    return result

def get_retorno_padrao_api(dados: list) -> dict:
    lista = []
    for record in dados:
        lista.append(get_dict_retorno_api(record))

    result = {"data": lista}

    return result

def atualizar_dados() -> None:
    print('Executando atualização de dados...')
    scraping_embrapa = ScrapingEmbrapa()
    lista = scraping_embrapa.get_lista_url_csv()
    
    # f = open('./lista_csv.json')
    # lista = json.load(f)

    for obj_url in lista:
        print("obj_url:", obj_url["url"])
        download_csv(obj_url["url"])

    load = LoadData()
    load.load_csv_to_database(lista)

    print(' atualização de dados concluída.')

@app.on_event("startup")
async def startup_event():
    print('Executando rotinas de inicialização...')
    if not database_file_exists():
        background_tasks = BackgroundTasks()
        background_tasks.add_task(atualizar_dados)
        await background_tasks()

@app.get("/")
def read_root(request: Request):
    return {"Descrição da API": "Banco de dados de uva, vinho e derivados - Embrapa Uva e Vinho",
            "Endpoints": [
                f'{request.url}lista_producao',
                f'{request.url}lista_processamento',
                f'{request.url}lista_comercializacao',
                f'{request.url}lista_importacao',
                f'{request.url}lista_exportacao'
            ]
            }

@app.get("/lista_urls_csv")
def read_lista_urls_csv():
    scraping_embrapa = ScrapingEmbrapa()
    lista = scraping_embrapa.get_lista_url_csv()

    return lista

@app.get("/lista_producao")
def get_lista_producao():
    dados = db.consultar(opt='opt_02')

    result = get_retorno_padrao_api(dados)

    return result


@app.get("/lista_processamento")
def get_lista_processamento():
    dados = db.consultar(opt='opt_03')
    result = get_retorno_padrao_api(dados)

    return result

@app.get("/lista_comercializacao")
def get_lista_comercializacao():
    dados = db.consultar(opt='opt_04')
    result = get_retorno_padrao_api(dados)

    return result


@app.get("/lista_importacao")
def get_lista_importacao():
    dados = db.consultar(opt='opt_05')
    result = get_retorno_padrao_api(dados)

    return result


@app.get("/lista_exportacao")
def get_lista_exportacao():
    dados = db.consultar(opt='opt_06')
    result = get_retorno_padrao_api(dados)

    return result
