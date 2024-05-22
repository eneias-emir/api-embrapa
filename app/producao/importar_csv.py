from io import StringIO

import pandas as pd
import requests
from sqlalchemy.orm import Session

from app.database_config import engine
from app.report.repository import ReportRepository


def import_producao_csv(db: Session):
    report = ReportRepository.find_by_type(db, 'Produção')
    for report_item in report.report_items:
        # Baixa o arquivo CSV
        response = requests.get(report_item.url)
        # Verifica se a resposta foi bem-sucedida
        if response.status_code == 200:
            # Cria um objeto StringIO para carregar os dados em memória
            csv_data = StringIO(response.text)

            # Carrega o CSV em um DataFrame
            df = pd.read_csv(csv_data, sep=';')
            column_rename_mapping = {}
            for year in range(1970, 2023):
                old_column_name = str(year)
                new_column_name = f"qtd_{year}_em_l"
                column_rename_mapping[old_column_name] = new_column_name
            df.rename(columns=column_rename_mapping, inplace=True)
            #Define o relacionamento com report_item
            df['report_item_id'] = report.id
            # Persiste os dados na tabela 'producao'
            df.to_sql('producao', con=engine, if_exists='replace', index=False)

            # Fecha a conexão com o banco de dados
            engine.dispose()
