"""
Создаёт окно конфигурации для отображения графического отчёта
'Категоризированная гистограмма'
"""
# pylint: disable=R0801
# pylint: disable=E0401

from Work.Scripts.colors import ERROR_INFO_COLOR, SUCCESS_INFO_COLOR
from Work.Library.histogram import Histogram
from Work.Library.choice_frames import \
    MultiChoiceFrame, SingleChoiceFrame
from Work.Library.report_settings_window import \
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
        groups = self.controller.get_products_groups()
        self.main = main
        self.frame_1: SingleChoiceFrame = SingleChoiceFrame(main, groups, self.rb_listener)

        self.frame_2: MultiChoiceFrame = MultiChoiceFrame(main, self.controller
                                                          .get_products_by_group(groups[0]),
                                                          True, listener=self)
        super().__init__(main, WINDOW_TITLE_GRAPH, self.frame_1, self.frame_2)
        self.left_choice_is_done = True
        self.set_left_title(SUBTITLE_LEFT)
        self.set_right_title(SUBTITLE_RIGHT)

        # Запуск обработчика событий
        self.main.mainloop()

    def rb_listener(self):
        """docstring_peryatin
        """
        self.update_products()

    def update_products(self):
        """docstring_peryatin
        """
        self.frame_2: MultiChoiceFrame = MultiChoiceFrame(self.main, self.controller
                                                          .get_products_by_group(
                                                              self.frame_1.get_data()),
                                                          True, listener=self)
        super().__init__(self.main, WINDOW_TITLE_GRAPH, self.frame_1, self.frame_2)

    def click_default(self, event):

        super().click_default(event)
        self.update_products()

    def click_reports(self, event):
        """Создаёт графический отчёт по выбранным данным"""
        if self.left_choice_is_done and self.right_choice_is_done:
            product_prices = self.controller.get_prices_by_group(
                self.frame_1.get_data(), self.frame_2.get_data())
            self.main.destroy()
            Histogram(WINDOW_TITLE) \
                .set_prices(list(product_prices['price'])) \
                .set_products(list(product_prices['name'])) \
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
