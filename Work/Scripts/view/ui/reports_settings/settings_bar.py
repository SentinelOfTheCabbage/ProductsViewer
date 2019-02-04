from tkinter import Frame, Tk, Label, Checkbutton, IntVar, BooleanVar

from Work.Scripts.view.ui.reports_settings.report_settings_window import \
    SettingsWindow


class SettingsBar(SettingsWindow):

    def __init__(self, main):
        self.frame_1 = LeftFrame(["Ягоды", "Картошка", "Зёрна",
                                  "Мясо", "Для беременных", "Деликатесы",
                                  "Птица", "Рыба", "Хлеб",
                                  "Молочное", "Овощи", "Фрукты и ягоды"])
        self.frame_2 = RightFrame(["ГОСТ", "СТО", "ТУ"])
        super().__init__(main, self.frame_1, self.frame_2,
                         title_main="Заголовок")

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
        self.frame_1.clear()
        self.frame_2.clear()

    def click_default(self, event):
        self.frame_1.default()
        self.frame_2.default()


class LeftFrame(Frame):
    chosen_group_dict = {}

    def __init__(self, prod_groups: list, **kw):
        prod_groups = list(set(prod_groups))
        super().__init__(**kw)
        for i in range(len(prod_groups)):
            self.grid_rowconfigure(i // 2, weight=1)
            self.grid_columnconfigure(i % 2, weight=1)
            var = self.chosen_group_dict[prod_groups[i]] = BooleanVar()
            if i % 2 == 0:
                var.set(True)
            check_btn = Checkbutton(self, text=prod_groups[i],
                                    variable=var,
                                    font=("Times New Roman", 14))

            check_btn.grid(row=i // 2, column=i % 2, sticky="w")

    def get_chosen_groups(self):
        return self.chosen_group_dict

    def default(self):
        iterator = list(self.chosen_group_dict.values())
        for i in range(len(iterator)):
            iterator[i].set(True) if i % 2 == 0 else iterator[i].set(False)

    def clear(self):
        for var in self.chosen_group_dict.values():
            var.set(False)


class RightFrame(Frame):
    chosen_quality_dict = {}

    def __init__(self, quality_subgroups: list, **kw):
        super().__init__(**kw)
        self.grid_columnconfigure(0, weight=1)
        for i in range(len(quality_subgroups)):
            self.grid_rowconfigure(i, weight=1)
            var = self.chosen_quality_dict[quality_subgroups[i]] = BooleanVar()
            check_btn = Checkbutton(self, text=quality_subgroups[i],
                                    variable=var)
            var.set(True)
            check_btn.grid(row=i, column=0, sticky="w")

    def get_chosen_subgroups(self):
        return self.chosen_quality_dict

    def default(self):
        for var in self.chosen_quality_dict.values():
            var.set(True)

    def clear(self):
        for var in self.chosen_quality_dict.values():
            var.set(False)


SettingsBar(Tk())
