"""
Модуль предоставляет возможность для работы с диаграммой типа
"Категоризированная диаграмма рассеивания".
"""

import matplotlib.pyplot as plt

from Work.Scripts.src.presentation.reports import chart_interfaces


class ScatterChart(chart_interfaces.IChart):
    """Предоставляет удобный интерфейс для создания окна и диаграммы
        типа "Категоризированная диаграмма рассеивания" внутри него.

        Для создания качественного отчёта рекомендуется передать список
        групп продуктов, список цен, список количества проданных продуктов,
        заголовок диаграммы (рекомендуется дата отсчёта),
        установить название оси Ox (рекомендуется "Количество") и
        установить название оси Oy (рекомендуется название "Цена")

        """
    _x_coord = []
    _y_coord = []
    _color = "blue"
    _marker = "o"
    _exception_text = "Amount of x-coordinates and " \
                      "y-coordinates should be equals"

    def set_coord(self, x_coord: list, y_coord: list):
        """ Устанавливает координаты точек. Сначала задаётся
        список координат X, после список координат по оси Y.

        :param x_coord: список координат по оси X
        :param y_coord: список координат по оси Y
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        if len(x_coord) != len(y_coord):
            raise Exception(self._exception_text)
        self._x_coord = x_coord
        self._y_coord = y_coord
        return self

    def set_points(self, points: list):
        """ Устанавливает список точек. Передаётся список, состоящий из
        списков двух значений: координата по X и координата по Y.

        :param points: список точек
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._x_coord.clear()
        self._y_coord.clear()
        tuple_points = [(point['price'], point['amount']) for point in points]
        try:
            for (x_coord, y_coord) in tuple_points:
                self._x_coord.append(x_coord)
                self._y_coord.append(y_coord)
        except ValueError:
            raise Exception(self._exception_text)
        return self

    def set_color(self, color):
        """ Устанавливает цвет точек. Цвет по умолчанию: синий.

        :param color: цвет RGB (рекомендуется в формате HEX)
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._color = color
        return self

    def show(self):
        """Строит и показывает диаграмму рассеивания,
        исходя из переданных значений.

        При вызове этой функции открывается новое окно с отчётом
        на основе переданных значений. Если значение не передавалось,
        то используется значение по умолчанию.
        """
        plt.gcf().canvas.set_window_title(self._title)
        plt.scatter(self._x_coord, self._y_coord, marker=self._marker,
                    edgecolors=self._color, c=self._color)
        plt.ylabel(self._y_title)
        plt.xlabel(self._x_title)
        plt.show()


# ScatterChart()\
#     .set_points([[1, 2], [2, 3]])\
#     .set_color("#FF0000")\
#     .set_x_title("Название оси X")\
#     .set_y_title("Название оси Y")\
#     .show()
