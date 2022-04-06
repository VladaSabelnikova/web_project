import os
import sys

import psycopg2
from dotenv import load_dotenv

from etl.backoff_function import backoff
from etl.log import create_logger

load_dotenv()


@backoff()
def conn() -> psycopg2.extensions.connection:

    """
    Тест backoff.

    Returns: connection

    """

    connection = psycopg2.connect(
        host='localhost',
        port=5433,  # noqa: WPS432
        password=os.getenv('DB_PASSWORD'),
        user=os.getenv('DB_USER'),
        dbname=os.getenv('DB_NAME')
    )

    logger.info('Всё ок!')

    return connection


if __name__ == '__main__':
    logger = create_logger(__name__, stream_out=sys.stderr)
    conn()
