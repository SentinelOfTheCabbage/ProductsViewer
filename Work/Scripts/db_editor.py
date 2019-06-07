"""
Модуль для создания окон, предназначенных
для редактирования БД

Отключены следующие ошибки pylint:
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)

Автор: Перятин Виталий
"""
# pylint: disable=E0401

from tkinter import StringVar, NSEW, E, EW

from Work.Scripts.custom_widgets import PVStandardButton, PVFrame, \
    PVLabel, PVCombobox
from Work.Scripts.command_frames import InsertFrame, \
    SelectFrame, UpdateFrame, DeleteFrame
from Work.Scripts.config import MAIN_BACKGROUND
from Work.Scripts.event_listener import IEventListener

EDIT_TYPE_TEXT = "Команда для редактироавния БД"
TABLE_CHOICE_TEXT = "Выберите таблицу"
BTN_EXEC_TEXT = "Изменить"
WIDTH = 600
HEIGHT = 500


class DbEditorWindow:
    """
    Класс, создержащий основную информацию о конфигурации окна для
    массового редактиорвания БД

    Автор: Перятин Виталий
    """
    commands = ['Вывести', 'Вставить', 'Заменить', 'Удалить']
    tables = ['Продукты', 'Чеки']

    def __init__(self, master, listener: IEventListener = None, title=""):
        self.listener = listener
        self.master = master
        master['bg'] = MAIN_BACKGROUND
        master.title(title)
        x_x = WIDTH - master.winfo_reqwidth() / 2
        y_y = (HEIGHT - master.winfo_reqheight()) / 2
        master.wm_geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, x_x, y_y))

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
        self.btn_exec.bind("<ButtonRelease-1>", self.click_exec)
        self.btn_exec.grid(row=3, column=0, columnspan=3,
                           sticky=E, padx=8, pady=8)

        self.set_command_frame(self.edit_type_choice.get())
        master.mainloop()

    def set_command_frame(self, command: str):
        """
        Устанавливает необходимое окно исходя из
        переданного названия команды

        Автор: Перятин Виталий
        """
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
        """
        Передаёт название команды для установки необходимого окна

        Автор: Перятин Виталий
        """
        self.set_command_frame(self.edit_type_choice.get())

    def click_exec(self, event):
        """
        Исполняет основную операцию выбранной команды
        (Вывести, Вставить, Заменить, Удалить)

        Автор: Перятин Виталий
        """
        self.content_frame.click_exec(self.listener)
