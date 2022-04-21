"""Модуль содержит ETL процесс."""
import sys
from time import sleep

from etl_class import ETL
from log import create_logger
from models import config
from state_storage import JsonFileStorage, State


def main() -> None:  # noqa: WPS213, WPS210

    """
    Функция реализует работу ETL процесса.
    Подробнее см.
    https://ru.wikipedia.org/wiki/ETL
    """

    host = config.elastic_search_parameters.elastic_host
    port = config.elastic_search_parameters.elastic_port
    address = f'http://{host}:{port}'

    # Создаём экземпляр класса с интерфейсом ETL.
    etl = ETL(config.postgres_parameters.dict(), address)

    # Создаём стартовые значения для работы ETL процесса.
    # Переменная pack — размер пачки для вставки.
    # Переменная begin — место, с которого мы начинаем «обыск» данных в PG.
    # Переменная time — самое минимально возможное время последнего обновления.
    # Переменная index_name — название индекса ES.
    pack, begin, time, index_name = config.pack_size, 0, config.smallest_time, config.index_name

    # Создаём хранилище состояния (для времени).
    state = State(JsonFileStorage('state.json'))
    state.set_state('time', time)
    all_dates = []

    while True:

        # Достаём данные из PG.
        row_data = etl.extract(time_from_storage=time, pack_size=pack, begin=begin)
        logger.info('Data has been received.')

        if row_data:

            # Трансформируем данные в пригодный для ES формат.
            transformed_data, new_date = etl.transform(row_data, index_name)
            all_dates.append(new_date)
            logger.info('Data has been transformed.')

            # Записываем данные в ES.
            etl.load(transformed_data)
            logger.info('Data has been loaded.')

            begin += pack

        else:  # Если данных для вставки нет, то:

            # Обновляем дату.
            old_date = state.get_state('time')
            state.set_state('time', max([old_date, *all_dates]))

            # Начинаем обход сначала.
            begin = 0
            time = state.get_state('time')

            logger.info('No packs to insert. Last update %s', time)
            sleep(10)  # Даём фору, что бы зря не долбать PG.


logger = create_logger(__file__, stream_out=sys.stdout)

if __name__ == '__main__':
    main()
