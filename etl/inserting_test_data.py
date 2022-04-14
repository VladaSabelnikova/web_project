import psycopg2

from etl.models import config

INSERT = """
INSERT INTO content.video
    (id, created_at, title, h1, description, updated_at, audio_track_id, lang, video_track_id)
VALUES (
        gen_random_uuid(),
        '2022-04-13 18:25:09.308911+00:00',
        'Видео № {}',
        'h1',
        'описание',
        '2022-04-13 18:25:09.308911+00:00',
        '359530ef-8c7a-4122-b3ac-e50923ecc6c8',
        'b31ee168-c1c5-41f4-a08c-0e1f0405b9cc',
        'b323351d-c69a-4073-bc62-c63d3a20a6ca'
        )
"""


def main():
    with psycopg2.connect(**config.postgres_parameters.dict()) as con_postgres:
        cur_postgres = con_postgres.cursor()
        for i in range(20_000, 30_000):
            insert = INSERT.format(i)
            cur_postgres.execute(insert)


if __name__ == '__main__':
    main()
