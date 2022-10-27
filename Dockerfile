FROM python:3.10-slim-buster AS env

WORKDIR /app

RUN apt update -y
RUN apt install postgresql-server-dev-all -y

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install libpq5
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "/app/main.py"]
