import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

from webapp.import_csv import import_csv

# Configure the logging module
logging.basicConfig(level=logging.INFO)

# URL da página web
PATH: str = 'http://vitibrasil.cnpuv.embrapa.br/index.php'


def setup_driver() -> webdriver.Chrome:
    """Configura e retorna uma instância do driver do Chrome."""
    options = webdriver.ChromeOptions()
    options.add_argument(
        '--headless --no-sandbox --disable-dev-shm-usage --start-maximized --disable-infobars --disable-extensions '
        '--incognito --disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    # Oculta o atributo 'webdriver' do navegador
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

    return driver


def import_csv_to_base(db):
    """
    Intera por um array de string com o nome ds botões da página
    Ignorando 'Apresentação', 'Publicação', onde os mesmos não tem csv
    E finaliza o driver do chorome
    """
    logging.info('Selenium: Iniciando webdriver (Chrome)...')
    driver = setup_driver()
    logging.info(f'Selenium: Navegando para url {PATH}... ')
    driver.get(PATH)
    logging.info(f'Selenium: Obtendo títulos dos botões de menu principal do {PATH}... ')
    menu_options = get_button_list_by_class(driver, 'btn_opt')
    try:
        for menu_option, table_name in menu_options:
            if table_name not in ['Apresentação', 'Publicação']:
                process_table(driver, menu_option, table_name)
    finally:
        driver.quit()
        logging.info('Selenium: Webdriver fechado.')


def process_table(driver, menu_option, table_name):
    """
    Navega até a página do menu e importa o csv.
    Navega também sobre as categorias do menu e importa o csv.

    Args:
        driver: Instância do driver do chorome.
        menu_option: Opção do menu.
        table_name: Nome da tabela baseado no nome do botão do menu da página.
    """
    driver.get(f'{PATH}?opcao={menu_option}')
    btn_sub_options = get_button_list_by_class(driver, 'btn_sopt')
    if not btn_sub_options:
        logging.info(f'Selenium: Obtendo URL do CSV de {table_name}...')
        url = get_csv_link(driver)
        import_csv(url, table_name, None)
    else:
        for menu_sub_option, categoria in btn_sub_options:
            import_categoria_csv(driver, menu_option, menu_sub_option, table_name, categoria)


def get_button_list_by_class(driver: webdriver.Chrome, class_name: str) -> list:
    """Obtém uma lista de botões com uma determinada classe."""
    return [(btn.get_attribute('value'), btn.text) for btn in driver.find_elements(By.CLASS_NAME, class_name)]


def get_csv_link(driver: webdriver.Chrome) -> str:
    """Obtém o link para download do arquivo CSV de um botão"""
    return next((href.get_attribute('href') for href in driver.find_elements(By.LINK_TEXT, "DOWNLOAD") if
                 href and '.csv' in href.get_attribute('href').lower()), "")


def import_categoria_csv(driver, menu_option, menu_sub_option, table_name, categoria):
    """
    Obtém a url do menu_sub_option de menu_option, para importar o csv

    Args:
        driver: Instância do driver.
        menu_option: Opção do menu.
        menu_sub_option: Subopção do menu.
        table_name: Nome da tabela.
        categoria: Categoria do sub-relatório, ou seja menu_sub_option
    """
    driver.get(f'{PATH}?opcao={menu_option}&subopcao={menu_sub_option}')
    logging.info(f'Selenium: Obtendo URL de {table_name}, subreport de {categoria}...')
    url = get_csv_link(driver)
    import_csv(url, table_name, categoria)
