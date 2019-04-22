"""
Предоставляет классы, которые генерируют шаблонные фреймы для экрана настроек
"""
import datetime
from abc import ABC, abstractmethod
from tkinter import Frame, Checkbutton, BooleanVar, StringVar, Radiobutton, W, \
    X, BOTH, Button, Label, EW, NSEW
from tkcalendar import Calendar
from Work.Scripts.src.presentation.custom.custom_widgets import VerticalScrolledFrame

FONT_STYLE = "Times New Roman"
FONT_SIZE_BTN_TEXT = 14
CALENDAR_TEXT_FONT = (FONT_STYLE, 12)
CHOSEN_DATE_LABEL = (FONT_STYLE, 11)
DATE_FORMAT = "%d.%m.%Y"
BTN_TEXT_APPLY = "Подтвердить"


class ChoiceFrameListener(ABC):
    """
    Интерфейс для обработки основных событий с корневого окна
    """

    @abstractmethod
    def clear(self):
        """
        Вызывается при нажатии на кнопку очистки данных
        """

    @abstractmethod
    def default_choice(self):
        """
        Вызывается при нажатии на кнопку "По умолчанию"
        """

    @abstractmethod
    def get_data(self):
        """
        Возвращает выбранные во фрейме данные
        :return выбранные во фрейме данные
        """


class OnEventInfoListener(ABC):
    """
    Интерфейс для обработки ошибок, связанных с неверным количеством
    выбранных данных
    """

    @abstractmethod
    def error(self, frame: ChoiceFrameListener):
        """
        Вызывается при ошибочном выборе данных
        :param frame: фрейм, вызывающий событие ошибочного выбора
        """

    @abstractmethod
    def success(self, frame: ChoiceFrameListener):
        """
        Вызывается при успешном выборе данных
        :param frame: фрейм, вызывающий событие успешного выбора
        """


# pylint: disable=too-many-ancestors
class MultiChoiceFrame(Frame, ChoiceFrameListener):
    """Фрейм для множественного выбора данных"""

    def __init__(self, master, values: list, is_scrolled: bool = False,
                 listener: OnEventInfoListener = None, **kw):
        """
        Создаёт фрейм для множественного выбора данных
        :param master: корневой виджет
        :param values: список значений для выбора
        :param is_scrolled: возможность прокрутки элементов
        :param listener: слушатель событий ошибночности выбора
        :param kw: ключевые слова для конфигурации Frame()
        """
        super().__init__(master, kw)

        self.checked_list = []
        self.values = []
        self.buttons = {}
        self.scrolled_frame = None
        self.listener = listener

        self.fill_frame_by_list(values, is_scrolled)

    def fill_frame_by_list(self, values: list, is_scrolled: bool):
        items = list(set(values))
        items.sort()
        self.values = items

        # Конфигурация Checkbutton исходя из списка значений
        for i, item in enumerate(items):
            self.checked_list.append(BooleanVar(self))
            self.checked_list[-1].set(0)

            if is_scrolled and len(items) > 6:
                if self.scrolled_frame is None:
                    self.scrolled_frame = VerticalScrolledFrame(self)
                    self.scrolled_frame.pack(fill=BOTH)

                choice_btn = Checkbutton(self.scrolled_frame.interior,
                                         text=item,
                                         variable=self.checked_list[-1],
                                         onvalue=1, offvalue=0,
                                         command=self.click_choice_btn,
                                         font=(FONT_STYLE, FONT_SIZE_BTN_TEXT),
                                         padx=30,
                                         anchor=W)
                choice_btn.pack(fill=X)
            else:
                choice_btn = Checkbutton(self, text=item,
                                         variable=self.checked_list[-1],
                                         onvalue=1, offvalue=0,
                                         command=self.click_choice_btn,
                                         font=(FONT_STYLE, FONT_SIZE_BTN_TEXT))
                if len(items) < 6:
                    row_pos = i
                    column_pos = 0
                else:
                    row_pos = i // 2
                    column_pos = i % 2

                self.grid_rowconfigure(row_pos, weight=1)
                self.grid_columnconfigure(column_pos, weight=1)

                choice_btn.grid(row=row_pos,
                                column=column_pos,
                                sticky=W)

            self.buttons[item] = choice_btn

        # Первоначальный выбор значений
        for i in range(len(self.values)):
            if len(self.values) < 6:
                self.buttons[self.values[i]].select()
            else:
                if i % 2 == 0:
                    self.buttons[self.values[i]].select()
                else:
                    self.buttons[self.values[i]].deselect()

    def click_choice_btn(self):
        """ Слушатель нажатия на любую из кнопок Checkbutton """
        true_vars = {checking_var.get() for checking_var in self.checked_list
                     if checking_var.get()}
        if true_vars:
            self.listener.success(self)
        else:
            self.listener.error(self)

    def clear(self):
        """Вызывается при нажатии на кнопку очистки данных"""
        for btn in self.buttons.values():
            btn.deselect()
        self.click_choice_btn()

    def default_choice(self):
        """Выбирает список занчений Checkbutton по умолчанию"""
        for i in range(len(self.values)):
            if len(self.values) < 6:
                self.buttons[self.values[i]].select()
            else:
                if i % 2 == 0:
                    self.buttons[self.values[i]].select()
                else:
                    self.buttons[self.values[i]].deselect()
        self.click_choice_btn()

    def get_data(self):
        """
        Возвращает выбранный список значений
        :return выбранный спсиок значений
        """
        data = []
        for is_checked, text in zip(self.checked_list, self.values):
            if is_checked.get():
                data.append(text)
        return data


# pylint: disable=too-many-ancestors
class SingleChoiceFrame(Frame, ChoiceFrameListener):
    """Фрейм для одиночного выбора данных"""

    buttons = {}
    values = []

    def __init__(self, master, values: list, rb_listener=None, **kw):
        """
        Создаёт фрейм для одиночного выбора данных
        :param master: корневой виджет
        :param values: список значений для выбора
        :param kw: ключевые слова для конфигурации Frame()
        """
        super().__init__(master, kw)

        self.checked_flag = StringVar(self)
        items = list(set(values))
        items.sort()
        self.values = items

        # Конфигурация Radiobutton исходя из списка значений
        for i, item in enumerate(items):
            choice_btn = Radiobutton(self, text=item,
                                     variable=self.checked_flag,
                                     value=item,
                                     font=(FONT_STYLE, FONT_SIZE_BTN_TEXT),
                                     command=rb_listener)
            self.buttons[item] = choice_btn
            if i == 0:
                choice_btn.select()

            if len(items) < 6:
                row_pos = i
                column_pos = 0
            else:
                row_pos = i // 2
                column_pos = i % 2

            self.grid_rowconfigure(row_pos, weight=1)
            self.grid_columnconfigure(column_pos, weight=1)

            choice_btn.grid(row=row_pos,
                            column=column_pos,
                            sticky=W)

    def clear(self):
        pass

    def default_choice(self):
        """ Устанавливает значение по умолчанию на первый Radiobutton """
        self.buttons[self.values[0]].select()

    def get_data(self):
        """
        Возвращает выбранное значение
        :return выбранное значение
        """
        return self.checked_flag.get()


# pylint: disable=too-many-ancestors
class CalendarFrame(Frame, ChoiceFrameListener):
    """Фрейм для выбора даты"""

    def __init__(self, master, **kw):
        """
        Создаёт фрейм для выбора даты
        :param master: корневой виджет
        :param kw: ключевые слова для конфигурации Frame()
        """
        super().__init__(master, kw)

        self.date = None
        self.grid_rowconfigure(1, weight=1)

        self.label = Label(self, font=CHOSEN_DATE_LABEL)
        self.cal = Calendar(self, font=CALENDAR_TEXT_FONT,
                            selectmode='day',
                            locale='RU', cursor="hand2",
                            year=2019, month=2, day=5,
                            command=self.click_btn_apply)

        self.label.grid(row=0, column=0)
        self.cal.grid(row=1, column=0, sticky=NSEW)
        btn = Button(self, text=BTN_TEXT_APPLY, command=self.click_btn_apply)
        btn.grid(row=2, column=0, sticky=EW)
        self.set_date(datetime.datetime.now())

    def click_btn_apply(self):
        """Сохраняет дату при нажатии на кнопку подтверждения"""
        self.set_date(self.cal.selection_get())

    def set_date(self, date: datetime):
        """Устанавливает дату и отображает её в текстовом поле"""
        self.label['text'] = self.date = date.strftime(DATE_FORMAT)

    def clear(self):
        pass

    def default_choice(self):
        """ Устанавливает текущую дату """
        self.set_date(datetime.datetime.now())

    def get_data(self):
        """
        Возвращает выбранную дату
        :return выбранная дата
        """
        return self.date
