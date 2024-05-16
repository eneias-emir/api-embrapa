from io import StringIO
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from sqlalchemy import inspect

from webapp.database_config import engine
from unidecode import unidecode
from sqlalchemy.orm import Session
import logging
import ftfy

# Configure the logging module
logging.basicConfig(level=logging.INFO)

PATH: str = 'http://vitibrasil.cnpuv.embrapa.br/index.php'


def setup_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--headless --no-sandbox --disable-dev-shm-usage --start-maximized --disable-infobars --disable-extensions '
        '--incognito --disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

    return driver


def get_button_list_by_class(driver: webdriver.Chrome, class_name: str) -> list:
    return [(btn.get_attribute('value'), btn.text) for btn in driver.find_elements(By.CLASS_NAME, class_name)]


def add_csv_item(option: str, sub_option: str, option_desc: str, sub_option_desc: str,
                 driver: webdriver.Chrome, csv_list: list) -> None:
    csv_list.extend({"opt": option, "subopt": sub_option, "desc_opt": option_desc, "desc_subopt": sub_option_desc,
                     "url": href.get_attribute('href')}
                    for href in driver.find_elements(By.LINK_TEXT, "DOWNLOAD") if
                    '.csv' in href.get_attribute('href').lower())


def get_csv_link(driver: webdriver.Chrome) -> str:
    return next((href.get_attribute('href') for href in driver.find_elements(By.LINK_TEXT, "DOWNLOAD") if
                 href and '.csv' in href.get_attribute('href').lower()), "")


def navigate_to_url_and_get_buttons(driver, url):
    logging.info(f'Selenium: Navegando para url {url}... ')
    driver.get(url)
    logging.info(f'Selenium: Obtendo títulos dos botões de menu principal do {url}... ')
    return get_button_list_by_class(driver, 'btn_opt')


def get_csv_url_list(db: Session):
    csv_url_list = []
    logging.info('Selenium: Iniciando webdriver(Chrome)... ')
    driver = setup_driver()
    for value_opt, txt_opt in navigate_to_url_and_get_buttons(driver, PATH):
        if txt_opt not in ['Apresentação', 'Publicação']:
            driver.get(f'{PATH}?opcao={value_opt}')
            btn_sub_options = get_button_list_by_class(driver, 'btn_sopt')
            if not btn_sub_options:
                logging.info(f'SqlAlchemy: Carrega report {txt_opt}... ')
                logging.info(f'Selenium: obtendo link do csv do {txt_opt}...')
                link = get_csv_link(driver)
                import_csv(link, txt_opt, None)
            else:
                for subopt, txt in btn_sub_options:
                    driver.get(f'{PATH}?opcao={value_opt}&subopcao={subopt}')
                    logging.info(f'Selenium: Obtendo link de {txt_opt}, subreport de {txt}...')
                    link = get_csv_link(driver)
                    import_csv(link, txt_opt, txt)

    return csv_url_list


def import_csv(link: str, table_name: str, categoria: str):
    texto_processado = unidecode(table_name).lower()
    logging.info(f"Request: Baixando dados da tabela {texto_processado}, categoria {categoria}, de {link}...")

    response = requests.get(link)
    # Verifica se a resposta foi bem-sucedida
    if response.status_code == 200:
        inspector = inspect(engine)
        table_exists = inspector.has_table(texto_processado)

        # Cria um objeto StringIO para carregar os dados em memória
        csv_data = StringIO(ftfy.fix_text(response.text.replace('\t', ';')))
        # Carrega o CSV em um DataFrame
        logging.info(f'Pandas: Carregando csv... ')
        df = pd.read_csv(csv_data, delimiter=';', encoding='utf-8')
        df = unir_e_somar_colunas_duplicadas(df)
        str_columns = [unidecode(name_column).lower() for name_column in df.columns if not name_column.isnumeric()]
        df.rename(columns=dict(zip(df.columns, str_columns)), inplace=True)
        logging.info(f'Pandas: Ajustando colunas str_columns {str_columns}... ')
        df = df.melt(id_vars=str_columns, var_name='ano', value_name='qtd')
        df = df.assign(categoria=categoria)
        # Defina a chave composta como o índice do DataFrame
        df.set_index(['id', 'ano', 'qtd', 'categoria'], inplace=True)
        # Remova a definição do índice
        df.to_sql(texto_processado, con=engine, if_exists='append')
        logging.info(f'SqlAchemy: Encerrando Conexão com banco... ')
        # Fecha a conexão com o banco de dados
        engine.dispose()


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

