import environ


@environ.config(prefix="TELEGRAM_BOT_WASTES")
class AppConfig:
    telegram_token: str = environ.var()

    @environ.config
    class DB:
        name: str = environ.var()
        host: str = environ.var()
        port: int = environ.var(converter=int)
        user: str = environ.var()
        password: str = environ.var()
    db = environ.group(DB)

    @environ.config
    class Redis:
        host: str = environ.var()
        port: int = environ.var(converter=int)
        password: str = environ.var()
    redis = environ.group(Redis)


def setup_config() -> AppConfig:
    return environ.to_config(AppConfig)
