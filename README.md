
# Projeto API Embrapa - Tech Challenge FIAP

Este é um projeto Python com FastAPI para realizar scraping de dados a partir do site da embrapa.<br/>
Com o objetivo de capturar as informações do site e disponibilizar por meio de uma API.

Link para acesso à API: [API Playground](https://utq9zejz3b.us-east-1.awsapprunner.com/docs)

[![Deploy to AWS](https://github.com/muhlucas/embrapa_tech_challenge_fiap/actions/workflows/main.yml/badge.svg)](https://github.com/muhlucas/embrapa_tech_challenge_fiap/actions/workflows/main.yml)


---- 


## Configuração do Ambiente

1. **Clone o Repositório:**
```bash 
git clone git@github.com:muhlucas/embrapa_tech_challenge_fiap.git
```
   
### criando um ambiente virtual

```bash 
python -m venv .venv
```

#### No Mac
```bash 
source .venv/bin/activate
```


#### No Windows
```bash 
.venv\Scripts\activate
```

#### Desativando o ambiente virtual e voltando para o modo global do python

```bash 
deactivate
```

### Instalando dependencias do projeto

```bash 
pip install -r requirements.txt
```

### Crie um arquivo de variavel de ambiente .env

Você pode criar um arquivo .env na raiz do projeto.<br/> 
Se não fornecer a variável DB_URL, será utilizado um banco de dados SQLite local.<br/>
Exemplo de .env:

   ```bash
   DB_URL=sqlite:///./database.db
   ```

### Executando o FastAPI

1.	Execute o FastAPI:
```bash
uvicorn webapp.main:app --reload
```

2. Acesse a Documentação Swagger:

Navegue até ``http://localhost:8000/docs`` em seu navegador para acessar a documentação interativa Swagger.


### Scrapping de Dados

Para realizar a inserção dos dados a partir do scraping, realize uma rota da API GET /api/importar-csv.

## Docker com Docker Compose

Caso queira utilizar o docker em vez de rodar direto no seu sistema 

1. Construa a Imagem Docker:
```bash
docker-compose build
```

2. Execute o Contêiner Docker:
```bash
docker-compose up
```

## Processo de Deploy 

![deploy](https://github.com/muhlucas/embrapa_tech_challenge_fiap/assets/2555291/ea3bb315-8871-4293-a35a-f68fef0e8e53)

