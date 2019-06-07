"""
Модуль содержащий все команды для редактирования базы данных

Отключены следующие ошибки pylint:
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)

Автор: Перятин Виталий
"""
# pylint: disable=E0401

from abc import ABC, abstractmethod

from Work.Scripts.key_words import Expression
from Work.Scripts.ui_table_constants import \
    ProductColumns, TableNameUI


class ICommand(ABC):
    """
    Интерфейс комманды для редактирования базы данных

    Автор: Перятин Виталий
    """
    _table_name: str = None

    def set_table_name(self, table_name: str):
        """
        Выбирает таблицу для редактирования
        :param table_name: имя таблицы для редактирования

        Автор: Перятин Виталий
        """
        self._table_name = table_name

    def get_table_name(self):
        """
        Получает таблицу, которую необходимо редактировать

        Автор: Перятин Виталий
        """
        return self._table_name

    @abstractmethod
    def get_data(self):
        """
        Получает данные и выражения, которые выбрал полтзователь

        Автор: Перятин Виталий
        """



class ConditionProvider:
    """
    Хранит в себе все созданные выражения для редактирования БД
    и предоставляет их другим объектам

    Автор: Перятин Виталий
    """

    _conditions = []

    def add_condition(self, conditions: Expression):
        """
        Добавляет ыражение для редактирования БД

        :param conditions: выражение для редактирования БД

        Автор: Перятин Виталий
        """
        self._conditions[conditions.field] = conditions

    def set_conditions(self, conditions: list):
        """
        Устанавливает новый список выражений для редактирования БД

        :param conditions: список выражений для редактирования БД

        Автор: Перятин Виталий
        """
        self._conditions = conditions

    def remove_condition(self, conditions: Expression):
        """
        Удаляет выражение для редактироавния БД

        :param conditions: выражение для редактироавния БД

        Автор: Перятин Виталий
        """
        self._conditions.remove(conditions.field)

    def get_conditions(self):
        """
        Получает список выражений для редактирования БД

        :return: список выражений для редактирования БД

        Автор: Перятин Виталий
        """
        return self._conditions

    def items(self):
        """
        Разбивает выражение на составляющие

        :return: составляющие выражения для редактирования БД

        Автор: Перятин Виталий
        """
        return [(expr.field, expr.compare_op, expr.value)
                for expr in self._conditions]


class CommandSelect(ICommand, ConditionProvider):
    """
    Класс для создания команды выборки данных

    Автор: Перятин Виталий
    """
    def __init__(self, table):
        if table == TableNameUI.PRODUCTS.value:
            self._columns = list(ProductColumns.get_empty_row().keys())
            self.set_conditions([])
        else:
            self._columns = []

    def add_column(self, column: str):
        """
        Добавляет колонку по которой производится выборка данных

        :param column: название колонки

        Автор: Перятин Виталий
        """
        self._columns.append(column)

    def remove_column(self, column: str):
        """
        Удаляет колонку по которой производится выборка данных

        :param column: название колонки

        Автор: Перятин Виталий
        """
        self._columns.remove(column)

    def set_columns(self, columns: list):
        """
        Устанавливает список колонок, по которым производится выборка данных

        :param column: список иконок

        Автор: Перятин Виталий
        """
        self._columns = columns

    def get_columns(self):
        """
        Получает список колонок, по которым производится выборка данных

        :return: список колонок, по которым производится выборка данных

        Автор: Перятин Виталий
        """
        return self._columns

    def get_data(self):
        pass


class CommandInsert(ICommand):
    """
    Класс для создания команды вставки данных

    Автор: Перятин Виталий
    """
    _row = []

    def add_row(self, titled_row: dict):
        """
        Добавялет строку для вставки в БД

        :param titled_row: строка для вставки в БД

        Автор: Перятин Виталий
        """
        self._row = titled_row

    def get_row(self):
        """
        Получает строку для вставки в БД

        :return: строка для вставки в БД

        Автор: Перятин Виталий
        """
        return self._row

    def get_data(self):
        """
        Получает данные для вставки в БД

        Автор: Перятин Виталий
        """


class CommandUpdate(ICommand, ConditionProvider):
    """
    Класс для создания команды обновления данных

    Автор: Перятин Виталий
    """
    _values = {}

    def update_values(self, values: dict):
        """
        Добавляет значения, которые нужно обновить в БД

        :param values: значения, которые нужно обновить в БД

        Автор: Перятин Виталий
        """
        self._values = values

    def get_values(self):
        """
        Получает значения, которые нужно обновить в БД

        :return: значения, которые нужно обновить в БД

        Автор: Перятин Виталий
        """
        return self._values

    def get_data(self):
        """
        Получает данные для обновления в БД

        Автор: Перятин Виталий
        """


class CommandDelete(ICommand, ConditionProvider):
    """
    Класс для создания команды для удаления записей из БД

    Автор: Перятин Виталий
    """

    def get_data(self):
        """
        Получает данные для удаления записей из БД

        Автор: Перятин Виталий
        """
