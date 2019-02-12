from Work.Scripts.res.values.colors import ERROR_INFO_COLOR, SUCCESS_INFO_COLOR
from Work.Scripts.src.view.reports.box_whiskers import Diagram
from Work.Scripts.src.view.ui.reports_settings.choice_frames import \
    MultiChoiceFrame, SingleChoiceFrame
from Work.Scripts.src.view.ui.reports_settings.report_settings_window import \
    SettingsWindow, SUCCESS_INFO_TEXT

ERROR_LEFT_INFO_TEXT = "Выберите группу продуктов"
ERROR_RIGHT_INFO_TEXT = "Выберите продукты"

PRICES_TEXT = "Цены"
QUALITY_TEXT = "Категории качества"
SUBTITLE_LEFT = "Группа продуктов"
SUBTITLE_RIGHT = "Продукты"

WINDOW_TITLE = "Категоризированная диаграмма Бокса-Вискера"


class SettingsBoxAndWhisker(SettingsWindow):

    def __init__(self, main):
        self.frame_1 = SingleChoiceFrame(main, self.reports_interactor
                                         .get_products_groups())
        self.left_choice_is_done = True

        self.frame_2 = MultiChoiceFrame(main, [self.reports_interactor
                                        .get_products_by_group(None)],
                                        True, listener=self)
        super().__init__(main, self.frame_1, self.frame_2)

        self.set_left_title(SUBTITLE_LEFT)
        self.set_right_title(SUBTITLE_RIGHT)

        # Запуск обработчика событий
        self.main.mainloop()

    def click_reports(self, event):
        qualities = self.reports_interactor.get_quality_categories()
        prices = list(self.reports_interactor
                      .get_box_and_whisker_prices(self.frame_1.get_data(),
                                                  qualities,
                                                  self.frame_2.get_data())
                      .values())

        self.main.destroy()
        Diagram(WINDOW_TITLE) \
            .set_prices(prices) \
            .set_box_labels(qualities) \
            .set_title(self.frame_1.get_data()) \
            .set_x_title(QUALITY_TEXT) \
            .set_y_title(PRICES_TEXT) \
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
            self.set_info_text(ERROR_INFO_COLOR, ERROR_LEFT_INFO_TEXT)
        elif not self.right_choice_is_done:
            self.set_info_text(ERROR_INFO_COLOR, ERROR_RIGHT_INFO_TEXT)
        else:
            self.set_info_text(SUCCESS_INFO_COLOR, SUCCESS_INFO_TEXT)

# SettingsBoxAndWhisker(Tk())
