from Work.Scripts.view.reports.box_whiskers import Diagram
from Work.Scripts.view.ui.reports_settings.choice_frames import \
    MultiChoiceFrame, SingleChoiceFrame
from Work.Scripts.view.ui.reports_settings.report_settings_window import \
    SettingsWindow, SUCCESS_INFO_TEXT

ERROR_LEFT_INFO_TEXT = "Выберите группу продуктов"
ERROR_RIGHT_INFO_TEXT = "Выберите продукты"


class SettingsBoxAndWhisker(SettingsWindow):

    def __init__(self, main):
        self.frame_1 = SingleChoiceFrame(main, ["Ягоды", "Картошка", "Зёрна",
                                                "Мясо", "Для беременных",
                                                "Деликатесы",
                                                "Птица", "Рыба", "Хлеб",
                                                "Молочное", "Овощи",
                                                "Фрукты и ягоды"])
        self.left_choice_is_done = True

        self.frame_2 = MultiChoiceFrame(main, ["Молоко", "Курица", "Индейка",
                                               "Сосиски",
                                               "Петрушка",
                                               "Мука", "Макороны", "Хлеб"],
                                        True, listener=self)
        super().__init__(main, self.frame_1, self.frame_2)

        self.set_left_title("Группа продуктов")
        self.set_right_title("Продукты")

        # Запуск обработчика событий
        self.main.mainloop()

    def click_reports(self, event):
        qualities = ['ГОСТ', 'СТО', 'ТУ']
        prices = list(SettingsWindow.reports_interactor
                      .get_box_and_whisker_prices(self.frame_1.get_data(),
                                                  qualities,
                                                  self.frame_2.get_data())
                      .values())

        print(prices)
        Diagram().set_prices(prices) \
            .set_box_labels(qualities) \
            .set_title(self.frame_1.get_data()) \
            .set_x_title("Категории качества") \
            .set_y_title("Цены") \
            .show()

    def click_clear(self, event):
        self.frame_1.clear()
        self.frame_2.clear()

    def click_default(self, event):
        self.frame_1.default_choice()
        self.frame_2.default_choice()

    def error(self, frame):
        if frame == self.frame_2:
            self.right_choice_is_done = False
        self.output_success_info()

    def success(self, frame):
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


# SettingsBoxAndWhisker(Tk())
