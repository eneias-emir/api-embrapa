from io import StringIO
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy.orm import Session
import requests
from app.database_config import engine
from app.models.report import Report
from app.models.report_item import ReportItem
from app.report.repository import ReportRepository
from app.report.shema import ReportSchema
from app.report_item.repository import ReportItemRepository
from app.report_item.shema import ReportItemSchema
import logging

# Configure the logging module
logging.basicConfig(level=logging.INFO)

PATH: str = 'http://vitibrasil.cnpuv.embrapa.br/index.php'


def setup_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--headless --no-sandbox --disable-dev-shm-usage --start-maximized --disable-infobars --disable-extensions --incognito --disable-blink-features=AutomationControlled')
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
    logging.info(f'Selenium: obtendo link do botão de download...')
    return next((href.get_attribute('href') for href in driver.find_elements(By.LINK_TEXT, "DOWNLOAD") if
                 href and '.csv' in href.get_attribute('href').lower()), "")


def navigate_to_url_and_get_buttons(driver, url):
    logging.info(f'Selenium: Navegando para url {url}... ')
    driver.get(url)
    logging.info(f'Selenium: Obtendo títulos dos botões de menu principal do {url}... ')
    return get_button_list_by_class(driver, 'btn_opt')


def save_report_if_not_exists(db, txt_opt):
    logging.info(f'SqlAlchemy: Verificando se {txt_opt} já foi cadastrado no banco de dados... ')
    if not ReportRepository.exists_by_type(db, txt_opt):
        logging.info(f'SqlAlchemy: Salvando {txt_opt}... ')
        ReportRepository.save(db, Report(**ReportSchema(type=txt_opt,report_items=[]).dict()))


def save_report_item_if_not_exists(db, txt, txt_opt, r, driver):
    logging.info(f'SqlAlchemy: Verificando se {txt_opt} já foi cadastrado no banco de dados... ')
    if not ReportItemRepository.exists_by_type(db, txt):
        logging.info(f'SqlAlchemy: Carrega report {txt_opt}... ')
        link = get_csv_link(driver)
        logging.info(f'SqlAlchemy: Salvando report_item {txt}... ')
        ReportItemRepository.save(db, ReportItem(**ReportItemSchema(type=txt, url=link, report_id=r.id,producoes=[]).dict()))


def get_csv_url_list(db):
    csv_url_list = []
    logging.info('Selenium: Iniciando webdriver(Chrome)... ')
    driver = setup_driver()
    for value_opt, txt_opt in navigate_to_url_and_get_buttons(driver, PATH):
        driver.get(f'{PATH}?opcao={value_opt}')
        btn_sub_options = get_button_list_by_class(driver, 'btn_sopt')
        save_report_if_not_exists(db, txt_opt)
        if not btn_sub_options:
            logging.info(f'SqlAlchemy: Carrega report {txt_opt}... ')
            r = ReportRepository.find_by_type(db, txt_opt)
            if not ReportItemRepository.find_by_report_id(db, r.id):
                logging.info(f'SqlAlchemy: Salvando {txt_opt} Sem sub classificação... ')
                link = get_csv_link(driver)
                ReportItemRepository.save(db, ReportItem(
                    **ReportItemSchema(type='Sem sub classificação', url=link, report_id=r.id,producoes=[]).dict()))
            add_csv_item(value_opt, "", txt_opt, "", driver, csv_url_list)
        else:
            for subopt, txt in btn_sub_options:
                driver.get(f'{PATH}?opcao={value_opt}&subopcao={subopt}')
                r = ReportRepository.find_by_type(db, txt_opt)
                save_report_item_if_not_exists(db, txt, txt_opt, r, driver)
                add_csv_item(value_opt, subopt, txt_opt, txt, driver, csv_url_list)

    return csv_url_list
