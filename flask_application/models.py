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

    elastic_address: str
    elastic_index: str


class FlaskSettings(EnvMixin):
    host: str
    port: int
    es_settings: ElasticSettings = ElasticSettings()


flask_config = FlaskSettings()
