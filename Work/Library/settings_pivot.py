"""
Модуль для создания экрана настроек для сводной таблицы

Автор: Фёдоров Андрей
"""
# pylint: disable=R0801,R0902,R0903

from tkinter import Label, Entry, W, Button, EW
from tkinter.ttk import Combobox
import pandas as pd
import numpy as np
from Work.Scripts.config import NAME_TITLES
from Work.Scripts.conf import ROOT_DIR
from Work.Scripts.db_controller import MainTableController
from Work.Scripts.db_saver import Save

WINDOW_TITLE = "Настройка сводной таблицы"


class SettingsPivot:
    """
    Класс для содания экрана насторек
    для создания сводного отчета

    Автор: Фёдоров Андрей
    """

    def __init__(self, main):
        self.main = main
        window_width = 300
        window_height = 150
        center_width = (self.main.winfo_screenwidth() - window_width) // 2
        center_height = (self.main.winfo_screenheight() - window_height) // 2
        self.main.geometry("{}x{}+{}+{}".format(window_width, window_height,
                                                center_width, center_height))
        self.main.resizable(width=False, height=False)
        self.main.title(WINDOW_TITLE)

        self.text_column = Label(main, text="Стобец: ")
        self.text_index = Label(main, text="Индекс:")
        self.text_param = Label(main, text="Подсчитываемый параметр: ")
        self.text_format_export = Label(main, text="Формат для экспорта: ")

        self.list1 = NAME_TITLES
        self.list2 = ["Средняя стоимость", "Количество"]
        self.list3 = ["csv", "xlsx", "pickle"]

        self.edit_text_column = Combobox(main, state="readonly", values=self.list1)
        self.edit_text_column.set(self.list1[0])
        self.edit_text_index = Combobox(main, state="readonly", values=self.list1)
        self.edit_text_index.set(self.list1[1])
        self.edit_text_param = Combobox(main, state="readonly", values=self.list2)
        self.edit_text_param.set(self.list2[1])
        self.edit_text_format_export = Combobox(main, state="readonly", values=self.list3)
        self.edit_text_format_export.set(self.list3[0])

        self.button_apply = Button(main, text="OK", command=self.create_pivot_report)

        # Конфигурация таблицы упаковки виджетов
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_rowconfigure(3, weight=1)
        self.main.grid_rowconfigure(4, weight=1)

        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=2)

        self.text_column.grid(row=0, column=0, sticky=EW)
        self.text_index.grid(row=1, column=0, sticky=EW)
        self.text_param.grid(row=2, column=0, sticky=EW)
        self.text_format_export.grid(row=3, column=0, sticky=EW)

        self.edit_text_column.grid(row=0, column=1, sticky=EW)
        self.edit_text_index.grid(row=1, column=1, sticky=EW)
        self.edit_text_param.grid(row=2, column=1, sticky=EW)
        self.edit_text_format_export.grid(row=3, column=1, sticky=EW)

        self.button_apply.grid(row=4, column=1, sticky=EW)
        self.frame: pd.DataFrame

    def create_pivot_report(self):
        """
        Создаёт сводный отчёт

        Автор: Фёдоров Андрей
        """
        column = self.edit_text_column.get()
        index = self.edit_text_index.get()
        param = self.edit_text_param.get()
        export_format = self.edit_text_format_export.get()

        self.frame: pd.DataFrame = pd.read_pickle(ROOT_DIR + r"\Data\temp.pickle")
        if param == "Количество":
            self.frame = self.frame.pivot_table(index=index, columns=column, values=index, aggfunc='count')
        else:
            self.frame = self.frame.pivot_table(index=index, columns=column, values="Цена", aggfunc=np.mean)
        if export_format == "csv":
            Save().csv_ind(self.frame)
        elif export_format == "xlsx":
            Save().xlsx_ind(self.frame)
        elif export_format == "pickle":
            Save().pickle(self.frame, 1)
        self.main.destroy()
