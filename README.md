# Projeto API Embrapa - Tech Challenge FIAP

Este é um projeto Python com FastAPI para realizar scraping de dados a partir do site da embrapa.
E construir uma api em torno desses dados

## Configuração do Ambiente

1. **Clone o Repositório:**
   ```bash 
   git clone git@github.com:muhlucas/embrapa_tech_challenge_fiap.git
   
## criando um ambiente virtual

python -m venv .venv

### No Mac
source .venv/bin/activate

### No Windows
.venv\Scripts\activate

## Desativando o ambiente virtual e voltando para o modo global do python

deactivate

## Instalando dependencias do projeto

pip install -r requirements.txt

## Crie um arquivo de variavel de ambiente .env

Você pode criar um arquivo .env na raiz do projeto. Se não fornecer a variável DB_URL, será utilizado um banco de dados SQLite local.
Exemplo de .env:

   ```bash
   DB_URL=sqlite:///./database.db
   ```

## Executando o FastAPI

1.	Execute o FastAPI:
```bash
uvicorn webapp.main:app --reload
```

2. Acesse a Documentação Swagger:

Navegue até http://localhost:8000/docs em seu navegador para acessar a documentação interativa Swagger.


## Scrapping de Dados

Para realizar a inserção dos dados a partir do scraping, realize uma rota da API GET /api/importar-csv.

# Docker com Docker Compose

Caso queira utilizar o docker em vez de rodar direto no seu sistema 

1. Construa a Imagem Docker:
```bash
docker-compose build
```

2. Execute o Contêiner Docker:
```bash
docker-compose up
```






