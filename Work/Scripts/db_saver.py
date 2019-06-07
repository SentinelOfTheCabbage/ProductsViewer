"""
Author: Andrew Fedorov
Модуль сохранения БД.
"""
import pickle
from tkinter import Tk, filedialog, Frame
import pandas as pd
from Work.Scripts import conf


class SaveAs(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'),
                                ('pickle files', '.pickle')]
        options['initialfile'] = 'New'
        options['parent'] = self

    def asksaveasfilename(self):
        """
        Метод позволяет выбрать путь для сохранения файла в привычном окне
        :return: возвращает путь к будущему файлу
        """
        filename = filedialog.asksaveasfilename(**self.file_opt)
        return filename

    def csv(self, table: pd.DataFrame):
        """
        Author: Andrey Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате csv .
        """
        name = self.asksaveasfilename()
        table.to_csv(name + '.csv', sep=';', encoding='utf8', index=False)

    def csv_ind(self, table: pd.DataFrame):
        """
        Author: Andrey Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате csv с индексами.
        """
        name = self.asksaveasfilename()
        table.to_csv(name + '.csv', sep=';', encoding='utf8', index=True)

    def pickle(self, table: pd.DataFrame, recent):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame, recent: список изменений.
        :return: Сохраняет файл в формате pickle.
        """
        del(table["Категория"])
        del(table["Производитель"])
        del(table["Скидка"])
        f = open(conf.ROOT_DIR + r'\Data\filename.txt', 'r')
        path = f.read()
        f.close()
        table1 = pd.read_pickle(path)
        table1["_db_products"] = table
        try:
            Save().update_temp(recent)
            name = self.asksaveasfilename()
            with open(name, "wb") as handle:
                pickle.dump(table1, handle)
            f = open(conf.ROOT_DIR + r'\Data\filename.txt', 'w')
            f.write(name)
            f.close()
        except FileNotFoundError:
            pass

    def xlsx(self, table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате xlsx.
        """
        name = self.asksaveasfilename()
        table.to_excel(name + '.xlsx', index=False)

    def xlsx_ind(self, table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате xlsx с индексами.
        """
        name = self.asksaveasfilename()
        table.to_excel(name + '.xlsx', index=True)


class Save:
    @staticmethod
    def csv(table: pd.DataFrame):
        """
        Author: Andrey Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате csv .
        """
        name = conf.ROOT_DIR + r"\Data\db"
        table.to_csv(name + '.csv', sep=';', encoding='utf8', index=False)

    @staticmethod
    def csv_ind(table: pd.DataFrame):
        """
        Author: Andrey Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате csv с индексами.
        """
        name = conf.ROOT_DIR + r"\Outputs\pivot_table.csv"
        table.to_csv(name, sep=';', encoding='utf8', index=True)

    def pickle(self, table: pd.DataFrame, param, recent):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате pickle.
        """
        if param == 0:
            self.update_temp(recent)
            f_f = open(conf.ROOT_DIR + r'\Data\filename.txt', 'r')
            te_xt = f_f.read()
            f_f.close()
        elif param == 1:
            te_xt = conf.ROOT_DIR + r"\Outputs\pivot_table.pickle"
        name = r'' + te_xt
        table.to_pickle(name)

    @staticmethod
    def xlsx(table: pd.DataFrame, na):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате xlsx.
        """
        name = conf.ROOT_DIR + r"\Outputs" + na
        table.to_excel(name + '.xlsx', index=False)

    @staticmethod
    def xlsx_ind(table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате xlsx с индексами.
        """
        name = conf.ROOT_DIR + r"\Outputs\pivot_table"
        table.to_excel(name + '.xlsx', index=True)

    @staticmethod
    def update_temp(recent):
        frame: pd.DataFrame = pd.read_pickle(conf.ROOT_DIR + r"\Data\temp.pickle")

        for i in recent["del"]:
            frame = frame.loc[frame.id != i]
        s = 0
        for i in ("name", "price", "qual", "producer", "group_name","discount"):
            s += len(recent["ch"][i])
        if s > 0:
            for i in ("name", "price", "qual", "producer", "group_name","discount"):
                for g in recent["ch"][i]:
                    if i == "name":
                        frame["Назв продукта"][frame.id == g[0]] = g[1]
                    elif i == "price":
                        frame["Цена"][frame.id == g[0]] = g[1]
                    elif i == "qual":
                        frame["Кат товара"][frame.id == g[0]] = g[1]
                    elif i == "producer":
                        frame["Производитель"][frame.id == g[0]] = g[1]
                        frame["producer_id"][frame.id == g[0]] = g[2]
                    elif i == "group_name":
                        frame["Категория"][frame.id == g[0]] = g[1]
                        frame["group_id"][frame.id == g[0]] = g[2]
                    elif i == "discount":
                        frame["Скидка"][frame.id == g[0]] = g[1]
                        frame["discount_id"][frame.id == g[0]] = g[2]
        pd.to_pickle(frame, conf.ROOT_DIR + r"\Data\temp.pickle")
