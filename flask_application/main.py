"""Модуль содержит ручки для flask."""
from flask import Flask, render_template

from for_elastic_search import ElasticSearchMethods
from flask_models import flask_config
from waitress import serve

app = Flask(__name__)


@app.route('/')
def index() -> str:

    """
    Функция по ручке «root».

    Returns:
        Вернёт html содержащий все данные из ES.
    """

    data_from_es = es_methods.get_all()['hits']['hits']

    return render_template('all_videos.html', data_from_es=data_from_es, title='Главная')


@app.route('/<id>')
def get_by_id(id: str) -> str:  # noqa: WPS125

    """
    Функция по ручке /<id>.

    Args:
        id: id видео, которое нам хочется посмотреть

    Returns:
        Вернёт html содержащий видео, пригодное для просмотра.
    """

    data = es_methods.get_by_id(id)
    h1, title, description = data['h1'], data['title'], data['description']

    return render_template('video_display.html', id=id, title=title, h1=h1, description=description)


def main() -> None:

    """Запускаем сервер."""

    host, port = flask_config.host, flask_config.port
    serve(app, port=port, host=host)


if __name__ == '__main__':
    address_es = flask_config.es_settings.elastic_address
    index_es = flask_config.es_settings.elastic_index

    es_methods = ElasticSearchMethods(address_es, index_es)

    main()
