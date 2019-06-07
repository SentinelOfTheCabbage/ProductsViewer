"""
Модуль соддержащий абстракцию для извлечения
таблиц из файла

Автор: Перятин Виталий
"""
# pylint: disable=R0903
from abc import ABC


class IDataExtractor(ABC):
    """
    Интерфейс для извлечения данных

    Автор: Перятин Виталий
    """
    _db_products: dict
    _db_discounts: dict
    _db_vouchers: dict
    _db_sales: dict
    _db_groups: dict
    _db_producers: dict
