from tkinter import Frame, Tk, Label, Checkbutton, IntVar, BooleanVar, \
    Radiobutton, StringVar

from Work.Scripts.view.ui.custom_widgets import VerticalScrolledFrame
from Work.Scripts.view.ui.reports_settings.report_settings_window import \
    SettingsWindow


class SettingsBoxAndWhisker(SettingsWindow):

    def __init__(self, main):
        self.frame_1 = LeftFrame(["Ягоды", "Картошка", "Зёрна",
                                  "Мясо", "Для беременных", "Деликатесы",
                                  "Птица", "Рыба", "Хлеб",
                                  "Молочное", "Овощи", "Фрукты и ягоды"])
        self.frame_2 = RightFrame(["Молоко", "Курица", "Индейка", "Сосиски",
                                   "Петрушка",
                                   "Мука", "Макороны", "Хлеб"])
        super().__init__(main, self.frame_1, self.frame_2)

        self.set_left_title("Категория продуктов")
        self.set_right_title("Продукты")

        # Запуск обработчика событий
        self.main.mainloop()

    def get_group_list(self):
        chosen_group_list = []
        for k, v in dict(self.frame_1.get_chosen_groups()).items():
            chosen_group_list.append(k) if v.get() == 1 else None
        return chosen_group_list

    def get_quality_list(self):
        quality_list = []
        for k, v in dict(self.frame_2.get_chosen_subgroups()).items():
            quality_list.append(k) if v.get() == 1 else None
        return quality_list

    def click_report(self, event):
        print(self.get_group_list())
        print(self.get_quality_list())

    def click_clear(self, event):
        self.frame_2.clear()

    def click_default(self, event):
        self.frame_1.default()
        self.frame_2.default()


class LeftFrame(Frame):

    def __init__(self, prod_groups: list, **kw):
        super().__init__(**kw)

        self.prod_groups = list(set(prod_groups))
        self.prod_groups.sort()

        self.var = StringVar()
        self.var.set(self.prod_groups[0])
        for i in range(len(self.prod_groups)):
            self.grid_rowconfigure(i // 2, weight=1)
            self.grid_columnconfigure(i % 2, weight=1)

            radio_btn = Radiobutton(self, text=self.prod_groups[i],
                                    variable=self.var,
                                    value=self.prod_groups[i],
                                    font=("Times New Roman", 14))

            radio_btn.grid(row=i // 2, column=i % 2, sticky="w")

    def get_chosen_groups(self):
        return self.var

    def default(self):
        self.var.set(self.prod_groups[0])


class RightFrame(VerticalScrolledFrame):
    chosen_quality_dict = {}

    def __init__(self, products: list, **kw):
        super().__init__(**kw)
        buttons = []
        for prod in products:
            var = self.chosen_quality_dict[prod] = BooleanVar()
            buttons.append(
                Checkbutton(self.interior, text=prod))
            buttons[-1].pack()
            var.set(True)

    def get_chosen_subgroups(self):
        return self.chosen_quality_dict

    def default(self):
        for var in self.chosen_quality_dict.values():
            var.set(True)

    def clear(self):
        for var in self.chosen_quality_dict.values():
            var.set(False)


# SettingsBoxAndWhisker(Tk())
