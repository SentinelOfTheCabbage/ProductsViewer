from Work.Scripts.view.reports.clustered_chart import ClusteredChart
from Work.Scripts.view.ui.reports_settings.choice_frames import \
    MultiChoiceFrame
from Work.Scripts.view.ui.reports_settings.report_settings_window import \
    SettingsWindow, TEXT_KEY, SUCCESS_INFO_TEXT

SUBTITLE_LEFT = "Група продуктов"
SUBTITLE_RIGHT = "Категория качества"
ERROR_LEFT_INFO_TEXT = "Выберите продукты"
ERROR_RIGHT_INFO_TEXT = "Выберите категорию"


def get_data_1():
    return ["Ягоды", "Картошка", "Зёрна", "Мясо"]


def get_data_2():
    return ["ГОСТ", "СТО", "ТУ"]


class SettingsBarChart(SettingsWindow):

    def __init__(self, main):
        self.frame_1 = MultiChoiceFrame(main, get_data_1(),
                                        listener=self)
        self.frame_2 = MultiChoiceFrame(main, get_data_2(),
                                        True, listener=self)
        super().__init__(main, self.frame_1, self.frame_2)

        self.title_left_label[TEXT_KEY] = SUBTITLE_LEFT
        self.title_right_label[TEXT_KEY] = SUBTITLE_RIGHT

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
        prices = list(SettingsWindow.reports_interactor
                      .get_prices_by_group_and_quality(self.frame_1.get_data(),
                                                       self.frame_2.get_data())
                      .values())

        ClusteredChart() \
            .set_groups(self.frame_1.get_data()) \
            .set_quality_labels(self.frame_2.get_data()) \
            .set_prices(prices) \
            .set_y_title("Цены") \
            .show()

    def click_clear(self, event):
        self.frame_1.clear()
        self.frame_2.clear()

    def click_default(self, event):
        self.frame_1.default_choice()
        self.frame_2.default_choice()

    def error(self, frame):
        if frame == self.frame_1:
            self.left_choice_is_done = False
        if frame == self.frame_2:
            self.right_choice_is_done = False
        self.output_success_info()

    def success(self, frame):
        if frame == self.frame_1:
            self.left_choice_is_done = True
        if frame == self.frame_2:
            self.right_choice_is_done = True
        self.output_success_info()

    def output_success_info(self):
        if not self.left_choice_is_done:
            self.set_info_text("red", ERROR_LEFT_INFO_TEXT)
        elif not self.right_choice_is_done:
            self.set_info_text("red", ERROR_RIGHT_INFO_TEXT)
        else:
            self.set_info_text("green", SUCCESS_INFO_TEXT)
