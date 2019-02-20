from Work.Scripts.src.controller.commands import CommandSelect, CommandInsert, \
    CommandUpdate, CommandDelete

import pandas as pd
import numpy as np

from Work.Scripts.src.controller.data_validity import DataValidity
from Work.Scripts.src.controller.factory import IDBFactory, TestDbFactory
from Work.Scripts.src.model.interactor.interactors import MainTableInteractor, \
    ReportsInteractor
import Work.Scripts.src.test.extractor as test

data_validity = DataValidity()
db_factory = TestDbFactory()


class MainTableController:

    def __init__(self):
        self.main_interactor = MainTableInteractor(
            db_factory.create_table_extractor())

    def get_np_array(self):
        pass

    def get_data_frame(self):
        pass

    def get_columns_by_table(self, table):
        pass

    def select(self, command_select: CommandSelect = None):
        pass

    def insert(self, command_insert: CommandInsert):
        pass

    def update(self, command_update: CommandUpdate):
        pass

    def delete(self, command_delete: CommandDelete):
        pass

    def get_data(self):
        return self.main_interactor.get_data()


class ReportsController:

    def __init__(self):
        self.reports_interactor = ReportsInteractor(
            db_factory.create_table_extractor())

    def get_products_groups(self):
        return self.reports_interactor.get_products_groups()

    def get_quality_categories(self):
        return self.reports_interactor.get_quality_categories()

    def get_prices_by_group_and_quality(self, groups: list, quality: list):
        return self.reports_interactor.get_prices_by_group_and_quality(
            groups, quality)

    def get_products_groups(self):
        return self.reports_interactor.get_products_groups()

    def get_products_by_group(self, group: str):
        return self.reports_interactor.get_products_by_group(group)

    def get_quality_categories(self):
        return self.reports_interactor.get_quality_categories()

    def get_box_and_whisker_prices(self, product_group: str, qualities: list,
                                   products: list):
        return self.reports_interactor.get_box_and_whisker_prices(
            product_group, qualities, products)

    def get_prices_by_group(self, product_group: str, products: list):
        return self.reports_interactor.get_prices_by_group(product_group,
                                                           products)

    def get_spreading(self, product_group: str, date: str):
        return self.reports_interactor.get_spreading(product_group,
                                                     date)

    # controller = DBController()


# selector = CommandSelect()
# selector.set_columns(['Наименование', 'Цена'])
# print(controller.select(selector))

df = pd.DataFrame(np.arange(12).reshape(3, 4),
                  columns=['A', 'B', 'C', 'D'])
df = df.drop('A', axis=1)
print(df)
