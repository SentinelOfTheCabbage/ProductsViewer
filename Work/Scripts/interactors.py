"""docstring_peryatin
Отключены следующие ошибки pylint:
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)
    R0201 - Ошибка использования self в некоторых методах класса
"""
# pylint: disable=E0401
# pylint: disable=R0201
from pandas import DataFrame, Series

from Work.Scripts.db_controller import MainTableController, \
    ReportsController


class ListMainTableInteractor(MainTableController):
    """docstring_peryatin
    """
    def __init__(self, save_curr_state=False):
        """docstring_peryatin
        """
        super().__init__(save_curr_state)

    def tolist(self, d_f: DataFrame):
        """docstring_peryatin
        """
        if (d_f is not None) and (isinstance(d_f, DataFrame)):
            full_list = d_f.values.tolist()
            full_list.insert(0, d_f.columns.tolist())
            return full_list
        return None

    def get_columns_by_table(self, table):
        """docstring_peryatin
        """
        return self.tolist(super().get_columns_by_table(table))

    def select(self, column_choices: dict, expressions):
        """docstring_peryatin
        """
        event = super().select(column_choices, expressions)
        event.data = self.tolist(event.data)
        return event

    def get_products_groups(self):
        """docstring_peryatin
        """
        return list(super().get_products_groups())

    def get_qualities(self):
        """Return quality_list"""
        return list(super().get_qualities())

    def get_producers(self):
        """Return performers"""
        return list(super().get_producers())

    def get_products_names(self):
        """Return product names"""
        return list(super().get_products_names())

    def get_max_price(self):
        """Return product names"""
        return super().get_max_price()

    def get_max_discount(self):
        """Return product names"""
        return super().get_max_discount()

    def update(self, set_frames: list, expressions: list):
        """docstring_peryatin
        """
        event = super().update(set_frames, expressions)
        event.data = self.tolist(event.data)
        return event

    def delete(self, expressions):
        """docstring_peryatin
        """
        event = super().delete(expressions)
        event.data = self.tolist(event.data)
        return event

    def get_data(self):
        """docstring_peryatin
        """
        return self.tolist(super().get_data_frame())[:100]


class ListReportsAdapter(ReportsController):
    """docstring_peryatin
    """
    def __init__(self):
        """docstring_peryatin
        """
        super().__init__()
    def tolist(self, series: Series):
        """docstring_peryatin
        """
        if (series is not None) and (isinstance(series, Series)):
            return series.tolist()
        return None
    def get_products_groups(self):
        """docstring_peryatin
        """
        return self.tolist(super().get_products_groups())
