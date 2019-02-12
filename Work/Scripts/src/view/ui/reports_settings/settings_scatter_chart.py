from Work.Scripts.src.view.reports.scatter_chart import ScatterChart
from Work.Scripts.src.view.ui.reports_settings.choice_frames import \
    SingleChoiceFrame, CalendarFrame
from Work.Scripts.src.view.ui.reports_settings.report_settings_window import \
    SettingsWindow, SUCCESS_INFO_TEXT

ERROR_LEFT_INFO_TEXT = "Выберите группу продуктов"
ERROR_RIGHT_INFO_TEXT = "Выберите дату"
SUBTITLE_LEFT = "Группа продуктов"
SUBTITLE_RIGHT = "День отчёта"
PRICES_TEXT = "Цены"
AMOUNT_TEXT = "Количество"

WINDOW_TITLE = "Категоризированная диаграмма рассеивания"


class SettingsScatterChart(SettingsWindow):
    def __init__(self, main):
        self.frame_1 = SingleChoiceFrame(main, self.reports_interactor
                                         .get_products_groups())
        self.left_choice_is_done = True

        self.frame_2 = CalendarFrame(main)
        super().__init__(main, self.frame_1, self.frame_2)

        self.set_left_title(SUBTITLE_LEFT)
        self.set_right_title(SUBTITLE_RIGHT)

        # Запуск обработчика событий
        self.main.mainloop()

    def click_reports(self, event):
        points = list(SettingsWindow.reports_interactor
                      .get_spreading(self.frame_1.get_data(),
                                     self.frame_2.get_data()))
        self.main.destroy()
        ScatterChart(WINDOW_TITLE) \
            .set_points(points) \
            .set_color("red") \
            .set_x_title(AMOUNT_TEXT) \
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
            self.set_info_text("red", ERROR_LEFT_INFO_TEXT)
        elif not self.right_choice_is_done:
            self.set_info_text("red", ERROR_RIGHT_INFO_TEXT)
        else:
            self.set_info_text("green", SUCCESS_INFO_TEXT)

# ScatterChart()\
#     .set_points([[1, 2], [2, 3]])\
#     .set_color("#FF0000")\
#     .set_x_title("Название оси X")\
#     .set_y_title("Название оси Y")\
#     .show()
