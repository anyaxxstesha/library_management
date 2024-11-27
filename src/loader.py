from typing import Any
import json

from src.repr_mixin import ReprMixin


class BaseFileLoader(ReprMixin):
    """Базовый класс для работы с файлом"""

    def __init__(self, filename: str, **kwargs):
        self.filename = filename

    def dump(self, data: Any) -> None:
        """Записывает данные в файл"""
        raise NotImplementedError

    def load(self) -> Any:
        """Получает данные из файла"""
        raise NotImplementedError


class JSONFileLoader(BaseFileLoader):
    """Класс для работы с json файлом"""

    def dump(self, data: Any) -> None:
        """Записывает данные в json файл"""
        with open(self.filename, 'w') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))


    def load(self) -> Any:
        """Получает данные из json файла"""
        with open(self.filename, 'r') as file:
            return json.loads(file.read())
