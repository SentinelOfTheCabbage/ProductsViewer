"""
Файл содержит классы представляющие собой вспомогающие поля в главном окне
Автор: Озирный Максим
"""
from tkinter import Frame, Scrollbar, Label, Canvas, Button, \
    Checkbutton, IntVar
from tkinter.ttk import Combobox, Scale

from Work.Scripts.src.test.change_viewer import ChangeViewer
from Work.Scripts.src.view.ui.main_window.config import COLOR_BG_FRAME_TABLE, \
    COLOR_FG_FRAME_TABLE, COLOR_BG_FRAME_FILTR, COLOR_FG_FRAME_FILTR, \
    COLOR_BG_TITLE_LAST_CH, COLOR_BG_LAST_CH, HEIGHT_INFO_FRAME, \
    FONT_TITLE_FILTR, CURSOR_CHANGE_WIGHT, CURSOR_CHANGE_HEIGHT, \
    MIN_SIZE_TABLE, WIDTH_FILR_FRAME, MIN_WIDTH_TABLE, MIN_WIDTH_FILR_FRAME

import Work.Scripts.src.view.ui.main_window.config as conf


class RowFilterPanel(Frame):
    """
    Класс отвечающий за создание и позиционирование
    контента для работы с фильтрацией строк
    Автор: Озирный Максим
    """
    x = 0
    width = WIDTH_FILR_FRAME
    width_2 = width
    _list_filtr = [["Наименование", ["Кефир", "Молоко", "Хлеб"]],
                   ["Цена", 1280],
                   ["Производитель", ["деревня", "простоквашино"]],
                   ["Группа", ["Выпечка", "Молочка", "Мясо", "Алкоголь"]],
                   ["Скидка", 40],
                   ["Качество", ["ГОСТ", "СТО", "ТУ"]]]

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.canvas = Canvas(self, bg=COLOR_BG_FRAME_TABLE,
                             width=WIDTH_FILR_FRAME - 16)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=16)

    def content(self):
        """
        Функция создающая и позиционирующая содержимое
        поля отвечающего за фильтрацию строк
        Автор: Озирный Максим
        """
        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = Frame(self.canvas, bg=COLOR_BG_FRAME_TABLE)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)
        # для корректной прокрутки canvas прописываем событие изменяющее
        # положение содержимого при прокрутке
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas:
        self.on_frame_configure(self.canvas))
        self.canvas.grid(row=0, column=0, sticky="nwes")
        scroll.grid(row=0, column=1, sticky="nwes")
        # Заголовок поля
        title_1 = Label(self.frame, text="Продукты", bg=COLOR_BG_FRAME_FILTR,
                        fg=COLOR_FG_FRAME_FILTR, font=FONT_TITLE_FILTR)
        title_1.grid(row=0, column=0, sticky="we", padx=10, ipadx=10,
                     columnspan=2)
        # Черта под заголовком
        frame5 = Frame(self.frame, height=1, bg="#000")
        frame5.grid(row=1, column=0, sticky="we", padx=10, ipadx=10,
                    columnspan=2)
        ind = 0
        # в цикле создаются и позиционируются подзаголовки и соответствующие
        # им объекты (Scale или Combobox) в зависимости от содержимого списка
        for ind in range(len(self._list_filtr)):
            title = Label(self.frame, bg=COLOR_BG_FRAME_FILTR, bd=0,
                          fg=COLOR_FG_FRAME_FILTR,
                          text="{}:".format(self._list_filtr[ind][0]))
            title.grid(row=2 + 2*ind, column=0, sticky="w", padx=10, pady=2)
            if self._list_filtr[ind][0] == "Цена" or \
                    self._list_filtr[ind][0] == "Скидка":
                slider = IntVar()
                scale = Scale(self.frame, orient="horizontal", length=95,
                              from_=0,
                              to=self._list_filtr[ind][1], variable=slider)
                scale.grid(row=2 + 2*ind+1, column=0, sticky="w", padx=20,
                           pady=2)
                label = Label(self.frame, textvariable=slider, width=2,
                              anchor="w", justify="left")
                label.grid(row=2 + 2*ind+1, column=1, sticky="w", pady=2)
            else:
                box = Combobox(self.frame, width=13,
                               values=self._list_filtr[ind][1])
                box.grid(row=2 + 2*ind+1, column=0, sticky="w", padx=20,
                         pady=2)

        # Кнопка вызывающая функцию отвечающюю за фильтрацию строк
        btn = Button(self.frame, text="Сохранить")
        btn.grid(row=3 + 2*ind+1, column=0, sticky="we", padx=10, pady=2,
                 columnspan=2)

        # отслеживаем события для изменения ширины поля
        self.frame.bind("<ButtonPress-1>", self.start_move)
        self.frame.bind("<ButtonRelease-1>", self.stop_move)
        self.frame.bind("<B1-Motion>", self.on_motion)
        self.frame.bind("<Motion>", self.change_cursor)
        self.frame.bind("<Leave>", self.on_leave)

    @staticmethod
    def on_frame_configure(main_lab2):
        """
        Функция необходимая для прокрутки содержимого в canvas
        Автор: Озирный Максим
        """
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    def change_cursor(self, event=None):
        if event.x < 4:
            self.frame.config(cursor=CURSOR_CHANGE_WIGHT)
        else:
            self.frame.config(cursor='arrow')

    def on_leave(self, event=None):
        self.frame.config(cursor='arrow')

    def close(self):
        """
        Функция очищает поле
        Автор: Озирный Максим
        """
        self.destroy()

    def open(self):
        """
        Функция заполняет поле контентом и устанавливает нужную высоту поля
        Автор: Озирный Максим
        """
        self.content()
        self.canvas.config(width=conf.WIDTH_FILR_FRAME)
        self.width_2 = conf.WIDTH_FILR_FRAME
        self.grid(row=1, column=1, sticky="nwes")

    def start_move(self, event=None):
        """
        Функция отслеживает при помощи условия возможность увеличения поля
        при этом изменяя переменную этого класса и изменяя внешний вид курсора
        Автор: Озирный Максим
        """
        # Проверка местоположения курсора для доступа к изменению ширины поля
        if event.x < 4:
            self.x = event.x_root
            self.frame.config(cursor=CURSOR_CHANGE_WIGHT)

    def stop_move(self, event=None):
        """
        Функция изменяет переменную, отвечающую за высоту поля,
        для дальнейшего корректного изменения параметра этого поля
        Автор: Озирный Максим
        """
        self.x = None
        self.width_2 = self.canvas.winfo_width()
        conf.WIDTH_FILR_FRAME = self.width_2
        self.frame.config(cursor='arrow')

    def on_motion(self, event):
        """
        Функция высчитывает и устанавливает новую высоту поля
        Автор: Озирный Максим
        """
        # Проверка на допустимость изменения ширины поля
        if self.x:
            deltay = self.x - event.x_root
            self.width = self.width_2
            if self.width + deltay < \
                    self.master.winfo_width() - MIN_WIDTH_TABLE - 60 \
                    and self.width + deltay > MIN_WIDTH_FILR_FRAME:
                self.width += deltay
                self.canvas.config(width=self.width)


class ColumnFilterPanel(Frame):
    """
    Функция создающая и позиционирующая содержимое
    поля отвечающего за фильтрацию столбцов
    Автор: Озирный Максим
    """
    x = 0
    width = WIDTH_FILR_FRAME
    width_2 = width
    _list_table = ["Наименование", "Цена", "Производитель", "Группа", "Скидка",
                   "Качество"]

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.canvas = Canvas(self, bg=COLOR_BG_FRAME_TABLE,
                             width=WIDTH_FILR_FRAME - 16)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=16)

    def click(self, event=None):
        """
        Функция вызываемая при нажатии на checkbox
        Автор: Озирный Максим
        """
        pass

    def content(self):
        """
        Функция создающая и позиционирующая содержимое
        поля отвечающего за фильтрацию столбцов
        Автор: Озирный Максим
        """
        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = Frame(self.canvas, bg=COLOR_BG_FRAME_TABLE)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)
        # для корректной прокрутки canvas прописываем событие изменяющее
        # положение содержимого при прокрутке
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas:
        self.on_frame_configure(self.canvas))
        self.canvas.grid(row=0, column=0, sticky="nwes")
        scroll.grid(row=0, column=1, sticky="nwes")
        # Заголовок поля
        title_1 = Label(self.frame, text="Продукты", bg=COLOR_BG_FRAME_FILTR,
                        fg=COLOR_FG_FRAME_FILTR, font=FONT_TITLE_FILTR)
        title_1.grid(row=0, column=0, sticky="we", padx=10, ipadx=10)
        # Черта под заголовком
        frame5 = Frame(self.frame, height=1, bg="#000")
        frame5.grid(row=1, column=0, sticky="we", padx=10, ipadx=10)
        ind = 0
        # в цикле создаются и позиционируются подзаголовки и соответствующие
        # им объекты (Scale или Combobox) в зависимости от содержимого списка
        for ind in range(len(self._list_table)):
            check = Checkbutton(self.frame, bg=COLOR_BG_FRAME_TABLE, bd=0,
                                fg=COLOR_FG_FRAME_TABLE,
                                text="{}".format(self._list_table[ind]))
            check.bind("<Button-1>", self.click)
            check.grid(row=2 + ind, column=0, sticky="w", padx=10)

        # Кнопка вызывающая функцию отвечающюю за фильтрацию строк
        btn = Button(self.frame, text="Сохранить")
        btn.grid(row=4 + ind, column=0, sticky="we", padx=10, pady=2)

        # отслеживаем события для изменения ширины поля
        self.frame.bind("<ButtonPress-1>", self.start_move)
        self.frame.bind("<ButtonRelease-1>", self.stop_move)
        self.frame.bind("<B1-Motion>", self.on_motion)
        self.frame.bind("<Motion>", self.change_cursor)
        self.frame.bind("<Leave>", self.on_leave)

    @staticmethod
    def on_frame_configure(main_lab2):
        """
        Функция необходимая для прокрутки содержимого в canvas
        Автор: Озирный Максим
        """
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    def change_cursor(self, event=None):
        if event.x < 4:
            self.frame.config(cursor=CURSOR_CHANGE_WIGHT)
        else:
            self.frame.config(cursor='arrow')

    def on_leave(self, event=None):
        self.frame.config(cursor='arrow')

    def close(self):
        """
        Функция очищает поле
        Автор: Озирный Максим
        """
        self.destroy()

    def open(self):
        """
        Функция заполняет поле контентом и устанавливает нужную высоту поля
        Автор: Озирный Максим
        """
        self.content()
        self.canvas.config(width=conf.WIDTH_FILR_FRAME)
        self.width_2 = conf.WIDTH_FILR_FRAME
        self.grid(row=1, column=2, sticky="nwes")

    def start_move(self, event=None):
        """
        Функция отслеживает при помощи условия возможность увеличения поля
        при этом изменяя переменную этого класса и изменяя внешний вид курсора
        Автор: Озирный Максим
        """
        # Проверка местоположения курсора для доступа к изменению высоты поля
        if event.x < 4:
            self.x = event.x_root
            self.frame.config(cursor=CURSOR_CHANGE_WIGHT)

    def stop_move(self, event=None):
        """
        Функция изменяет переменную, отвечающую за высоту поля,
        для дальнейшего корректного изменения параметра этого поля
        Автор: Озирный Максим
        """
        self.x = None
        self.width_2 = self.canvas.winfo_width()
        conf.WIDTH_FILR_FRAME = self.width_2
        self.frame.config(cursor='arrow')

    def on_motion(self, event):
        """
        Функция высчитывает и устанавливает новую высоту поля
        Автор: Озирный Максим
        """
        # Проверка на допустимость изменения высоты поля
        if self.x:
            deltay = self.x - event.x_root
            self.width = self.width_2
            if self.width + deltay < \
                    self.master.winfo_width() - MIN_WIDTH_TABLE - 60 \
                    and self.width + deltay > MIN_WIDTH_FILR_FRAME:
                self.width += deltay
                self.canvas.config(width=self.width)


class ChangeHistoryPanel(Canvas):
    """
    Класс отвечающий за интерфейс контента, который является
    информацией о последних изменениях пользователем
    Автор: Озирный Максим
    """
    y = 0
    height = HEIGHT_INFO_FRAME
    height_2 = height

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.master = master
        self.canvas = Canvas(self, bg=COLOR_BG_LAST_CH,
                             height=HEIGHT_INFO_FRAME)
        self.change_viewer = ChangeViewer()
        self.list_last_ch = self.change_viewer.get_history()
        # Устанавливаем размерную сетку для содержимого
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=12)

    @staticmethod
    def on_frame_configure(main_lab2):
        """
        Функция необходимая для прокрутки содержимого в canvas
        Автор: Озирный Максим
        """
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    def content(self):
        """
        Функция создающая и позиционирующая содержимое класса
        Автор: Озирный Максим
        """
        top_lab = Label(self, text="Последние изменения", anchor="w",
                        bg=COLOR_BG_TITLE_LAST_CH)
        self.top_lab = top_lab
        # отслеживаем события для изменения высоты поля
        top_lab.bind("<ButtonPress-1>", self.start_move)
        top_lab.bind("<ButtonRelease-1>", self.stop_move)
        top_lab.bind("<B1-Motion>", self.on_motion)
        top_lab.bind("<Motion>", self.change_cursor)
        top_lab.bind("<Leave>", self.on_leave)

        # создается полоса прокрутки и поле которые связываются с canvas
        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = Frame(self.canvas, bg=COLOR_BG_LAST_CH)
        self.canvas.create_window((0, 0), window=self.frame, anchor="n")
        self.canvas.configure(yscrollcommand=scroll.set,
                              height=HEIGHT_INFO_FRAME)
        # для корректной прокрутки canvas прописываем событие изменяющее
        # положение содержимого при прокрутке
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas:
                   self.on_frame_configure(self.canvas))
        # позиционируются объекты
        top_lab.grid(row=0, column=0, columnspan=2, sticky="nwes")
        self.canvas.grid(row=1, column=0, sticky="nwes")
        scroll.grid(row=1, column=1, sticky="nwes")
        # в цикле создаются и позиционируются текстовые поля с текстом,
        # соответствующим содержимому списка
        for ind in range(len(self.list_last_ch)):
            message = Label(self.frame, bg=COLOR_BG_LAST_CH, padx=10, bd=2,
                            fg="{}".format(self.list_last_ch[ind][0]),
                            text="{}".format(self.list_last_ch[ind][1]))
            message.grid()

    def change_cursor(self, event=None):
        if event.y < 4:
            self.top_lab.config(cursor=CURSOR_CHANGE_HEIGHT)
        else:
            self.top_lab.config(cursor='arrow')

    def on_leave(self, event=None):
        self.top_lab.config(cursor='arrow')

    def start_move(self, event=None):
        """
        Функция отслеживает при помощи условия возможность увеличения поля
        при этом изменяя переменную этого класса и изменяя внешний вид курсора
        Автор: Озирный Максим
        """
        # Проверка местоположения курсора для доступа к изменению высоты поля
        if event.y < 4:
            self.y = event.y_root
            self.top_lab.config(cursor=CURSOR_CHANGE_HEIGHT)

    def stop_move(self, event=None):
        """
        Функция изменяет переменную, отвечающую за высоту поля,
        для дальнейшего корректного изменения параметра этого поля
        Автор: Озирный Максим
        """
        self.y = None
        self.height_2 = self.canvas.winfo_height()
        conf.HEIGHT_INFO_FRAME = self.height_2
        self.top_lab.config(cursor='arrow')

    def on_motion(self, event):
        """
        Функция высчитывает и устанавливает новую высоту поля
        Автор: Озирный Максим
        """
        # Проверка на допустимость изменения высоты поля
        if self.y:
            deltay = self.y - event.y_root
            self.height = self.height_2
            if self.height + deltay < \
                    self.master.winfo_height() - MIN_SIZE_TABLE - 75:
                self.height += deltay
                self.canvas.config(height=self.height)

    def close(self):
        """
        Функция очищает поле
        Автор: Озирный Максим
        """
        self.destroy()

    def open(self):
        """
        Функция заполняет поле контентом и устанавливает нужную высоту поля
        Автор: Озирный Максим
        """
        self.content()
        self.canvas.config(height=conf.HEIGHT_INFO_FRAME)
        self.height_2 = conf.HEIGHT_INFO_FRAME
        self.grid(row=2, column=0, columnspan=4, sticky="nwes")
