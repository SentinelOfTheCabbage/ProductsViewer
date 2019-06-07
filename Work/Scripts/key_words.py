"""
Модуль для преобразования выражений Expression в Boolean выражения

Автор: Перятин Виталий
"""

from enum import Enum


class CompareOp(Enum):
    """
    Операции сравнения

    Автор: Перятин Виталий
    """
    EQUAL = "="
    NOT_EQUAL = "!="
    LESS = "<"
    LESS_OR_EQUAL = "<="
    MORE = ">"
    MORE_OR_EQUAL = ">="


class Expression:
    """
    Выражение для редактирования БД

    Автор: Перятин Виталий
    """

    def __init__(self, field: str, compare_op: CompareOp, value):
        self.field = field
        self.compare_op = compare_op
        self.value = value

    def set_field(self, field):
        """
        Устанавливает новое поле в выражение

        :param field: поле

        Автор: Перятин Виталий
        """
        self.field = field

    def set_compare_op(self, compare_op):
        """
        Устанавливает в выражение операцию сравнения

        :param compare_op: операция сравнения

        Автор: Перятин Виталий
        """
        self.compare_op = compare_op

    def set_value(self, value):
        """
        Устанавливает значение в выражение

        :param value: значение

        Автор: Перятин Виталий
        """
        self.value = value

    def get_expression(self):
        """
        Возвращает построенное выражение

        :return: выражение

        Автор: Перятин Виталий
        """
        return self.field, self.compare_op, self.value
