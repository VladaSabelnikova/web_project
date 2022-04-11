"""Модуль содержит pydantic классы."""
from typing import Tuple

from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


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

        env_file = '.env_etl'
        env_file_encoding = 'utf-8'
        secrets_dir = './settings/secrets'

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:

            """
            Штука, для определения порядка приоритета для переменных окружения.
            Мы переопределяем порядок по умолчанию,
            т.к. хотим, что бы переменные из файлов dotenv были выше по приоритету,
            нежели переменные ОС.
            Подробнее см.
            https://pydantic-docs.helpmanual.io/usage/settings/#customise-settings-sources

            Args:
                init_settings: переменные, пришедшие при инициализации
                env_settings: переменные ОС
                file_secret_settings: кастомные переменные из dotenv файлов

            Returns:
                Вернёт порядок (по убыванию значимости) приоритета.
            """

            return init_settings, file_secret_settings, env_settings


class PostgresSettings(EnvMixin):

    """
    Класс pydantic.
    Тут настройки для Postgres.
    """

    dbname: str
    user: str
    password: str
    host: str = 'localhost'
    port: int = 5433


class ElasticSettings(EnvMixin):

    """
    Класс pydantic.
    Тут настройки для ElasticSearch.
    """

    elastic_host: str
    elastic_port: int


class ETLSettings(EnvMixin):

    """
    Класс pydantic.
    Тут настройки для работы ETL.
    Содержит (вложено) настройки для Postgres и ElasticSearch,
    а так же необходимую информацию для ETL.
    """

    postgres_parameters: PostgresSettings = PostgresSettings()
    elastic_search_parameters: ElasticSettings = ElasticSettings()

    pack_size: int = 5
    smallest_time: str = '0001-01-01 00:00:00.448000 +00:00'
    index_name: str = 'videos'


config = ETLSettings()
