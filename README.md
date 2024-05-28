# Projeto API Embrapa RS - Tech Challenge MLE1

## Objetivo

Este projeto foi criado para atender a demanda de geração de uma API de consulta pública dos dados disponibilizados no site da Embrapa do Rio Grande do Sul.

O site da Embrapa contendo os dados pode ser acessado através do endereço <http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01>.

Neste site os dados podem ser consultados e filtrados pelo ano, e os tipos de consultas estão dispostos nas abas **produção, processamento, comercialização, impotação e exportação**. Em cada aba existe a opção de download do arquivo no formato CSV contendo os dados referentes a aba selecionada.

O objetivo deste projeto é fornecer uma forma de acesso a esses dados através de uma API, para que a mesma possa ser consumida por alguma automação para geração de um banco de dados que possa servir de base para análises através de um modelo de machine learning.


## Descrição da API

Esta API foi desenvolvida em Python, utilizando o framework FastApi. 

O processo de carga dos dados é executado na execução da API, onde é feito um processo de scraping no site da Embrapa, buscando por todos os links de download de arquivos CSV e gerando uma lista dos mesmos com a referencia da aba onde eles estão no site da embrapa. 

Em seguida, a API faz o download de cada um desses arquivos, cria um banco de dados local, processa cada um desses arquivos e grava no banco de dados.

O banco de dados escolhido foi o SQLite, devido a praticidade de não precisar ser instalado e configurado, e também por não se tratar de um volume de dados muito grande que exija um banco mais potente. Além disso, o projeto não irá receber uma carga elevada de consultas simultaneas, pois se trata de dados históricos atualizados com uma baixa frequencia.

Os testes foram executados usando pytest com TestClient, para validação do funcionamento dos endpoints.

## Repositório da API no github

https://github.com/eneias-emir/api-embrapa

## Endpoints disponibilizados

Auth
- /api/v1/login/register
- /token

Inventory
- /api/v1/inventory/
- /api/v1/inventory/all_csvs
- /api/v1/inventory/production
- /api/v1/inventory/production/{year}
- /api/v1/inventory/processing
- /api/v1/inventory/processing/{year}
- /api/v1/inventory/comercialization
- /api/v1/inventory/comercialization/{year}
- /api/v1/inventory/imports
- /api/v1/inventory/imports/{year}
- /api/v1/inventory/exports
- /api/v1/inventory/exports/{year}




## Processo de deploy da API


### 1. Deploy no desktop para testes locais

Após a replicação do repositório no ambiente de execução, basta seguir os passos listados abaixo:

#### Criando um ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Desativando o ambiente virtual e voltando para o modo global do python

deactivate

#### Rodando o projeto

```bash
python -m api_embrapa
```

#### Executando testes

```bash
pytest -vv
```

### 2. Deploy em container docker

A configuração do **docker-compose.yml** ativa uma imagem docker configurada no Containerfiles/APIEmbrapa.Containerfile. Esta configuração gera uma imagem baseada em **browserless/chrome**, efetua a instalação do python 3 e instala as dependencias.

Para gerar a imagem, basta executar os comandos abaixo:

Para construir as imagens:

```bash
docker-compose build
```

Para rodar a aplicação:

```bash
docker-compose up
```
