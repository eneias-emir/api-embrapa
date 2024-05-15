class AppConfig:
    """Class de configuração que armazena constants necessárias para a utilização do projeto."""

    PATH_DATA = "./data"
    DATABASE_NAME = "vitibrasil_embrapa"
    DATABASE_EXTENSION = ".db"
    SECRET_KEY = "api-embrapa-development"
    API_EMBRAPRA_SESSION_SECRET_KEY = "api-embrapa-development"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    URL_EMBRAPA = "http://vitibrasil.cnpuv.embrapa.br/index.php"
