import pandas as pd
from pandas import DataFrame, np

from Work.Scripts.src.model.repository.interf_extractor import IDataExtractor


class DataExtractor(IDataExtractor):
    # def get_data(self):
    #     tables = {
    #         'products': DataFrame(self.get_table_products()[1:],
    #                               columns=self.get_table_products()[0]),
    #         'producers': DataFrame(columns=['id', 'Наименование']),
    #         'groups': DataFrame(columns=['id', 'Наименование']),
    #         'discounts': DataFrame(columns=['id', 'Наименование']),
    #         'checks': DataFrame(columns=['id', 'Наименование']),
    #         'sales': DataFrame(columns=['id', 'Наименование']),
    #     }
    #     return tables

    def get_data(self):
        data = np.array([
            ["Наименование", "Цена", "Группа", "Производитель", "Качество",
             "Чек", "Дата"],
            ["Молоко", 50, "Молочное", "Вимм-билль-данн", "ГОСТ", 14423,
             "19.02.19"],
            ["Хлеб", 40, "Бакалея", "Хлебушек", "ГОСТ", 14413,
             "19.02.19"],
            ["Кефир", 70, "Молочное", "Вимм-билль-данн", "ГОСТ", 12413,
             "19.02.19"]
        ])
        return pd.DataFrame(data[1:], columns=data[0])
