import redis

from startup.config import AppConfig


def setup_redis_connection(config: AppConfig.Redis) -> redis.client.Redis:
    conn = redis.Redis(
        host=config.host,
        port=config.port,
        password=config.password,
    )
    if conn.ping():
        return conn
