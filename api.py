from typing import Union
from fastapi import FastAPI
from Database import Database
import json

from ScrapingEmbrapa import ScrapingEmbrapa
from utils import download_csv
from LoadData import LoadData

app = FastAPI()
db = Database()

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


@app.get("/atualizar_dados")
def atualizar_dados():
    scraping_embrapa = ScrapingEmbrapa()
    lista = scraping_embrapa.get_lista_url_csv()
    #lista = json.loads('[{"opt":"opt_02","subopt":"","desc_opt":"Produção","desc_subopt":"","url":"http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"},{"opt":"opt_03","subopt":"subopt_01","desc_opt":"Processamento","desc_subopt":"Viníferas","url":"http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"},{"opt":"opt_03","subopt":"subopt_02","desc_opt":"Processamento","desc_subopt":"Americanas e híbridas","url":"http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv"},{"opt":"opt_03","subopt":"subopt_03","desc_opt":"Processamento","desc_subopt":"Uvas de mesa","url":"http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv"},{"opt":"opt_03","subopt":"subopt_04","desc_opt":"Processamento","desc_subopt":"Sem classificação","url":"http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv"},{"opt":"opt_04","subopt":"","desc_opt":"Comercialização","desc_subopt":"","url":"http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"},{"opt":"opt_05","subopt":"subopt_01","desc_opt":"Importação","desc_subopt":"Vinhos de mesa","url":"http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv"},{"opt":"opt_05","subopt":"subopt_02","desc_opt":"Importação","desc_subopt":"Espumantes","url":"http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv"},{"opt":"opt_05","subopt":"subopt_03","desc_opt":"Importação","desc_subopt":"Uvas frescas","url":"http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv"},{"opt":"opt_05","subopt":"subopt_04","desc_opt":"Importação","desc_subopt":"Uvas passas","url":"http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv"},{"opt":"opt_05","subopt":"subopt_05","desc_opt":"Importação","desc_subopt":"Suco de uva","url":"http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv"},{"opt":"opt_06","subopt":"subopt_01","desc_opt":"Exportação","desc_subopt":"Vinhos de mesa","url":"http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"},{"opt":"opt_06","subopt":"subopt_02","desc_opt":"Exportação","desc_subopt":"Espumantes","url":"http://vitibrasil.cnpuv.embrapa.br/download/ExpEspumantes.csv"},{"opt":"opt_06","subopt":"subopt_03","desc_opt":"Exportação","desc_subopt":"Uvas frescas","url":"http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv"},{"opt":"opt_06","subopt":"subopt_04","desc_opt":"Exportação","desc_subopt":"Suco de uva","url":"http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv"}]')

    for obj_url in lista:
        print("obj_url:", obj_url["url"])
        download_csv(obj_url["url"])

    load = LoadData()
    load.load_csv_to_database(lista)

    return lista

@app.get("/lista_producao")
def get_lista_producao():
    return db.consultar(opt='opt_02')


@app.get("/lista_processamento")
def get_lista_processamento():
    return db.consultar(opt='opt_03')


@app.get("/lista_comercializacao")
def get_lista_comercializacao():
    return db.consultar(opt='opt_04')


@app.get("/lista_importacao")
def get_lista_importacao():
    return db.consultar(opt='opt_05')


@app.get("/lista_exportacao")
def get_lista_exportacao():
    return db.consultar(opt='opt_06')
