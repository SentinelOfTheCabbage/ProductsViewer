import datetime
from abc import ABC, abstractmethod
from tkinter import Frame, Checkbutton, BooleanVar, StringVar, Radiobutton, W, \
    X, BOTH, Button, Label

from Work.Scripts.src.view.ui.custom_widgets import VerticalScrolledFrame

from tkcalendar import Calendar

FONT_STYLE = "Times New Roman"
FONT_SIZE_BTN_TEXT = 14


class ChoiceFrameListener(ABC):
    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def default_choice(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class OnEventInfoListener(ABC):

    @abstractmethod
    def error(self, frame: ChoiceFrameListener):
        pass

    @abstractmethod
    def success(self, frame: ChoiceFrameListener):
        pass


class MultiChoiceFrame(Frame, ChoiceFrameListener):

    def __init__(self, master, values: list, is_scrolled: bool = False,
                 listener: OnEventInfoListener = None, **kw):
        super().__init__(master, kw)

        self.checked_list = []
        self.values = []
        self.buttons = {}
        self.scrolled_frame = None
        self.listener = listener

        items = list(set(values))
        items.sort()
        self.values = items

        for i in range(len(items)):
            self.checked_list.append(BooleanVar(self))
            self.checked_list[-1].set(0)

            if is_scrolled and len(items) > 6:
                if self.scrolled_frame is None:
                    self.scrolled_frame = VerticalScrolledFrame(self)
                    self.scrolled_frame.pack(fill=BOTH)

                choice_btn = Checkbutton(self.scrolled_frame.interior,
                                         text=items[i],
                                         variable=self.checked_list[-1],
                                         onvalue=1, offvalue=0,
                                         command=self.click_choice_btn,
                                         font=(FONT_STYLE, FONT_SIZE_BTN_TEXT),
                                         padx=30,
                                         anchor=W)
                choice_btn.pack(fill=X)
            else:
                choice_btn = Checkbutton(self, text=items[i],
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

            self.buttons[items[i]] = choice_btn

        for i in range(len(self.values)):
            if len(self.values) < 6:
                self.buttons[self.values[i]].select()
            else:
                if i % 2 == 0:
                    self.buttons[self.values[i]].select()
                else:
                    self.buttons[self.values[i]].deselect()

    def click_choice_btn(self):
        true_vars = {checking_var.get() for checking_var in self.checked_list
                     if checking_var.get()}
        if len(true_vars) > 0:
            self.listener.success(self)
        else:
            self.listener.error(self)

    def clear(self):
        for btn in self.buttons.values():
            btn.deselect()
        self.click_choice_btn()

    def default_choice(self):
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
        data = []
        for is_checked, text in zip(self.checked_list, self.values):
            if is_checked.get():
                data.append(text)
        return data


class SingleChoiceFrame(Frame, ChoiceFrameListener):
    buttons = {}
    values = []

    def __init__(self, master, values: list, **kw):
        super().__init__(master, kw)

        self.checked_flag = StringVar()
        items = list(set(values))
        items.sort()
        self.values = items

        for i in range(len(items)):
            choice_btn = Radiobutton(self, text=items[i],
                                     variable=self.checked_flag,
                                     value=items[i],
                                     font=(FONT_STYLE, FONT_SIZE_BTN_TEXT))
            self.buttons[items[i]] = choice_btn
            choice_btn.select() if i == 0 else None

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
        self.buttons[self.values[0]].select()

    def get_data(self):
        return self.checked_flag.get()


class CalendarFrame(Frame, ChoiceFrameListener):

    def __init__(self, master, **kw):
        super().__init__(master, kw)

        self.date = None
        self.grid_rowconfigure(1, weight=1)

        self.label = Label(self, text="text", font=("Times New Roman", 14))
        self.cal = Calendar(self, font=("Times New Roman", 12),
                            selectmode='day',
                            locale='RU', cursor="hand2",
                            year=2019, month=2, day=5, command=self.print_sel)

        self.label.grid(row=0, column=0)
        self.cal.grid(row=1, column=0, sticky="nsew")
        btn = Button(self, text="ok", command=self.print_sel)
        btn.grid(row=2, column=0, sticky="we")
        self.set_date(datetime.datetime.now())

    def print_sel(self):
        self.set_date(self.cal.selection_get())

    def set_date(self, date: datetime):
        self.label['text'] = self.date = date.strftime("%d-%m-%Y")

    def clear(self):
        pass

    def default_choice(self):
        self.set_date(datetime.datetime.now())

    def get_data(self):
        return self.date
