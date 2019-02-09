"""asd"""
from tkinter import Frame, Canvas, Label, BOTH, Button, \
    Checkbutton, Tk, Scrollbar, Menu
from config import WIN_W_START, WIN_H_START, COLOR_BG_TITLE_TABLE, \
    COLOR_BG_EVENT_ROW, COLOR_BG_ODD_ROW, COLOR_TEXT_TABLE, COLOR_BG_LAST_CH, \
    COLOR_BG_TITLE_LAST_CH, COLOR_BG_FRAME_TABLE, COLOR_BG_FRAME_FILTR, \
    COLOR_FG_FRAME_TABLE, COLOR_FG_FRAME_FILTR, COLOR_BG_MENU, COLOR_FG_MENU


class App:
    """asd """
    last_ch_bool = False
    filtr_bool = False
    table_bool = False

    def __init__(self, master, title="Заголовок"):
        self.master = master
        master.title(title)
        master.iconbitmap('img.ico')
        master.minsize(WIN_W_START, WIN_H_START - 20)
        master.resizable(True, True)
        master.geometry("{winw}x{winh}+{centerw}+{centerh}".format(
            winw=WIN_W_START,
            winh=WIN_H_START,
            centerw=(master.winfo_screenwidth() - WIN_W_START) // 2,
            centerh=(master.winfo_screenheight() - WIN_H_START - 30) // 2))
        master.grid_rowconfigure(0, weight=1, minsize=150)
        master.grid_rowconfigure(1, minsize=0)
        master.grid_rowconfigure(2, minsize=24)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, minsize=0)
        master.grid_columnconfigure(2, minsize=0)
        master.grid_columnconfigure(3, minsize=24)

        footbar = MainMenu(master)
        footbar.build_menu()
        self.main_frame = BDFrame(master, bg="#f0f0f0")
        self.filtr_frame = FiltrFrame(master)
        self.filtr_frame.content()
        self.table_frame = TableFrame(master)
        self.table_frame.content()
        self.last_ch_frame = InfoFrame(self.master)

        self.bottom_btn = Button(master, bg="red", anchor="w",
                                 text="Последние изменения ↑")
        self.bottom_btn.bind("<ButtonRelease-1>", self.click_extend_menu)

        right_menu = Frame(master)

        self.filtr_btn = Canvas(right_menu, height=50, width=20,
                                bd=0, bg="#f0f0f0")
        self.filtr_btn.bind("<ButtonRelease-1>", self.click_filtr)
        self.filtr_btn.create_text((20, 50), angle="-90", anchor="ne",
                                   text="фильтр")
        self.filtr_btn.place(x=0, y=0)

        self.table_btn = Canvas(right_menu, height=55, width=20,
                                bd=0, bg="#f0f0f0")
        self.table_btn.bind("<ButtonRelease-1>", self.click_table)
        self.table_btn.create_text((20, 55), angle="-90", anchor="ne",
                                   text="таблицы")
        self.table_btn.place(x=0, y=54)

        self.main_frame.grid(row=0, column=0, sticky="nwes")
        self.filtr_frame.grid(row=0, column=1, sticky="nwes")
        self.table_frame.grid(row=0, column=2, sticky="nwes")
        # self.last_ch_frame.grid(row=1, column=0, columnspan=4, sticky="nwes")
        right_menu.grid(row=0, column=3, sticky="nwes")
        self.bottom_btn.grid(row=2, column=0, columnspan=4, sticky="nwes")

        self.master.bind_all("<MouseWheel>", self.on_mousewheel)
        self.master.bind('<Left>', self.left_key)
        self.master.bind('<Right>', self.right_key)
        self.master.bind('<Up>', self.top_key)
        self.master.bind('<Down>', self.bottom_key)
        master.mainloop()

    def left_key(self, event):
        """ asd"""
        self.main_frame.canvas.xview_scroll(-1, "units")

    def right_key(self, event):
        """ asd"""
        self.main_frame.canvas.xview_scroll(1, "units")

    def top_key(self, event):
        """asd """
        widget = self.widget_pointer()
        if "bdframe" in widget and "canvas" in widget:
            self.main_frame.cont.yview_scroll(-1, "units")
        elif "infoframe" in widget and "canvas" in widget:
            self.last_ch_frame.canvas.yview_scroll(-1, "units")

    def bottom_key(self, event):
        """ asd"""
        widget = self.widget_pointer()
        if "bdframe" in widget and "canvas" in widget:
            self.main_frame.cont.yview_scroll(1, "units")
        elif "infoframe" in widget and "canvas" in widget:
            self.last_ch_frame.canvas.yview_scroll(1, "units")

    def on_mousewheel(self, event):
        """ asd"""
        widget = self.widget_pointer()
        sgn = -1 * (event.delta // 120)
        if "bdframe" in widget and "canvas" in widget:
            self.main_frame.cont.yview_scroll(sgn, "units")
        elif "infoframe" in widget and "canvas" in widget:
            self.last_ch_frame.canvas.yview_scroll(sgn, "units")

    def widget_pointer(self):
        """ asd"""
        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)
        widget = "{}".format(widget)
        return widget

    def click_extend_menu(self, event):
        """asd """
        if self.last_ch_bool:
            self.bottom_btn.config(text="Последние изменения ↑")
            self.last_ch_frame.close()
        else:
            self.bottom_btn.config(text="Последние изменения ↓")
            self.last_ch_frame = InfoFrame(self.master)
            self.last_ch_frame.open()
        self.last_ch_bool = not self.last_ch_bool

    def click_filtr(self, event):
        """ asd"""
        if self.table_bool:
            self.master.grid_columnconfigure(2, minsize=0)
            self.table_btn.config(bg="#f0f0f0")
            self.table_bool = not self.table_bool
        if self.filtr_bool:
            self.master.grid_columnconfigure(1, minsize=0)
            self.filtr_btn.config(bg="#f0f0f0")
        else:
            self.filtr_btn.config(bg="#B2B2B2")
            self.master.grid_columnconfigure(1, minsize=140)
        self.filtr_bool = not self.filtr_bool

    def click_table(self, event):
        """ asd"""
        if self.filtr_bool:
            self.master.grid_columnconfigure(1, minsize=0)
            self.filtr_btn.config(bg="#f0f0f0")
            self.filtr_bool = not self.filtr_bool
        if self.table_bool:
            self.master.grid_columnconfigure(2, minsize=0)
            self.table_btn.config(bg="#f0f0f0")
        else:
            self.table_btn.config(bg="#B2B2B2")
            self.master.grid_columnconfigure(2, minsize=140)
        self.table_bool = not self.table_bool


class FiltrFrame(Frame):
    """asd """
    _list_filtr = ["Данон", "Coca-Cola", "Черниголовка", "Останкино"]

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.config(bg=COLOR_BG_FRAME_FILTR)

    def click_check(self, *args):
        """ asd"""
        print("click_check")

    def content(self):
        """ asd"""
        for i in range(len(self._list_filtr)):
            check = Checkbutton(self, bg=COLOR_BG_FRAME_FILTR, bd=0,
                                fg=COLOR_FG_FRAME_FILTR,
                                text="{}".format(self._list_filtr[i]))
            check.bind("<Button-1>", self.click_check)
            check.place(x=10, y=24*i)


class BDFrame(Canvas):
    """ asd"""
    _bd_array = [
        ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров", "Наиль",
         "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров", "Наиль", "Ласт"],
        ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
         "Макс",
         "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
         "Виталий",
         "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
         "Андрей",
         "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров", "Наиль",
         "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров", "Наиль", "Ласт"],
        ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
         "Макс",
         "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
         "Виталий",
         "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
         "Андрей",
         "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров", "Наиль",
         "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров", "Наиль", "Ласт"],
        ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
         "Макс",
         "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
         "Виталий",
         "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
         "Андрей",
         "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров", "Наиль",
         "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров", "Наиль", "Ласт"],
        ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
         "Макс",
         "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
         "Виталий",
         "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
         "Андрей",
         "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров", "Наиль",
         "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров", "Наиль", "Сулейманов"],
        ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
         "Макс",
         "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
         "Виталий",
         "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
         "Андрей",
         "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров", "Наиль",
         "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров", "Наиль", "Ласт"],
        ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
         "Макс",
         "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
         "Виталий",
         "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
         "Федоров",
         "Наиль", "Ласт"],
        ["Ласт", "Ласт", "Ласт", "Ласт", "Ласт", "Ласт",
         "Ласт",
         "Ласт", "Ласт", "Ласт", "Ласт", "Ласт", "Ласт",
         "Ласт",
         "Ласт", "Ласт"]
    ]
    col = len(_bd_array[0])
    row = len(_bd_array)

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, minsize=24)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=24)

        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas, background="blue")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.grid(row=0, column=0, sticky="nwes")

        self.titles = Canvas(self.frame, bg="orange")
        self.cont = Canvas(self.frame, bg="yellow", height=350)
        self.titles.grid(row=0, column=0, sticky="nwes")
        self.frame2 = Frame(self.cont, background="blue")
        self.cont.create_window((0, 0), window=self.frame2, anchor="nw")
        self.cont.grid(row=1, column=0, sticky="nwes")

        scroll_x = Scrollbar(self, orient="horizontal",
                             command=self.canvas.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")

        scroll_y = Scrollbar(self, orient="vertical", command=self.cont.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.cont.configure(yscrollcommand=scroll_y.set)
        self.canvas.configure(xscrollcommand=scroll_x.set)
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas:
                        self.on_frame_configure(self.canvas))
        self.frame2.bind("<Configure>", lambda event, canvas=self.cont:
                         self.on_frame_configure(self.cont))
        self.content(self.titles, self.frame2)

    def on_frame_configure(self, main_lab2):
        """Reset the scroll region to encompass the inner frame"""
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    def content(self, frame1, frame2):
        """ asd"""
        for r in range(self.row):
            for c in range(self.col):
                if r == 0:
                    btn = Frame(frame1, bg="#000", bd=0)
                else:
                    btn = Frame(frame2, bg="#000", bd=0)
                btn.grid(row=r, column=c)
                border = Frame(btn, height=2, bg="red")
                border.pack(side="top", expand=True, fill="x")
                btn2 = Label(btn, width=10, bd=2, fg=COLOR_TEXT_TABLE,
                             bg=COLOR_BG_ODD_ROW,
                             text="{}".format(self._bd_array[r][c]))
                btn2.pack(expand=True, fill=BOTH)
                if r % 2 == 0:
                    btn2.config(bg=COLOR_BG_EVENT_ROW)
                if r == 0:
                    btn2.config(bg=COLOR_BG_TITLE_TABLE)


class InfoFrame(Canvas):
    """ asd"""
    _list_last_ch = [
        ("black", "чё-то добавилось"), ("red", "удалили то-то"),
        ("red", "Ошибка чего то там"), ("red", "хз что произошло"),
        ("red", "Наиль лох"), ("red", "и не только он"),
        ("red", "(я тоже лох)"), ("red", "Но зато я не Наиль"),
        ("red", "что хорошо"), ("white", "конечноже"),
        ("white", "чё-то добавилось"), ("red", "удалили то-то"),
        ("red", "Ошибка чего то там"), ("red", "хз что произошло"),
        ("red", "Наиль лох"), ("red", "и не только он"),
        ("red", "(я тоже лох)"), ("red", "Но зато я не Наиль"),
        ("red", "что хорошо"), ("black", "конечноже")
        ]

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=12)

    def on_frame_configure(self, main_lab2):
        """Reset the scroll region to encompass the inner frame"""
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    # def append_str(self, color="#000", text="Default text"):
    #     self._list_last_ch.append((color, text))
    #     self.update(True)

    def content(self):
        """ asd"""
        top_lab = Label(self, text="Последние изменения", anchor="w",
                        bg=COLOR_BG_TITLE_LAST_CH)

        self.canvas = Canvas(self, bg=COLOR_BG_LAST_CH, height=130)
        frame = Frame(self.canvas, bg=COLOR_BG_LAST_CH)
        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.create_window((0, 0), window=frame, anchor="n")
        self.canvas.configure(yscrollcommand=scroll.set)
        frame.bind("<Configure>", lambda event, canvas=self.canvas:
                   self.on_frame_configure(self.canvas))
        top_lab.grid(row=0, column=0, columnspan=2, sticky="nwes")
        self.canvas.grid(row=1, column=0, sticky="nwes")
        scroll.grid(row=1, column=1, sticky="nwes")
        for r in range(len(self._list_last_ch)):
            message = Label(frame, bg=COLOR_BG_LAST_CH, padx=10, bd=2,
                            fg="{}".format(self._list_last_ch[r][0]),
                            text="{}".format(self._list_last_ch[r][1]))
            message.grid()

    def close(self):
        """ asd"""
        self.destroy()
        # for child in self.winfo_children():
        #     for child2 in child.winfo_children():
        #         child2.grid_forget()
        #     child.grid_forget()

    def open(self):
        """ asd"""
        self.content()
        self.grid(row=1, column=0, columnspan=4, sticky="nwes")
    # def remove(self):
    #     self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
    #
    #     self.canvas.configure(yscrollcommand=self.scroll.set)
    #     # self.canvas.configure(scrollregion=canvas.bbox("all"))
    #     self.frame.bind("<Configure>",
    #                     lambda event,
    #                            canvas=self.canvas: self.onFrameConfigure(
    #                         self.canvas))
    #     self.top_lab.grid(row=0, column=0, columnspan=2, sticky="nwes")
    #     self.canvas.grid(row=1, column=0, sticky="nwes")
    #     self.scroll.grid(row=1, column=1, sticky="nwes")
    #     for child in self.frame.winfo_children():
    #         child.grid()


class TableFrame(Frame):
    """ asd"""
    _list_table = ["продукты", "чеки", "группы", "Таблица_4", "Таблица_5",
                   "Таблица_6", "Таблица_7", "Таблица_8"]

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.config(bg=COLOR_BG_FRAME_TABLE)

    def click(self, *args):
        """asd """
        print("click_table")

    def content(self):
        """ asd"""
        for j in range(len(self._list_table)):
            tables_name = Button(self, bg=COLOR_BG_FRAME_TABLE, bd=0,
                                 fg=COLOR_FG_FRAME_TABLE,
                                 text="{}".format(self._list_table[j]))
            tables_name.bind("<Button-1>", self.click)
            tables_name.place(x=10, y=24*j)


class MainMenu(Menu):
    """ asd"""
    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)

    def build_menu(self):
        """asd"""
        main_menu = Menu()

        file = Menu(tearoff=0, bg=COLOR_BG_MENU, fg=COLOR_FG_MENU)
        file.add_command(label="Открыть")
        file.add_command(label="Создать копию")
        file.add_command(label="Переименовать")
        file.add_command(label="Сохранить")
        file.add_command(label="Сохранить как...")
        file.add_separator()
        file.add_command(label="Выйти")

        change = Menu(tearoff=0, bg=COLOR_BG_MENU, fg=COLOR_FG_MENU)
        change.add_command(label="Назад")
        change.add_command(label="Вперёд")
        change.add_command(label="Вырезать")
        change.add_command(label="Копировать")
        change.add_command(label="Вставить")
        change.add_command(label="Найти и заменить")

        otchet_menu = Menu(tearoff=0, bg=COLOR_BG_MENU, fg=COLOR_FG_MENU)
        otchet_menu.add_command(label="Простой отчёт")
        otchet_menu.add_command(label="Статистика")
        otchet_menu.add_command(label="Сводная таблица")
        otchet_menu.add_command(label="Столбчатая диаграмма")
        otchet_menu.add_command(label="Гистограмма")
        otchet_menu.add_command(label="Диаграмма 'Ящика с усами'")
        otchet_menu.add_command(label="Диаграмма рассеивания")

        main_menu.add_cascade(label="Файл", menu=file)
        main_menu.add_cascade(label="Изменить", menu=change)
        main_menu.add_cascade(label="Отчёты", menu=otchet_menu)

        self.master.config(bg="red", menu=main_menu)


App(Tk(), "База данных продуктов")
