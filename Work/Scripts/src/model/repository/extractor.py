import pickle

from Work.Scripts.src.model.repository.interf_extractor import IDataExtractor


class DataExtractor(IDataExtractor):

    _database = {}

    def __init__(self):
        with open(r'D:\PycharmProjects\ProductsViewer\Work\Data\db.pickle', "rb") as open_data_base:
            self._data_base = pickle.load(open_data_base)

    def get_db_products(self):
        return self._data_base['_db_products']

    def get_db_discounts(self):
        return self._data_base['_db_discounts']

    def get_db_vouchers(self):
        return self._data_base['_db_vouchers']

    def get_db_sales(self):
        return self._data_base['_db_sales']

    def get_db_groups(self):
        return self._data_base['_db_groups']
