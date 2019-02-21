import numpy as np
import pandas as pd

from Work.Scripts.src.controller.commands import CommandSelect, CommandInsert, \
    CommandUpdate, CommandDelete
from Work.Scripts.src.controller.data_validity import DataValidity
from Work.Scripts.src.controller.factory import TestDbFactory
from Work.Scripts.src.model.interactor.interactors import MainTableInteractor, \
    ReportsInteractor

data_validity = DataValidity()
db_factory = TestDbFactory()


class MainTableController:

    def __init__(self):
        self.main_interactor = MainTableInteractor(
            db_factory.create_table_extractor())

    def get_np_array(self):
        pass

    def get_data_frame(self):
        return self.main_interactor.get_data()

    def get_columns_by_table(self, table):
        pass

    def select(self, column_choices: dict, expressions):
        columns = []

        for col, var in column_choices.items():
            if var.get():
                columns.append(col)

        if not columns:
            print("Не выбраны колонки")
        elif expressions is None:
            print("Не заполнены условия")
        else:
            selector = CommandSelect()
            selector.set_columns(columns)
            selector.set_conditions(expressions)
            return self.main_interactor.select(selector)
        return None

    def insert(self, col_to_values: dict):
        is_full_row = True
        row = []
        for val in col_to_values.values():
            if not val.get():
                val.master['bg'] = 'yellow'
                is_full_row = False
            else:
                val.master['bg'] = 'white'
                row.append(val.get())
        if is_full_row:
            inserter = CommandInsert()
            inserter.add_row(row)
            self.main_interactor.insert(inserter)

    def update(self, set_frames: list, expressions: list):
        values = {}
        updater = CommandUpdate()
        for set_frame in set_frames:
            values.update(set_frame.get_col_to_value())
        if values:
            updater.update_values(values)
            self.main_interactor.update(updater)

        if not values:
            print("Не заполнены значения")
        elif expressions is None:
            print("Не заполнены условия")
        else:
            updater.update_values(values)
            updater.set_conditions(expressions)
            self.main_interactor.update(updater)

    def delete(self, expressions):
        if expressions is None:
            print("Не заполнены условия")
        else:
            deleter = CommandDelete()
            deleter.set_conditions(expressions)
            self.main_interactor.delete(deleter)

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
