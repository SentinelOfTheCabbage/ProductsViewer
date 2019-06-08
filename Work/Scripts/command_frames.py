"""
Модуль создаёт графическое окно для
множественного редактирования базы данных

Автор: Перятин Виталий
Отключены следующие ошибки pylint:
    R0903 - Мало методов в классе
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)
"""
# pylint: disable=E0401
# pylint: disable=R0903
# pylint: disable=R0901
# pylint: disable=W0613
# pylint: disable=R0902

from abc import ABC, abstractmethod
from tkinter import Frame, NSEW, W, StringVar, \
    BooleanVar, EW
from tkinter.messagebox import showwarning
from tkinter.ttk import Style

from Work.Scripts.interactors import ListMainTableInteractor
from Work.Scripts.key_words import CompareOp, Expression
from Work.Scripts.ui_table_constants import ProductColumns
from Work.Scripts.custom_widgets import VerticalScrolledFrame, \
    SubtitleLabel, PVAddButton, PVCancelButton, PVFrame, PVLabel, \
    PVCheckbutton, PVCombobox, PVEntry
from Work.Scripts.event_listener import IEventListener

CONTROLLER = ListMainTableInteractor()
ERROR_TITLE = "Внимание"


class IRemoveListener(ABC):
    """
    Интерфейс-слушатель для реагирования
    на события удаления записей

    Автор: Перятин Виталий
    """

    @abstractmethod
    def remove_expr(self, expr_frame):
        """
        Реагирует на события удаления записей
        :param expr_frame: фрейм, в котором необхдоимо слушать событие удаления

        Автор: Перятин Виталий
        """


class ICommandCreator(ABC):
    """
    Интерфейс-слушатель для реагирования на события нажатий на кнопки

    Автор: Перятин Виталий
    """

    @abstractmethod
    def click_exec(self, event_listener: IEventListener):
        """
        Реагирует на события нажатия кнопок
        :param event_listener:

        Автор: Перятин Виталий
        """


class ExpressionEditor(PVFrame):
    """
    Фрейм для редактирования выражений
    изменения базы дданных

    Автор: Перятин Виталий
    """

    expr_frames = []

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        where_label = SubtitleLabel(self, text="Где")
        self.where_frame = VerticalScrolledFrame(self)

        where_label.grid(row=0, column=1, sticky=NSEW)
        self.where_frame.grid(row=1, column=1, sticky=NSEW)

        btn_add_expr = PVAddButton(self, text="+")
        btn_add_expr.bind("<Button-1>", self.click_add_expr)
        btn_add_expr.grid(row=2, column=1, padx=8, sticky=NSEW)

        self.clear_expressions()

    def click_add_expr(self, event):
        """
        Добавляет новые выражения дял редактирования базы данных

        :param event: событие нжаатия кнопки

        Автор: Перятин Виталий
        """
        expression_frame = ExpressionFrame(self.where_frame.interior, self)
        expression_frame.pack(expand=True, fill='x')
        self.expr_frames.append(expression_frame)

    def remove_expr(self, expr_frame):
        """
        Удаляет выражение

        :param expr_frame: родительский фрейм откуда нужно удалить выражение

        Автор: Перятин Виталий
        """
        self.expr_frames.remove(expr_frame)

    def clear_expressions(self):
        """
        Очищает все выражения, добавленные пользователем

        Автор: Перятин Виталий
        """
        self.expr_frames = []

    def get_expressions(self):
        """
        Получает все выражения, добавленны епользователем

        Автор: Перятин Виталий
        """
        expressions = []
        has_error = False
        for expr_frame in self.expr_frames:
            expr = expr_frame.get_expr()
            if expr is None:
                has_error = True
            else:
                expressions.append(expr)
        if has_error:
            return None
        return expressions


class ExpressionFrame(PVFrame):
    """
    Фрейм для создания и отображения одного выражения

    Автор: Перятин Виталий
    """

    def __init__(self, master, remove_listener: ExpressionEditor):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3)

        self['padx'] = 2
        self['pady'] = 2

        self.remove_listener = remove_listener

        self.columns = [ProductColumns.NAME,
                        ProductColumns.PRICE,
                        ProductColumns.GROUP_NAME,
                        ProductColumns.PRODUCER_NAME,
                        ProductColumns.QUALITY]

        self.field = StringVar(self)
        self.field_chooser = PVCombobox(self, width=20, height=20,
                                        state="readonly",
                                        textvariable=self.field)
        self.field_chooser['values'] = self.columns
        self.field_chooser.current(0)
        self.compare_ops = [
            CompareOp.EQUAL,
            CompareOp.NOT_EQUAL,
            CompareOp.LESS,
            CompareOp.LESS_OR_EQUAL,
            CompareOp.MORE,
            CompareOp.MORE_OR_EQUAL,
        ]

        self.compare_var = StringVar(self)
        self.compare_op_chooser = PVCombobox(self, width=3, height=20,
                                             state="readonly",
                                             textvariable=self.compare_var)
        self.compare_op_chooser['values'] = self.compare_ops
        self.compare_op_chooser.current(0)

        self.value_var = StringVar(self)
        self.value_entry = PVEntry(self, width=20, text="Text",
                                   textvariable=self.value_var)

        btn_cancel = PVCancelButton(self, text="X")
        btn_cancel.bind("<Button-1>", self.click_cancel)

        self.field_chooser.grid(row=0, column=0, sticky=NSEW)
        self.compare_op_chooser.grid(row=0, column=1, sticky=NSEW)
        self.value_entry.grid(row=0, column=2, sticky=NSEW)
        btn_cancel.grid(row=0, column=3, sticky=NSEW)

    def click_cancel(self, event):
        """
        Отменяет редактирование выражения

        :param event: событие нажатия

        Автор: Перятин Виталий
        """
        self.remove_listener.remove_expr(self)
        self.destroy()

    def get_expr(self):
        """
        Получает составленное пользователем выражение

        Автор: Перятин Виталий
        """
        if (self.field.get() not in self.columns) or \
                (self.compare_var.get() not in self.compare_ops) or \
                (not self.value_var.get()):
            self['bg'] = 'yellow'
            return None
        self['bg'] = '#FFF'
        return Expression(self.field.get(),
                          self.compare_var.get(),
                          self.value_entry.get())


class ValueSetFrame(PVFrame):
    """
    Фрейм для установки значений в выражение

    Автор: Перятин Виталий
    """

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3)

        self['padx'] = 2
        self['pady'] = 2

        columns = [ProductColumns.NAME,
                   ProductColumns.PRICE,
                   ProductColumns.GROUP_NAME,
                   ProductColumns.PRODUCER_NAME,
                   ProductColumns.QUALITY]

        self.column_chooser = PVCombobox(self, width=20, height=20,
                                         state="readonly")
        self.column_chooser['values'] = columns
        self.column_chooser.current(0)

        assign_label = PVLabel(self, text='=')

        self.value_entry = PVEntry(self, width=20, text="Text",
                                   textvariable=StringVar())

        btn_cancel = PVCancelButton(self, text="X")
        btn_cancel.bind("<Button-1>", self.click_cancel)

        self.column_chooser.grid(row=0, column=0, sticky=NSEW)
        assign_label.grid(row=0, column=1, sticky=NSEW)
        self.value_entry.grid(row=0, column=2, sticky=NSEW)
        btn_cancel.grid(row=0, column=3, sticky=NSEW)

    def click_cancel(self, event):
        """
        Отмена действия

        :param event: Событие нажатия кнопки

        Автор: Перятин Виталий
        """
        self.destroy()

    def get_col_to_value(self):
        """docstring_peryatin
        """
        return {self.column_chooser.get(): self.value_entry.get()}


class SelectFrame(ExpressionEditor, ICommandCreator):
    """
    Фрейм для выбора столбцов

    Автор: Перятин Виталий
    """

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0, minsize=10)
        self.grid_rowconfigure(1, weight=1)

        columns_label = SubtitleLabel(self, text="Столбцы")
        columns_frame = VerticalScrolledFrame(self)

        columns = ProductColumns.get_empty_row().keys()

        self.check_vars = {}
        for col in columns:
            checking_var = BooleanVar(self)
            self.check_vars[col] = checking_var
            check_btn = PVCheckbutton(columns_frame.interior, text=col,
                                      variable=checking_var)
            checking_var.set(True)
            check_btn.pack(anchor=W)

        columns_label.grid(row=0, column=0, sticky=NSEW)
        columns_frame.grid(row=1, column=0, sticky=NSEW)

    def click_exec(self, event_listener: IEventListener):
        """
        Реагирует на внешние события

        :param event_listener: слушатель событий

        Автор: Перятин Виталий
        """
        event = CONTROLLER.select(self.check_vars, self.get_expressions())
        if event.error != 0:
            showwarning(ERROR_TITLE, event.text, parent=self)
        else:
            event_listener.notify(event)


class InsertFrame(PVFrame, ICommandCreator):
    """
    Фрейм для вставки значений

    Автор: Перятин Виталий
    """

    values = {}

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.grid_columnconfigure(0)
        self.grid_columnconfigure(1, weight=10)
        self.grid_columnconfigure(2, weight=10)
        self.grid_columnconfigure(3)

        self.grid_rowconfigure(0, weight=0, minsize=10)
        self.grid_rowconfigure(1, weight=1)

        self.style = Style()

        columns = ProductColumns.get_empty_row().keys()

        col_and_vals = VerticalScrolledFrame(self)

        for col_name in columns:
            col_and_val_frame = PVFrame(col_and_vals.interior)
            col_and_val_frame.grid_columnconfigure(0, weight=1, minsize=180)
            col_and_val_frame.grid_columnconfigure(1, weight=2)

            value_var = StringVar()
            col_label = PVLabel(col_and_val_frame, text=col_name)
            style = Style()
            style.configure("custom.TCombobox", fieldbackground="#000")
            value_entry = PVCombobox(col_and_val_frame, textvariable=value_var,
                                     style="custom.TCombobox")
            value_entry['values'] = CONTROLLER.get_vals_by_col(col_name)
            col_label.grid(row=0, column=0, sticky=W, padx=(24, 0))
            value_entry.grid(row=0, column=1, sticky=EW, padx=(0, 24))
            self.values[col_label['text']] = value_entry

            col_and_val_frame.pack(expand=True, fill='x', pady=10)

            separator = Frame(col_and_vals.interior, bg='grey', height=1)
            separator.pack(expand=True, fill='x')
        col_and_vals.grid(row=1, column=1, columnspan=2,
                          pady=(8, 0), padx=50, sticky=NSEW)

        separator = Frame(self, height=1, bg='grey')
        separator.grid(row=2, column=0, columnspan=4, sticky=EW)

    def click_exec(self, event_listener: IEventListener):
        """
        Реагирует на внешние события

        :param event_listener: слушатель событий

        Автор: Перятин Виталий
        """
        event = CONTROLLER.insert(self.values)
        if event.error != 0:
            showwarning(ERROR_TITLE, event.text, parent=self)
        else:
            event_listener.notify(event)


class UpdateFrame(ExpressionEditor, ICommandCreator):
    """
    Фрейм для формирования выражений для обновления базы данных
    """

    value_set_frames = []

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0, minsize=10)
        self.grid_rowconfigure(1, weight=1)

        set_label = SubtitleLabel(self, text="Установить")
        set_label.grid(row=0, column=0)

        self.set_frame = VerticalScrolledFrame(self)

        self.set_frame.grid(row=1, column=0, padx=10, sticky=NSEW)

        btn_add_value = PVAddButton(self, text="+")
        btn_add_value.bind("<Button-1>", self.click_add_value)
        btn_add_value.grid(row=2, column=0, padx=(8, 18), sticky=NSEW)

    def click_add_value(self, event):
        """
        Добавляет значение в выражение
        по обноввлению базы данных

        :param event: событие нажатия кнопки

        Автор: Перятин Виталий
        """
        value_set_frame = ValueSetFrame(self.set_frame.interior)
        value_set_frame.pack(expand=True, fill='x')
        self.value_set_frames.append(value_set_frame)

    def click_exec(self, event_listener: IEventListener):
        """
        Реагирует на нажатие кнопки, обновляет базу данных
        в соответствии с созданными выражениями

        :param event_listener: слушатель событий

        Автор: Перятин Виталий
        """

        event = CONTROLLER.update(self.value_set_frames,
                                  self.get_expressions())
        if event.error != 0:
            showwarning(ERROR_TITLE, event.text, parent=self)
        else:
            event_listener.notify(event)


class DeleteFrame(ExpressionEditor, ICommandCreator):
    """
    Фрейм для создания выражений для
    удаления записей в базе данных

    Автор: Перятин Виталий
    """
    expr_frames = []

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=0, minsize=10)
        self.grid_rowconfigure(1, weight=1)

    def click_exec(self, event_listener: IEventListener):
        """
        Реагирует на нажатие кнопки для удаления записей,
        удаляет выбранные записи из базы данных

        :param event_listener: слушатель событий

        Автор: Перятин Виталий
        """
        event = CONTROLLER.delete(self.get_expressions())
        if event.error != 0:
            showwarning(ERROR_TITLE, event.text, parent=self)
        else:
            event_listener.notify(event)
