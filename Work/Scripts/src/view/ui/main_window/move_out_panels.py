from tkinter import Frame, Scrollbar, Label, Canvas, Button, Scale, Checkbutton

from Work.Scripts.src.test.change_viewer import ChangeViewer
from Work.Scripts.src.view.ui.main_window.config import COLOR_BG_FRAME_TABLE, \
    COLOR_FG_FRAME_TABLE, COLOR_BG_FRAME_FILTR, COLOR_FG_FRAME_FILTR, \
    COLOR_BG_TITLE_LAST_CH, COLOR_BG_LAST_CH, HEIGHT_INFO_FRAME


class RowFilterPanel(Frame):
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
        title_1 = Label(self, text="Производители:", bg=COLOR_BG_FRAME_FILTR,
                        fg=COLOR_FG_FRAME_FILTR, )
        title_1.place(x=20, y=14)
        for i in range(len(self._list_filtr)):
            check = Checkbutton(self, bg=COLOR_BG_FRAME_FILTR, bd=0,
                                fg=COLOR_FG_FRAME_FILTR,
                                text="{}".format(self._list_filtr[i]))
            check.bind("<Button-1>", self.click_check)
            check.place(x=10, y=40 + 24 * i)
        title_2 = Label(self, text="Цена:", bg=COLOR_BG_FRAME_FILTR,
                        fg=COLOR_FG_FRAME_FILTR, )
        title_2.place(x=20, y=40 + 24 * (i + 1))
        scale = Scale(self, orient="horizontal", length=100, from_=0, to=228,
                      bg=COLOR_BG_FRAME_FILTR)
        scale.place(x=20, y=40 + 24 * (i + 2))


class ColumnFilterPanel(Frame):
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
            tables_name.place(x=10, y=24 * j)


class ChangeHistoryPanel(Canvas):
    """ asd"""

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.canvas = Canvas(self, bg=COLOR_BG_LAST_CH,
                             height=HEIGHT_INFO_FRAME)
        self.grid_rowconfigure(0)
        self.change_viewer = ChangeViewer()
        self.list_last_ch = self.change_viewer.get_history()
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

        frame = Frame(self.canvas, bg=COLOR_BG_LAST_CH)
        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.create_window((0, 0), window=frame, anchor="n")
        self.canvas.configure(yscrollcommand=scroll.set)
        frame.bind("<Configure>", lambda event, canvas=self.canvas:
        self.on_frame_configure(self.canvas))
        top_lab.grid(row=0, column=0, columnspan=2, sticky="nwes")
        self.canvas.grid(row=1, column=0, sticky="nwes")
        scroll.grid(row=1, column=1, sticky="nwes")
        for r in range(len(self.list_last_ch)):
            message = Label(frame, bg=COLOR_BG_LAST_CH, padx=10, bd=2,
                            fg="{}".format(self.list_last_ch[r][0]),
                            text="{}".format(self.list_last_ch[r][1]))
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
