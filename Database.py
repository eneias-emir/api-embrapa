import sqlite3
import os

from AppConfig import AppConfig

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


class Database:
    connection = None

    def __init__(self) -> None:
        self.dbName = AppConfig.DATABASE_NAME.value
        self.dbFileName = self.dbName + AppConfig.DATABASE_EXTENSION.value
        self.connect_database()

    def connect_database(self) -> None:
        # Get the current working directory
        working_dir = AppConfig.PATH_DATA.value
        # Construct the full path to the database file
        db_file = os.path.join(working_dir, self.dbFileName)

        # checking the existence of the database
        if not os.path.exists(db_file):
            # Create the database file by opening a connection
            self.connection = sqlite3.connect(
                'file:' + db_file + '?mode=rwc', uri=True)

            self.init_database()

            print(
                f"SQLite database file '{self.dbFileName}' created successfully.")
        else:
            print(f"SQLite database file '{self.dbFileName}' already exists.")
            self.connection = sqlite3.connect( db_file, check_same_thread=False )
            self._createTabDadosEmbrapa()

    def init_database(self) -> None:
        self._createTabDadosEmbrapa()

    def _createTabDadosEmbrapa(self):
        # Create a cursor object to execute SQL statements
        cursor = self.connection.cursor()
        # Create the TabData table with columns

        cursor.execute('DROP TABLE IF EXISTS DADOS_EMBRAPA')

        cursor.execute(STM_DADOS_EMBRAPA)
        self.connection.commit()
        cursor.close()

    def gravar_reg(self, reg: dict) -> None:
        reg_dict = (reg['id_origem'], reg['opt'], reg['desc_opt'], reg['subopt'], reg['desc_subopt'], reg['grupo'], reg['codigo'], reg['descricao'], reg['ano'], reg['qtde'], reg['valor'])

        cursor = self.connection.cursor()
        cursor.execute('insert into DADOS_EMBRAPA(ID_ORIGEM, OPT, DESC_OPT, SUBOPT, DESC_SUBOPT, GRUPO, CODIGO, DESCRICAO, ANO, QTDE, VALOR) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', reg_dict)
        cursor.close()
    def consultar(self, opt: str) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM DADOS_EMBRAPA where OPT = ?", (opt,))

        rows = cursor.fetchall()
        return rows
    def commit(self) -> None:
        self.connection.commit()