import pandas as pd
import numpy as np

from Work.Scripts.src.controller.commands import CommandSelect, CommandInsert, \
    CommandUpdate, CommandDelete
from Work.Scripts.src.controller.key_words import CompareOp, Expression


class MainTableInteractor:
    def __init__(self):
        pass

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
        df = pd.DataFrame(data=self.get_np_array()[1:],
                          columns=self.get_np_array()[0])
        return df

    def get_columns_by_table(self, table):
        data = []
        if table == "Продукты":
            data = ['Наименование', 'Цена', 'Качество', 'Производитель']
        elif table == "Чеки":
            data = []
        return data

    def select(self, command_select: CommandSelect):
        df = inter.get_data_frame()
        drop_list = [item for item in df.columns.values if item not in
                     command_select.get_columns()]
        df = df.drop(drop_list, axis=1)
        print(df)
        for col, op, val in command_select.items():
            df = df[self.filter(df[col], op, val)]
        return df

    @staticmethod
    def filter(field: str, compare_op: str, value):
        return {
            CompareOp.EQUAL: field == value,
            CompareOp.NOT_EQUAL: field != value,
            CompareOp.LESS: field < value,
            CompareOp.LESS_OR_EQUAL: field <= value,
            CompareOp.MORE: field > value,
            CompareOp.MORE_OR_EQUAL: field >= value
        }[compare_op]

    def insert(self, command_insert: CommandInsert):
        print(command_insert)

    def update(self, command_update: CommandUpdate):
        print(command_update)

    def delete(self, command_delete: CommandDelete):
        print(command_delete)


inter = MainTableInteractor()
selector = CommandSelect()
exprs = [
    Expression('Цена', CompareOp.MORE, 6),
    Expression('Наименование', CompareOp.MORE, 7),
]
selector.set_conditions(exprs)
selector.set_columns(['Наименование', 'Цена'])

print(inter.select(selector))
