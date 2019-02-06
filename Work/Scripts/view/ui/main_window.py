from tkinter import Frame, Canvas, Label, X, Y, BOTH, Button, RIGHT, BOTTOM, \
    Checkbutton, Tk, Scrollbar, Menu, W, font

from config import *


class App:
    last_ch_bool = False
    filtr_bool = False
    table_bool = False

    def __init__(self, master, title="Заголовок"):
        self.master = master
        master.title(title)
        master.iconbitmap('img.ico')
        master.minsize(WIN_W_START, WIN_H_START)
        master.resizable(True, True)
        master.geometry("{winw}x{winh}+{centerw}+{centerh}".format(
            winw=WIN_W_START,
            winh=WIN_H_START,
            centerw=(master.winfo_screenwidth() - WIN_W_START) // 2,
            centerh=(master.winfo_screenheight() - WIN_H_START - 30) // 2))
        master.grid_rowconfigure(0, weight=2, minsize=150)
        master.grid_rowconfigure(1)
        master.grid_rowconfigure(2, minsize=24)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, minsize=0)
        master.grid_columnconfigure(2, minsize=0)
        master.grid_columnconfigure(3, minsize=24)

        footbar = MainMenu(master)
        footbar.build_menu("#000", 0)
        main_frame = Frame(master, bg='red')
        table_frame = Frame(master, bg='green')
        filtr_frame = Frame(master, bg='yellow', bd=0, width=0)
        self.last_ch_frame = InfoFrame(master, bg='blue')
        self.last_ch_frame.append_str("#000", "New string")

        bottom_btn = Button(master, text="text")
        bottom_btn.bind("<Button-1>", self.click_extend_menu)

        right_menu = Frame(master)

        filtr_btn = Canvas(right_menu, height=50, width=20, bd=0, bg="#f0f0f0")
        filtr_btn.bind("<Button-1>", self.click_filtr)
        filtr_btn.create_text((20, 50), angle="-90", anchor="ne",
                              text="фильтр")
        filtr_btn.place(x=0, y=0)

        table_btn = Canvas(right_menu, height=55, width=20, bd=0, bg="#f0f0f0")
        table_btn.bind("<Button-1>", self.click_table)
        table_btn.create_text((20, 55), angle="-90", anchor="ne",
                              text="таблицы")
        table_btn.place(x=0, y=54)

        main_frame.grid(row=0, column=0, sticky="nwes")
        filtr_frame.grid(row=0, column=1, sticky="nwes")
        table_frame.grid(row=0, column=2, sticky="nwes")
        self.last_ch_frame.grid(row=1, column=0, columnspan=4, sticky="nwes")
        right_menu.grid(row=0, column=3, sticky="nwes")
        bottom_btn.grid(row=2, column=0, columnspan=4, sticky="nwes")

        master.mainloop()

    def click_extend_menu(self, event):
        if self.last_ch_bool:
            self.master.grid_rowconfigure(1, minsize=0)
            #self.last_ch_frame['height'] = 0
        else:
            self.master.grid_rowconfigure(1, minsize=170)
        self.last_ch_bool = not self.last_ch_bool

    def click_filtr(self, event):
        if self.table_bool:
            self.master.grid_columnconfigure(2, minsize=0)
            self.table_bool = not self.table_bool
        if self.filtr_bool:
            self.master.grid_columnconfigure(1, minsize=0)
            #self.filtr_frame['height'] = 0
        else:
            self.master.grid_columnconfigure(1, minsize=170)
        self.filtr_bool = not self.filtr_bool

    def click_table(self, event):
        if self.filtr_bool:
            self.master.grid_columnconfigure(1, minsize=0)
            self.filtr_bool = not self.filtr_bool
        if self.table_bool:
            self.master.grid_columnconfigure(2, minsize=0)
            #self.table_frame['height'] = 0
        else:
            self.master.grid_columnconfigure(2, minsize=170)
        self.table_bool = not self.table_bool

class InfoFrame(Frame):
    _list_str = [("#f00", "Программа запущена")]

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)

    def append_str(self, color="#000", text="Default text"):
        self._list_str.append((color, text))
        self.update()

    def update(self):
        for r in range(len(self._list_str)):
            btnn = Frame(self, bg="#fff", bd=1)
            btnn.pack(side="top", expand=True, fill=X)
            btnn2 = Label(btnn, anchor='w', bg="#fff", padx=10, bd=2,
                          fg="{}".format(self._list_str[r][0]),
                          text="{}".format(self._list_str[r][1]))
            btnn2.pack(side="top", expand=True, fill=X)


class MainMenu(Menu):
    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)

    def build_menu(self, color, bd):
        main_menu = Menu()

        file = Menu(tearoff=0, bg="#fff")
        file.add_command(label="Найти")
        file.add_command(label="Выбрать")
        file.add_command(label="Выбрать всё")
        file.add_command(label="Назад")
        file.add_command(label="Вперёд")
        file.add_command(label="Помощь")
        file.add_command(label="Об авторах")
        file.add_separator()
        file.add_command(label="Выход")

        change = Menu(tearoff=0, bg="#fff")
        change.add_command(label="Новая БД")
        change.add_command(label="Редактировать БД")
        change.add_command(label="Открыть БД")
        change.add_command(label="Сохранить")
        change.add_command(label="Сохранить как...")

        otchet_menu = Menu(tearoff=0, bg="#fff")
        otchet_menu.add_command(label="Простой отчёт")
        otchet_menu.add_command(label="Статистика")
        otchet_menu.add_command(label="Сводная таблица")
        otchet_menu.add_command(label="Столбчатая диаграмма")
        otchet_menu.add_command(label="Гистограмма")
        otchet_menu.add_command(label="Диаграмма Босо-Вискеря")
        otchet_menu.add_command(label="Диаграмма рассеивания")

        main_menu.add_cascade(label="Меню", menu=file)
        main_menu.add_cascade(label="Изменение БД", menu=change)
        main_menu.add_cascade(label="Отчёты", menu=otchet_menu)

        self.master.config(menu=main_menu, bg="{}".format(color), bd="{}".format(bd))



a = App(Tk(), "База данных продуктов")
