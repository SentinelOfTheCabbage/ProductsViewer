"""
Файл содержит классы представляющие собой вспомогающие поля в главном окне
т.е. фильтрацию и последние изменения
Автор: Озирный Максим
"""
# pylint: disable=E0401
# pylint: disable=R0901
from tkinter import Frame, Scrollbar, Label, Canvas, Button, \
    Checkbutton, IntVar
from tkinter.ttk import Combobox, Scale

from Work.Scripts import config as conf
from Work.Scripts.config import WIDTH_FILR_FRAME, COLOR_BG_FRAME_TABLE, \
    COLOR_BG_FRAME_FILTR, FONT_TITLE_FILTR, COLOR_FG_FRAME_FILTR, \
    CURSOR_CHANGE_WIGHT, MIN_WIDTH_TABLE, MIN_WIDTH_FILR_FRAME, \
    COLOR_FG_FRAME_TABLE, COLOR_BG_LAST_CH, HEIGHT_INFO_FRAME, \
    CURSOR_CHANGE_HEIGHT, MIN_SIZE_TABLE, COLOR_BG_TITLE_LAST_CH, \
    PADX_FILTR_TABLE, NAME_TITLES
from Work.Scripts.interactors import ListMainTableInteractor
from Work.Scripts.filters import FilterColumns as fil
# from Work.Scripts.filters import FilterRows as filrow

INTERACTOR = ListMainTableInteractor(True)


class ScaleFilter(Frame):
    """
    класс для посос прокрутки со специальными функциями и доп полем

    Автор: Озирный Максим
    """
    def __init__(self, master, value, **kw):
        super().__init__(master, {}, **kw)
        self.slider = IntVar(self)
        scale = Scale(self, orient="horizontal", length=95,
                      from_=0, to=value,
                      variable=self.slider, command=self.float_to_int)

        scale.pack(side="left")
        label = Label(self, textvariable=self.slider, width=6,
                      anchor="w", justify="left", background="#fff")
        label.pack(side="right", padx=10)

    def float_to_int(self, event=None):# pylint: disable=W0613
        """
        функция приводит значение типа float к integer, ч
        тоб показать его пользователю
        """
        self.slider.set(self.slider.get())


class RowFilterPanel(Frame):
    """
    Класс отвечающий за создание и позиционирование
    контента для работы с фильтрацией строк

    Автор: Озирный Максим
    """
    pos_x = 0
    width = WIDTH_FILR_FRAME
    width_2 = width
    _list_filtr = {"Цена": 0,
                   "Производитель": None,
                   "Группа": None,
                   "Скидка": 40,
                   "Качество": None}

    def __init__(self, master, m_table, **kw):
        super().__init__(master, {}, **kw)
        self.m_table = m_table
        self.canvas = Canvas(self, bg=COLOR_BG_FRAME_TABLE, bd=0,
                             width=WIDTH_FILR_FRAME - 16)
        self.frame = Frame(self.canvas, bg=COLOR_BG_FRAME_TABLE)

        self._list_filtr["Цена"] = INTERACTOR.get_max_price()
        self._list_filtr["Производитель"] = INTERACTOR.get_producers()
        self._list_filtr["Группа"] = INTERACTOR.get_products_groups()
        self._list_filtr["Скидка"] = INTERACTOR.get_max_discount()
        self._list_filtr["Качество"] = INTERACTOR.get_qualities()

        # отслеживаем события для изменения ширины поля
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<Motion>", self.change_cursor)
        self.canvas.bind("<Leave>", self.on_leave)
        self.frame.bind("<ButtonPress-1>", self.start_move)
        self.frame.bind("<ButtonRelease-1>", self.stop_move)
        self.frame.bind("<B1-Motion>", self.on_motion)
        self.frame.bind("<Motion>", self.change_cursor)
        self.frame.bind("<Leave>", self.on_leave)

        self.content()

    def content(self):
        """
        Функция создающая и позиционирующая содержимое
        поля отвечающего за фильтрацию строк

        Автор: Озирный Максим
        """
        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scroll.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)
        # для корректной прокрутки canvas прописываем событие изменяющее
        # положение содержимого при прокрутке
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas:
                        self.on_frame_configure(self.canvas))
        self.canvas.pack(side="top", fill="both", expand=1)
        # Заголовок поля
        title_1 = Label(self.frame, text="Продукты", bg=COLOR_BG_FRAME_FILTR,
                        fg=COLOR_FG_FRAME_FILTR, font=FONT_TITLE_FILTR)
        title_1.pack(side="top", padx=PADX_FILTR_TABLE+20, anchor="w")
        # Черта под заголовком
        line = Frame(self.frame, height=1, width=130, bg="#000")
        line.pack(side="top", padx=PADX_FILTR_TABLE, anchor="w")
        # в цикле создаются и позиционируются подзаголовки и соответствующие
        # им объекты (Scale или Combobox) в зависимости от содержимого списка
        for key in list(self._list_filtr.keys()):
            title = Label(self.frame, bg=COLOR_BG_FRAME_FILTR, bd=0,
                          fg=COLOR_FG_FRAME_FILTR,
                          text="{}:".format(key))
            title.pack(side="top", padx=PADX_FILTR_TABLE, anchor="w")
            if key in ("Цена", "Скидка"):
                scale = ScaleFilter(self.frame, self._list_filtr[key],
                                    bg=COLOR_BG_FRAME_TABLE)
                scale.pack(side="top", padx=PADX_FILTR_TABLE+10)
            else:
                box = Combobox(self.frame, width=15, state="readonly",
                               values=self._list_filtr[key])
                box.pack(side="top", padx=PADX_FILTR_TABLE+10, anchor="w")

        btn_1 = Button(self.frame, text="Сохранить", width=15,
                       command=self.save)
        btn_1.pack(side="top", padx=PADX_FILTR_TABLE+10, pady=10, anchor="w")

    def save(self, event=None):# pylint: disable=W0613
        """
        функция предназначенная для применения фильтрации
        Автор: Озирный Максим
        """
        ch = list(self.frame.winfo_children())
        g = 0
        slov = {}
        for i in range(len(ch)):
            if type(ch[i]) == type(Combobox()):
                slov.update({list(self._list_filtr.keys())[g]: ch[i].get()})
                g += 1
            if type(ch[i]) == type(ScaleFilter(self.canvas, self._list_filtr["Цена"])):
                slov.update({list(self._list_filtr.keys())[g]: ch[i].slider.get()})
                g += 1
        # filrow().filter(slov, self.m_table)

    @staticmethod
    def on_frame_configure(main_lab2):
        """
        Функция необходимая для прокрутки содержимого в canvas

        Автор: Озирный Максим
        """
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    def change_cursor(self, event=None):
        """
        функция предназначенная для изменения иконки курсора
        в крайнем левом положении

        Автор: Озирный Максим
        """
        if event.x < 4:
            self.config(cursor=CURSOR_CHANGE_WIGHT)
        else:
            self.config(cursor='arrow')

    def on_leave(self, event=None):# pylint: disable=W0613
        """
        функция предназначенная для возврата стандартной иконки курсора

        Автор: Озирный Максим
        """
        self.config(cursor='arrow')

    def close(self):
        """
        Функция очищает поле
        Автор: Озирный Максим
        """
        self.pack_forget()

    def open(self):
        """
        Функция упаковывает объект и устанавливает нужную ширину поля
        Автор: Озирный Максим
        """
        # self.content()
        self.canvas.config(width=conf.WIDTH_FILR_FRAME)
        self.width_2 = conf.WIDTH_FILR_FRAME
        self.pack(side="right", fill="y")

    def start_move(self, event=None):
        """
        Функция отслеживает при помощи условия возможность увеличения поля
        при этом изменяя переменную этого класса и изменяя внешний вид курсора
        Автор: Озирный Максим
        """
        # Проверка местоположения курсора для доступа к изменению ширины поля
        if event.x < 4:
            self.pos_x = event.x_root
            self.config(cursor=CURSOR_CHANGE_WIGHT)

    def stop_move(self, event=None):# pylint: disable=W0613
        """
        Функция изменяет переменную, отвечающую за высоту поля,
        для дальнейшего корректного изменения параметра этого поля
        Автор: Озирный Максим
        """
        self.pos_x = None
        self.width_2 = self.canvas.winfo_width()
        conf.WIDTH_FILR_FRAME = self.width_2 - 4
        self.config(cursor='arrow')

    def on_motion(self, event):
        """
        Функция высчитывает и устанавливает новую высоту поля
        Автор: Озирный Максим
        """
        # Проверка на допустимость изменения ширины поля
        if self.pos_x:
            deltay = self.pos_x - event.x_root
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
    mass = []
    pos_x = 0
    width = WIDTH_FILR_FRAME
    width_2 = width
    _list_table = NAME_TITLES

    def __init__(self, master, m_table, **kw):
        super().__init__(master, {}, **kw)
        self.m_table = m_table
        self.canvas = Canvas(self, bg=COLOR_BG_FRAME_TABLE,
                             width=WIDTH_FILR_FRAME - 16)
        self.frame = Frame(self.canvas, bg=COLOR_BG_FRAME_TABLE)

        # отслеживаем события для изменения ширины поля
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<Motion>", self.change_cursor)
        self.canvas.bind("<Leave>", self.on_leave)
        self.frame.bind("<ButtonPress-1>", self.start_move)
        self.frame.bind("<ButtonRelease-1>", self.stop_move)
        self.frame.bind("<B1-Motion>", self.on_motion)
        self.frame.bind("<Motion>", self.change_cursor)
        self.frame.bind("<Leave>", self.on_leave)

        self.content()

    def content(self):
        """
        Функция создающая и позиционирующая содержимое
        поля отвечающего за фильтрацию столбцов
        Автор: Озирный Максим
        """
        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scroll.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)
        # для корректной прокрутки canvas прописываем событие изменяющее
        # положение содержимого при прокрутке
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas:
                        self.on_frame_configure(self.canvas))
        self.canvas.pack(side="top", fill="both", expand=1)
        # Заголовок поля
        title_1 = Label(self.frame, text="Продукты", bg=COLOR_BG_FRAME_FILTR,
                        fg=COLOR_FG_FRAME_FILTR, font=FONT_TITLE_FILTR)
        title_1.pack(side="top", padx=PADX_FILTR_TABLE+20, anchor="w")
        # Черта под заголовком
        line = Frame(self.frame, height=1, width=130, bg="#000")
        line.pack(side="top", padx=PADX_FILTR_TABLE, anchor="w")
        # в цикле создаются и позиционируются подзаголовки и соответствующие
        # им объекты (Scale или Combobox) в зависимости от содержимого списка
        for ind in range(len(self._list_table)):
            var = IntVar()
            self.mass.append(var)
            check = Checkbutton(self.frame, bg=COLOR_BG_FRAME_TABLE, bd=0,
                                fg=COLOR_FG_FRAME_TABLE, variable=self.mass[ind],
                                text="{}".format(self._list_table[ind]))
            check.pack(side="top", padx=PADX_FILTR_TABLE, anchor="w")

        # Кнопка вызывающая функцию отвечающюю за  запуск фильтрации строк
        btn = Button(self.frame, text="Сохранить", width=15,
                     command=self.click_save)
        btn.pack(side="top", padx=PADX_FILTR_TABLE+10, pady=10, anchor="w")


    @staticmethod
    def on_frame_configure(main_lab2):
        """
        Функция необходимая для прокрутки содержимого в canvas
        Автор: Озирный Максим
        """
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    def click_save(self, event=None):# pylint: disable=W0613
        """
        функция предназначенная для применения фильтрации

        Автор: Озирный Максим
        """
        listik = []
        for i in self.mass:
            listik.append(i.get())
        listik2 = []
        len_list = len(listik)
        for i in range(len_list):
            if listik[i] == 1:
                listik2.append(self._list_table[i])
        fil().filter(listik2, self.m_table)

    def change_cursor(self, event=None):
        """
        функция предназначенная для изменения иконки курсора
        в крайнем левом положении

        Автор: Озирный Максим
        """
        if event.x < 4:
            self.config(cursor=CURSOR_CHANGE_WIGHT)
        else:
            self.config(cursor='arrow')

    def on_leave(self, event=None):# pylint: disable=W0613
        """
        функция предназначенная для возврата стандартной иконки курсора

        Автор: Озирный Максим
        """
        self.config(cursor='arrow')

    def close(self):
        """
        Функция очищает поле
        Автор: Озирный Максим
        """
        self.pack_forget()

    def open(self):
        """
        Функция упаковывает объект и устанавливает нужную ширину поля
        Автор: Озирный Максим
        """
        # self.content()
        self.canvas.config(width=conf.WIDTH_FILR_FRAME)
        self.width_2 = conf.WIDTH_FILR_FRAME
        self.pack(side="right", fill="y")

    def start_move(self, event=None):
        """
        Функция отслеживает при помощи условия возможность увеличения поля
        при этом изменяя переменную этого класса и изменяя внешний вид курсора
        Автор: Озирный Максим
        """
        # Проверка местоположения курсора для доступа к изменению высоты поля
        if event.x < 4:
            self.pos_x = event.x_root
            self.config(cursor=CURSOR_CHANGE_WIGHT)

    def stop_move(self, event=None):# pylint: disable=W0613
        """
        Функция изменяет переменную, отвечающую за высоту поля,
        для дальнейшего корректного изменения параметра этого поля
        Автор: Озирный Максим
        """
        self.pos_x = None
        self.width_2 = self.canvas.winfo_width()
        conf.WIDTH_FILR_FRAME = self.width_2 - 4
        self.config(cursor='arrow')

    def on_motion(self, event):
        """
        Функция высчитывает и устанавливает новую высоту поля
        Автор: Озирный Максим
        """
        # Проверка на допустимость изменения высоты поля
        if self.pos_x:
            deltay = self.pos_x - event.x_root
            self.width = self.width_2
            if self.width + deltay < \
                    self.master.winfo_width() - MIN_WIDTH_TABLE - 60 and \
                    self.width + deltay > MIN_WIDTH_FILR_FRAME:
                self.width += deltay
                self.canvas.config(width=self.width)


class ChangeHistoryPanel(Canvas):
    """
    Класс отвечающий за интерфейс контента, который является
    информацией о последних изменениях пользователем
    Автор: Озирный Максим
    """
    pos_y = 0
    height = HEIGHT_INFO_FRAME
    height_2 = height

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.canvas = Canvas(self, bg=COLOR_BG_LAST_CH,
                             height=HEIGHT_INFO_FRAME)
        self.frame = Frame(self.canvas, bg=COLOR_BG_LAST_CH)
        self.list_last_ch = [("black", "Дальнейшие изменения отсутствуют")]

        self.content()

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
        self.canvas = Canvas(self, bg=COLOR_BG_LAST_CH,
                             height=HEIGHT_INFO_FRAME)
        self.frame = Frame(self.canvas, bg=COLOR_BG_LAST_CH)
        self.top_lab = Label(self, text="Последние изменения", anchor="w",
                             bg=COLOR_BG_TITLE_LAST_CH)
        # отслеживаем события для изменения высоты поля

        self.top_lab.bind("<ButtonPress-1>", self.start_move)
        self.top_lab.bind("<ButtonRelease-1>", self.stop_move)
        self.top_lab.bind("<B1-Motion>", self.on_motion)
        self.top_lab.bind("<Motion>", self.change_cursor)
        self.top_lab.bind("<Leave>", self.on_leave)
        # создается полоса прокрутки и поле которые связываются с canvas
        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.create_window((0, 0), window=self.frame, anchor="n")
        self.canvas.configure(yscrollcommand=scroll.set,
                              height=HEIGHT_INFO_FRAME)
        # для корректной прокрутки canvas прописываем событие изменяющее
        # положение содержимого при прокрутке
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas:
                        self.on_frame_configure(self.canvas))
        # позиционируются объекты
        self.top_lab.pack(side="top", fill="x")
        scroll.pack(side="right", fill="y")
        self.canvas.pack(side="top", fill="both", expand=1)
        # в цикле создаются и позиционируются текстовые поля с текстом,
        # соответствующим содержимому списка
        ind = len(self.list_last_ch) - 1
        message = Label(self.frame, bg=COLOR_BG_LAST_CH, padx=10, bd=2,
                        fg="{}".format(self.list_last_ch[ind][0]),
                        text="{}".format(self.list_last_ch[ind][1]))
        message.pack(side="bottom", anchor="w")

    def dop_content(self, lst, event=None):
        message = Label(self.frame, bg=COLOR_BG_LAST_CH, padx=10, bd=2,
                        fg="{}".format(lst[0]),
                        text="{}".format(lst[1]))
        message.pack(side="bottom", anchor="w")

    def change_cursor(self, event=None):
        """
        функция предназначенная для изменения иконки курсора
        в крайнем верхнем положении

        Автор: Озирный Максим
        """
        if event.y < 4:
            self.top_lab.config(cursor=CURSOR_CHANGE_HEIGHT)
        else:
            self.top_lab.config(cursor='arrow')

    def on_leave(self, event=None):# pylint: disable=W0613
        """
        функция предназначенная для возврата стандартной иконки курсора

        Автор: Озирный Максим
        """
        self.top_lab.config(cursor='arrow')

    def start_move(self, event=None):
        """
        Функция отслеживает при помощи условия возможность увеличения поля
        при этом изменяя переменную этого класса и изменяя внешний вид курсора
        Автор: Озирный Максим
        """
        # Проверка местоположения курсора для доступа к изменению высоты поля
        if event.y < 4:
            self.pos_y = event.y_root
            self.top_lab.config(cursor=CURSOR_CHANGE_HEIGHT)

    def stop_move(self, event=None):# pylint: disable=W0613
        """
        Функция изменяет переменную, отвечающую за высоту поля,
        для дальнейшего корректного изменения параметра этого поля
        Автор: Озирный Максим
        """
        self.pos_y = None
        self.height_2 = self.canvas.winfo_height()
        conf.HEIGHT_INFO_FRAME = self.height_2
        self.top_lab.config(cursor='arrow')

    def on_motion(self, event):
        """
        Функция высчитывает и устанавливает новую высоту поля
        Автор: Озирный Максим
        """
        # Проверка на допустимость изменения высоты поля
        if self.pos_y:
            deltay = self.pos_y - event.y_root
            self.height = self.height_2
            if self.height + deltay < \
                    self.master.winfo_height() - MIN_SIZE_TABLE - 75:
                self.height += deltay
                self.canvas.config(height=self.height)

    def close(self):
        """
        Функция "распаковывает" объект
        Автор: Озирный Максим
        """
        self.pack_forget()

    def open(self):
        """
        Функция упаковывает объект
        Автор: Озирный Максим
        """
        self.pack(side="bottom", fill="x")
