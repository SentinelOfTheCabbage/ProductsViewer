"""asd"""
from tkinter import Frame, Canvas, Label, Button, \
    Checkbutton, Tk, Scrollbar, Menu, NSEW, NE, W, NW, NS, EW, Entry

from Work.Scripts.res.values.menu import MainMenuFactory, MainMenuListener
from Work.Scripts.src.test.main_table_interactor import MainTableInteractor
from Work.Scripts.src.view.ui.main_window.config import WIN_W_START, \
    WIN_H_START, \
    WIDTH_FILR_FRAME, COLOR_TEXT_TABLE, COLOR_BG_ODD_ROW, COLOR_BG_EVENT_ROW, \
    COLOR_BG_TITLE_TABLE, FILTER_TAB_TEXT, TABLES_TAB_TEXT, \
    LAST_CHANGES_CLOSED_TAB, LAST_CHANGES_OPENED_TAB, MENU_FILE_TEXT, \
    MENU_CHANGE_TEXT, MENU_REPORT_TEXT
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
        master.grid_rowconfigure(0, weight=1, minsize=150)
        master.grid_rowconfigure(1, minsize=0)
        master.grid_rowconfigure(2, minsize=24)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, minsize=0)
        master.grid_columnconfigure(2, minsize=0)
        master.grid_columnconfigure(3, minsize=24)

        footbar = OptionsMenu(master)
        footbar.create_menu()
        self.main_frame = MainTableFrame(master, bg="#f0f0f0")
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

        self.main_frame.grid(row=0, column=0, sticky=NSEW)
        self.filtr_frame.grid(row=0, column=1, sticky=NSEW)
        self.table_frame.grid(row=0, column=2, sticky=NSEW)
        # self.last_ch_frame.grid(row=1, column=0, columnspan=4, sticky="nwes")
        self.right_menu.grid(row=0, column=3, sticky=NSEW)
        self.bottom_btn.grid(row=2, column=0, columnspan=4, sticky=NSEW)

        self.master.bind_all("<MouseWheel>", self.on_mousewheel)
        self.master.bind('<Left>', self.left_key)
        self.master.bind('<Right>', self.right_key)
        self.master.bind('<Up>', self.top_key)
        self.master.bind('<Down>', self.bottom_key)
        self.master.bind("<Configure>", self.new_height)
        master.mainloop()

    def get_tab_btn(self, text):
        tab = Canvas(self.right_menu, height=55, width=20, bd=0, bg="#f0f0f0")
        tab.create_text((20, 55), angle="-90", anchor=NE, text=text)
        return tab

    def new_height(self, event):
        if self.last_ch_bool:
            self.main_frame.cont.config(
                height=self.master.winfo_height() - 94 -
                       self.last_ch_frame.canvas.winfo_height())
        else:
            self.main_frame.cont.config(height=self.master.winfo_height() - 70)

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
        print(self)
        print(widget)
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
    col = len(_bd_array[0])
    row = len(_bd_array)
    list_cell = []
    list_check = []

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, minsize=24)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=24)

        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas, background="blue")
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        self.titles = Canvas(self.frame, bg="orange")
        self.cont = Canvas(self.frame, bg="#f0f0f0", height=350)
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
        self.content(self.titles, self.frame2)

        self.menu = Menu(self.master, tearoff=0)
        self.menu.add_command(label="Undo")
        self.menu.add_command(label="Redo")

        self.plus = Menu(self.master, tearoff=0)
        self.plus.add_command(label="мб плюс что-то")
        self.plus.add_command(label="или кого-то")

    def context_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def click_plus(self, event):
        self.plus.post(event.x_root, event.y_root)

    def widget_pointer(self):
        """ asd"""
        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)
        widget = "{}".format(widget)
        return widget

    def click_check(self, event):
        widget = self.widget_pointer()
        if widget[49:] == "":
            z = 0
        else:
            z = int(widget[49:]) - 1
        if "#000" in "{}".format(
                self.list_cell[self.col * z]["disabledbackground"]):
            if z % 2 == 0:
                self.list_check[z].config(background=COLOR_BG_ODD_ROW)
                for i in range(self.col):
                    self.list_cell[self.col * z + i].config(
                        disabledbackground=COLOR_BG_ODD_ROW)
            else:
                self.list_check[z].config(background=COLOR_BG_EVENT_ROW)
                for i in range(self.col):
                    self.list_cell[self.col * z + i].config(
                        disabledbackground=COLOR_BG_EVENT_ROW)
        else:
            self.list_check[z].config(background="#000")
            for i in range(self.col):
                self.list_cell[self.col * z + i].config(
                    disabledbackground="#000")

    def on_frame_configure(self, main_lab2):
        """Reset the scroll region to encompass the inner frame"""
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    def content(self, frame1, frame2):
        """ asd"""
        for r in range(self.row):
            for c in range(self.col + 1):
                if r == 0:
                    if c == 0:
                        self.cell = Label(frame1, width=3, text="+",
                                          relief="flat")
                        self.cell.bind("<Button-1>", self.click_plus)
                    else:
                        self.cell = Entry(frame1, relief="flat", width=11,
                                          disabledbackground=COLOR_BG_TITLE_TABLE)
                        self.cell.insert(0, "{}".format(
                            self._bd_array[r][c - 1]))
                        self.cell.config(state="disabled", bg="red")
                else:
                    if c == 0:
                        self.cell = CheckRowButton(frame2, r)
                        self.cell.bind("<Button-1>", self.click_check)
                        self.list_check.append(self.cell)
                    else:
                        self.cell = Entry(frame2, relief="flat", width=11,
                                          disabledbackground=COLOR_BG_ODD_ROW)
                        self.cell.insert(0, "{}".format(
                            self._bd_array[r][c - 1]))
                        self.cell.config(state="disabled", bg="red")
                        self.list_cell.append(self.cell)
                        if r % 2 == 0:
                            self.cell.config(
                                disabledbackground=COLOR_BG_EVENT_ROW)
                self.cell.bind("<Button-3>", self.context_menu)
                self.cell.grid(row=r, column=c, sticky="nwes")
                self.cell.config(bd=2, fg=COLOR_TEXT_TABLE,
                                 bg=COLOR_BG_ODD_ROW,
                                 )
                self.cell.bind("<Button-3>", self.context_menu)
                if r % 2 == 0:
                    self.cell.config(bg=COLOR_BG_EVENT_ROW)
                if r == 0:
                    self.cell.config(bg=COLOR_BG_TITLE_TABLE)

class CheckRowButton(Checkbutton):
    """"asd"""

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)


class OptionsMenu(Menu, MainMenuListener):
    """ asd"""

    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)

    def create_menu(self):
        """asd"""
        menu_factory = MainMenuFactory(self)

        menu_file = menu_factory.get_menu(MENU_FILE_TEXT,
                                          menu_factory.get_file_items())
        menu_change = menu_factory.get_menu(MENU_CHANGE_TEXT,
                                            menu_factory.get_change_items())
        menu_report = menu_factory.get_menu(MENU_REPORT_TEXT,
                                            menu_factory.get_report_items())

        main_menu = Menu()
        main_menu.add_cascade(menu_file)
        main_menu.add_cascade(menu_change)
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
