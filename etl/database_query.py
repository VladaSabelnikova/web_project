"""
Модуль содержит шаблонный запрос к базе данных, нужный для ETL в момент extract.
Константу SELECT_FROM_PG мы будем использовать как форматную строку,
именно по этой причине в строке у нас есть фигурные скобки.
"""

SELECT_FROM_PG = """  
    SELECT
        v.title,
        v.description,
        v.h1,
        at.audio_file,
        vt.video_file,
        v.updated_at > {} as data_changed,
        at.updated_at > {} OR vt.updated_at > {} as track_changed,
        GREATEST(v.updated_at, at.updated_at, vt.updated_at) as max_date

    FROM content.video v
    LEFT JOIN content.audio_track at on at.id = v.audio_track_id
    LEFT JOIN content.video_track vt on vt.id = v.video_track_id
    WHERE
        v.updated_at > {} OR
        at.updated_at > {} OR
        vt.updated_at > {}
    LIMIT {} OFFSET {}
"""
