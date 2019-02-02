"""
Модуль предоставляет возможность для работы с диаграммой типа
"Кластеризованная столбчатая диаграмма".
"""

import random
import matplotlib.pyplot as plt
from Work.Scripts.view.reports.chart_interfaces import IChart


class ClusteredChart(IChart):
    """Предоставляет удобный интерфейс для создания окна и диаграммы
    типа "Кластеризованная столбчатая диаграмма" внутри него.

    Для создания качественного отчёта рекомендуется передать список
    групп продуктов (кластеров),
    список подгрупп качества продуктов (Например, ГОСТ, СТО, ТУ),
    передать список цветов для подгрупп качества продуктов,
    дать название оси Ox (рекомендуется "Группы продуктов"),
    дать название оси Oy (рекомендуется "Цены"),
    заголовок для диаграммы ("Группа продуктов - качество производства")
    и список цен для каждой подгруппы качества продуктов каждой группы.

    """

    _colors = None
    _qualities_by_group = []
    _quality_labels = []
    _groups = []
    _x_title = ""
    _y_title = ""
    _except_diff_group_and_vals = "Lengths of groups list and values list " \
                                  "are different "
    _except_diff_legend_and_colors = "Lengths of quality labels list and " \
                                     "colors list are different "
    _except_diff_legend_and_vals = "Amount of quality labels and " \
                                   "quality values is different"

    def __init__(self, title=""):
        super().__init__(title)

    @staticmethod
    def random_color():
        """
        Возвращает случайный цвет. Используется для
        генерирования цвета по умолчанию.
        """
        return random.random(), random.random(), random.random()

    def set_quality_labels(self, quality_labels):
        """Устанавливает названия подгрупп качества.

        :param quality_labels: название подгруппы качества
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._quality_labels = quality_labels
        return self

    def set_colors(self, colors: list):
        """Устанавливает цвета для каждой подгруппы качества.

        :param colors: список цветов для подгрупп качества (столбцов)
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._colors = colors
        return self

    def set_prices(self, qualities_by_group: list):
        """Устанвливает список цен для кадой подгруппы качества каждой
        группы продуктов.

        :param qualities_by_group: список цен для каждой подгруппы качества
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._qualities_by_group = qualities_by_group
        return self

    def set_groups(self, groups: list):
        """Устанвливает список групп продуктов(кластеров)

        :param groups: список групп продуктов
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._groups = groups
        return self

    def show(self):
        """Строит и показывает столбчатую диаграмму, исходя из переданных
        значений.

        При вызове этой функции открывается новое окно с отчётом
        на основе переданных значений. Если значение не передавалось,
        то используется значение по умолчанию.
        """
        if len(self._groups) != len(self._qualities_by_group):
            raise Exception(self._except_diff_group_and_vals)
        elif len(self._quality_labels) != len(self._colors):
            raise Exception(self._except_diff_legend_and_colors)

        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))

        if self._colors is None:
            self._colors = [self.random_color()
                            for _ in range(len(self._quality_labels))]
        self.set_title(self._title)
        ax = plt.gca()
        ax.yaxis.grid(True, zorder=1)

        plt.xticks(range(len(self._groups)), self._groups)
        fig.autofmt_xdate(rotation=-90)

        width = 1 / (len(self._quality_labels)) - 0.5 / (
            len(self._quality_labels))
        try:
            for j in range(len(self._groups)):
                for i in range(len(self._quality_labels)):
                    start_pos = i / len(self._quality_labels)
                    switch_pos = width / 2 * (i + len(self._quality_labels))
                    plt.bar(start_pos - switch_pos + j,
                            self._qualities_by_group[j][i],
                            width=width,
                            color=self._colors[i], alpha=0.8,
                            label=self._quality_labels[i] if j == 0 else None,
                            zorder=2)
        except IndexError:
            raise Exception(self._except_diff_legend_and_vals)

        plt.legend(loc='upper right')
        plt.ylabel(self._y_title)
        plt.xlabel(self._x_title)
        plt.show()


ClusteredChart()\
    .set_groups(["Groups 1", "Groups 2", "Groups 3", "Groups 4"]) \
    .set_quality_labels(["ГОСТ", "СТО", "ТУ"]) \
    .set_colors(["red", "blue", "green"]) \
    .set_prices([[12, 34, 45], [34, 12, 43], [34, 12, 43], [34, 12, 43]])\
    .set_x_title("Название оси X")\
    .set_y_title("Название оси Y")\
    .show()
