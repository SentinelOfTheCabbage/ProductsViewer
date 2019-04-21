"""
Author: Andrew
"""
import tkinter
from tkinter import filedialog
import pandas as pd


class TkFileDialogExample(tkinter.Frame): # pylint: disable=too-many-ancestors
    """
    Класс графической составляющей ввода
    """

    def __init__(self):
        root = tkinter.Tk()
        root.title("GUI на Python")
        root.geometry("500x700")
        tkinter.Frame.__init__(self, root)
        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('pickle files', '.pickle')]
        options['initialfile'] = 'New'
        options['parent'] = root

    def asksaveasfilename(self):
        """
        Метод позволяет выбрать путь для сохранения файла в привычном окне
        :return: возвращает путь к будущему файлу
        """
        filename = filedialog.asksaveasfilename(**self.file_opt)
        return filename

    def askopenfilename(self):
        """
        Метод позволяет выбрать путь для открытия файла в привычном окне
        :return: возвращает путь к файлу
        """
        filename = filedialog.askopenfilename(**self.file_opt)
        return filename

    @staticmethod
    def option():
        """
        Метод реализует выбор пользователем значения из списка
        :return: выбранное значение
        """
        master = tkinter.Tk()
        master.title("Выберите стобец, индекс, подсчитываемый параметр")

        variable = tkinter.StringVar(master)
        variable.set("id")  # default value

        w_w = tkinter.OptionMenu(master, variable, "id", "name", "price", "producer_name",
                                 "group_name", "discount_id", "quality")
        w_w.pack()

        tkinter.mainloop()
        return variable.get()

    @staticmethod
    def option_2():
        """
        Метод реализует выбор пользователем значения из списка
        :return: выбранное значение
        """
        master = tkinter.Tk()
        message_label = tkinter.Label(master, text="Выберите нужный формат сохранения")
        message_label.grid(row=0, column=0, sticky='w')

        variable = tkinter.StringVar(master)
        variable.set("csv")  # default value

        w_w = tkinter.OptionMenu(master, variable, "csv", "txt", "xlsx", "pickle")
        w_w.grid(row=1, column=0, padx=5, pady=5)

        tkinter.mainloop()
        return variable.get()

    @staticmethod
    def option_3():
        """
        Метод реализует выбор пользователем нужной таблицы
        :return: имя выбранной таблицы
        """
        master = tkinter.Tk()
        master.title("Выберите нужную таблицу")

        variable = tkinter.StringVar(master)
        variable.set('_db_products')  # default value

        w_w = tkinter.OptionMenu(master, variable, '_db_products', '_db_sales',
                                 '_db_producers', '_db_groups', '_db_discounts', '_db_vouchers')
        w_w.pack()

        tkinter.mainloop()
        return variable.get()

    @staticmethod
    def entry():
        """
        Метод реализует ввод пользователем наименования
        :return: выбранное значение
        """

        def okay():
            global NA_ME
            NA_ME = message_entry.get()

        root = tkinter.Tk()

        message_label = tkinter.Label(text="Введите наименование или его часть")
        message_label.grid(row=0, column=0, sticky='w')
        message_entry = tkinter.Entry()
        message_entry.grid(row=1, column=1, padx=5, pady=5)

        o_k = tkinter.Button(root, text="Ok", command=okay)
        o_k.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        root.mainloop()
        return NA_ME


class Exporttable(pd.DataFrame):
    """
    Author: Andrew Fedorov
    Класс содержит методы экспорта таблицы  DataFrame в разных форматах
    """

    @staticmethod
    def csv(table: pd.DataFrame):
        """
        Author: Andrey Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате csv .
        """
        name = TkFileDialogExample().asksaveasfilename()
        table.to_csv(name+'.csv', sep=';', encoding='utf8', index=False)

    @staticmethod
    def csv_ind(table: pd.DataFrame):
        """
        Author: Andrey Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате csv с индексами.
        """
        name = TkFileDialogExample().asksaveasfilename()
        table.to_csv(name+'.csv', sep=';', encoding='utf8', index=False)

    @staticmethod
    def txt(table: pd.DataFrame):
        """
        Author: Andrey Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате txt .
        """
        name = TkFileDialogExample().asksaveasfilename()
        table.to_csv(name+'.txt', sep=';', encoding='utf8', index=False)

    @staticmethod
    def txt_ind(table: pd.DataFrame):
        """
        Author: Andrey Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате txt с индексами.
        """
        name = TkFileDialogExample().asksaveasfilename()
        table.to_csv(name+'.txt', sep=';', encoding='utf8', index=False)

    @staticmethod
    def pickle(table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате pickle.
        """
        name = TkFileDialogExample().asksaveasfilename()
        table.to_pickle(name+'.pickle')

    @staticmethod
    def xlsx(table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате xlsx.
        """
        name = TkFileDialogExample().asksaveasfilename()
        table.to_excel(name+'.xlsx', index=False)

    @staticmethod
    def xlsx_ind(table: pd.DataFrame):
        """
        Author: Andrew Fedorov
        :param table: таблица DataFrame
        :return: Сохраняет файл в формате xlsx с индексами.
        """
        name = TkFileDialogExample().asksaveasfilename()
        table.to_excel(name+'.xlsx', index=False)


class Reports:
    """
    Класс, содержащий методы создания отчетов
    """
    @staticmethod
    def sort_quality(table: pd.DataFrame):
        """
        Сортирует таблицу по искомому имени
        :return: Все продукты данной группы
        """
        name = TkFileDialogExample().entry()
        name = name.upper()
        df_d = table.quality.str.find(name)
        a_a = []
        rowsend = pd.DataFrame({'id': [], 'name': [], 'price': [],
                                'producer_name': [], 'group_name': [], 'discount_id': [],
                                'quality': [], })
        for num, row in enumerate(df_d):
            if row != -1:
                a_a.append(num)
        for i in a_a:
            rowsend = pd.concat([rowsend, table[table.index == i]])
        rowsend.id = pd.to_numeric(rowsend.id, downcast='integer')
        rowsend.discount_id = pd.to_numeric(rowsend.discount_id, downcast='integer')
        extension = TkFileDialogExample().option_2()
        if extension == "csv":
            Exporttable().csv(rowsend)
        elif extension == "pickle":
            Exporttable().pickle(rowsend)
        elif extension == "xlsx":
            Exporttable().xlsx(rowsend)
        elif extension == "txt":
            Exporttable().txt(rowsend)

    @staticmethod
    def sort_group_name(table: pd.DataFrame):
        """
        Сортирует таблицу по искомому имени
        :return: Все продукты данной группы
        """
        name = TkFileDialogExample().entry()
        df_d = table.group_name.str.find(name)
        a_a = []
        rowsend = pd.DataFrame({'id': [], 'name': [], 'price': [],
                                'producer_name': [], 'group_name': [], 'discount_id': [],
                                'quality': [], })
        for num, row in enumerate(df_d):
            if row != -1:
                a_a.append(num)
        for i in a_a:
            rowsend = pd.concat([rowsend, table[table.index == i]])
        rowsend.id = pd.to_numeric(rowsend.id, downcast='integer')
        rowsend.discount_id = pd.to_numeric(rowsend.discount_id, downcast='integer')
        extension = TkFileDialogExample().option_2()
        if extension == "csv":
            Exporttable().csv(rowsend)
        elif extension == "pickle":
            Exporttable().pickle(rowsend)
        elif extension == "xlsx":
            Exporttable().xlsx(rowsend)
        elif extension == "txt":
            Exporttable().txt(rowsend)

    @staticmethod
    def sort_producer_name(table: pd.DataFrame):
        """
        Сортирует таблицу по искомому имени
        :return: Все продукты с данного производителя
        """
        name = TkFileDialogExample().entry()
        df_d = table.producer_name.str.find(name)
        a_a = []
        rowsend = pd.DataFrame({'id': [], 'name': [], 'price': [],
                                'producer_name': [], 'group_name': [], 'discount_id': [],
                                'quality': [], })
        for num, row in enumerate(df_d):
            if row != -1:
                a_a.append(num)
        for i in a_a:
            rowsend = pd.concat([rowsend, table[table.index == i]])
        rowsend.id = pd.to_numeric(rowsend.id, downcast='integer')
        rowsend.discount_id = pd.to_numeric(rowsend.discount_id, downcast='integer')
        extension = TkFileDialogExample().option_2()
        if extension == "csv":
            Exporttable().csv(rowsend)
        elif extension == "pickle":
            Exporttable().pickle(rowsend)
        elif extension == "xlsx":
            Exporttable().xlsx(rowsend)
        elif extension == "txt":
            Exporttable().txt(rowsend)

    @staticmethod
    def sort_name(table: pd.DataFrame):
        """
        Сортирует таблицу по искомому имени
        :return: Все продукты с данным наименованием
        """
        name = TkFileDialogExample().entry()
        df_d = table.name.str.find(name)
        a_a = []
        rowsend = pd.DataFrame({'id': [], 'name': [], 'price': [],
                                'producer_name': [], 'group_name': [], 'discount_id': [],
                                'quality': []})
        for num, row in enumerate(df_d):
            if row != -1:
                a_a.append(num)
        for i in a_a:
            rowsend = pd.concat([rowsend, table[table.index == i]])
        rowsend.id = pd.to_numeric(rowsend.id, downcast='integer')
        rowsend.discount_id = pd.to_numeric(rowsend.discount_id, downcast='integer')
        extension = TkFileDialogExample().option_2()
        if extension == "csv":
            Exporttable().csv(rowsend)
        elif extension == "pickle":
            Exporttable().pickle(rowsend)
        elif extension == "xlsx":
            Exporttable().xlsx(rowsend)
        elif extension == "txt":
            Exporttable().txt(rowsend)

    @staticmethod
    def svod_table(rows: pd.DataFrame):
        """
        Формирование и сохранение сводной таблицы
        :return: сводная таблица по выбранным параметрам
        """

        columns = TkFileDialogExample().option()
        index = TkFileDialogExample().option()
        value = TkFileDialogExample().option()
        rows1 = rows.pivot_table(index=index, columns=columns, values=value, aggfunc='count')
        extension = TkFileDialogExample().option_2()
        if extension == "csv":
            Exporttable().csv_ind(rows1)
        elif extension == "pickle":
            Exporttable().pickle(rows1)
        elif extension == "xlsx":
            Exporttable().xlsx_ind(rows1)
        elif extension == "txt":
            Exporttable().txt_ind(rows1)


class Read:
    """
    Класс считывания таблиц пикл и преобразования в DataFrame
    """
    @staticmethod
    def read(path):
        """
        Author: Andrew Fedorov
        Функция чтения таблицы
        :param path: путь к таблице
        :return: требуемая таблица в формате DataFrame
        """
        table = pd.read_pickle(r""+path)
        dest = TkFileDialogExample().option_3()
        x_x = table[dest]
        return x_x

    @staticmethod
    def get_path():
        """
        Author: Andrew Fedorov
        :return: путь к файлу таблицы
        """
        pa_th = TkFileDialogExample().askopenfilename()
        return pa_th
