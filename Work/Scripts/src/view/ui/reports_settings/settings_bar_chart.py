"""
Создаёт окно конфигурации для отображения графического отчёта
'Кластеризованная столбчатая диаграмма'
"""

# pylint: disable=R0801
from Work.Scripts.res.values.colors import ERROR_INFO_COLOR, SUCCESS_INFO_COLOR
from Work.Scripts.src.view.reports.clustered_chart import ClusteredChart
from Work.Scripts.src.view.ui.reports_settings.choice_frames import \
    MultiChoiceFrame
from Work.Scripts.src.view.ui.reports_settings.report_settings_window import \
    SettingsWindow, SUCCESS_INFO_TEXT

WINDOW_TITLE_GRAPH = "Гистограмма"
SUBTITLE_LEFT = "Група продуктов"
SUBTITLE_RIGHT = "Категория качества"
ERROR_LEFT_INFO_TEXT = "Выберите продукты"
ERROR_RIGHT_INFO_TEXT = "Выберите категорию"
PRICES_TEXT = "Цены"

BAR_CHART_WINDOW_TITLE = "Кластеризованная столбчатая диаграмма"


class SettingsBarChart(SettingsWindow):
    """Класс для создания экрана конфигрции графика
    'Кластеризованная столбчатая диаграмма' """

    def __init__(self, main):
        """Создаёт окно конфигурации графика"""
        self.frame_1 = MultiChoiceFrame(main, self.reports_interactor
                                        .get_products_groups(),
                                        listener=self)
        self.frame_2 = MultiChoiceFrame(main, self.reports_interactor
                                        .get_quality_categories(),
                                        True, listener=self)
        super().__init__(main, WINDOW_TITLE_GRAPH, self.frame_1, self.frame_2)

        self.set_left_title(SUBTITLE_LEFT)
        self.set_right_title(SUBTITLE_RIGHT)

        # Запуск обработчика событий
        self.main.mainloop()

    def click_reports(self, event):
        """Создаёт графический отчёт по выбранным данным"""
        if self.left_choice_is_done and self.right_choice_is_done:
            prices = list(self.reports_interactor
                          .get_prices_by_group_and_quality(self.frame_1
                                                           .get_data(),
                                                           self.frame_2
                                                           .get_data())
                          .values())
            self.main.destroy()
            ClusteredChart(BAR_CHART_WINDOW_TITLE) \
                .set_groups(self.frame_1.get_data()) \
                .set_quality_labels(self.frame_2.get_data()) \
                .set_prices(prices) \
                .set_y_title(PRICES_TEXT) \
                .show()

    def error(self, frame):
        """
        Определяет в каком фрейме произошла ошибка и устанавливает
        в текстовом поле соответствующую надпись
        :param frame: фрейм, вызывающий событие ошибочного выбора
        """
        if frame == self.frame_1:
            self.left_choice_is_done = False
        if frame == self.frame_2:
            self.right_choice_is_done = False
        self.output_success_info()

    def success(self, frame):
        """
        Определяет в каком фрейме данные выбраны успешно и устанавливает
        в текстовом поле соответствующую надпись
        :param frame: фрейм, вызывающий событие успешного выбора
        """
        if frame == self.frame_1:
            self.left_choice_is_done = True
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
