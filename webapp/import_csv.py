import logging
from io import StringIO

import ftfy
import pandas as pd
import requests
from pandas import DataFrame
from requests.models import Response
from unidecode import unidecode

from webapp.database_config import engine

# Configure the logging module
logging.basicConfig(level=logging.INFO)


def import_csv(url: str, table_name: str, categoria: str):
    logging.info(f'Importando CSV: {url} para {table_name} (Categoria: {categoria})')
    table_name_processing = unidecode(table_name).lower()
    logging.info(f"Request: Baixando dados da tabela {table_name_processing}, categoria {categoria}, de {url}...")
    response = requests.get(url)
    # Verifica se a resposta foi bem-sucedida
    if response.status_code == 200:
        save_csv_in_database(response, table_name_processing, categoria)


def save_csv_in_database(response: Response, table_name_processing: str, categoria: str):
    # Carrega o CSV em um DataFrame
    df = created_csv_dataframe(response)
    # Cria uma coluna para categorizar o tipo do csv
    df = df.assign(categoria=categoria)
    # Defina a chave composta como o índice do DataFrame
    df.set_index(['id', 'ano', 'qtd', 'categoria'], inplace=True)
    # Salvando dados no banco
    df.to_sql(table_name_processing, con=engine, if_exists='append')
    logging.info(f'SqlAchemy: Encerrando Conexão com banco... ')
    # Fecha a conexão com o banco de dados
    engine.dispose()


def created_csv_dataframe(response: Response) -> DataFrame:
    logging.info(f'Pandas: Caregando e preparando dados para importação do csv... ')
    csv_data = StringIO(ftfy.fix_text(response.text.replace('\t', ';')))
    df = pd.read_csv(csv_data, delimiter=';', encoding='utf-8')
    df = unir_e_somar_colunas_duplicadas(df)
    return prepare_dataframe(df)


def prepare_dataframe(df: DataFrame):
    str_columns = [unidecode(name_column).lower() for name_column in df.columns if not name_column.isnumeric()]
    logging.info(f'Pandas: Renomenado colunas ... ')
    df.rename(columns=dict(zip(df.columns, str_columns)), inplace=True)
    logging.info(f'Pandas: alterando colunas do tipo int para convergir para coluna ano e qtd ... ')
    return df.melt(id_vars=str_columns, var_name='ano', value_name='qtd')


# Função para unir e somar colunas duplicadas
def unir_e_somar_colunas_duplicadas(df):
    colunas_unidas = {}
    for coluna in df.columns:
        coluna_sem_extensao = coluna.split('.')[0]  # Remover extensão ".1"
        if coluna_sem_extensao not in colunas_unidas:
            colunas_unidas[coluna_sem_extensao] = df[coluna]
        else:
            colunas_unidas[coluna_sem_extensao] += df[coluna]
    return pd.DataFrame(colunas_unidas)