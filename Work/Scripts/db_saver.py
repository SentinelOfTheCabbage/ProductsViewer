"""Docstring
"""
import tkinter
from tkinter import Tk, filedialog, Frame
import pandas as pd
from Work.Scripts import conf
from Work.Scripts.db_controller import MainTableController
# import pickle


class SaveAs(Frame):
    """Docstring
    """
    def __init__(self):
        Frame.__init__(self)
        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'),
                                ('pickle files', '.pickle')]
        options['initialfile'] = 'New'
        options['parent'] = self

    def option(self):
        """
        Метод реализует выбор пользователем значения из списка
        :return: выбранное значение
        """
        def okay():
            name = variable.get()
            if name == 'csv':
                self.csv(MainTableController().get_data_frame())
            elif name == 'xlsx':
                self.xlsx(MainTableController().get_data_frame())
            elif name == 'pickle':
                self.pickle(MainTableController().get_data_frame())
            master.destroy()

        master = Tk()
        message_label = tkinter.Label(master,
                                      text="Выберите нужный формат сохранения")
        message_label.grid(row=0, column=0, sticky='w')

        variable = tkinter.StringVar()
        variable.set('csv')

        w_w = tkinter.OptionMenu(master, variable, "csv", "xlsx", "pickle")
        w_w.grid(sticky='EW', row=1, column=0, padx=.5, pady=.5)

        o_k = tkinter.Button(master, text="Ok", command=okay)
        o_k.grid(row=3, column=0, padx=5, pady=5, sticky="e")

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

    def pickle(self, table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате pickle.
        """
        name = self.asksaveasfilename()
        table.to_pickle(name + '.pickle')

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
        name = conf.ROOT_DIR + r"\Data\db.pickle"
        table.to_csv(name + '.csv', sep=';', encoding='utf8', index=False)

    @staticmethod
    def csv_ind(table: pd.DataFrame):
        """
        Author: Andrey Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате csv с индексами.
        """
        name = conf.ROOT_DIR + r"\Data\db.pickle"
        table.to_csv(name + '.csv', sep=';', encoding='utf8', index=True)

    @staticmethod
    def pickle(table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате pickle.
        """
        f_f = open(conf.ROOT_DIR + r'\Data\filename.txt', 'r')
        te_xt = f_f.read()
        f_f.close()
        name = r'' + te_xt
        """
        with open(name,'rb') as fp:
            L = pickle.load(fp)
        L['_db_products'] = table
        """
        table.to_pickle(name)

    @staticmethod
    def xlsx(table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате xlsx.
        """
        name = conf.ROOT_DIR + r"\Data\db.pickle"
        table.to_excel(name + '.xlsx', index=False)

    @staticmethod
    def xlsx_ind(table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате xlsx с индексами.
        """
        name = conf.ROOT_DIR + r"\Data\db.pickle"
        table.to_excel(name + '.xlsx', index=True)


if __name__ == '__main__':
    f = open(conf.ROOT_DIR + r'\Data\Temp\filename.txt', 'r')
    f = f.read()
