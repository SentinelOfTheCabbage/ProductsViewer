"""asd"""
from tkinter import Frame, Canvas, Label, Button, PhotoImage, \
    Checkbutton, Tk, Scrollbar, Menu, NSEW, NE, W, NW, NS, EW, Entry

from Work.Scripts.res.values.menu import MainMenuFactory, MainMenuListener
from Work.Scripts.src.test.main_table_interactor import MainTableInteractor
from Work.Scripts.src.view.ui.db_editor.db_editor import DbEditorWindow
from Work.Scripts.src.view.ui.main_window.config import WIN_W_START, \
    WIN_H_START, \
    WIDTH_FILR_FRAME, COLOR_TEXT_TABLE, COLOR_BG_ODD_ROW, COLOR_BG_EVENT_ROW, \
    COLOR_BG_TITLE_TABLE, FILTER_TAB_TEXT, TABLES_TAB_TEXT, \
    LAST_CHANGES_CLOSED_TAB, LAST_CHANGES_OPENED_TAB, MENU_FILE_TEXT, \
    MENU_CHANGE_TEXT, MENU_REPORT_TEXT, DEFAULT_SEARCH_TEXT, HEIGHT_ROW, \
    COLOR_BG_SELECT_ROW, COLOR_TEXT_TITLE
from Work.Scripts.src.view.ui.main_window.move_out_panels import \
    ChangeHistoryPanel, ColumnFilterPanel, RowFilterPanel
from Work.Scripts.src.view.ui.reports_settings.settings_bar_chart import \
    SettingsBarChart
from Work.Scripts.src.view.ui.reports_settings.settings_box_and_whisker import \
    SettingsBoxAndWhisker
from Work.Scripts.src.view.ui.reports_settings.settings_histogram import \
    SettingsHistogram
from Work.Scripts.src.view.ui.reports_settings.settings_scatter_chart import \
    SettingsScatterChart

main_table_interactor = MainTableInteractor()


class MainWindow:
    """asd """
    last_ch_bool = False
    filter_bool = False
    table_bool = False
    plus_bool = False

    def __init__(self, master, title="Заголовок"):
        self.master = master
        master.title(title)
        master.iconbitmap(
            r'D:\PycharmProjects\ProductsViewer\Work\Scripts\res\drawable\img.ico')
        master.geometry("{winw}x{winh}+{centerw}+{centerh}".format(
            winw=WIN_W_START,
            winh=WIN_H_START,
            centerw=(master.winfo_screenwidth() - WIN_W_START) // 2,
            centerh=(master.winfo_screenheight() - WIN_H_START - 30) // 2))
        master.minsize(WIN_W_START, WIN_H_START - 20)
        master.resizable(True, True)
        master.grid_rowconfigure(0, minsize=24)
        master.grid_rowconfigure(1, weight=1, minsize=150)
        master.grid_rowconfigure(2, minsize=0)
        master.grid_rowconfigure(3, minsize=24)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, minsize=0)
        master.grid_columnconfigure(2, minsize=0)
        master.grid_columnconfigure(3, minsize=24)

        footbar = OptionsMenu(master)
        footbar.create_menu()

        self.search_frame = Frame(master)
        self.search_frame.grid_columnconfigure(0, minsize=30)
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_frame.grid_columnconfigure(2, minsize=30)
        self.search_frame.grid_columnconfigure(3, minsize=30)
        self.search_frame.grid_columnconfigure(4, minsize=49)
        self.btn_plus = Button(self.search_frame, text="+", bd=0,
                               command=self.plus)
        self.btn_plus.grid(row=0, column=0)
        self.search = Entry(self.search_frame, fg="#d0d0d0")
        self.search.insert(0, DEFAULT_SEARCH_TEXT)
        self.search.bind("<Button-1>", self.click_search)
        self.search.grid(row=0, column=1, sticky="w")

        self.btn_save = Button(self.search_frame, bd=1, relief="ridge",
                               text="save", command=self.save_new_row)
        self.btn_or_no = Button(self.search_frame, bd=1, relief="ridge",
                                text="or no", command=self.plus)
        self.btn_save.grid(row=0, column=2)
        self.btn_or_no.grid(row=0, column=3)
        self.btn_save.grid_forget()
        self.btn_or_no.grid_forget()

        self.main_frame = MainTableFrame(master, self, self.btn_save, self.btn_or_no,
                                         bg="#f0f0f0")
        self.filtr_frame = RowFilterPanel(master)
        self.filtr_frame.content()
        self.table_frame = ColumnFilterPanel(master)
        self.table_frame.content()
        self.last_ch_frame = ChangeHistoryPanel(self.master)

        self.bottom_btn = Button(master, bg="red", anchor=W,
                                 text=LAST_CHANGES_CLOSED_TAB)
        self.bottom_btn.bind("<ButtonRelease-1>", self.click_extend_menu)

        self.right_menu = Frame(master)

        self.filter_btn = self.get_tab_btn(FILTER_TAB_TEXT)
        self.filter_btn.bind("<ButtonRelease-1>", self.click_filter)
        self.filter_btn.place(x=0, y=0)

        self.table_btn = self.get_tab_btn(TABLES_TAB_TEXT)
        self.table_btn.bind("<ButtonRelease-1>", self.click_table)
        self.table_btn.place(x=0, y=54)

        self.search_frame.grid(row=0, column=0, columnspan=4, sticky=NSEW)
        self.main_frame.grid(row=1, column=0, sticky=NSEW)
        self.filtr_frame.grid(row=1, column=1, sticky=NSEW)
        self.table_frame.grid(row=1, column=2, sticky=NSEW)
        # self.last_ch_frame.grid(row=1, column=0, columnspan=4, sticky="nwes")
        self.right_menu.grid(row=1, column=3, sticky=NSEW)
        self.bottom_btn.grid(row=3, column=0, columnspan=4, sticky=NSEW)

        self.master.bind_all("<MouseWheel>", self.on_mousewheel)
        self.master.bind('<Left>', self.left_key)
        self.master.bind('<Right>', self.right_key)
        self.master.bind('<Up>', self.top_key)
        self.master.bind('<Down>', self.bottom_key)
        self.master.bind("<Configure>", self.new_height)
        self.master.bind("<Button-1>", self.del_focus)
        master.mainloop()

    def plus(self):
        """asd """
        if self.plus_bool:
            self.btn_plus.config(text="+")
            self.btn_save.grid_forget()
            self.btn_or_no.grid_forget()
            self.main_frame.del_new_row()
        else:
            self.btn_plus.config(text="×")
            self.main_frame.new_row()
        self.plus_bool = not self.plus_bool

    def save_new_row(self):
        self.main_frame._bd_array.append([])
        for i in range(self.main_frame.col):
            self.main_frame._bd_array[len(self.main_frame._bd_array)-1].append(
                "{}".format(self.main_frame.list_new_col[i].get()))
        r = len(self.main_frame._bd_array) - 1
        self.main_frame.frame2.grid_rowconfigure(r, minsize=22)
        self.main_frame.list_row[r] = 0
        for c in range(self.main_frame.col):
            self.new_frame = Frame(self.main_frame.frame2)
            self.cell = Entry(self.new_frame)
            self.main_frame.list_frame.append(self.new_frame)
            self.main_frame.list_cell.append(self.cell)
            self.cell.bind("<Button-1>", self.main_frame.click_cell)
            self.cell.bind("<Double-1>", self.main_frame.double_click_cell)
            self.cell.bind("<Button-3>", self.main_frame.context_menu)

            self.cell.insert(0, "{}".format(self.main_frame._bd_array[r][c]))
            self.new_frame.grid(row=r, column=c, sticky="nwes")
            self.cell.grid()
            self.cell.config(relief="flat", width=11,
                             state="disabled",
                             fg=COLOR_TEXT_TABLE,
                             bg="#fff",
                             )
        self.main_frame.repaint()

    def click_search(self, event):
        if self.search.get() == DEFAULT_SEARCH_TEXT:
            self.search.delete(0, "end")
            self.search.config(fg="#000")

    def del_focus(self, event):
        if ".!frame.!entry" != "{}".format(self.widget_pointer()):
            if self.search.get() == "":
                self.search.config(fg="#d0d0d0")
                self.search.insert(0, DEFAULT_SEARCH_TEXT)

    def get_tab_btn(self, text):
        tab = Canvas(self.right_menu, height=55, width=20, bd=0, bg="#f0f0f0")
        tab.create_text((20, 55), angle="-90", anchor=NE, text=text)
        return tab

    def new_height(self, event):
            if self.last_ch_bool:
                self.main_frame.cont.config(
                    height=self.master.winfo_height() - 99 -
                           self.main_frame.titles.winfo_height() -
                           self.last_ch_frame.canvas.winfo_height())
            else:
                self.main_frame.cont.config(
                    height=self.master.winfo_height() - 75 -
                           self.main_frame.titles.winfo_height())

    def left_key(self, event):
        """ asd"""
        self.main_frame.canvas.xview_scroll(-1, "units")

    def right_key(self, event):
        """ asd"""
        self.main_frame.canvas.xview_scroll(1, "units")

    def top_key(self, event):
        """asd """
        widget = self.widget_pointer()
        if "maintableframe" in widget and "canvas" in widget:
            self.main_frame.cont.yview_scroll(-1, "units")
        elif "changehistorypanel" in widget and "canvas" in widget:
            self.last_ch_frame.canvas.yview_scroll(-1, "units")

    def bottom_key(self, event):
        """ asd"""
        widget = self.widget_pointer()
        if "maintableframe" in widget and "canvas" in widget:
            self.main_frame.cont.yview_scroll(1, "units")
        elif "changehistorypanel" in widget and "canvas" in widget:
            self.last_ch_frame.canvas.yview_scroll(1, "units")

    def on_mousewheel(self, event):
        """ asd"""
        widget = self.widget_pointer()
        sgn = -1 * (event.delta // 120)
        if "maintableframe" in widget and "canvas" in widget:
            self.main_frame.cont.yview_scroll(sgn, "units")
        elif "changehistorypanel" in widget and "canvas" in widget:
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
            self.bottom_btn.config(text=LAST_CHANGES_CLOSED_TAB)
            self.last_ch_frame.close()
        else:
            self.bottom_btn.config(text=LAST_CHANGES_OPENED_TAB)
            self.last_ch_frame = ChangeHistoryPanel(self.master)
            self.last_ch_frame.open()
        self.last_ch_bool = not self.last_ch_bool

    def click_filter(self, event):
        """ asd"""
        if self.table_bool:
            self.master.grid_columnconfigure(2, minsize=0)
            self.table_btn.config(bg="#f0f0f0")
            self.table_bool = not self.table_bool
        if self.filter_bool:
            self.master.grid_columnconfigure(1, minsize=0)
            self.filter_btn.config(bg="#f0f0f0")
        else:
            self.filter_btn.config(bg="#B2B2B2")
            self.master.grid_columnconfigure(1, minsize=WIDTH_FILR_FRAME)
        self.filter_bool = not self.filter_bool

    def click_table(self, event):
        """ asd"""
        if self.filter_bool:
            self.master.grid_columnconfigure(1, minsize=0)
            self.filter_btn.config(bg="#f0f0f0")
            self.filter_bool = not self.filter_bool
        if self.table_bool:
            self.master.grid_columnconfigure(2, minsize=0)
            self.table_btn.config(bg="#f0f0f0")
        else:
            self.table_btn.config(bg="#B2B2B2")
            self.master.grid_columnconfigure(2, minsize=WIDTH_FILR_FRAME)
        self.table_bool = not self.table_bool

class MainTableFrame(Canvas):
    """ asd"""
    _bd_array = main_table_interactor.get_data(None, None)
    _array_titles = _bd_array[0]
    _array_cell = []
    for i in range(len(_bd_array)-1):
        _array_cell.append(_bd_array[i+1])
    col = len(_bd_array[0])
    row = len(_bd_array)
    list_new_col = []
    list_max = {}
    for i in range(col):
        list_new_col.append(1)
    widget = ""
    start_value = ""
    z = 0
    list_row = {}
    list_cell = []
    list_titles = []
    list_frame = []

    def __init__(self, master, main, btn1, btn2, **kw):
        super().__init__(master, {}, **kw)
        self.btn1 = btn1
        self.btn2 = btn2
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, minsize=24)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=24)

        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas, background="blue")
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        self.titles = Canvas(self.frame, bg=COLOR_BG_TITLE_TABLE)
        self.cont = Canvas(self.frame, height=350)
        self.titles.grid(row=0, column=0, sticky=NSEW)
        self.frame2 = Frame(self.cont, background="blue")
        self.cont.create_window((0, 0), window=self.frame2, anchor=NW)
        self.cont.grid(row=1, column=0, sticky=NSEW)

        scroll_x = Scrollbar(self, orient="horizontal",
                             command=self.canvas.xview)
        scroll_x.grid(row=1, column=0, sticky=EW)

        scroll_y = Scrollbar(self, orient="vertical", command=self.cont.yview)
        scroll_y.grid(row=0, column=1, sticky=NS)
        self.cont.configure(yscrollcommand=scroll_y.set)
        self.canvas.configure(xscrollcommand=scroll_x.set)
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas:
        self.on_frame_configure(self.canvas))
        self.frame2.bind("<Configure>", lambda event, canvas=self.cont:
        self.on_frame_configure(self.cont))
        self.add_arrow(self._bd_array[0])
        self.content(self.titles, self.frame2, self._bd_array)

        self.menu = Menu(self.master, tearoff=0, postcommand=self.new_xy_menu)
        self.menu.add_command(label="Изменить", command=self.before_change)
        self.menu.add_command(label="Добавить строку", command=main.plus)
        self.menu.add_command(label="Удалить строку", command=self.delete_row)

        self.black_menu = Menu(self.master, tearoff=0)
        self.black_menu.add_command(label="Отменить выделение",
                                    command=self.deselect)
        self.black_menu.add_command(label="Удалить строки",
                                    command=self.del_select)
        #self.master.bind("<Escape>", self.deselect)

    def del_select(self):
        for j in range(len(self.list_row)):
            if self.list_row[j] == 1:
                self.list_row[j] = 0
                self.frame2.grid_rowconfigure(j + 1, minsize=0)
                for i in range(self.col):
                    self.list_cell[
                        j * self.col + i].grid_forget()
                    self.list_frame[
                        j * self.col + i].grid_forget()
        self.repaint()

    def delete_row(self):
        if self.widget[54:-7] == "":
            z = 0
        else:
            z = int(self.widget[54:-7]) - 1
        self.frame2.grid_rowconfigure(z//self.col + 1, minsize=0)
        for i in range(self.col):
            self.list_cell[(z//self.col)*self.col + i].grid_forget()
            self.list_frame[(z // self.col) * self.col + i].grid_forget()
        self.repaint()

    def repaint(self):
        j = -1
        for i in range(len(self._bd_array)-1):
            if self.frame2.rowconfigure(i+1)['minsize'] == HEIGHT_ROW:
                j += 1
                if j % 2 == 0:
                    for z in range(len(self._bd_array[0])):
                        self.list_frame[i * len(self._bd_array[0]) + z].config(
                            bg=COLOR_BG_ODD_ROW)
                        self.list_cell[i * len(self._bd_array[0]) + z].config(
                            disabledbackground=COLOR_BG_ODD_ROW)
                else:
                    for y in range(len(self._bd_array[0])):
                        self.list_frame[i * len(self._bd_array[0]) + y].config(
                            bg=COLOR_BG_EVENT_ROW)
                        self.list_cell[i * len(self._bd_array[0]) + y].config(
                            disabledbackground=COLOR_BG_EVENT_ROW)

    def new_row(self):
        for r in range(self.col):
            new = Entry(self.titles, bd=0, width=self.list_max[r]+2)
            self.list_new_col[r] = new
            new.bind("<Key>", self.change_new_row)
            new.grid(row=1, column=1*r, sticky="w")

    def change_new_row(self, event):
        self.btn1.grid(row=0, column=2)
        self.btn2.grid(row=0, column=3)

    def del_new_row(self):
        for z in range(self.col):
            self.list_new_col[z].destroy()

    def deselect(self):
        # for j in range(len(self.list_row)):
        #     if self.list_row[j] == 1:
        #         self.list_row[j] = 0
        #         if j % 2 == 0:
        #             for i in range(self.col):
        #                 self.list_cell[self.col * j + i].config(
        #                     disabledbackground=COLOR_BG_ODD_ROW)
        #                 self.list_frame[self.col * j + i].config(
        #                     bg=COLOR_BG_ODD_ROW)
        #         else:
        #             for i in range(self.col):
        #                 self.list_cell[self.col * j + i].config(
        #                     disabledbackground=COLOR_BG_EVENT_ROW)
        #                 self.list_frame[self.col * j + i].config(
        #                     bg=COLOR_BG_EVENT_ROW)
        self.repaint()

    def new_xy_menu(self):
        self.widget = self.widget_pointer()

    def save_change(self, event=None):
        self.btn_on.destroy()
        self.btn_off.destroy()
        self.list_titles[self.z%self.col].config(width=11)
        self.list_cell[self.z].config(state="normal")
        self._bd_array[1 + self.z // self.col][self.z % self.col] = \
        self.list_cell[self.z].get()
        self.list_cell[self.z].config(state="disabled")
        self.max_width(self._bd_array, self.list_max, self.z%self.col)
        self.set_max_width(len(self._bd_array), len(self._bd_array[0]),
                           self.list_max)

    def set_max_width(self, num_row, num_col, list):
        for r in range(num_row):
            for c in range(num_col):
                if r == 0:
                    self.list_titles[c].config(width=self.list_max[c]+2)
                else:
                    self.list_cell[(r-1)*self.col + c].config(width=list[c]+2)

    def del_change(self, event=None):
        self.btn_on.destroy()
        self.btn_off.destroy()
        self.list_titles[self.z % self.col].config(
            width=self.list_max[self.z % self.col] + 2)
        self.list_cell[self.z].delete(0, "end")
        self.list_cell[self.z].insert(0, self.start_value)
        self.list_cell[self.z].config(state="disabled")

    def before_change(self):
        self.del_change(23)
        self.change()

    def change(self):
        if "entry" in self.widget:
            if self.widget[54:-7] == "":
                self.z = 0
            else:
                self.z = int(self.widget[54:-7]) - 1
        else:
            if self.widget[54:] == "":
                self.z = 0
            else:
                self.z = int(self.widget[54:]) - 1
        for c in range(self.col):
                self.list_titles[c].config(width=self.list_max[c] + 2)
        self.list_titles[self.z % self.col].config(
            width=self.list_max[self.z % self.col] + 9)
        self.list_cell[self.z].config(state="normal")
        self.btn_on = Button(self.list_frame[self.z], text="on", bd=0,
                             command=self.save_change)
        self.btn_off = Button(self.list_frame[self.z], text="off", bd=0,
                              command=self.del_change)
        self.btn_on.grid(row=0, column=1)
        self.btn_off.grid(row=0, column=2)
        self.start_value = self.list_cell[self.z].get()
        self.list_cell[self.z].bind('<Return>', self.save_change)
        self.list_cell[self.z].bind('<Escape>', self.del_change)
        self.list_cell[self.z].bind('<Double-1>', self.click_cell)

    def context_menu(self, event):
        self.new_xy_menu()
        if "entry" in self.widget:
            if self.widget[54:-7] == "":
                z = 0
            else:
                z = int(self.widget[54:-7]) - 1
        else:
            if self.widget[54:] == "":
                z = 0
            else:
                z = int(self.widget[54:]) - 1
        if COLOR_BG_SELECT_ROW == "{}".format(
            self.list_cell[z]["disabledbackground"]):
            self.black_menu.post(event.x_root, event.y_root)
        else:
            self.menu.post(event.x_root, event.y_root)

    def widget_pointer(self):
        """ asd"""
        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)
        widget = "{}".format(widget)
        return widget

    def click_title(self, event):
        widget = self.widget_pointer()
        if "entry" in widget:
            if widget[46:-7] == "":
                num = 0
            else:
                num = int(widget[46:-7]) - 1
        else:
            if widget[46:] == "":
                num = 0
            else:
                num = int(widget[46:]) - 1

        def sort_col(i):
            return i[num]

        self._array_cell.sort(key=sort_col)
        array = []
        for i in range(len(self._array_cell)):
            array.append(self._array_cell[i])
        array.insert(0, self._array_titles)

        self.recontent(self.titles, self.frame2, array)

    def click_cell(self, event):
        widget = self.widget_pointer()
        print(widget)
        if "entry" in widget:
            if widget[54:-7] == "":
                num = 0
            else:
                num = int(widget[54:-7]) - 1
        else:
            if widget[54:] == "":
                num = 0
            else:
                num = int(widget[54:]) - 1
        self.list_row[num // self.col] = not self.list_row[num // self.col]
        if "disabled" in "{}".format(
                self.list_cell[num]["state"]):
            if COLOR_BG_SELECT_ROW in "{}".format(
                    self.list_cell[num]["disabledbackground"]):
                if (num // self.col) % 2 == 0:
                    for i in range(self.col):
                        self.list_cell[
                            self.col * (num // self.col) + i].config(
                            disabledbackground=COLOR_BG_ODD_ROW)
                        self.list_frame[
                            self.col * (num // self.col) + i].config(
                            bg=COLOR_BG_ODD_ROW)
                else:
                    for i in range(self.col):
                        self.list_cell[
                            self.col * (num // self.col) + i].config(
                            disabledbackground=COLOR_BG_EVENT_ROW)
                        self.list_frame[
                            self.col * (num // self.col) + i].config(
                            bg=COLOR_BG_EVENT_ROW)
            else:
                for i in range(self.col):
                    self.list_cell[self.col * (num // self.col) + i].config(
                        disabledbackground=COLOR_BG_SELECT_ROW)
                    self.list_frame[self.col * (num // self.col) + i].config(
                        bg=COLOR_BG_SELECT_ROW)

    def double_click_cell(self, event):
        self.del_change(event)
        self.click_cell(event)
        self.new_xy_menu()
        self.change()

    def on_frame_configure(self, main_lab2):
        """Reset the scroll region to encompass the inner frame"""
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    def max_width(self, array, list, only=-1):
        if only != -1:
            max = len(self._bd_array[0][only])
            for row in range(len(array)):
                if max < len(self._bd_array[row][only]):
                    max = len(self._bd_array[row][only])
            list[only] = max
        else:
            for col in range(len(array[0])):
                max = len(self._bd_array[0][col])
                for row in range(len(array)):
                    if max < len(self._bd_array[row][col]):
                        max = len(self._bd_array[row][col])
                list[col] = max

    def add_arrow(self, list):
        for i in range(len(list)):
            list[i] += " ▲▼"

    def content(self, frame1, frame2, array):
        """ asd"""
        for child in frame1.winfo_children():
            for child2 in child.winfo_children():
                child2.destroy()
            child.destroy()
        for child in frame2.winfo_children():
            for child2 in child.winfo_children():
                child2.destroy()
            child.destroy()
        self.max_width(array, self.list_max)
        # for c in range(self.col):
        #     max = len(self._bd_array[0][c])
        #     for r in range(self.row):
        #         if max < len(self._bd_array[r][c]):
        #             max = len(self._bd_array[r][c])
        #     self.list_max[c] = max

        self.btn_on = Button(frame2, text="on")
        self.btn_off = Button(frame2, text="off")
        self.list_row = {}
        self.list_cell = []
        self.list_titles = []
        self.list_frame = []
        for r in range(len(array)):
            self.list_row[r] = 0
            frame2.grid_rowconfigure(r, minsize=HEIGHT_ROW)
            for c in range(len(array[0])):
                if r == 0:
                    self.new_frame = Frame(frame1)
                    self.cell = Entry(self.new_frame,
                                      disabledforeground=COLOR_TEXT_TITLE,
                                      fg=COLOR_TEXT_TITLE)
                    self.cell.bind("<Button-1>", self.click_title)
                    self.list_titles.append(self.cell)
                else:
                    self.new_frame = Frame(frame2)
                    self.cell = Entry(self.new_frame,
                                      disabledforeground=COLOR_TEXT_TABLE,
                                      fg=COLOR_TEXT_TABLE)
                    self.list_frame.append(self.new_frame)
                    self.list_cell.append(self.cell)
                    self.cell.bind("<Button-1>", self.click_cell)
                    self.cell.bind("<Double-1>", self.double_click_cell)
                    self.cell.bind("<Button-3>", self.context_menu)
                    self.new_frame.bind("<Button-1>", self.click_cell)
                    self.new_frame.bind("<Double-1>", self.double_click_cell)
                    self.new_frame.bind("<Button-3>", self.context_menu)
                self.cell.insert(0, "{}".format(array[r][c]))
                self.new_frame.config(bg=COLOR_BG_ODD_ROW, pady=5)
                self.new_frame.grid(row=r, column=c, sticky="nwes")
                self.cell.grid(sticky="nwes")
                self.cell.config(relief="flat", width=self.list_max[c]+2,
                                 state="disabled",
                                 bg="#fff",
                                 disabledbackground=COLOR_BG_ODD_ROW
                                 )
                if r % 2 == 0:
                    self.new_frame.config(bg=COLOR_BG_EVENT_ROW)
                    self.cell.config(disabledbackground=COLOR_BG_EVENT_ROW)
                if r == 0:
                    self.new_frame.config(bg=COLOR_BG_TITLE_TABLE)
                    self.cell.config(disabledbackground=COLOR_BG_TITLE_TABLE)
            frame2.grid_rowconfigure(0, minsize=0)

    def recontent(self, frame1, frame2, array):
        """ asd"""
        for r in range(len(array)-1):
            for c in range(len(array[0])):
                self.list_cell[r*len(array[0])+c].config(state="normal")
                self.list_cell[r*len(array[0])+c].delete(0, "end")
                self.list_cell[r*len(array[0])+c].insert(0, "{}".format(array[r+1][c]))
                self.list_cell[r*len(array[0])+c].config(state="disabled")
            frame2.grid_rowconfigure(0, minsize=0)

class OptionsMenu(Menu, MainMenuListener):
    """ asd"""

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)

    def create_menu(self):
        """asd"""
        menu_factory = MainMenuFactory(self)

        menu_file = menu_factory.get_menu(MENU_FILE_TEXT,
                                          menu_factory.get_file_items())
        menu_report = menu_factory.get_menu(MENU_REPORT_TEXT,
                                            menu_factory.get_report_items())

        main_menu = Menu()
        main_menu.add_cascade(menu_file)
        main_menu.add_cascade(menu_report)

        self.master.config(menu=main_menu)

    @staticmethod
    def create_simple_report():
        pass

    @staticmethod
    def create_statistic_report():
        pass

    @staticmethod
    def create_pivot_report():
        pass

    @staticmethod
    def create_scatter_chart():
        SettingsScatterChart(Tk())

    @staticmethod
    def create_bar_chart():
        SettingsBarChart(Tk())

    @staticmethod
    def create_box_and_whisker():
        SettingsBoxAndWhisker(Tk())

    @staticmethod
    def create_histogram():
        SettingsHistogram(Tk())

    @staticmethod
    def edit_db():
        DbEditorWindow(Tk(), "Расширенное редактирование БД")
