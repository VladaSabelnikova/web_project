CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.langs (
    id uuid NOT NULL
        CONSTRAINT langs_pk
            PRIMARY KEY,
    full_title TEXT NOT NULL,
    iso_639_1 TEXT NOT NULL,
    iso_639_2 TEXT,
    created_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.video (
    id uuid NOT NULL
        CONSTRAINT video_pk
            PRIMARY KEY,
    path_to_video TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);


CREATE TABLE IF NOT EXISTS content.audio_and_text (
    id uuid NOT NULL
        CONSTRAINT audio_and_text_pk
            PRIMARY KEY,
    id_video uuid NOT NULL
        CONSTRAINT audio_and_text_id_video___fk
            REFERENCES content.video,
    path_to_audio TEXT NOT NULL,
    title TEXT NOT NULL,
    h1 TEXT NOT NULL,
    description TEXT NOT NULL,
    lang uuid NOT NULL
        CONSTRAINT audio_and_text_lang___fk
            REFERENCES content.langs
);

CREATE UNIQUE INDEX IF NOT EXISTS audio_and_text_title_uindex
    ON content.audio_and_text (title);

CREATE UNIQUE INDEX audio_and_text_description_uindex
    ON content.audio_and_text (description);
