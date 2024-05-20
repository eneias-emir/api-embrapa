import pandas as pd

from api_embrapa.db.model import DadosEmbrapa, DadosEmbrapaItens, Login, session, Base, engine

class Database:
    def gravar_reg_principal(self, reg: dict) -> int:
        new_reg = DadosEmbrapa(
                id_origem=reg["id_origem"], 
                opt=reg["opt"], 
                desc_opt=reg["desc_opt"],
                subopt=reg["subopt"],
                desc_subopt=reg["desc_subopt"],
                grupo=reg["grupo"],
                codigo=reg["codigo"],
                descricao=reg["descricao"]
        )
        session.add(new_reg)
        session.commit()

        return new_reg.id

    def gravar_reg_itens(
        self, id_dados_embrapa: int, opt: str, ano: int, qtde: float, valor: float
    ) -> None:
        new_reg = DadosEmbrapaItens(
                id_dados_embrapa=id_dados_embrapa, 
                opt=opt,
                ano=ano, 
                qtde=qtde,
                valor=valor
        ) 

        session.add(new_reg)
        session.commit()

    def gravar_novo_login(self, username: str, password: str) -> None:
        new_reg = Login(username=username, password=password)

        session.add(new_reg)
        session.commit()

    def consultar_login(self, username: str) -> tuple:
        login = session.query(Login).filter(Login.username == username).first()

        if login:
            result = (login.id, login.username, login.password)
        else:
            result = (0, '', '')

        return result
    
    def consultar_itens(self, opt: str, year: int) -> list:
        if year == 0:
            itens = session.query(DadosEmbrapaItens).filter(DadosEmbrapaItens.opt == opt).all()
        else:
            itens = session.query(DadosEmbrapaItens).filter(
                (DadosEmbrapaItens.opt == opt) & (DadosEmbrapaItens.ano == year)
            ).all()

        result = [
            (reg.id_dados_embrapa, reg.ano, reg.qtde, reg.valor)
            for reg in itens
        ]

        return result

    def consultar(self, opt: str, year: int = 0) -> list:
        itens_year = self.consultar_itens(opt, year)

        dados = session.query(DadosEmbrapa).filter(DadosEmbrapa.opt == opt).all()

        products = [
            (reg.id, reg.id_origem, reg.opt, reg.desc_opt, reg.subopt, reg.desc_subopt, reg.grupo, reg.codigo, reg.descricao)
            for reg in dados
        ]

        # if the list is empty, put a item with zer values for each product
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
    
    def database_is_empty(self) -> bool:
        data = session.query(DadosEmbrapa.id).first()

        if data:
            result = False
        else:
            result = True

        return result
    
db = Database()