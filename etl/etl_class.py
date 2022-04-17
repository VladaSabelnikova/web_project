"""Модуль содержит класс, для работы ETL."""
import sys
from multiprocessing import Process
from pathlib import Path
from typing import List, Tuple, Dict, Union

import psycopg2
from elasticsearch import Elasticsearch, helpers

from backoff_function import backoff
from database_query import SELECT_FROM_PG
from log import create_logger
from models import document_config
from video_converter import MediaConverter


class ETL:

    """Класс-интерфейс для работы ETL процесса."""

    def __init__(
        self,
        postgres_parameters: Dict[str, Union[str, int]],
        elastic_search_address: str
    ) -> None:

        """
        Конструктор.

        Args:
            postgres_parameters: параметры подключения к Postgres (host, port)
            elastic_search_address: адрес, для подключения к ElasticSearch (http://host:port)
        """

        self.postgres_parameters = postgres_parameters
        self.elastic_search_address = elastic_search_address

    @backoff()
    def extract(self, time_from_storage: str, pack_size: int, begin: int) -> List[Tuple[str, ...]]:

        """
        Функция реализует «extract» задачу ETL.
        Т.е. подключается к PG и выхватывает оттуда данные.

        Args:
            time_from_storage: время последнего обновления
            pack_size: размер пачки
            begin: место старта

        Returns:
            Вернёт данные из БД, подходящие под условие запроса SELECT_FROM_PG.
        """

        with psycopg2.connect(**self.postgres_parameters) as con_postgres:
            cur_postgres = con_postgres.cursor()
            select = SELECT_FROM_PG.format(*[time_from_storage for _ in range(6)], pack_size, begin)  # noqa: WPS331
            cur_postgres.execute(select)
            data = cur_postgres.fetchall()
            return data  # noqa: WPS331

    def transform(self, data: List[Tuple[str, ...]], index_name: str) -> Tuple[List[dict], str]:

        """
        Функция реализует «transform» задачу ETL.
        Т.е. получает на вход данные из PG (data) и преобразует их в формат, подходящий ES.

        Args:
            data: «сырые» данные из PG
            index_name: индекс ES в который будет происходить вставка документов

        Returns:
            Вернёт список трансформированных данных и максимальную дату пачки.
        """

        all_dates_from_pack = []
        transformed_pack = []

        for id_video, title, description, h1, audio_file, video_file, data_changed, track_changed, max_date in data:
            doc = document_config

            all_dates_from_pack.append(f'{max_date}')

            if track_changed:

                dir_media = 'media_source/'
                mp_4 = f'{dir_media}{id_video}.mp4'
                mpeg_dash_manifest = f'../streams/{id_video}/dash.mpd'

                mc = MediaConverter()
                logger.info('Media converter started.')

                container = mc.make_container(f'{dir_media}{video_file}', f'{dir_media}{audio_file}', mp_4)
                logger.info('Container has been created.')

                packaging = Process(target=mc.to_mpeg_dash, args=(Path(container), mpeg_dash_manifest))
                packaging.start()
                logger.info('Packaging process has been started.')

            if data_changed:
                doc.id = id_video
                doc.index = index_name

                doc.source.id = id_video
                doc.source.title = title
                doc.source.description = description
                doc.source.h1 = h1
                logger.info('Metadata has been collected.')

            transformed_pack.append(doc.dict(by_alias=True))

        return transformed_pack, max(all_dates_from_pack)

    @backoff()
    def load(self, data: List[dict]) -> None:

        """
        Функция реализует «load» задачу ETL.
        Т.е. подключается к ES и загружает в него данные data.

        Для более быстрой работы используем загрузку пачками (bulk).

        Args:
            data: данные, которые нужно загрузить.
        """

        es = Elasticsearch(self.elastic_search_address)
        logger.info('Elastic connection has been created: %s', self.elastic_search_address)

        helpers.bulk(es, data)
        logger.info('Pack has been sent.')


logger = create_logger(__file__, stream_out=sys.stdout)
