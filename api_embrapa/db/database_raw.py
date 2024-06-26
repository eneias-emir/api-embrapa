import sqlite3
import os
import pandas as pd

from api_embrapa.appconfig import AppConfig
from api_embrapa.db.scripts_raw import ScriptsRaw

from typing import Any

class Database:
    connection = None

    def __init__(self) -> None:
        self.db_file_name = AppConfig.DATABASE_NAME + AppConfig.DATABASE_EXTENSION
        self.connect_database()

    def connect_database(self) -> None:
        # Get the current working directory
        working_dir = AppConfig.PATH_DATA

        # Create the directory if it does not exist.
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        # Construct the full path to the database file
        db_file = os.path.join(working_dir, self.db_file_name)
        # checking the existence of the database
        if not os.path.exists(db_file):
            # Create the database file by opening a connection
            self.connection = sqlite3.connect(
                "file:" + db_file + "?mode=rwc", uri=True, check_same_thread=False
            )

            self.init_database()

            print(f"* SQLite database file '{self.db_file_name}' created successfully.")
        else:
            print(f"* SQLite database file '{self.db_file_name}' already exists.")
            self.connection = sqlite3.connect(db_file, check_same_thread=False)

    def init_database(self) -> None:
        self._createTabDadosEmbrapa()
        self._createTabLogin()

    def _createTabDadosEmbrapa(self):
        # Create a cursor object to execute SQL statements
        cursor = self.connection.cursor()
        # Create the TabData table with columns

        cursor.execute("DROP TABLE IF EXISTS DADOS_EMBRAPA_ITENS")
        cursor.execute("DROP TABLE IF EXISTS DADOS_EMBRAPA")

        cursor.execute(ScriptsRaw.STM_DADOS_EMBRAPA)
        cursor.execute(ScriptsRaw.STM_DADOS_EMBRAPA_ITENS)

        self.connection.commit()
        cursor.close()

    def _createTabLogin(self):
        # Create a cursor object to execute SQL statements
        cursor = self.connection.cursor()
        # Create the TabData table with columns

        cursor.execute("DROP TABLE IF EXISTS LOGIN")

        cursor.execute(ScriptsRaw.STM_API_LOGIN)

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
            reg["descricao"].strip(),
        )

        cursor = self.connection.cursor()
        cursor.execute(
            ScriptsRaw.STM_INSERT_DADOS_EMBRAPA,
            reg_dict,
        )

        row = cursor.fetchone()
        (inserted_id,) = row if row else None

        cursor.close()

        return inserted_id

    def gravar_reg_itens(
        self, id_dados_embrapa: int, opt: str, ano: int, qtde: float, valor: float
    ) -> None:
        reg_dict = (id_dados_embrapa, opt, ano, qtde, valor)

        cursor = self.connection.cursor()
        cursor.execute(
            ScriptsRaw.STM_INSERT_DADOS_EMBRAPA_ITENS,
            reg_dict,
        )

        cursor.close()

    def gravar_novo_login(self, username: str, password: str) -> None:
        reg_dict = (username, password)

        cursor = self.connection.cursor()
        cursor.execute(
            ScriptsRaw.STM_INSERT_DADOS_LOGIN,
            reg_dict,
        )

        self.connection.commit()

        cursor.close()

    def consultar(self, opt: str, year: int = 0) -> list:
        itens_year = self.consultar_itens(opt, year)

        cursor = self.connection.cursor()
        cursor.execute(ScriptsRaw.STM_SELECT_DADOS_EMBRAPA, (opt,))

        products = cursor.fetchall()
        cursor.close()

        # if the list is empty, put a item with zero values for each product
        if not itens_year:
            itens_year = []
            for product in products:
                itens_year.append((product[0], year, 0, 0))


        # Convert sets of tuples into Pandas DataFrames
        products_df = pd.DataFrame(
            products,
            columns=[
                "id",
                "column1",
                "column2",
                "column3",
                "column4",
                "column5",
                "column6",
                "column7",
                "column8",
            ],
        )
        data_df = pd.DataFrame(itens_year, columns=["id", "year", "value1", "value2"])

        # Merge the two DataFrames on the 'id' column
        merged_df = pd.merge(products_df, data_df, on="id")

        # Group by 'id' and aggregate the data tuples into a list
        result = (
            merged_df.groupby(
                [
                    "id",
                    "column1",
                    "column2",
                    "column3",
                    "column4",
                    "column5",
                    "column6",
                    "column7",
                    "column8",
                ]
            )[["year", "value1", "value2"]]
            .apply(lambda x: [tuple(row) for row in x.values])
            .reset_index(name="data")
        )

        # Convert the result back to a list of tuples
        result_tuples = [tuple(row) for row in result.values]

        return result_tuples

    def consultar_login(self, username: str) -> Any:
        cursor = self.connection.cursor()
        cursor.execute(ScriptsRaw.STM_SELECT_DADOS_LOGIN, (username,))

        login = cursor.fetchone()
        cursor.close()

        if not login:
            login = (0, '', '')

        return login

    def consultar_itens(self, opt: str, year: int) -> list:
        cursor = self.connection.cursor()

        if year == 0:
            cursor.execute(ScriptsRaw.STM_SELECT_DADOS_EMBRAPA_ITENS, (opt,))
        else:
            cursor.execute(ScriptsRaw.STM_SELECT_DADOS_EMBRAPA_ITENS_ANO, (opt, year))

        rows = cursor.fetchall()
        cursor.close()

        return rows

    def database_is_empty(self) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT exists(SELECT 1 FROM DADOS_EMBRAPA) AS row_exists")

        row = cursor.fetchone()
        cursor.close()

        if row[0] == 1:
            return False
        else:
            return True

    def commit(self) -> None:
        self.connection.commit()


db = Database()
