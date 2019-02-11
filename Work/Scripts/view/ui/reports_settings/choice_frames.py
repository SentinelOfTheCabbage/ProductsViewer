from abc import ABC, abstractmethod
from tkinter import Frame, Checkbutton, BooleanVar, StringVar, Radiobutton


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


class MultiChoiceFrame(Frame, ChoiceFrameListener):

    def __init__(self, master, values: list, **kw):
        super().__init__(master, kw)

        self.checked_list = []
        self.values = []
        self.buttons = {}

        items = list(set(values))
        items.sort()
        self.values = items

        for i in range(len(items)):
            var = BooleanVar()
            choice_btn = Checkbutton(self, text=items[i],
                                     variable=var,
                                     font=("Times New Roman", 14))
            self.checked_list.append(var)
            self.buttons[items[i]] = choice_btn

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
                            sticky="w")
        self.default_choice()

    def clear(self):
        for btn in self.buttons.values():
            btn.deselect()

    def default_choice(self):
        for i in range(len(self.values)):
            if len(self.values) < 6:
                self.buttons[self.values[i]].select()
            else:
                if i % 2 == 0:
                    self.buttons[self.values[i]].select()
                else:
                    self.buttons[self.values[i]].deselect()

    def get_data(self):
        pass


class SingleChoiceFrame(Frame, ChoiceFrameListener):
    buttons = {}
    values = []

    def __init__(self, master, values: list, **kw):
        super().__init__(master, kw)

        self.checked_flag = StringVar()
        self.values = values
        items = list(set(values))
        items.sort()

        for i in range(len(items)):
            choice_btn = Radiobutton(self, text=items[i],
                                     variable=self.checked_flag,
                                     value=items[i],
                                     font=("Times New Roman", 14))
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
                            sticky="w")

    def clear(self):
        pass

    def default_choice(self):
        self.buttons[self.values[0]].select()

    def get_data(self):
        return self.checked_flag.get()


class CalendarFrame(Frame):
    def __init__(self, master, **kw):
        super().__init__(master, kw)
