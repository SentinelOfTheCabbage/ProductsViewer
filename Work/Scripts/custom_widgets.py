"""
Предоставляет элементы с видоизмененным
параметрами индивидуально для проекта

Автор: Перятин Виталий
Отключены следующие ошибки pylint:
    R0901 - Слишком много предкова
    W0614 - Ошибка использования self в некоторых методах класса
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)
"""
# pylint: disable=E0401
# pylint: disable=W0614
# pylint: disable=R0901

from tkinter import *
from tkinter.ttk import Combobox

from Work.Scripts.config import MAIN_BACKGROUND


class PVStandardButton(Button):
    """
    Кастомизированная под приложение стандартная кнопка

    Автор: Перятин Виталий
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self['bg'] = '#80DEEA'
        self['activebackground'] = '#4DD0E1'
        self['padx'] = 2
        self['pady'] = 2
        self['font'] = ("Courier", 14)


class PVAddButton(Button):
    """
    Кастомизированная под приложение кнопка добавления

    Автор: Перятин Виталий
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self['bg'] = '#80CBC4'
        self['activebackground'] = '#80CBC4'
        self['font'] = ("Courier", 12)


class PVCancelButton(Button):
    """
    Кастомизированная под приложение кнопка отмены

    Автор: Перятин Виталий
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self['bg'] = MAIN_BACKGROUND
        self['fg'] = '#B71C1C'
        self['relief'] = 'flat'
        self['activebackground'] = '#EF9A9A'
        self['font'] = ("Courier", 10, "bold")


class PVCombobox(Combobox):
    """
    Кастомизированное под приложение поле выбора

    Автор: Перятин Виталий
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        font = ("Times", 12)
        self['font'] = font
        master.option_add("*TCombobox*Listbox*Font", font)


class PVEntry(Entry):
    """
    Кастомизированное под приложение поле ввода текста

    Автор: Перятин Виталий
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self['font'] = ("Times", 12)


class PVFrame(Frame):
    """
    Кастомизированный под приложение Frame

    Автор: Перятин Виталий
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self['bg'] = MAIN_BACKGROUND


class PVLabel(Label):
    """
    Кастомизированное под приложение текстовое поле

    Автор: Перятин Виталий
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self['bg'] = MAIN_BACKGROUND
        self['padx'] = 10
        self['pady'] = 4
        self['font'] = ("Comic Sans MS", 12, "italic")


class PVCheckbutton(Checkbutton):
    """
    Кастомизированная под приложение кнопка выбора

    Автор: Перятин Виталий
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self['bg'] = MAIN_BACKGROUND
        self['activebackground'] = MAIN_BACKGROUND
        self['padx'] = 8
        self['font'] = ("Times", 12)


class SubtitleLabel(PVLabel):
    """
    Кастомизированный под приложение подзаголовок

    Автор: Перятин Виталий
    """
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self['pady'] = 10
        self['font'] = ("Comic Sans MS", 16, "italic")


class VerticalScrolledFrame(PVFrame):
    """
    Прокручиваемая рамка Tkinter
    Используйте атрибут «interior» для размещения виджетов внутри прокручиваемого фрейма
    Этот Frame реализует только вертикальную прокрутку

    Автор: Перятин Виталий
    """

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling itz
        vscrollbar = Scrollbar(self, orient=VERTICAL, width=16)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        hscrollbar = Scrollbar(self, orient=HORIZONTAL, width=16)
        hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)

        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                             xscrollcommand=hscrollbar.set)
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)
        content = Canvas(self.frame, bd=0, highlightthickness=0,
                         yscrollcommand=vscrollbar.set)
        content['bg'] = parent['bg']
        content.pack()
        self.canvas['bg'] = parent['bg']
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=content.yview)
        hscrollbar.config(command=self.canvas.xview)

        # reset the views
        content.xview_moveto(0)
        content.yview_moveto(0)
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = PVFrame(content)
        interior_id = content.create_window(0, 0, window=interior,
                                            anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            """
            Конфигурирует содержимое рамки
            :param event: событие нажатия

            Автор: Перятин Виталий
            """
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            content.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != content.winfo_width():
                # update the canvas's width to fit the inner frame
                content.config(width=interior.winfo_reqwidth())

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior_2(event):
            """
            Повторная конфигурация содержимого рамки
            :param event: событие нажатия

            Автор: Перятин Виталий
            """
            size = (
                self.frame.winfo_reqwidth(), self.frame.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.config(width=self.frame.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)
        self.frame.bind('<Configure>', _configure_interior_2)


class HorizontalScrolledFrame(PVFrame):
    """
    Прокручиваемая рамка Tkinter
    Используйте атрибут «interior» для размещения виджетов внутри прокручиваемого фрейма
    Этот Frame реализует только вертикальную прокрутку

    Автор: Перятин Виталий
    """

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling itz
        hscrollbar = Scrollbar(self, orient=HORIZONTAL, width=16)
        hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        xscrollcommand=hscrollbar.set)
        canvas['bg'] = parent['bg']
        canvas.pack(side=TOP, fill=BOTH, expand=TRUE)
        hscrollbar.config(command=canvas.xview)

        # reset the views
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = PVFrame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            """
            Конфигурирует содержимое рамки
            :param event: событие нажатия

            Автор: Перятин Виталий
            """
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqheight())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqheight() != canvas.winfo_height():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_height())

        canvas.bind('<Configure>', _configure_canvas)
