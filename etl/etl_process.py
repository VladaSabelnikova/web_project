"""Модуль содержит ETL процесс."""
import sys
from time import sleep

from etl_class import ETL
from log import create_logger
from models import config
from state_storage import JsonFileStorage, State


def main() -> None:

    """Функция реализует работу ETL процесса."""

    address = f'http://{config.elastic_search_parameters.elastic_host}:{config.elastic_search_parameters.elastic_port}'

    etl = ETL(config.postgres_parameters.dict(), address)
    pack, begin, time, index_name = config.pack_size, 0, config.smallest_time, config.index_name

    state = State(JsonFileStorage('state.json'))
    state.set_state('time', time)
    all_dates = []

    while True:

        row_data = etl.extract(time_from_storage=time, pack_size=pack, begin=begin)
        logger.info('Data has been received.')

        if row_data:

            transformed_data, new_date = etl.transform(row_data, index_name)
            all_dates.append(new_date)
            logger.info('Data has been transformed.')

            etl.load(transformed_data)
            logger.info('Data has been loaded.')

            begin += pack

        else:
            old_date = state.get_state('time')
            state.set_state('time', max([old_date, *all_dates]))
            begin = 0
            time = state.get_state('time')

            logger.info('No packs to insert. Last update %s', time)
            sleep(10)


logger = create_logger(__file__, stream_out=sys.stdout)

if __name__ == '__main__':
    main()
