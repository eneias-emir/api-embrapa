from selenium import webdriver
from selenium.webdriver.common.by import By

# funcao para fazer o setup do driver
def driver_setup():
    options = webdriver.ChromeOptions()
    # run Selenium in headless mode
    options.add_argument("--headless")
    # options.headless = True
    options.add_argument("--no-sandbox")
    # overcome limited resource problems
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("lang=en")
    # open Browser in maximized mode
    options.add_argument("start-maximized")
    # disable infobars
    options.add_argument("disable-infobars")
    # disable extension
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
    )

    return driver


class ScrapingEmbrapa:
    def __init__(self):
        self.url_embrapa: str = "http://vitibrasil.cnpuv.embrapa.br/index.php"

    def get_lista_btn_class(self, driver: webdriver, class_name: str) -> list:
        result = []

        botoes = driver.find_elements(By.CLASS_NAME, class_name)
        for btn in botoes:
            value = btn.get_attribute("value")
            txt = btn.text
            result.append((value, txt))

        return result

    def add_item_lista(
        self,
        opt: str,
        subopt: str,
        desc_opt: str,
        desc_subopt: str,
        driver: webdriver,
        lista: list,
    ) -> None:
        results = driver.find_elements(By.LINK_TEXT, "DOWNLOAD")

        for dictionary in results:
            href = dictionary.get_attribute("href")
            if ".csv" in href.lower():
                lista.append(
                    {
                        "opt": opt,
                        "subopt": subopt,
                        "desc_opt": desc_opt,
                        "desc_subopt": desc_subopt,
                        "url": href,
                    }
                )

    def get_lista_url_csv(self) -> list:
        lista_url_csv = []

        # initialize an instance of the Chrome driver (browser)
        driver = driver_setup()

        # faz o request na url principal
        driver.get(f"{self.url_embrapa}")

        # busca os botoes de opcoes, por itens da classe btn_opt
        btn_opcoes = self.get_lista_btn_class(driver, "btn_opt")

        for value_opt, txt_opt in btn_opcoes:
            driver.get(f"{self.url_embrapa}?opcao={value_opt}")

            btn_subopt = self.get_lista_btn_class(driver, "btn_sopt")

            if not btn_subopt:
                self.add_item_lista(value_opt, "", txt_opt, "", driver, lista_url_csv)
            else:
                for subopt, txt in btn_subopt:
                    driver.get(
                        f"{self.url_embrapa}?opcao={value_opt}&subopcao={subopt}"
                    )
                    self.add_item_lista(
                        value_opt, subopt, txt_opt, txt, driver, lista_url_csv
                    )

        return lista_url_csv
