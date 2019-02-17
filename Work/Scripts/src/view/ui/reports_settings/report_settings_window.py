"""Реализация UI с использованием библиотеки tkinter.  """

# pylint: disable=W0612,W0613,R0801
from abc import ABC, abstractmethod
from tkinter import Frame, NSEW, Label, RIGHT, Button, E

from Work.Scripts.res.values.colors import SUCCESS_INFO_COLOR, SEPARATOR_COLOR
from Work.Scripts.res.values.styles import SUBTITLE_TEXT_FONT
from Work.Scripts.src.test.graph_reports_interactor import ReportsInteractor
from Work.Scripts.src.view.ui.reports_settings.choice_frames import \
    OnEventInfoListener, ChoiceFrameListener

WINDOW_TITLE = "Конфигурация графического отчёта [{}]"

BTN_REPORT_TEXT = "Отчёт"
BTN_DEFAULT_TEXT = "По умолчанию"
BTN_CLEAR_TEXT = "Очистить"

FONT_STYLE = "Times New Roman"
FONT_SIZE_BTN = 11

TITLE_MAIN_KEY_PARAM = "title_main"
BTN_CLICK_EVENT = "<ButtonRelease-1>"

TEXT_KEY = "text"
FG_KEY = "fg"

SUCCESS_INFO_TEXT = "Нажмите на 'Отчёт' "


class SettingsWindow(OnEventInfoListener, ABC):
    """Главный класс для конфигурации UI.

    Соединяет во едино все фреймы интерфейса. Прописывает основные настройки
    для корневого экрана: рахмеры, заголовок и др. Реагирует на исключительные
    ситуации показаом диалогового окна. Создаёт резиновый интерфейс для
    экрана программы.
    """

    left_choice_is_done = True
    right_choice_is_done = True
    reports_interactor = ReportsInteractor()

    def __init__(self, main, title: str,
                 frame_left: Frame, frame_right: Frame):
        """Создаёт окно для настройки параметров графических отчётов"""
        self.main = main
        window_width = 600
        window_height = 350
        center_width = (self.main.winfo_screenwidth() - window_width) // 2
        center_height = (self.main.winfo_screenheight() - window_height) // 2
        self.main.geometry("{}x{}+{}+{}".format(window_width, window_height,
                                                center_width, center_height))
        self.main.resizable(width=False, height=False)
        self.main.title(WINDOW_TITLE.format(title))

        self.frame_1: ChoiceFrameListener = None
        self.frame_2: ChoiceFrameListener = None

        # Конфигурация таблицы упаковки виджетов
        self.main.grid_rowconfigure(0, minsize=20)
        self.main.grid_rowconfigure(1, weight=0)
        self.main.grid_rowconfigure(2, weight=1)
        self.main.grid_rowconfigure(3, weight=0)
        self.main.grid_rowconfigure(4, weight=0)

        self.main.grid_columnconfigure(0, weight=2, minsize=2)
        self.main.grid_columnconfigure(1, weight=0)
        self.main.grid_columnconfigure(2, weight=1)

        # Создание и упоковка текстовых полей
        self.title_left_label = Label(self.main,
                                      font=SUBTITLE_TEXT_FONT)
        self.title_left_label.grid(row=1, column=0)
        self.title_right_label = Label(self.main,
                                       font=SUBTITLE_TEXT_FONT)
        self.title_right_label.grid(row=1, column=2)
        separator = Frame(self.main, bg=SEPARATOR_COLOR, height=10)
        separator.grid(row=1, column=1, sticky=NSEW, rowspan=2, pady=10)

        self.info_text = Label(self.main, font=(FONT_STYLE, 12))
        self.info_text.grid(row=3, column=0, columnspan=3, sticky=E, padx=10)

        # Упаковка кнопок
        btns_frame = Frame(self.main)
        btns_frame.grid(row=4, column=0, columnspan=3, sticky=E)

        btn_report = Button(btns_frame, text=BTN_REPORT_TEXT,
                            font=(FONT_STYLE, FONT_SIZE_BTN))
        btn_report.bind(BTN_CLICK_EVENT, self.click_reports)
        btn_report.pack(side=RIGHT, padx=10, pady=10)

        btn_default = Button(btns_frame, text=BTN_DEFAULT_TEXT,
                             font=(FONT_STYLE, FONT_SIZE_BTN))
        btn_default.bind(BTN_CLICK_EVENT, self.click_default)
        btn_default.pack(side=RIGHT, padx=0, pady=10)

        btn_clear = Button(btns_frame, text=BTN_CLEAR_TEXT,
                           font=(FONT_STYLE, FONT_SIZE_BTN))
        btn_clear.bind(BTN_CLICK_EVENT, self.click_clear)
        btn_clear.pack(side=RIGHT, padx=10, pady=10)

        # Упаковка левого и правого фреймов для выбора данных
        frame_left.master = self.main
        frame_left.grid(row=2, column=0, sticky=NSEW, padx=10, pady=5)

        frame_right.master = self.main
        frame_right.grid(row=2, column=2, sticky=NSEW, padx=10, pady=5)
        self.set_info_text(SUCCESS_INFO_COLOR, SUCCESS_INFO_TEXT)

    def set_info_text(self, color: str, text):
        """Устанавливает текс в текстовом поле для вывода ошибок
        при выборе данных """
        self.info_text[FG_KEY] = color
        self.info_text[TEXT_KEY] = text

    def set_left_title(self, title):
        """Устанавливает подзаголовок для левого фрейма"""
        self.title_left_label.configure(text=title)

    def set_right_title(self, title):
        """Устанавливает подзаголовок для правого фрейма"""
        self.title_right_label[TEXT_KEY] = title

    @abstractmethod
    def click_reports(self, event):
        """Выполняется при нажатии на кнопку 'Отчёты' """

    def click_default(self, event):
        """Выбирает данные по умолчанию"""
        self.frame_1.default_choice()
        self.frame_2.default_choice()

    def click_clear(self, event):
        """Очищает выбраные данные"""
        self.frame_1.clear()
        self.frame_2.clear()

    @abstractmethod
    def output_success_info(self):
        """Выводит информацию в текстовое поле об успешности выбора"""
