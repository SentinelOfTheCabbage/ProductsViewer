"""
Содержит константы для работы с базой данных

Автор: Перятиин Виталий
"""
from enum import Enum


class TableName(Enum):
    """
    Константы с названиями таблицы

    Автор: Перятин Виталий
    """
    PRODUCTS = "Products"
    VOUCHERS = "Vouchers"


class ProductsColumn(Enum):
    """
    Константы с названиями столбцов

    Автор: Перятин Виталий
    """
    ID = "id"
    NAME = "name"
    PRICE = "price"
    PRODUCER_NAME = "producer_name"
    GROUP_NAME = "group_name"
    DISCOUNT_NAME = "discount_id"
    QUALITY = "quality"

    @staticmethod
    def get_columns():
        """
        Получает список названий столбца
        :return: список значений столбца

        Автор: Перятин Виталий
        """
        return [
            ProductsColumn.ID,
            ProductsColumn.NAME,
            ProductsColumn.PRICE,
            ProductsColumn.PRODUCER_NAME,
            ProductsColumn.GROUP_NAME,
            ProductsColumn.DISCOUNT_NAME,
            ProductsColumn.QUALITY
        ]


class VouchersColumn(Enum):
    """
    Класс, содержащий, константы для работы с таблицей чеков

    Автор: Перятин Виталий
    """
    ID = "id"
    DATE = "date"
    TIME = "time"
    TOTAL = "total"

    @staticmethod
    def get_columns():
        """
        Получает список названий столбцов
        :return: список названий столбцов

        Автор: Перятин Виталий
        """
        return [
            VouchersColumn.ID,
            VouchersColumn.DATE,
            VouchersColumn.TIME,
            VouchersColumn.TOTAL
        ]
