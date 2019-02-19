import pandas as pd
import numpy as np

from Work.Scripts.src.controller.commands import CommandSelect, CommandInsert, \
    CommandUpdate, CommandDelete
from Work.Scripts.src.controller.key_words import CompareOp, Expression


class MainTableInteractor:
    selector = CommandSelect()
    df = pd.DataFrame()
    select_df = pd.DataFrame()

    def __init__(self):
        self.df = self.get_data_frame()


    def get_np_array(self):
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
        return data

    def get_data(self, row_filter, column_filter):
        data = [
            ["Наименование", "Цена", "Группа", "Производитель", "Качество",
             "Чек", "Дата"],
            ["Молоко", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль"],

        ]
        return data

    def get_data_frame(self):
        df = pd.DataFrame(self.get_np_array()[1:],
                          columns=self.get_np_array()[0])
        return df

    def get_columns_by_table(self, table):
        data = []
        if table == "Продукты":
            data = ['Наименование', 'Цена', 'Качество', 'Производитель']
        elif table == "Чеки":
            data = []
        return data

    def select(self, command_select: CommandSelect = None):
        if not(command_select is None):
            self.selector = command_select
        drop_list = [item for item in self.df.columns.values if item not in
                     self.selector.get_columns()]
        self.select_df = self.df.drop(drop_list, axis=1)
        for col, op, val in self.selector.items():
            self.select_df = self.select_df[self.filter(
                self.select_df, col, op, val)]
        return self.select_df

    @staticmethod
    def get_type_of(series: pd.Series):
        if series.array:
            try:
                float(series.array[0])
                return float
            except:
                return str
        return None

    @staticmethod
    def filter(df: pd.DataFrame, field, compare_op: str, value):
        def get_type_of(series: pd.Series):
            if series.array:
                try:
                    float(series.array[0])
                    return float
                except:
                    return str
            return None

        field_val = df[field].astype(get_type_of(df[field]))
        return {
            CompareOp.EQUAL: field_val == value,
            CompareOp.NOT_EQUAL: field_val != value,
            CompareOp.LESS: field_val < value,
            CompareOp.LESS_OR_EQUAL: field_val <= value,
            CompareOp.MORE: field_val > value,
            CompareOp.MORE_OR_EQUAL: field_val >= value
        }[compare_op]

    def insert(self, command_insert: CommandInsert):
        index = self.df.index[-1] + 1
        self.df.loc[index] = command_insert.get_row()
        return self.select()

    def update(self, command_update: CommandUpdate):
        command_update.get_values()
        for col, op, val in command_delete.items():
            for field, set_val in command_update.get_values().items():
                self.df.loc[self.filter(
                    self.df, col, op, val
                ), field] = set_val

    def delete(self, command_delete: CommandDelete):
        # for col, op, val in command_delete.items():
        #     self.df = self.df.drop(np.where(
        #         self.filter(self.df, self.df[col].astype(
        #             self.get_type_of(self.df[col])
        #         ), op, val))[0])
        return self.select()


inter = MainTableInteractor()
selector = CommandSelect()
exprs = [
    # Expression('Наименование', CompareOp.EQUAL, "Молоко"),
    # Expression('Цена', CompareOp.MORE, 60),
]
selector.set_conditions(exprs)
selector.set_columns(['Наименование', 'Цена', 'Качество'])
inter.select(selector)
command_delete = CommandDelete()

exprs_delete = [
    Expression('Цена', CompareOp.MORE, 60)
]
command_delete.set_conditions(exprs_delete)
print(inter.delete(command_delete))
