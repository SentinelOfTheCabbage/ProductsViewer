# pylint: disable=R0801
"""
Создаёт окно конфигурации для отображения графического отчёта
'Категоризированная диаграмма рассеивания'
"""

from Work.Scripts.src.presentation.reports.scatter_chart import ScatterChart
from Work.Scripts.src.presentation.reports_settings.choice_frames import \
    SingleChoiceFrame, CalendarFrame
from Work.Scripts.src.presentation.reports_settings.report_settings_window import \
    SettingsWindow, SUCCESS_INFO_TEXT

WINDOW_TITLE_GRAPH = "Диаграмма рассеивания"
ERROR_LEFT_INFO_TEXT = "Выберите группу продуктов"
ERROR_RIGHT_INFO_TEXT = "Выберите дату"
SUBTITLE_LEFT = "Группа продуктов"
SUBTITLE_RIGHT = "День отчёта"
PRICES_TEXT = "Цены"
AMOUNT_TEXT = "Количество"

GRAPH_TITLE = "Категоризированная диаграмма рассеивания"


class SettingsScatterChart(SettingsWindow):
    """Класс для создания экрана конфигрции графика
            'Диаграмма рассеивания' """
    def __init__(self, main):
        """Создаёт окно конфигурации графика"""
        self.frame_1: SingleChoiceFrame = SingleChoiceFrame(main, self.controller
                                         .get_products_groups())

        self.frame_2: CalendarFrame = CalendarFrame(main)
        super().__init__(main, WINDOW_TITLE_GRAPH, self.frame_1, self.frame_2)
        self.left_choice_is_done = True

        self.set_left_title(SUBTITLE_LEFT)
        self.set_right_title(SUBTITLE_RIGHT)

        # Запуск обработчика событий
        self.main.mainloop()

    def click_reports(self, event):
        """Создаёт графический отчёт по выбранным данным"""
        if self.left_choice_is_done and self.right_choice_is_done:
            points = list(self.controller
                          .get_spreading(self.frame_1.get_data(),
                                         self.frame_2.get_data()))
            self.main.destroy()
            ScatterChart(GRAPH_TITLE) \
                .set_points(points) \
                .set_color("red") \
                .set_x_title(AMOUNT_TEXT) \
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
