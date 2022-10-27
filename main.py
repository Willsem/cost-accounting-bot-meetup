from startup import \
    setup_logger, \
    setup_config, \
    setup_postgres_connection, \
    setup_redis_connection
from repository import WasteRepository, UserRepository
from cache import CacheService
from services import WasteService
from bot import WasteBot


def main():
    logger = setup_logger()

    try:
        config = setup_config()

        postgres_connection = setup_postgres_connection(config.db)
        waste_repository = WasteRepository(postgres_connection)
        user_repository = UserRepository(postgres_connection)

        redis_connection = setup_redis_connection(config.redis)
        cache_service = CacheService(redis_connection)

        waste_service = WasteService(user_repository, waste_repository, logger)

        logger.info("bot is starting")
        WasteBot(config.telegram_token, waste_service, cache_service, logger).run()
    except Exception as e:
        logger.fatal('fail during the running', exc_info=e)
    finally:
        try:
            postgres_connection.close()
            redis_connection.close()
        except Exception as e:
            logger.fatal('fail during the closing connections', exc_info=e)


if __name__ == '__main__':
    main()
