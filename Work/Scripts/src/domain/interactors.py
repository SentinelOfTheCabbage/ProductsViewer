from pandas import DataFrame, Series

from Work.Scripts.src.model.repository.db_controller import MainTableController, \
    ReportsController


class ListMainTableInteractor(MainTableController):
    def __init__(self, save_curr_state=False):
        super().__init__(save_curr_state)

    def tolist(self, df: DataFrame):
        if (df is not None) and (isinstance(df, DataFrame)):
            full_list = df.values.tolist()
            full_list.insert(0, df.columns.tolist())
            return full_list

    def get_columns_by_table(self, table):
        return self.tolist(super().get_columns_by_table(table))

    def select(self, column_choices: dict, expressions):
        event = super().select(column_choices, expressions)
        event.data = self.tolist(event.data)
        return event

    def update(self, set_frames: list, expressions: list):
        event = super().update(set_frames, expressions)
        event.data = self.tolist(event.data)
        return event

    def delete(self, expressions):
        event = super().delete(expressions)
        event.data = self.tolist(event.data)
        return event

    def prev_state(self):
        event = super().prev_state()
        event.data = self.tolist(event.data)
        return event

    def next_state(self):
        event = super().next_state()
        event.data = self.tolist(event.data)
        return event

    def get_data(self):
        return self.tolist(super().get_data_frame())[:100]


class ListReportsAdapter(ReportsController):

    def __init__(self):
        super().__init__()

    def tolist(self, series: Series):
        if (series is not None) and (isinstance(series, Series)):
            return series.tolist()

    def get_products_groups(self):
        return self.tolist(super().get_products_groups())

