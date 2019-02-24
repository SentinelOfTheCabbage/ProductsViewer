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
    FONT_TITLE_FILTR, CURSOR_CHANGE_HEIGHT

import Work.Scripts.src.view.ui.main_window.config as conf

class RowFilterPanel(Frame):
    """
    Класс отвечающий за создание и позиционирование
    контента для работы с фильтрацией строк
    Автор: Озирный Максим
    """
    _list_filtr = [["Наименование", ["Кефир", "Молоко", "Хлеб"]],
                   ["Цена", 1280],
                   ["Производитель", ["деревня", "простоквашино"]],
                   ["Группа", ["Выпечка", "Молочка", "Мясо", "Алкоголь"]],
                   ["Скидка", 40],
                   ["Качество", ["ГОСТ", "СТО", "ТУ"]]]

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.config(bg=COLOR_BG_FRAME_FILTR)

    def content(self):
        """
        Функция создающая и позиционирующая содержимое
        поля отвечающего за фильтрацию строк
        Автор: Озирный Максим
        """
        # Заголовок поля
        title_1 = Label(self, text="Продукты", bg=COLOR_BG_FRAME_FILTR,
                        fg=COLOR_FG_FRAME_FILTR, font=FONT_TITLE_FILTR)
        title_1.place(relx=.15, y=14)
        # Черта под заголовком
        frame = Frame(self, height=1, bg="#000")
        frame.place(relx=.05, relwidth=.9, y=40)
        ind = 0
        # в цикле создаются и позиционируются подзаголовки и соответствующие
        # им объекты (Scale или Combobox) в зависимости от содержимого списка
        for ind in range(len(self._list_filtr)):
            title = Label(self, bg=COLOR_BG_FRAME_FILTR, bd=0,
                          fg=COLOR_FG_FRAME_FILTR,
                          text="{}:".format(self._list_filtr[ind][0]))
            title.place(relx=.1, y=45 + 24 * ind*2)
            if self._list_filtr[ind][0] == "Цена" or \
                    self._list_filtr[ind][0] == "Скидка":
                slider = IntVar()
                scale = Scale(self, orient="horizontal", length=95, from_=0,
                              to=self._list_filtr[ind][1], variable=slider)
                scale.place(relx=.2, y=45 + 23 * (ind*2+1))
                label = Label(self, textvariable=slider)
                label.place(relx=.8, y=47 + 23 * (ind*2+1))
            else:
                box = Combobox(self, width=13, values=self._list_filtr[ind][1])
                box.place(relx=.2, y=45 + 24 * (ind*2+1))

        # Кнопка вызывающая функцию отвечающюю за фильтрацию строк
        btn = Button(self, text="Сохранить")
        btn.place(relx=.2, y=50 + 24 * (ind*2 + 2))


class ColumnFilterPanel(Frame):
    """
    Функция создающая и позиционирующая содержимое
    поля отвечающего за фильтрацию столбцов
    Автор: Озирный Максим
    """
    _list_table = ["Наименование", "Цена", "Производитель", "Группа", "Скидка",
                   "Качество"]

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.config(bg=COLOR_BG_FRAME_TABLE)

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
        # Заголовок поля
        title_1 = Label(self, text="Продукты", bg=COLOR_BG_FRAME_TABLE,
                        fg=COLOR_FG_FRAME_TABLE, font=FONT_TITLE_FILTR)
        title_1.place(relx=.2, y=14)
        # Черта под заголовком
        frame = Frame(self, height=1, bg="#000")
        frame.place(relx=.05, relwidth=.9, y=40)
        # в цикле создаются чекбоксы с соответсвующим текстом в зависимости от
        # содержимого списка
        ind = 0
        for ind in range(len(self._list_table)):
            check = Checkbutton(self, bg=COLOR_BG_FRAME_TABLE, bd=0,
                                fg=COLOR_FG_FRAME_TABLE,
                                text="{}".format(self._list_table[ind]))
            check.bind("<Button-1>", self.click)
            check.place(relx=.1, y=45 + 24 * ind)
        # Кнопка вызывающая функцию отвечающюю за фильтрацию столбцов
        btn = Button(self, text="Сохранить")
        btn.place(relx=.2, y=50 + 24 * (ind + 1))


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
        self.canvas = Canvas(self, bg=COLOR_BG_LAST_CH,
                             height=HEIGHT_INFO_FRAME)
        self.change_viewer = ChangeViewer()
        self.list_last_ch = self.change_viewer.get_history()
        # Устанавливаем размерную сетку для содержимого
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=12)

    def on_frame_configure(self, main_lab2):
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

        # создается полоса прокрутки и поле которые связываются с canvas
        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        frame = Frame(self.canvas, bg=COLOR_BG_LAST_CH)
        self.canvas.create_window((0, 0), window=frame, anchor="n")
        self.canvas.configure(yscrollcommand=scroll.set,
                              height=HEIGHT_INFO_FRAME)
        # для корректной прокрутки canvas прописываем событие изменяющее
        # положение содержимого при прокрутке
        frame.bind("<Configure>", lambda event, canvas=self.canvas:
                   self.on_frame_configure(self.canvas))
        # позиционируются объекты
        top_lab.grid(row=0, column=0, columnspan=2, sticky="nwes")
        self.canvas.grid(row=1, column=0, sticky="nwes")
        scroll.grid(row=1, column=1, sticky="nwes")
        # в цикле создаются и позиционируются текстовые поля с текстом,
        # соответствующим содержимому списка
        for ind in range(len(self.list_last_ch)):
            message = Label(frame, bg=COLOR_BG_LAST_CH, padx=10, bd=2,
                            fg="{}".format(self.list_last_ch[ind][0]),
                            text="{}".format(self.list_last_ch[ind][1]))
            message.grid()

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
        self.height_2 = self.height
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
