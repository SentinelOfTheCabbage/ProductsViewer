from tkinter import Tk, filedialog, Frame, Canvas
import pandas as pd
from Work.Scripts.src.controller.adapters import ListMainTableAdapter
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
        table = pd.read_pickle(r"" + path)
        x_x = table['_db_products']
        return x_x

    def open(self, m_table):
        m_table.content(ListMainTableAdapter().tolist(self.read(self.askopenfilename()))[:100])

