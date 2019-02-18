from tkinter import Tk, StringVar, NSEW, E, EW
from tkinter.ttk import Combobox

from Work.Scripts.src.view.ui.custom_widgets import PVStandardButton, PVFrame, \
    PVLabel, PVCombobox
from Work.Scripts.src.view.ui.db_editor.command_frames import InsertFrame, \
    SelectFrame, UpdateFrame, DeleteFrame
from Work.Scripts.src.view.ui.main_window.config import MAIN_BACKGROUND

EDIT_TYPE_TEXT = "Команда для редактироавния БД"
TABLE_CHOICE_TEXT = "Выберите таблицу"
BTN_EXEC_TEXT = "Изменить"


class DbEditorWindow:
    commands = ['Вывести', 'Вставить', 'Заменить', 'Удалить']
    tables = ['Продукты', 'Чеки']

    def __init__(self, master, title):
        self.master = master
        master['bg'] = MAIN_BACKGROUND
        master.title(title)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=2)
        master.grid_columnconfigure(2, weight=2)

        master.grid_rowconfigure(0)
        master.grid_rowconfigure(1)
        master.grid_rowconfigure(2, weight=1, minsize=150)
        master.grid_rowconfigure(3)

        edit_type_label = PVLabel(master, text=EDIT_TYPE_TEXT)
        self.edit_type_choice = PVCombobox(master, width=30, height=20,
                                    state="readonly")
        self.edit_type_choice['values'] = self.commands
        self.edit_type_choice.bind('<<ComboboxSelected>>', self.choose_command)
        self.edit_type_choice.current(0)

        self.table_var = StringVar()

        table_choice_label = PVLabel(master, text=TABLE_CHOICE_TEXT)
        table_choice = PVCombobox(master, width=30, height=20,
                                state="readonly",
                                textvariable=self.table_var)
        table_choice['values'] = self.tables
        table_choice.current(0)
        table_choice.grid(row=1, column=1, sticky=EW, padx=10)

        self.edit_type_choice.grid(row=0, column=1, sticky=EW, padx=10)

        empty_frame = PVFrame(master)
        empty_frame.grid(row=0, column=2)

        table_choice_label.grid(row=1, column=0, sticky=E)
        edit_type_label.grid(row=0, column=0, sticky=E)

        self.btn_exec = PVStandardButton(master)
        self.btn_exec.bind("<Button-1>", self.click_exec)
        self.btn_exec.grid(row=3, column=0, columnspan=3,
                           sticky=E, padx=8, pady=8)

        self.set_command_frame(self.edit_type_choice.get())
        master.mainloop()

    def set_command_frame(self, command: str):
        if command == "Вывести":
            self.content_frame = SelectFrame(self.master)
        elif command == "Вставить":
            self.content_frame = InsertFrame(self.master)
        elif command == "Заменить":
            self.content_frame = UpdateFrame(self.master)
        elif command == "Удалить":
            self.content_frame = DeleteFrame(self.master)
        self.btn_exec['text'] = command
        self.content_frame.grid(row=2, column=0, columnspan=3, sticky=NSEW)

    def choose_command(self, event):
        self.set_command_frame(self.edit_type_choice.get())

    def click_exec(self, event):
        self.content_frame.click_exec()


# DbEditorWindow(Tk(), "Расширенное редактирование БД")
