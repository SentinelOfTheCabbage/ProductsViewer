"""
Модуль для хранения констант UI таблицы

Автор: Перятин Виталий
"""
# pylint: disable=E1101
from enum import Enum


class TableNameUI(Enum):
    """
    Хранит имена таблиц

    Автор: Перятин Виталий
    """
    PRODUCTS = "Продукты"
    VOUCHERS = "Чеки"


class IColumnsName(Enum):
    """
    Содержит имена столбцов для каждой из таблицы

    Автор: Перятин Виталий
    """


class VoucherColumns(IColumnsName):
    """
    Содержит имена столбцов для таблицы скидок

    Автор: Перятин Виталий
    """
    NAME = "Наименование"
    TOTAL = "Итого"


class ProductColumns(IColumnsName):
    """
    Содержит имена столбцов для таблицы продуктов

    Автор: Перятин Виталий
    """

    NAME = "Наименование"
    PRICE = "Цена"
    PRODUCER_NAME = "Производитель"
    GROUP_NAME = "Группа продукта"
    DISCOUNT_NAME = "Скидка"
    QUALITY = "Категория качества"

    @staticmethod
    def get_empty_row():
        """
        Возвращает пустую таблицу

        :return: Пустая таблица с названием столбцов

        Автор: Перятин Виталий
        """
        return {
            ProductColumns.NAME: None,
            ProductColumns.PRICE: None,
            ProductColumns.PRODUCER_NAME: None,
            ProductColumns.GROUP_NAME: None,
            ProductColumns.DISCOUNT_NAME: None,
            ProductColumns.QUALITY: None
        }
