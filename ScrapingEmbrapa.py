from selenium import webdriver
from selenium.webdriver.common.by import By


# funcao para fazer o setup do driver
def driver_setup():
    options = webdriver.ChromeOptions()
    #run Selenium in headless mode
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    #overcome limited resource problems
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("lang=en")
    #open Browser in maximized mode
    options.add_argument("start-maximized")
    #disable infobars
    options.add_argument("disable-infobars")
    #disable extension
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

    return driver


class ScrapingEmbrapa:
    def __init__(self):
        self.url_embrapa: str = 'http://vitibrasil.cnpuv.embrapa.br/index.php'

    def get_lista_url_csv(self) -> list:
        lista_url_csv = []

        # initialize an instance of the Chrome driver (browser)
        driver = driver_setup()

        for i in range(2, 7):
            for j in range(1, 6):
                opt = f'opt_0{i}'
                subopt = f'subopt_0{j}'
                driver.get(f'{self.url_embrapa}?opcao={opt}&subopcao={subopt}')

                results = driver.find_elements(By.LINK_TEXT, "DOWNLOAD")

                for dictionary in results:
                    href = dictionary.get_attribute('href')
                    print("href=", href)
                    if ('.csv' in href.lower() ) and (href not in lista_url_csv):
                        lista_url_csv.append(href)

        return lista_url_csv




