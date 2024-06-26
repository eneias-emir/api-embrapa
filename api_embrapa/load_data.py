import csv
from api_embrapa.embrapa_csv_params import EmbrapaCsvParams
from api_embrapa.db.database_raw import db

from api_embrapa.utils import url_to_csv_filename


class LoadData:
    grupo_dados: str = ""
    lin_cabecalho: list = []

    def __init__(self):
        self.gerar_cabecalho_padrao()

    def gerar_cabecalho_padrao(self):
        for ano in range(1970, 2024):
            self.lin_cabecalho.append(ano)

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

            ind_cabecalho = 0
            id_reg_principal = db.gravar_reg_principal(reg)
            while ind < len(linha):
                ano = self.lin_cabecalho[ind_cabecalho]
                qtde = linha[ind]
                valor = 0

                if importacao_exportacao:
                    valor = linha[ind + 1]

                db.gravar_reg_itens(
                    id_dados_embrapa=id_reg_principal,
                    opt=reg["opt"],
                    ano=ano, 
                    qtde=qtde, 
                    valor=valor
                    )

                if importacao_exportacao:
                    ind += 2
                else:
                    ind += 1

                ind_cabecalho += 1

    def gravar_linha(self, item_config: dict, linha: list) -> None:
        opt = item_config["opt"]
        subopt = item_config["subopt"]

        reg = dict()
        reg["opt"] = opt
        reg["desc_opt"] = item_config["desc_opt"]
        reg["subopt"] = subopt
        reg["desc_subopt"] = item_config["desc_subopt"]
        reg["id_origem"] = linha[0]

        if (
            opt == EmbrapaCsvParams.OPT_PRODUCAO
            or opt == EmbrapaCsvParams.OPT_PROCESSAMENTO
            or opt == EmbrapaCsvParams.OPT_COMERCIALIZACAO
        ):
            self.gravar_reg(
                linha, reg, ind_inicio_ano=3, codigo=linha[1], descricao=linha[2]
            )
        elif (
            opt == EmbrapaCsvParams.OPT_IMPORTACAO
            or opt == EmbrapaCsvParams.OPT_EXPORTACAO
        ):
            self.gravar_reg(
                linha,
                reg,
                ind_inicio_ano=2,
                codigo="",
                descricao=linha[1],
                importacao_exportacao=True,
            )

    def processar_csv(self, item: dict) -> None:
        # self.gerar_cabecalho_padrao()

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
                if row[0].lower() != "id":
                    self.gravar_linha(item, row)
                # else:
                #     self.lin_cabecalho = row

        db.commit()

    def load_csv_to_database(self, lista_csv: list) -> None:
        for item in lista_csv:
            self.processar_csv(item)
