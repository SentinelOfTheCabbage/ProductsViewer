"""Реализация UI с использованием библиотеки tkinter.  """
from abc import ABC, abstractmethod
from tkinter import *

TITLE_MAIN_TEXT = "Выберите параметры"

BTN_REPORT_TEXT = "Отчёт"
BTN_DEFAULT_TEXT = "По умолчанию"
BTN_CLEAR_TEXT = "Очистить"

FONT_STYLE = "Times New Roman"
FONT_SIZE_BTN = 11
FONT_SIZE_TITLE = 24
FONT_SIZE_SUBTITLE = 14

TITLE_MAIN_KEY_PARAM = "title_main"
BTN_CLICK_EVENT = "<ButtonRelease-1>"


class SettingsWindow(ABC):
    """Главный класс для конфигурации UI.

    Соединяет во едино все фреймы интерфейса. Прописывает основные настройки
    для корневого экрана: рахмеры, заголовок и др. Реагирует на исключительные
    ситуации показаом диалогового окна. Создаёт резиновый интерфейс для
    экрана программы.

    """

    title_left_label = None
    title_right_label = None

    def __init__(self, main, frame_left: Frame, frame_right: Frame,
                 **params):
        self.main = main
        window_width = 800
        window_height = 400
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

        self.title_main = Label(self.main, text=params[
            TITLE_MAIN_KEY_PARAM] if TITLE_MAIN_KEY_PARAM in params
        else TITLE_MAIN_TEXT, font=(FONT_STYLE, FONT_SIZE_TITLE))
        self.title_main.grid(row=0, column=0, columnspan=3)
        self.title_left_label = Label(self.main,
                                      font=(FONT_STYLE, FONT_SIZE_SUBTITLE))
        self.title_left_label.grid(row=1, column=0)
        self.title_right_label = Label(self.main,
                                       font=(FONT_STYLE, FONT_SIZE_SUBTITLE))
        self.title_right_label.grid(row=1, column=2)
        separator = Frame(self.main, bg="grey", height=10)
        separator.grid(row=1, column=1, sticky=NSEW, rowspan=2, pady=10)

        self.info_text = Label(self.main, font=(FONT_STYLE, 12))
        self.info_text.grid(row=3, column=0, columnspan=3, sticky=E, padx=10)

        btn_frame = Frame(self.main)
        btn_frame.grid(row=4, column=0, columnspan=3, sticky=E)

        btn1 = Button(btn_frame, text=BTN_REPORT_TEXT,
                      font=(FONT_STYLE, FONT_SIZE_BTN))
        btn1.bind(BTN_CLICK_EVENT, self.click_reports)
        btn1.pack(side=RIGHT, padx=10, pady=10)

        btn2 = Button(btn_frame, text=BTN_DEFAULT_TEXT,
                      font=(FONT_STYLE, FONT_SIZE_BTN))
        btn2.bind(BTN_CLICK_EVENT, self.click_default)
        btn2.pack(side=RIGHT, padx=0, pady=10)

        btn3 = Button(btn_frame, text=BTN_CLEAR_TEXT,
                      font=(FONT_STYLE, FONT_SIZE_BTN))
        btn3.bind(BTN_CLICK_EVENT, self.click_clear)
        btn3.pack(side=RIGHT, padx=10, pady=10)

        frame_left.master = self.main
        frame_left.grid(row=2, column=0, sticky=NSEW, padx=10, pady=5)

        frame_right.master = self.main
        frame_right.grid(row=2, column=2, sticky=NSEW, padx=10, pady=5)

    def set_info_text(self, color: str, text):
        self.info_text['fg'] = color
        self.info_text['text'] = text

    def set_main_title(self, title):
        self.title_main['text'] = title

    def set_left_title(self, title):
        self.title_left_label.configure(text=title)

    def set_right_title(self, title):
        self.title_right_label['text'] = title

    @abstractmethod
    def click_reports(self, event):
        pass

    @abstractmethod
    def click_default(self, event):
        pass

    @abstractmethod
    def click_clear(self, event):
        pass
