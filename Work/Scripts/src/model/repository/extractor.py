import os
import pickle

from Work.Scripts.src.model.repository.interf_extractor import IDataExtractor


class DataExtractor(IDataExtractor):
    def __init__(self):
        os.chdir(r'D:\PycharmProjects\ProductsViewer\Work\Data')
        with open('db.pickle', "rb") as open_data_base:
            data_base = pickle.load(open_data_base)

        self._db_products = data_base['_db_products']
        self._db_discounts = data_base['_db_discounts']
        self._db_vouchers = data_base['_db_vouchers']
        self._db_sales = data_base['_db_sales']
        self._db_groups = data_base['_db_groups']

        file_name = 'database.txt'

    def get_data(self):
        pass
