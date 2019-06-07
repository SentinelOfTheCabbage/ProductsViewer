"""
Author: Andrew Fedorov
Модуль открытия БД.
"""

from tkinter import filedialog, Frame
import pandas as pd
from Work.Scripts import conf
from Work.Scripts.config import NAME_TITLES
# from Work.Scripts.interactors import ListMainTableInteractor


class Open(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.file_opt = options = {}
        options['filetypes'] = [('pickle files', '.pickle')]
        options['initialfile'] = 'db.pickle'
        options['parent'] = self

    def askopenfilename(self):
        """
        Author: Andrew Fedorov
        Метод позволяет выбрать путь для открытия файла в привычном окне
        :return: возвращает путь к файлу
        """
        filename = filedialog.askopenfilename(**self.file_opt)
        if filename != "":
            f = open(conf.ROOT_DIR + r'\Data\filename.txt', 'w')
            f.write(filename)
            f.close()
            return filename

    @staticmethod
    def read(path):
        """
        Author: Andrew Fedorov
        Функция чтения таблицы
        :param path: путь к таблице
        :return: требуемая таблица в формате DataFrame
        """
        products_table = None
        try:
            if len(path) > 0:
                main_table = pd.read_pickle(r"" + path)
                products_table = main_table['_db_products']
        except FileNotFoundError:
            pass
        finally:
            return products_table

    def open(self, m_table):
        # main_table_df: pd.DataFrame = self.read(self.askopenfilename())
        # if main_table_df is not None:
        #     main_table_df = main_table_df.rename(columns={
        #         'id': 'id',
        #         'name': NAME_TITLES[0],
        #         'price': NAME_TITLES[1],
        #         'producer_name': NAME_TITLES[2],
        #         'group_name': NAME_TITLES[3],
        #         'discount_id': NAME_TITLES[4],
        #         'quality': NAME_TITLES[5]
        #     })
        #     m_table.before_content(ListMainTableInteractor().tolist(main_table_df))
        pass