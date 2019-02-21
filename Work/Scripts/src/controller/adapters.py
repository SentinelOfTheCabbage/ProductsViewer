from pandas import DataFrame

from Work.Scripts.src.controller.commands import CommandDelete, CommandUpdate, \
    CommandInsert, CommandSelect
from Work.Scripts.src.controller.db_controller import MainTableController


class ListMainTableAdapter(MainTableController):
    def __init__(self):
        super().__init__()

    def tolist(self, df: DataFrame):
        full_list = df.values.tolist()
        full_list.insert(0, df.columns.tolist())
        return full_list

    def get_columns_by_table(self, table):
        return self.tolist(super().get_columns_by_table(table))

    def select(self, column_choices: dict, expressions):
        df = super().select(column_choices, expressions)
        if df is not None:
            return self.tolist(df)
        else:
            return None

    def insert(self, col_to_values: dict):
        return self.tolist(super().insert(col_to_values))

    def update(self, set_frames: list, expressions: list):
        return self.tolist(super().update(set_frames, expressions))

    def delete(self, expressions):
        return self.tolist(super().delete(expressions).values.tolist())

    def get_data(self):
        return self.tolist(super().get_data_frame())
