import pandas as pd
from tkinter import messagebox
from Work.Scripts.db_controller import MainTableController
from Work.Scripts.interactors import ListMainTableInteractor
from Work.Scripts.conf import ROOT_DIR
from Work.Scripts.db_saver import Save


class FilterColumns:
    def filter(self, list_, m_table):

        Save().update_temp(m_table.recent_change)
        frame: pd.DataFrame = pd.read_pickle(ROOT_DIR + r"\Data\temp.pickle")

        if len(list_)<6:
            for i in frame.columns:
                if i in list_:
                    del(frame[i])
            self.open(frame, m_table)
        else:
            messagebox.showerror("Ошибка", "Извините, не выделено ни одного поля!")

    def open(self, frame: pd.DataFrame, m_table):
        if frame is not None:
            m_table.before_content(ListMainTableInteractor().tolist(frame))


class FilterRows:

    @staticmethod
    def temp_saver(bd_array):
        pd.to_pickle(pd.DataFrame(bd_array, columns=bd_array[0])[1:], ROOT_DIR + r"\Data\temp.pickle")

    def filter(self, slov, m_table):
        Save().update_temp(m_table.recent_change)
        frame: pd.DataFrame = pd.read_pickle(ROOT_DIR + r"\Data\temp.pickle")
        price = slov["Цена"]
        prod = slov["Производитель"]
        group = slov["Группа"]
        disc = slov["Скидка"]
        qual = slov["Качество"]

        rowsend = pd.DataFrame({'id': [], 'Назв продукта': [], "Цена": [], 'producer_id': [],
                                'Производитель': [], 'group_id': [], 'Категория': [], 'discount_id': [], 'Скидка': [],
                                'Кат товара': []})
        rowsend1 = pd.DataFrame({'id': [], 'Назв продукта': [], "Цена": [], 'producer_id': [],
                                'Производитель': [], 'group_id': [], 'Категория': [], 'discount_id': [], 'Скидка': [],
                                'Кат товара': []})
        rowsend2 = pd.DataFrame({'id': [], 'Назв продукта': [], "Цена": [], 'producer_id': [],
                                'Производитель': [], 'group_id': [], 'Категория': [], 'discount_id': [], 'Скидка': [],
                                'Кат товара': []})
        if prod != "Все":
            df_d = frame["Производитель"].str.find(prod)
            a_a = []
            for num, row in enumerate(df_d):
                if row != -1:
                    a_a.append(df_d.index[num])
            for i in a_a:
                rowsend = pd.concat([rowsend, frame[frame.index == i]], sort=False)
        else:
            rowsend = frame
        if rowsend.index.size != 0:
            if group != "Все":
                df_d = rowsend["Категория"].str.find(group)
                a_a = []
                for num, row in enumerate(df_d):
                    if row != -1:
                        a_a.append(df_d.index[num])
                for i in a_a:
                    rowsend1 = pd.concat([rowsend1, rowsend[rowsend.index == i]], sort=False)
            else:
                rowsend1 = rowsend
            if rowsend1.index.size != 0:
                if qual != "Все":
                    df_e = rowsend1["Кат товара"].str.find(qual)
                    a_a = []
                    for num, row in enumerate(df_e):
                        if row != -1:
                            a_a.append(df_e.index[num])
                    for i in a_a:
                        rowsend2 = pd.concat([rowsend2, rowsend1[rowsend1.index == i]], sort=False)
                else:
                    rowsend2 = rowsend1
                if rowsend2.index.size != 0:
                    if price != 0:
                        rowsend2 = rowsend2[rowsend2["Цена"] <= price]
                    if rowsend2.index.size != 0:
                        if disc != 0:
                            rowsend2 = rowsend2[rowsend2["Скидка"] <= disc]
            else:
                rowsend2 = rowsend1
        else:
            rowsend2 = rowsend
        if rowsend2.index.size != 0:
            FilterColumns().open(rowsend2, m_table)
        else:
            messagebox.showerror("Ошибка", "Извините, товары не найдены")

    def sort_name(self, slov, m_table):
        Save().update_temp(m_table.recent_change)
        frame: pd.DataFrame = pd.read_pickle(ROOT_DIR + r"\Data\temp.pickle")

        rowsend = pd.DataFrame({'id': [], 'Назв продукта': [], "Цена": [], 'producer_id': [],
                                'Производитель': [], 'group_id': [], 'Категория': [], 'discount_id': [], 'Скидка': [],
                                'Кат товара': []})

        if frame.index.size != 0 and slov != "Найти":
            df_d = frame["Назв продукта"].str.find(slov)
            a_a = []
            for num, row in enumerate(df_d):
                if row != -1:
                    a_a.append(df_d.index[num])
            for i in a_a:
                rowsend = pd.concat([rowsend, frame[frame.index == i]], sort=False)
            if rowsend.index.size != 0:
                FilterColumns().open(rowsend, m_table)
            else:
                messagebox.showerror("Ошибка", "Извините, товары не найдены")
        elif slov != "Найти":
            messagebox.showerror("Ошибка", "Извините, товары не найдены")


