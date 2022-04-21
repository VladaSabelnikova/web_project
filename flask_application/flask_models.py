"""Модуль содержит конфиги для flask."""
from pydantic import BaseSettings


class EnvMixin(BaseSettings):

    """
    Класс pydantic.
    Миксин, он нужен, для вынесения общих настроек.
    """

    class Config:

        """
        Настройки pydantic.
        Подробнее см.
        https://pydantic-docs.helpmanual.io/usage/model_config/
        """

        env_file = '.env_flask_app'
        env_file_encoding = 'utf-8'


class ElasticSettings(EnvMixin):
    """
    Класс pydantic.
    Настройки ES.
    """

    elastic_address: str
    elastic_index: str


class FlaskSettings(EnvMixin):

    """
    Класс pydantic.
    Общие настройки приложения Flask.
    """

    host: str
    port: int
    es_settings: ElasticSettings = ElasticSettings()


# Конфигурация, на основе классов pydantic.

flask_config = FlaskSettings()
