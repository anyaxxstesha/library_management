from src.manager import BookManager
from src.repr_mixin import ReprMixin


class App(ReprMixin):
    """Основной класс, реализующий взаимодействие с пользователем."""
    manager: BookManager

    def start(self):
        """Запускает приложение"""
        self.manager = BookManager.load()
        try:
            #self.manager = BookManager.load()
            self.interact()
        finally:
            self.manager.dump()

    def interact(self):
        """Основное меню приложения"""
        while True:
            print("\nВыберите действие:")
            print("1. Создать книгу")
            print("2. Найти книгу/книги по названию, автору или году издания")
            print("3. Просмотреть список всех книг")
            print("4. Изменить статус книги")
            print("5. Удалить книгу")
            print("0. Выйти")
            try:

                choice = self.cast_int(input("Ваш выбор: "))

                if choice == 1:
                    self.create()
                elif choice == 2:
                    self.sorted_list()
                elif choice == 3:
                    self.list()
                elif choice == 4:
                    self.update_status()
                elif choice == 5:
                    self.delete()
                elif choice == 0:
                    break
                else:
                    print("Неверный ввод. Попробуйте снова.")
            except (ValueError, TypeError) as exc:
                print(f"Ошибка: {exc.args[0]}")

    def create(self):
        """Создает экземпляр книги и выводит пользователю сообщение об успешном создании"""
        print("Введите данные для создания книги:")
        title = input("Название: ")
        author = input("Автор: ")
        year = self.cast_int(input("Год издания, e.g. 1894: "))
        result = self.manager.create(title=title, author=author, year=year)

        print(f"Создана книга: {result}")

    def sorted_list(self):
        """Выводит пользователю список всех книг, соответствующих определенным параметрам"""
        print("Введите данные для поиска книг(title, author, year - поиск как по одному параметру,"
              " так и по любой комбинации данных параметров, не нужный параметр пропустить, нажав Enter):")
        title = input("Название: ")
        author = input("Автор: ")
        year = self.cast_int(input("Год издания, e.g. 1894: "), raise_exception=False)

        search_params = {}
        if title:
            search_params['title'] = title
        if author:
            search_params['author'] = author
        if year:
            search_params['year'] = year

        result = self.manager.search(**search_params)

        print(f"Найдены книги:")
        self.pretty_list(result)

    def list(self):
        """Выводит пользователю список всех книг"""

        result = self.manager.search()

        print(f"Все имеющиеся книги:")
        self.pretty_list(result)

    def update_status(self):
        """Выводит пользователю книгу после изменения ее статуса"""
        print("Введите данные для изменения статуса книги:")
        book_id = self.cast_int(input("id книги: "))
        status = input("Статус(доступны две опции 'В наличии' и 'Выдана', введите одну из них): ")

        result = self.manager.update_status(book_id, status)

        print(f"Книга после изменений: {result}")

    def delete(self):
        """Выводит пользователю удаленную книгу"""
        print("Введите данные для удаления книги:")
        book_id = self.cast_int(input("id книги: "))

        result = self.manager.delete(book_id)

        print(f"Удалена книга: {result}")

    @staticmethod
    def cast_int(input_value, raise_exception=True) -> int:
        try:
            return int(input_value)
        except ValueError as exc:
            if raise_exception:
                raise ValueError("Ошибка ввода: ожидалось число.") from exc

    @staticmethod
    def pretty_list(_list: list) -> None:
        print("\n".join([f"    {str(book)}" for book in _list]))
