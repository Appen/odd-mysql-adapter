import logging
from os import getenv
from typing import Any


class MissingEnvironmentVariable(Exception):
    pass


def get_env(env: str, default_value: Any = None) -> str:
    value = getenv(env)
    if not value:
        if default_value is not None:
            return default_value
        raise MissingEnvironmentVariable(f'{env} does not exist')
    return value


class BaseConfig:
    ODD_HOST = get_env('MYSQL_HOST', 'localhost')
    ODD_PORT = get_env('MYSQL_PORT', '3306')
    ODD_DATABASE = get_env('MYSQL_DATABASE')
    ODD_USER = get_env('MYSQL_USER')
    ODD_PASSWORD = get_env('MYSQL_PASSWORD')
    ODD_SSL_DISABLED = bool(get_env('MYSQL_SSL_DISABLED', False))

    SCHEDULER_INTERVAL_MINUTES = get_env('SCHEDULER_INTERVAL_MINUTES', 60)


class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True


class ProductionConfig(BaseConfig):
    FLASK_DEBUG = False


def log_env_vars(config: dict):
    logging.info('Environment variables:')
    logging.info(f'MYSQL_HOST={config["ODD_HOST"]}')
    logging.info(f'MYSQL_PORT={config["ODD_PORT"]}')
    logging.info(f'MYSQL_DATABASE={config["ODD_DATABASE"]}')
    logging.info(f'MYSQL_USER={config["ODD_USER"]}')
    if config["ODD_PASSWORD"] != '':
        logging.info('MYSQL_PASSWORD=***')
    logging.info(f'SCHEDULER_INTERVAL_MINUTES={config["SCHEDULER_INTERVAL_MINUTES"]}')
