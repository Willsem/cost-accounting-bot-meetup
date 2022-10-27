# Телеграм бот для учета расходов

Для запуска необходимо установить [Docker desktop](https://www.docker.com/products/docker-desktop/)

## Запуск через docker-compose

1. Установить в `TELEGRAM_BOT_WASTES_TELEGRAM_TOKEN` в файле `docker-compose` значение токена вашего бота
2. Собрать локальный образ бота

```sh
docker-compose build
```

3. Запустить все окружение

```sh
docker-compose up -d
```

## Запуск локально

1. Запуск инфраструктурных зависимостей

```sh
docker-compose up postgres redis -d
```

2. Создание python окружения

```sh
python3 -m venv venv
. ./venv/bin/activate
```

3. Установка всех зависимостей

```sh
pip install -r requirements.txt
```

4. Установка dotenv (необходимо установить node)

```sh
npm i -g dotenv-cli
```

5. Установить в `TELEGRAM_BOT_WASTES_TELEGRAM_TOKEN` в файле `.env` значение токена вашего бота

6. Запустить бота

```sh
make run
```

или

```sh
dotenv -e ./.env -- ./venv/bin/python3.11 main.py
```

## Остановка всего окружения

```sh
docker-compose down
```
