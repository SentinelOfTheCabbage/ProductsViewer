from tkinter import filedialog, Frame
import pandas as pd
from Work.Scripts.src.domain.interactors import ListMainTableInteractor
from Work.Scripts import conf


class Open(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.file_opt = options = {}
        options['filetypes'] = [('pickle files', '.pickle')]
        options['initialfile'] = 'db.pickle'
        options['parent'] = self

    def askopenfilename(self):
        """
        Метод позволяет выбрать путь для открытия файла в привычном окне
        :return: возвращает путь к файлу
        """
        filename = filedialog.askopenfilename(**self.file_opt)
        f = open(conf.ROOT_DIR+r'\Data\Temp\filename.txt', 'w')
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
        main_table_df: pd.DataFrame = self.read(self.askopenfilename())
        if main_table_df is not None:
            m_table.content(ListMainTableInteractor().tolist(main_table_df)[:100])

