"""Модуль содержит pydantic классы."""
from typing import Tuple, Optional
from uuid import UUID

from pydantic import BaseSettings, BaseModel
from pydantic.env_settings import SettingsSourceCallable


def custom_prefix(name: str) -> str:

    """
    Функция для создания псевдонимов полей pydantic.
    Подробнее см.
    https://pydantic-docs.helpmanual.io/usage/model_config/#alias-generator

    Args:
        name: название поля

    Returns:
        Вернёт новый вариант названия.
    """

    return f'_{name}'


class Source(BaseModel):

    """
    Класс pydantic.
    Нужен для работы с содержимым ElasticSearch документов.
    """

    id: Optional[UUID]
    title: Optional[str]
    description: Optional[str]
    h1: Optional[str]


class Document(BaseModel):

    """
    Класс pydantic.
    Нужен для работы с ElasticSearch документами.
    """

    id: Optional[UUID]
    index: Optional[str]
    source: Source = Source()

    class Config:

        """
        Настройки pydantic.
        Подробнее см.
        https://pydantic-docs.helpmanual.io/usage/model_config/
        """

        alias_generator = custom_prefix


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

    elastic_host: str = 'localhost'
    elastic_port: int = 9200
    address: str = f'http://{elastic_host}:{elastic_port}'


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


# Конфиги, построенные на основе классов pydantic.

config = ETLSettings()
document_config = Document()
