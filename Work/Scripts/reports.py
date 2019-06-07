import pandas as pd
from Work.Scripts.db_controller import MainTableController
from Work.Scripts.db_saver import Save

class SimpleReport:

    @staticmethod
    def sort_producer_name(table: pd.DataFrame):
        """
        Сортирует таблицу по искомому имени
        :return: Все продукты с данного производителя
        """
        name = "Питерские крыши"
        del(table["producer_id"])
        del (table["group_id"])
        del (table["discount_id"])
        del (table["Скидка"])
        del (table["Цена"])
        df_d = table["Производитель"].str.find(name)
        a_a = []
        rowsend = pd.DataFrame({'id': [], 'Назв продукта': [],
                                'Производитель': [], 'Категория': [],
                                'Кат товара': [], })
        for num, row in enumerate(df_d):
            if row != -1:
                a_a.append(num)
        for i in a_a:
            rowsend = pd.concat([rowsend, table[table.index == i]])
        rowsend.id = pd.to_numeric(rowsend.id, downcast='integer')
        Save().xlsx(rowsend.sort_values("id"), r"\simple_report")

    @staticmethod
    def statistic(table: pd.DataFrame):
        statable1 = pd.DataFrame({"col1": [], "col2": []})
        for i, g in enumerate(table["Категория"].unique()):
            statable1 = pd.concat([statable1, pd.DataFrame({"col1": [g], "col2": [None]})])
        for i in range(statable1.col1.size):
            statable1.iloc[i].col2 = table["Цена"][table["Категория"] == statable1.iloc[i].col1].mean()
        statable2 = pd.DataFrame({"col1": [], "col2": []})
        for i, g in enumerate(table["Производитель"].unique()):
            statable2 = pd.concat([statable2, pd.DataFrame({"col1": [g], "col2": [None]})])
        for i in range(statable2.col1.size):
            statable2.iloc[i].col2 = table["Цена"][table["Производитель"] == statable2.iloc[i].col1].mean()
        statable3 = pd.DataFrame({"col1": [], "col2": []})
        for i, g in enumerate(table["Кат товара"].unique()):
            statable3 = pd.concat([statable3, pd.DataFrame({"col1": [g], "col2": [None]})])
        for i in range(statable3.col1.size):
            statable3.iloc[i].col2 = table["Цена"][table["Кат товара"] == statable3.iloc[i].col1].mean()
        statable4 = pd.DataFrame({"col1": ["По всей базе данных:"], "col2": [table["Цена"].mean()]})
        statable = pd.concat([pd.concat([statable1, statable2]),pd.concat([statable3,statable4])])
        statable = statable.rename(columns={"col1": "Группа","col2":"Средняя стоимость"})
        Save().xlsx(statable, r"\statistic")
