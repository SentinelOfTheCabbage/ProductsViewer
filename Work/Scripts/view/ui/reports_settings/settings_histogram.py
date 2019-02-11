from tkinter import Checkbutton, BooleanVar

from Work.Scripts.view.ui.custom_widgets import VerticalScrolledFrame
from Work.Scripts.view.ui.reports_settings.choice_frames import \
    MultiChoiceFrame
from Work.Scripts.view.ui.reports_settings.report_settings_window import \
    SettingsWindow


class SettingsHistogram(SettingsWindow):

    def __init__(self, main):
        self.frame_1 = MultiChoiceFrame(main,
                                        ["Производитель", "Группа продуктов",
                                         "Чеки"])
        self.frame_2 = MultiChoiceFrame(main, ["Молочное", "Овощи",
                                               "Мясопродукты и яйца",
                                               "Фруктоы и ягоды",
                                               "Зерннвые",
                                               "Картофель"])
        super().__init__(main, self.frame_1, self.frame_2)

        self.set_left_title("Категория")
        self.set_right_title("Продукты")

        # Запуск обработчика событий
        self.main.mainloop()

    def get_group_list(self):
        chosen_group_list = []
        for k, v in dict(self.frame_1.get_data()).items():
            chosen_group_list.append(k) if v.get() == 1 else None
        return chosen_group_list

    def get_quality_list(self):
        quality_list = []
        for k, v in dict(self.frame_2.get_data()).items():
            quality_list.append(k) if v.get() == 1 else None
        return quality_list

    def click_clear(self, event):
        pass

    def click_default(self, event):
        pass

    def click_reports(self, event):
        pass


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

# SettingsHistogram(Tk())
