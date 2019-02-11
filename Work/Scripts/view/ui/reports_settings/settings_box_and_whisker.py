from Work.Scripts.view.ui.reports_settings.choice_frames import \
    MultiChoiceFrame
from Work.Scripts.view.ui.reports_settings.report_settings_window import \
    SettingsWindow


class SettingsBoxAndWhisker(SettingsWindow):

    def __init__(self, main):
        self.frame_1 = MultiChoiceFrame(main, ["Ягоды", "Картошка", "Зёрна",
                                               "Мясо", "Для беременных",
                                               "Деликатесы",
                                               "Птица", "Рыба", "Хлеб",
                                               "Молочное", "Овощи",
                                               "Фрукты и ягоды"])
        self.frame_2 = MultiChoiceFrame(main, ["Молоко", "Курица", "Индейка",
                                               "Сосиски",
                                               "Петрушка",
                                               "Мука", "Макороны", "Хлеб"])
        super().__init__(main, self.frame_1, self.frame_2)

        self.set_left_title("Категория продуктов")
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
