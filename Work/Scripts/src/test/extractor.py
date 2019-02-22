import pandas as pd
from pandas import np

from Work.Scripts.src.model.repository.UI_table_constants import ProductColumns
from Work.Scripts.src.model.repository.interf_extractor import IDataExtractor


class DataExtractor(IDataExtractor):

    def get_data(self):
        data = np.array([
            list(ProductColumns.get_empty_row().keys()),
            ["Молоко", 50, "М", "Молочное", 0, "ГОСТ"],
            ["Хлеб", 34, "Хлебное гнездо", "Бакалея", 0, "ГОСТ"],
            ["Торт", 420, "От палыча", "Сладкое", 10, "СТО"],
            ["Творог", 70, "Простоквашино", "Молочное", 0, "ГОСТ"],
            ["Кефир", 60, "Простоквашино", "Молочное", 0, "ГОСТ"],
            ["Сметана", 80, "Простоквашино", "Молочное", 0, "ГОСТ"],
            ["Булочка", 20, "Хлопушка", "Бакалея", 5, "ТУ"],
            ["Макароны", 70, "Такие с птичкино", "Бакалея", 0, "СТО"],
            ["Рис", 60, "Китерс", "Бакалея", 0, "СТО"],
        ])
        return pd.DataFrame(data[1:], columns=data[0])
