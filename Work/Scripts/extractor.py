"""
Модуль для извлечения данных из БД

Автор: Перятин Виталий
Отключены следующие ошибки pylint:
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)
    R0903 - Ошибка количества методов в классе
"""
# pylint: disable=E0401
# pylint: disable=R0903

import os
import pickle

from Work.Scripts.conf import ROOT_DIR
from Work.Scripts.interf_extractor import IDataExtractor


class DataExtractor(IDataExtractor):
    """
    Извлекает данные из БД

    Автор: Перятин Виталий
    """
    def __init__(self):
        os.chdir(ROOT_DIR + r'\Data')
        with open('db.pickle', "rb") as open_data_base:
            data_base = pickle.load(open_data_base)

        self._db_products = data_base['_db_products']
        self._db_discounts = data_base['_db_discounts']
        self._db_vouchers = data_base['_db_vouchers']
        self._db_sales = data_base['_db_sales']
        self._db_groups = data_base['_db_groups']
        self._db_producers = data_base['_db_producers']

    def get_data(self):
        """
        Получает данные из БД

        Автор: Перятин Виталий
        """
