from abc import ABC, abstractmethod
from tkinter import Frame, NSEW, W, StringVar, \
    BooleanVar, EW
from tkinter.ttk import Style

from Work.Scripts.src.controller.adapters import ListMainTableAdapter
from Work.Scripts.src.controller.key_words import CompareOp, Expression
from Work.Scripts.src.model.repository.UI_table_constants import ProductColumns
from Work.Scripts.src.view.ui.custom_widgets import VerticalScrolledFrame, \
    SubtitleLabel, PVAddButton, PVCancelButton, PVFrame, PVLabel, \
    PVCheckbutton, PVCombobox, PVEntry

controller = ListMainTableAdapter()


class IRemoveListener(ABC):

    @abstractmethod
    def remove_expr(self, expr_frame):
        pass


class ICommandCreator(ABC):

    @abstractmethod
    def click_exec(self):
        pass


class ExpressionEditor(PVFrame):
    expr_frames = []

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        where_label = SubtitleLabel(self, text="Где")
        self.where_frame = VerticalScrolledFrame(self, bg='blue')

        where_label.grid(row=0, column=1, sticky=NSEW)
        self.where_frame.grid(row=1, column=1, sticky=NSEW)

        btn_add_expr = PVAddButton(self, text="+")
        btn_add_expr.bind("<Button-1>", self.click_add_expr)
        btn_add_expr.grid(row=2, column=1, padx=8, sticky=NSEW)

    def click_add_expr(self, event):
        expression_frame = ExpressionFrame(self.where_frame.interior, self)
        expression_frame.pack(expand=True, fill='x')
        self.expr_frames.append(expression_frame)

    def remove_expr(self, expr_frame):
        self.expr_frames.remove(expr_frame)

    def get_expressions(self):
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
        else:
            return expressions


class ExpressionFrame(PVFrame):

    def __init__(self, master, remove_listener: ExpressionEditor):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3)

        self['padx'] = 2
        self['pady'] = 2

        self.remove_listener = remove_listener

        self.columns = [ProductColumns.NAME.value,
                        ProductColumns.PRICE.value,
                        ProductColumns.GROUP_NAME.value,
                        ProductColumns.PRODUCER_NAME.value,
                        ProductColumns.QUALITY.value]

        self.field = StringVar(self)
        self.field_chooser = PVCombobox(self, width=20, height=20,
                                        state="readonly",
                                        textvariable=self.field)
        self.field_chooser['values'] = self.columns
        self.field_chooser.current(0)
        self.compare_ops = [
            CompareOp.EQUAL.value,
            CompareOp.NOT_EQUAL.value,
            CompareOp.LESS.value,
            CompareOp.LESS_OR_EQUAL.value,
            CompareOp.MORE.value,
            CompareOp.MORE_OR_EQUAL.value,
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
        self.remove_listener.remove_expr(self)
        self.destroy()

    def get_expr(self):
        if (self.field.get() not in self.columns) or \
                (self.compare_var.get() not in self.compare_ops) or \
                (not self.value_var.get()):
            self['bg'] = 'yellow'
            return None
        else:
            self['bg'] = '#FFF'
            return Expression(self.field.get(),
                              self.compare_var.get(),
                              self.value_entry.get())


class ValueSetFrame(PVFrame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3)

        self['padx'] = 2
        self['pady'] = 2

        columns = [ProductColumns.NAME.value,
                   ProductColumns.PRICE.value,
                   ProductColumns.GROUP_NAME.value,
                   ProductColumns.PRODUCER_NAME.value,
                   ProductColumns.QUALITY.value]

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
        self.destroy()

    def get_col_to_value(self):
        return {self.column_chooser.get(): self.value_entry.get()}


class SelectFrame(ExpressionEditor, ICommandCreator):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0, minsize=10)
        self.grid_rowconfigure(1, weight=1)

        columns_label = SubtitleLabel(self, text="Столбцы")
        columns_frame = VerticalScrolledFrame(self)

        columns = [ProductColumns.NAME.value,
                   ProductColumns.PRICE.value,
                   ProductColumns.GROUP_NAME.value,
                   ProductColumns.PRODUCER_NAME.value,
                   ProductColumns.QUALITY.value]

        self.check_vars = {}
        for col in columns:
            checking_var = BooleanVar(self)
            self.check_vars[col] = checking_var
            check_btn = PVCheckbutton(columns_frame.interior, text=col,
                                      variable=checking_var)
            check_btn.pack(anchor=W)

        columns_label.grid(row=0, column=0, sticky=NSEW)
        columns_frame.grid(row=1, column=0, sticky=NSEW)

    def click_exec(self):
        print(controller.select(self.check_vars, self.get_expressions()))


class InsertFrame(PVFrame, ICommandCreator):
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

        columns = [ProductColumns.NAME.value,
                   ProductColumns.PRICE.value,
                   ProductColumns.GROUP_NAME.value,
                   ProductColumns.PRODUCER_NAME.value,
                   ProductColumns.QUALITY.value]

        col_and_vals = VerticalScrolledFrame(self)

        # self.style.configure("custom.TCombobox", fg="white",
        #                      bg="black")

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
            value_entry['values'] = ['1', '2', '3']
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

    def click_exec(self):
        controller.insert(self.values)


class UpdateFrame(ExpressionEditor, ICommandCreator):
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
        value_set_frame = ValueSetFrame(self.set_frame.interior)
        value_set_frame.pack(expand=True, fill='x')
        self.value_set_frames.append(value_set_frame)

    def click_exec(self):
        controller.update(self.value_set_frames, self.get_expressions())


class DeleteFrame(ExpressionEditor, ICommandCreator):
    expr_frames = []

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=0, minsize=10)
        self.grid_rowconfigure(1, weight=1)

    def click_exec(self):
        controller.delete(self.get_expressions())
