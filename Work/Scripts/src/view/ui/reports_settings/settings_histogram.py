# pylint: disable=R0801
"""
Создаёт окно конфигурации для отображения графического отчёта
'Категоризированная гистограмма'
"""

from Work.Scripts.res.values.colors import ERROR_INFO_COLOR, SUCCESS_INFO_COLOR
from Work.Scripts.src.view.reports.histogram import Histogram
from Work.Scripts.src.view.ui.reports_settings.choice_frames import \
    MultiChoiceFrame, SingleChoiceFrame
from Work.Scripts.src.view.ui.reports_settings.report_settings_window import \
    SettingsWindow, SUCCESS_INFO_TEXT

WINDOW_TITLE_GRAPH = "Категоризированная гистограмма"
ERROR_LEFT_INFO_TEXT = "Выберите группу продуктов"
ERROR_RIGHT_INFO_TEXT = "Выберите продукты"
SUBTITLE_LEFT = "Группа продуктов"
SUBTITLE_RIGHT = "Продукты"
PRICES_TEXT = "Цены"
WINDOW_TITLE = "Категоризированная гистограмма"


class SettingsHistogram(SettingsWindow):
    """Класс для создания экрана конфигрции графика
        'Категоризированная гистограмма' """

    def __init__(self, main):
        """Создаёт окно конфигурации графика"""
        frame_1 = SingleChoiceFrame(main, self.controller
                                    .get_products_groups())

        frame_2 = MultiChoiceFrame(main, self.controller
                                   .get_products_by_group(None),
                                   True, listener=self)
        super().__init__(main, WINDOW_TITLE_GRAPH, frame_1, frame_2)
        self.left_choice_is_done = True
        self.set_left_title(SUBTITLE_LEFT)
        self.set_right_title(SUBTITLE_RIGHT)

        # Запуск обработчика событий
        self.main.mainloop()

    def click_reports(self, event):
        """Создаёт графический отчёт по выбранным данным"""
        if self.left_choice_is_done and self.right_choice_is_done:
            prices = list(self.controller
                          .get_prices_by_group(self.frame_1.get_data(),
                                               self.frame_2.get_data()))
            self.main.destroy()
            Histogram(WINDOW_TITLE) \
                .set_prices(prices) \
                .set_products(self.frame_2.get_data()) \
                .set_color("red") \
                .set_x_title(self.frame_1.get_data()) \
                .set_y_title(PRICES_TEXT) \
                .show()

    def error(self, frame):
        """
        Определяет в каком фрейме произошла ошибка и устанавливает
        в текстовом поле соответствующую надпись
        :param frame: фрейм, вызывающий событие ошибочного выбора
        """
        if frame == self.frame_2:
            self.right_choice_is_done = False
        self.output_success_info()

    def success(self, frame):
        """
        Определяет в каком фрейме данные выбраны успешно и устанавливает
        в текстовом поле соответствующую надпись
        :param frame: фрейм, вызывающий событие успешного выбора
        """
        if frame == self.frame_2:
            self.right_choice_is_done = True
        self.output_success_info()

    def output_success_info(self):
        """Выводит информацию в текстовое поле об успешности выбора"""
        if not self.left_choice_is_done:
            self.set_info_text(ERROR_INFO_COLOR, ERROR_LEFT_INFO_TEXT)
        elif not self.right_choice_is_done:
            self.set_info_text(ERROR_INFO_COLOR, ERROR_RIGHT_INFO_TEXT)
        else:
            self.set_info_text(SUCCESS_INFO_COLOR, SUCCESS_INFO_TEXT)

# SettingsBoxAndWhisker(Tk())
