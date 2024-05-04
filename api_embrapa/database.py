import sqlite3
import os

from api_embrapa.appconfig import AppConfig

STM_DADOS_EMBRAPA = """
  create table DADOS_EMBRAPA (
    ID            integer primary key autoincrement,
    ID_ORIGEM     integer,
    OPT           text(10),
    DESC_OPT      text(100),
    SUBOPT        text(10),
    DESC_SUBOPT   text(100),
    GRUPO         text(50),
    CODIGO        text(50),
    DESCRICAO     text(100),
    ANO           integer,
    QTDE          real,
    VALOR         real)
"""

STM_DADOS_EMBRAPA_ITENS = """
  create table DADOS_EMBRAPA_ITENS (
    ID               integer primary key autoincrement,
    ID_DADOS_EMBRAPA integer,
    ANO           integer,
    QTDE          real,
    VALOR         real)
"""


STM_SELECT_DADOS_EMBRAPA = """
  select
    ID,
    ID_ORIGEM,
    OPT,
    DESC_OPT,
    SUBOPT,
    DESC_SUBOPT,
    GRUPO,
    CODIGO,
    DESCRICAO,
    ANO,
    QTDE,
    VALOR
  from DADOS_EMBRAPA
  where OPT = ?  
"""

STM_INSERT_DADOS_EMBRAPA = """
insert into DADOS_EMBRAPA(ID_ORIGEM, 
                          OPT, 
                          DESC_OPT, 
                          SUBOPT, 
                          DESC_SUBOPT, 
                          GRUPO, 
                          CODIGO, 
                          DESCRICAO) 
                   values(?, ?, ?, ?, ?, ?, ?, ?) 
                   RETURNING ID
"""

STM_INSERT_DADOS_EMBRAPA_ITENS = """
insert into DADOS_EMBRAPA_ITENS(ID_DADOS_EMBRAPA, 
                          ANO, 
                          QTDE, 
                          VALOR) 
                   values(?, ?, ?, ?) 
"""


class Database:
    connection = None

    def __init__(self) -> None:
        self.dbName = AppConfig.DATABASE_NAME
        self.dbFileName = self.dbName + AppConfig.DATABASE_EXTENSION
        self.connect_database()

    def connect_database(self) -> None:
        # Get the current working directory
        working_dir = AppConfig.PATH_DATA
        # Construct the full path to the database file
        db_file = os.path.join(working_dir, self.dbFileName)
        print(db_file)
        # checking the existence of the database
        if not os.path.exists(db_file):
            # Create the database file by opening a connection
            self.connection = sqlite3.connect(
                "file:" + db_file + "?mode=rwc", uri=True, check_same_thread=False
            )

            self.init_database()

            print(f"SQLite database file '{self.dbFileName}' created successfully.")
        else:
            print(f"SQLite database file '{self.dbFileName}' already exists.")
            self.connection = sqlite3.connect(db_file, check_same_thread=False)

    def init_database(self) -> None:
        self._createTabDadosEmbrapa()

    def _createTabDadosEmbrapa(self):
        # Create a cursor object to execute SQL statements
        cursor = self.connection.cursor()
        # Create the TabData table with columns

        cursor.execute("DROP TABLE IF EXISTS DADOS_EMBRAPA_ITENS")
        cursor.execute("DROP TABLE IF EXISTS DADOS_EMBRAPA")

        cursor.execute(STM_DADOS_EMBRAPA)
        cursor.execute(STM_DADOS_EMBRAPA_ITENS)

        self.connection.commit()
        cursor.close()

    def gravar_reg_principal(self, reg: dict) -> int:
        reg_dict = (
            reg["id_origem"],
            reg["opt"],
            reg["desc_opt"],
            reg["subopt"],
            reg["desc_subopt"],
            reg["grupo"],
            reg["codigo"],
            reg["descricao"].strip()
        )

        cursor = self.connection.cursor()
        cursor.execute(
            STM_INSERT_DADOS_EMBRAPA,
            reg_dict,
        )

        row = cursor.fetchone()
        (inserted_id, ) = row if row else None
        
        cursor.close()

        return inserted_id
    
    def gravar_reg_itens(self, id_dados_embrapa: int, ano: int, qtde: float, valor: float) -> None:
        reg_dict = (
            id_dados_embrapa,
            ano,
            qtde,
            valor
        )

        cursor = self.connection.cursor()
        cursor.execute(
            STM_INSERT_DADOS_EMBRAPA_ITENS,
            reg_dict,
        )
        
        cursor.close()


    def consultar(self, opt: str) -> list:
        cursor = self.connection.cursor()
        cursor.execute(STM_SELECT_DADOS_EMBRAPA, (opt,))

        rows = cursor.fetchall()
        cursor.close()

        return rows

    def database_is_empty(self) -> bool:
        cursor = self.connection.cursor()
        cursor.execute('SELECT exists(SELECT 1 FROM DADOS_EMBRAPA) AS row_exists')

        row = cursor.fetchone()
        cursor.close()

        if row[0] == 1:
            return False
        else:
            return True

    def commit(self) -> None:
        self.connection.commit()


db = Database()
