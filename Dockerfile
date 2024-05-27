FROM python:3.12-alpine3.19

# Definir o diretório de trabalho
WORKDIR /app

# Copiar todos os arquivos do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Atualizar e instalar dependências necessárias
RUN apk update && apk add --no-cache \
    bash \
    chromium \
    chromium-chromedriver \
    curl \
    g++ \
    gcc \
    libffi-dev \
    make \
    musl-dev \
    openjpeg-dev \
    openssl-dev \
    tiff-dev \
    zlib-dev \
    postgresql-dev \
    gcc \
    && rm -rf /var/cache/apk/*

# Instalar as dependências do Python
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Definir a variável de ambiente para o Chrome
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Definir o entrypoint do contêiner
ENTRYPOINT ["python3", "-m", "uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
