from flask import Flask, render_template

from for_elastic_search import ElasticSearchMethods
from models import flask_config

app = Flask(__name__)


@app.route('/')
def index():
    data_from_es = es_methods.get_all()['hits']['hits']

    return render_template('all_videos.html', data_from_es=data_from_es)


@app.route('/<id>')
def get_by_id(id):
    return render_template('video_display.html', id=id)


def main():

    host, port = flask_config.host, flask_config.port
    app.run(host=host, port=port)


if __name__ == '__main__':
    address_es = flask_config.es_settings.elastic_address
    index_es = flask_config.es_settings.elastic_index

    es_methods = ElasticSearchMethods(address_es, index_es)

    main()
