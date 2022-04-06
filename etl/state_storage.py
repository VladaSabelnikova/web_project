"""Файл с кодом для хранения состояния."""
import abc
import json
from pathlib import Path
from typing import Any, Optional


class BaseStorage:

    """
    Класс для определения методов сохранения и чтения.
    Он будет общим для всех типов хранилищ, будь-то json или БД.
    """

    @abc.abstractmethod
    def save_state(self, state: dict) -> None:

        """
        Сохранить состояние в постоянное хранилище.

        Args:
            state: состояние, словарь, который нужно записать в файл
        """

        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:

        """Загрузить состояние локально из постоянного хранилища."""

        pass


class JsonFileStorage(BaseStorage):

    """
    Класс для работы с файлом формата JSON.
    Реализованы запись и чтение.
    """

    def __init__(self, file_path: Optional[str] = None):

        """
        Конструктор.

        Args:
            file_path: путь до хранилища
        """

        self.file_path = file_path if file_path else ''

    def save_state(self, state: dict) -> None:

        """
        Метод сохраняет состояние (dict) в json файл.

        Args:
            state: состояние, словарь, который нужно записать в файл
        """
        json_file = Path(self.file_path)
        json_data = json.dumps(state)
        json_file.write_text(json_data)

    def retrieve_state(self) -> dict:

        """
        Метод достаёт из файла json данные и преобразует их в объект словарь.

        Returns:
            Вернёт словарь, в котором будет содержимое json.
        """

        return json.loads(Path(self.file_path).read_text())


class State:

    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):

        """
        Конструктор.

        Args:
            storage: объект типа хранилища, в нём должны быть реализованы методы чтения и записи
        """

        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:  # noqa: WPS615

        """
        Метод устанавливает состояние для определённого ключа.

        Args:
            key: ключ
            value: значение этого ключа
        """

        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:  # noqa: WPS615

        """
        Метод получает состояние по определённому ключу.

        Args:
            key: ключ, по которому нужно получить состояние

        Returns:
            Возвращает словарь по соответствующему ключу,
            если такого ключа не нашлось — None.
        """

        current_storage = self.storage.retrieve_state()
        return current_storage.get(key, None)
