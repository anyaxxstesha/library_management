class ReprMixin:
    """
    Класс, отвечающий за repr всех дочерних объектов
    """

    def __repr__(self):
        attrs = ", ".join([f"{k}={repr(v)}" for k, v in self.__dict__.items()])
        return f'{self.__class__.__name__}({attrs})'
