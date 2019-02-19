from Work.Scripts.src.controller.commands import CommandSelect
from Work.Scripts.src.test.main_table_interactor import MainTableInteractor

import pandas as pd
import numpy as np


class DBController:
    selector = CommandSelect()
    main_table_interactor = MainTableInteractor()

    def __init__(self):
        pass

    def select(self, selector: CommandSelect):
        self.selector = selector
        table: list = self.main_table_interactor.get_data(None, None)
        filter_columns = self.selector.get_columns()
        for i, col in enumerate(table[0]):
            if not (col in filter_columns):
                for row in table:
                    row.remove(row[i])
        return table

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


# controller = DBController()
# selector = CommandSelect()
# selector.set_columns(['Наименование', 'Цена'])
# print(controller.select(selector))

df = pd.DataFrame(np.arange(12).reshape(3, 4),
                  columns=['A', 'B', 'C', 'D'])
df = df.drop('A', axis=1)
print(df)
