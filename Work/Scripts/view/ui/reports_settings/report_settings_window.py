"""Реализация UI с использованием библиотеки tkinter.  """
from abc import ABC, ABCMeta
from tkinter import *

from Work.Scripts.view.ui.listeners import ISettingsWindowListener


class SettingsWindow(ISettingsWindowListener, ABC):
    """Главный класс для конфигурации UI.

    Соединяет во едино все фреймы интерфейса. Прописывает основные настройки
    для корневого экрана: рахмеры, заголовок и др. Реагирует на исключительные
    ситуации показаом диалогового окна. Создаёт резиновый интерфейс для
    экрана программы.

    """

    def __init__(self, main, frame_left: Frame, frame_right: Frame,
                 **params):
        self.main = main
        window_width = 600
        window_height = 300
        center_width = (self.main.winfo_screenwidth() - window_width) // 2
        center_height = (self.main.winfo_screenheight() - window_height) // 2
        self.main.geometry("{}x{}+{}+{}".format(window_width, window_height,
                                                center_width, center_height))
        self.main.resizable(width=False, height=False)

        self.main.grid_rowconfigure(0, weight=0)
        self.main.grid_rowconfigure(1, weight=0)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_rowconfigure(3, weight=0)
        self.main.grid_rowconfigure(4, weight=0)

        self.main.grid_columnconfigure(0, weight=2, minsize=2)
        self.main.grid_columnconfigure(1, weight=0)
        self.main.grid_columnconfigure(2, weight=1)

        self.title_main = Label(self.main, text=params['title_main'] if 'title_main' in params else "",
                                font=("Times New Roman", 24))
        self.title_main.grid(row=0, column=0, columnspan=3)
        self.title_left = Label(self.main,
                                font=("Times New Roman", 14))
        self.title_left.grid(row=1, column=0)
        self.title_right = Label(self.main, text="Качество продуктов",
                                 font=("Times New Roman", 14))
        self.title_right.grid(row=1, column=2)
        separator = Frame(self.main, bg="grey", height=10)
        separator.grid(row=1, column=1, sticky="nwes", rowspan=2, pady=10)

        self.info_text = Label(self.main, text="Выберте продукты",
                               font=("Times New Roman", 12))
        self.info_text.grid(row=3, column=0, columnspan=3, sticky=E, padx=10)

        btn_frame = Frame(self.main)
        btn_frame.grid(row=4, column=0, columnspan=3, sticky=E)

        btn1 = Button(btn_frame, text="Отчёт",
                      font=("Times New Roman", 11))
        btn1.bind("<Button-1>", self.click_report)
        btn1.pack(side=RIGHT, padx=10, pady=10)

        btn2 = Button(btn_frame, text="По умолчанию",
                      font=("Times New Roman", 11))
        btn2.bind("<Button-1>", self.click_default)
        btn2.pack(side=RIGHT, padx=0, pady=10)

        btn3 = Button(btn_frame, text="Очистить",
                      font=("Times New Roman", 11))
        btn3.bind("<Button-1>", self.click_clear)
        btn3.pack(side=RIGHT, padx=10, pady=10)

        frame_left.master = self.main
        frame_left.grid(row=2, column=0, sticky="nwes", padx=10, pady=5)

        frame_right.master = self.main
        frame_right.grid(row=2, column=2, sticky="nwes", padx=10, pady=5)



    def set_info_text(self, color: str, text):
        self.info_text['fg'] = color
        self.info_text['text'] = text

    def set_main_title(self, title):
        self.title_main['text'] = title

    def set_left_title(self, title):
        self.title_left.configure(text=title)

    def set_right_title(self, title):
        self.title_right['text'] = title
