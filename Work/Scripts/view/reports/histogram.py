"""
Модуль предоставляет возможность для работы с диаграммой типа
"Категоризированная гистограмма".
"""
import random
import matplotlib.pyplot as plt

import chart_interfaces


class Histogram(chart_interfaces.IChart):
    """Предоставляет удобный интерфейс для создания окна и диаграммы
    типа "Категоризированная гистограмма" внутри него.

    Для создания качественного отчёта рекомендуется передать список
    продуктов, список цен для каждого продукта, цвет для столбцов,
    дать название оси Ox (рекомендуется "Продукты"),
    дать название оси Oy (рекомендуется "Цены"),
    и заголовок для диаграммы (рекомендуется название группы продуктов).

    """

    _products = []
    _prices = []
    _color = (random.random(), random.random(), random.random())
    _exception_text = "Lengths of price's list and label's list are different"

    def set_color(self, color):
        """ Устанавливает цвет столбцов. Цвет по умолчанию: случайный.

        :param color: цвет RGB (рекомендуется в формате HEX)
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._color = color
        return self

    def set_prices(self, prices: list):
        """ Устанавливвает список цен отдельных продуктов.

        :param prices: список цен для продуктов
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._prices = prices
        return self

    def set_products(self, products: list):
        """ Устанавливвает список продуктов. Используется для наименования
        столбцов по оси Ox.

        :param products: список продуктов
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._products = products
        return self

    def show(self):
        """Строит и показывает гистограмму, исходя из переданных значений.

        При вызове этой функции открывается новое окно с отчётом
        на основе переданных значений. Если значение не передавалось,
        то используется значение по умолчанию.
        """
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))

        plt.title(self._title)

        plt.gca().yaxis.grid(True, zorder=1)
        plt.xticks(range(len(self._products)), self._products)
        fig.autofmt_xdate(rotation=-90)

        if len(self._prices) != len(self._products):
            raise Exception(self._exception_text)

        width = 0.5
        for i in range(len(self._prices)):
            plt.bar(i,
                    self._prices[i],
                    width=width,
                    color=self._color, alpha=0.8,
                    label=self._products[i],
                    zorder=2)

        plt.ylabel(self._y_title)
        plt.xlabel(self._x_title)
        plt.show()


Histogram("Заголовок") \
    .set_prices([1, 2, 3]) \
    .set_products(["текст", "текст", "текст"]) \
    .set_color("#FF0000")\
    .set_x_title("Название оси X")\
    .set_y_title("Название оси Y")\
    .show()
