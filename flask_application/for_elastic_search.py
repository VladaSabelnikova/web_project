"""Модуль с интерфейсом, для работы с ES."""
from typing import Dict, Any

from elasticsearch import Elasticsearch


class ElasticSearchMethods:

    """Класс, с интерфейсом для работы с API ES."""

    def __init__(self, address: str, index_name: str) -> None:

        """
        Конструктор.

        Args:
            address: адрес до ES.
            index_name: название индекса ES.
        """

        self.address, self.index_name = address, index_name
        self.es = Elasticsearch(self.address)

    def get_all(self) -> Dict[str, Any]:

        """
        Метод достаёт из ES все данные.

        Returns:
            Вернёт словарь, содержащий все документы.
        """

        return self.es.search(index=self.index_name, query={'match_all': {}})

    def get_by_id(self, id: str) -> Dict[str, Any]:  # noqa: WPS125

        """
        Метод достаёт из ES документ по его id.

        Args:
            id: id желаемого документа

        Returns:
            Вернёт словарь-документ.
        """

        return self.es.get(index=self.index_name, id=id)['_source']
