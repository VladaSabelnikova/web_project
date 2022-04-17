"""Модуль содержит ETL процесс."""
import sys
from time import sleep

from etl_class import ETL
from log import create_logger
from models import config
from state_storage import JsonFileStorage, State


def main() -> None:

    """Функция реализует работу ETL процесса."""

    etl = ETL(config.postgres_parameters.dict(), config.elastic_search_parameters.address)
    pack, begin, time, index_name = config.pack_size, 0, config.smallest_time, config.index_name

    state = State(JsonFileStorage('state.json'))
    state.set_state('time', time)
    all_dates = []

    while True:

        row_data = etl.extract(time_from_storage=time, pack_size=pack, begin=begin)

        if row_data:

            transformed_data, new_date = etl.transform(row_data, index_name)
            all_dates.append(new_date)

            etl.load(transformed_data)
            logger.info('Recorded updated data.\nPack size %s\n', len(row_data))

            begin += pack

        else:
            old_date = state.get_state('time')
            state.set_state('time', max([old_date, *all_dates]))
            begin = 0
            time = state.get_state('time')

            logger.info('No packs to insert. Last update %s', time)
            sleep(10)


if __name__ == '__main__':

    logger = create_logger(__file__, stream_out=sys.stdout)
    main()