import csv
from api_embrapa.database import Database

from api_embrapa.utils import url_to_csv_filename

OPT_PRODUCAO = "opt_02"
OPT_PROCESSAMENTO = "opt_03"
OPT_COMERCIALIZACAO = "opt_04"
OPT_IMPORTACAO = "opt_05"
OPT_EXPORTACAO = "opt_06"


class LoadData:
    db: Database
    grupo_dados: str = ""
    lin_cabecalho: list = []

    def create_database(self):
        self.db = Database()

    def gravar_reg(
        self,
        linha: list,
        reg: dict,
        ind_inicio_ano: int,
        codigo: str,
        descricao: str,
        importacao_exportacao: bool = False,
    ) -> None:
        if descricao.isupper():
            self.grupo_dados = descricao
        else:
            ind = ind_inicio_ano
            reg["codigo"] = codigo
            reg["descricao"] = descricao
            reg["grupo"] = self.grupo_dados
            while ind < len(linha):
                reg["ano"] = self.lin_cabecalho[ind]
                reg["qtde"] = linha[ind]

                if importacao_exportacao:
                    reg["valor"] = linha[ind + 1]
                else:
                    reg["valor"] = 0

                self.db.gravar_reg(reg)

                if importacao_exportacao:
                    ind += 2
                else:
                    ind += 1

    def gravar_linha(self, item_config: dict, linha: list) -> None:
        opt = item_config["opt"]
        subopt = item_config["subopt"]

        reg = dict()
        reg["opt"] = opt
        reg["desc_opt"] = item_config["desc_opt"]
        reg["subopt"] = subopt
        reg["desc_subopt"] = item_config["desc_subopt"]
        reg["id_origem"] = linha[0]

        if opt == OPT_PRODUCAO:
            self.gravar_reg(linha, reg, ind_inicio_ano=2, codigo="", descricao=linha[1])
        elif opt == OPT_PROCESSAMENTO or opt == OPT_COMERCIALIZACAO:
            self.gravar_reg(
                linha, reg, ind_inicio_ano=3, codigo=linha[1], descricao=linha[2]
            )
        elif opt == OPT_IMPORTACAO or opt == OPT_EXPORTACAO:
            self.gravar_reg(
                linha,
                reg,
                ind_inicio_ano=2,
                codigo="",
                descricao=linha[1],
                importacao_exportacao=True,
            )

    def processar_csv(self, item: dict) -> None:
        file_path = url_to_csv_filename(item["url"])

        with open(file_path, newline="", encoding="utf8") as csvfile:
            # identifica o separador de colunas do csv
            dialect = csv.Sniffer().sniff(csvfile.readline(), ";\t")
            # retorna o ponteiro para o inicio do arquivo csv
            csvfile.seek(0)
            # cria o reader do csv
            data = csv.reader(csvfile, dialect)

            self.grupo_dados = ""
            # i = 0
            for row in data:
                if row[0].lower() == "id":
                    self.lin_cabecalho = row
                else:
                    self.gravar_linha(item, row)

                # i += 1
                # if i == 5:
                #    break

        self.db.commit()

    def load_csv_to_database(self, lista_csv: list) -> None:
        self.create_database()

        for item in lista_csv:
            self.processar_csv(item)
