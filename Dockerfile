FROM python:3.12.3

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENTRYPOINT ["python3","-m","uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "8000"]