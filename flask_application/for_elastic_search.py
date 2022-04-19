from elasticsearch import Elasticsearch


class ElasticSearchMethods:

    def __init__(self, address, index_name):
        self.address, self.index_name = address, index_name
        self.es = Elasticsearch(self.address)

    def get_all(self):
        return self.es.search(index=self.index_name, query={'match_all': {}})

    def get_by_id(self, id: str):
        return self.es.get(index=self.index_name, id=id)['_source']
