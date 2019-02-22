import copy

import pandas as pd
import numpy as np

from Work.Scripts.src.controller.commands import CommandSelect, CommandInsert, \
    CommandUpdate, CommandDelete
from Work.Scripts.src.controller.key_words import CompareOp, Expression



# Метод/функция для получения средних цен по выбранным категориям
# продуктов и выбранному качеству
import random

from Work.Scripts.src.model.repository.DB_constants import TableName
from Work.Scripts.src.model.repository.interf_extractor import IDataExtractor


class ReportsInteractor:

    def __init__(self, extractor: IDataExtractor):
        self.extractor = extractor

    def get_prices_by_group_and_quality(self, groups: list, quality: list):
        data = {}
        for group in groups:
            data[group] = [random.randint(10, 100) for _ in
                           range(len(quality))]
        return data

    def get_prices_by_group(self, product_group: str, products: list):
        data = [random.randint(10, 100) for _ in range(len(products))]
        return data

    def get_box_and_whisker_prices(self, product_group: str, qualities: list,
                                   products: list):
        data = {}
        for quality in qualities:
            data[quality] = [random.randint(10, 100) for _ in range(20)]
        print(data)
        return data

    def get_spreading(self, product_group: str, date: str):

        def get_random_point():
            return {
                'price': random.randint(10, 100),
                'amount': random.randint(10, 100)
            }

        data = [get_random_point() for _ in range(20)]
        return data

    def get_products_groups(self):
        data = ["Ягоды", "Картошка", "Зёрна",
                "Мясо", "Для беременных",
                "Деликатесы",
                "Птица", "Рыба", "Хлеб",
                "Молочное", "Овощи",
                "Фрукты и ягоды"]
        return data

    def get_quality_categories(self):
        data = ["ГОСТ", "СТО", "ТУ"]
        return data

    def get_products_by_group(self, group: str):
        data = ["Молоко 'М'", "Молоко 'Простоквашино' ",
                "Кефир 'Домик в деревне'", "Творог 'Домик в деревне' "]
        return data


def get_columns_by_table(table):
    data = []
    if table == "Продукты":
        data = ['Наименование', 'Цена', 'Качество', 'Производитель']
    elif table == "Чеки":
        data = []
    return data


class MainTableInteractor:
    df = pd.DataFrame()
    select_df = pd.DataFrame()

    def __init__(self, extractor: IDataExtractor):
        self.extractor = extractor
        self.df = self.get_data()
        self.selector = CommandSelect(TableName.PRODUCTS.value)

    def get_data(self):
        return self.extractor.get_data()

    def set_data(self, data: pd.DataFrame):
        self.df = data

    def select(self, command_select: CommandSelect = None):
        if not(command_select is None):
            self.selector = command_select
        drop_list = [item for item in self.df.columns.values if item not in
                     self.selector.get_columns()]
        self.select_df = self.df.drop(drop_list, axis=1)
        for col, op, val in self.selector.items():
            self.select_df = self.select_df[self._filter(
                self.select_df, col, op, val)]
        return self.select_df

    @staticmethod
    def _filter(df: pd.DataFrame, field, compare_op: str,
                value, reverse=False):
        def get_type_of(series: pd.Series):
            if series.array:
                try:
                    float(series.array[0])
                    float(value)
                    return float
                except:
                    return str
            return None

        def reverse_op(op):
            return {
                CompareOp.EQUAL.value: CompareOp.NOT_EQUAL.value,
                CompareOp.NOT_EQUAL.value: CompareOp.EQUAL.value,
                CompareOp.LESS.value: CompareOp.MORE_OR_EQUAL.value,
                CompareOp.LESS_OR_EQUAL.value: CompareOp.MORE.value,
                CompareOp.MORE.value: CompareOp.LESS_OR_EQUAL.value,
                CompareOp.MORE_OR_EQUAL.value: CompareOp.LESS.value
            }[op]

        data_type = get_type_of(df[field])
        value = data_type(value)
        field_val = df[field].astype(data_type)
        if reverse:
            compare_op = reverse_op(compare_op)
        return {
                CompareOp.EQUAL.value: field_val == value,
                CompareOp.NOT_EQUAL.value: field_val != value,
                CompareOp.LESS.value: field_val < value,
                CompareOp.LESS_OR_EQUAL.value: field_val <= value,
                CompareOp.MORE.value: field_val > value,
                CompareOp.MORE_OR_EQUAL.value: field_val >= value
            }[compare_op]

    def insert(self, command_insert: CommandInsert):
        row = command_insert.get_row()
        self.df = self.df.append(row, ignore_index=True)
        return row.values()

    def update(self, command_update: CommandUpdate):
        command_update.get_values()
        for col, op, val in command_update.items():
            for field, set_val in command_update.get_values().items():
                self.df.loc[self._filter(
                    self.df, col, op, val
                ), field] = set_val
        return self.select(self.selector)

    def delete(self, command_delete: CommandDelete):
        for col, op, val in command_delete.items():
            self.df = self.df[self._filter(self.df, col, op, val, True)]
        return self.select(self.selector)

    def get_vals_by_col(self, column: str):
        vals = list(set(self.df[column].tolist()))
        vals.sort()
        return vals

    def get_db_copy(self):
        return copy.deepcopy(self.df)
