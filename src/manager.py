from typing import Self, Any, Type

from src.entity import BaseEntity, Book, StatusEnum
from src.loader import BaseFileLoader, JSONFileLoader
from src.repr_mixin import ReprMixin


class BaseManager(ReprMixin):
    """Базовый класс менеджера для работы с сущностями"""
    loader: BaseFileLoader = None
    model: Type[BaseEntity] = None
    _id: int = 1

    def __init__(self, entities: list | None = None):
        self._entities = entities or []

    def search(self, **kwargs) -> list:
        """
        Производит поиск по точному соответствию
        переданных аргументов.
        """
        sorted_entities = self._entities
        print(kwargs)
        for param, value in kwargs.items():
            sorted_entities = filter(lambda x: getattr(x, param, None) == value, sorted_entities)
        return list(sorted_entities)

    def search_with_index(self, **kwargs) -> tuple | None:
        """
        Производит поиск по точному соответствию
        переданных аргументов.
        Возвращает первую соответствующую сущность
        и ее индекс.
        """
        for index, entity in zip(range(len(self._entities)), self._entities):
            if all(getattr(entity, param, None) == value for param, value in kwargs.items()):
                return entity, index
        raise ValueError(f"Книга с {', '.join([f'{k}={v}' for k, v in kwargs.items()])} не найдена")

    @property
    def next_id(self) -> int:
        _next = self._id
        self._id += 1
        return _next

    def serialize(self) -> list[dict[str, Any]]:
        """Преобразует все сущности в словари"""
        return [entity.serialize() for entity in self._entities]

    @classmethod
    def deserialize(cls, entities: list[dict[str, Any]]) -> list[BaseEntity]:
        """Преобразует данные в список объектов Entity"""
        return [cls.model(**entity_dict) for entity_dict in entities]

    def dump(self) -> None:
        """Сериализует все сущности"""
        if not self.loader:
            raise NotImplementedError("Не установлен загрузчик")
        serialized_entities = self.serialize()
        to_dump = {
            "meta": {"next_id": self._id},
            "data": serialized_entities
        }
        self.loader.dump(to_dump)

    @classmethod
    def load(cls) -> Self:
        """Десериализует все сущности"""
        if not cls.loader:
            raise NotImplementedError("Не установлен загрузчик")
        try:
            loaded = cls.loader.load()
        except FileNotFoundError:
            return cls()
        data = loaded.get("data", [])
        cls._id = loaded.get("meta", {}).get("next_id", len(data) + 1)
        entities = cls.deserialize(data)
        return cls(entities)


class BookManager(BaseManager):
    """Менеджер для работы с книгами"""

    loader: JSONFileLoader = JSONFileLoader('../data/books.json')
    model: Type[Book] = Book

    def create(self, **data) -> Book:
        """Создает новую книгу"""
        book = self.model(id=self.next_id, status=StatusEnum.IN_STOCK, **data)
        self._entities.append(book)
        return book

    def list(self, **kwargs) -> list[Book]:
        """
        Возвращает список, отфильтрованный по точному соответствию kwargs.
        Если kwargs не были переданы - возвращает все книги.
        """
        return self.search(**kwargs)

    def update_status(self, book_id: int, status: str) -> Book:
        """Изменяет статус книги"""
        book, _ = self.search_with_index(id=book_id)
        book.status = status
        return book

    def delete(self, book_id: int) -> Book:
        """Удаляет книгу"""
        book, index = self.search_with_index(id=book_id)
        self._entities.pop(index)
        return book
