from Work.Scripts.view.ui.reports_settings.choice_frames import \
    MultiChoiceFrame
from Work.Scripts.view.ui.reports_settings.report_settings_window import \
    SettingsWindow


class SettingsBarChart(SettingsWindow):

    def __init__(self, main):
        self.frame_1 = MultiChoiceFrame(main, ["Ягоды", "Картошка", "Зёрна",
                                               "Мясо"])
        self.frame_2 = MultiChoiceFrame(main, ["ГОСТ", "СТО", "ТУ"])
        super().__init__(main, self.frame_1, self.frame_2)

        self.title_left_label['text'] = "1"
        self.title_right_label['text'] = "2"

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

    def click_reports(self, event):
        self.frame_1.get_data()

    def click_clear(self, event):
        self.frame_1.clear()

    def click_default(self, event):
        self.frame_1.default_choice()
