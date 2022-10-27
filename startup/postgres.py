import psycopg2

from startup.config import AppConfig


def setup_postgres_connection(config: AppConfig.DB):
    return psycopg2.connect(
        dbname=config.name,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
    )
