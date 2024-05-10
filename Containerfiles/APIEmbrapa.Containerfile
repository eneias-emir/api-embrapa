FROM browserless/chrome:latest

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

USER root

RUN apt update -y && apt install python3 python3-pip -y

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api_embrapa /code/api_embrapa

CMD ["python3", "-m", "api_embrapa"]