"""
Модуль предоставляет возможность для работы с диаграммой типа
"Диаграмма Бокса-Векселя".
"""
import matplotlib.pyplot as plt

from Work.Scripts.res.values.colors import DEFAULT_WHISKER_COLOR, \
    DEFAULT_BOX_COLOR, DEFAULT_MEDIAN_COLOR
from Work.Scripts.src.presentation.reports import chart_interfaces

GRAPH_TITLE_BOX_AND_WHISKER = "Категоризированная диаграмма Бокса-Вискера"


class Diagram(chart_interfaces.IChart):
    """Предоставляет удобный интерфейс для создания окна и диаграммы
    типа "Box and Whiskers" внутри него.

    Для создания качественного отчёта рекомендуется передать список
    меток для оси Ox (заисит от выбранной категории),
    заголовок для диаграммы (рекомендуется название выбранной категории),
    установить выбранную категорию в названии оси Ox,
    установить название оси Oy (рекомендуется название "Цена") и
    передать список цен для кадого "ящика".

    """

    _prices = []
    _whisker_color = None
    _box_color = None
    _median_color = None
    _box_labels = []
    _except_x_axis_and_vals = "Lengths of X-axis labels and " \
                              "values list are different"

    def set_prices(self, prices: list):
        """Устанавливает список цен для диаграммы.

        Длина списка из списков цен должна соответствовать длине списка
        названий для "ящиков".
        :param prices: список из списка цен для каждого "ящика"
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._prices = prices
        return self

    def set_box_labels(self, box_labels: list):
        """Устанавливает названия для "ящиков" на оси Ox.

        :param box_labels: список названий для "ящиков" на оси Ox
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._box_labels = box_labels
        return self

    def set_colors(self,
                   whisker_color=DEFAULT_WHISKER_COLOR,
                   box_color=DEFAULT_BOX_COLOR,
                   median_color=DEFAULT_MEDIAN_COLOR):
        """Устанавливает цвета для "ящика" и "усов" в формате HEX.

        :param whisker_color: цвет "усов" в формате HEX
        :param box_color: цвет "ящика" в формате HEX
        :param median_color: цвет линии усредненного значения в формате HEX
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._whisker_color = whisker_color
        self._box_color = box_color
        self._median_color = median_color
        return self

    def show(self):
        """Строит и показывает диаграмму Бокса-Вескеля, исходя из переданных
        значений.

        При вызове этой функции открывается новое окно с отчётом
        на основе переданных значений. Если значение не передавалось,
        то используется значение по умолчанию.
        """

        if len(self._box_labels) != len(self._prices):
            raise Exception(self._except_x_axis_and_vals)

        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
        fig.canvas.set_window_title(GRAPH_TITLE_BOX_AND_WHISKER)
        plt.boxplot(self._prices,
                    patch_artist=True,
                    medianprops={'color': self._median_color},
                    boxprops={'color': self._box_color,
                              'facecolor': self._box_color},
                    whiskerprops={'color': self._whisker_color},
                    capprops={'color': self._whisker_color})

        fig.autofmt_xdate(rotation=-90)
        axis_nums = [x + 1 for x in range(len(self._box_labels))]

        plt.xticks(axis_nums, self._box_labels)
        plt.ylabel(self._y_title)
        plt.xlabel(self._x_title)
        plt.show()

#
# Diagram().set_prices([[10, 20, 30, 40, 50], [1, 45, 23, 12, 34]]) \
#     .set_box_labels(["Ящик 1", "Ящик 2"]) \
#     .set_title("Заголовок") \
#     .set_x_title("Название оси X") \
#     .set_y_title("Название оси Y") \
#     .show()
