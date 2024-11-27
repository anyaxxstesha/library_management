from dataclasses import dataclass
from enum import Enum
from typing import Self, Any

from src.repr_mixin import ReprMixin


class BaseEntity(ReprMixin):
    """Базовый класс сущности"""

    def __init__(self, **kwargs) -> None:
        """Инициализатор экземпляра класса"""

        for field_name in self.__annotations__.keys():
            value = kwargs.get(field_name, ...)
            setattr(self, field_name, value)

    def __setattr__(self, key: str, value: Any) -> None:
        """Переопределяет метод __setattr__ для валидации значений полей"""
        self._validate(key, value)
        super().__setattr__(key, value)

    def _validate(self, field_name: str, value: Any = ...) -> Any:
        """Валидация поля по имени и значению"""
        if value is ...:
            raise ValueError(f"Пропущено обязательное поле: {field_name}")

        field_type = self.__class__.__annotations__.get(field_name, ...)
        if not isinstance(value, field_type):
            try:
                value = field_type(value)
            except TypeError as exc:
                raise TypeError(
                    f"Некорректный тип для поля: {field_name}"
                    f" (ожидалось {field_type.__name__}, получено {value.__class__.__name__})")  from exc
        return value

    def serialize(self) -> dict[str, Any]:
        """Преобразует экземпляр класса в словарь"""
        serialized = {}
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, Enum):
                field_value = field_value.value
            serialized[field_name] = field_value
        return serialized

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> Self:
        """Создает экземпляр класса из словаря"""
        return cls(**data)


class StatusEnum(Enum):
    """Статусы книг"""

    IN_STOCK = "В наличии"
    ISSUED = "Выдана"


class Book(BaseEntity):
    """Класс книги"""

    id: int
    title: str
    author: str
    year: int
    status: StatusEnum

    def __str__(self):
        return f"id: {self.id} | {self.title} by {self.author}, {self.year}, status: {self.status}"
