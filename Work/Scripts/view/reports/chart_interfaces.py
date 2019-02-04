"""
В модуле находятся все классы и интерфейсы для создания диаграмм
"""
from abc import ABC, abstractmethod


class IChart(ABC):
    """Интерфейс для созданияя диаграмм. Содержит в себе заголовок
    и метод для открытия окна с отчётом. """

    _title = ""
    _x_title = ""
    _y_title = ""

    def __init__(self, title=""):
        self._title = title

    def set_title(self, title):
        """Устанавливает заголовок отчёта.

        :param title: заголовок отчёта
        :return: возвращает себя для реализации паттерна "Builder"
        """
        self._title = title
        return self

    @abstractmethod
    def show(self):
        """Создаёт график на основе переданных данных и
        открывает окно отчёта"""

    def set_x_title(self, x_title: str):
        """Устанавливает заголовок для оси Ox.

        :param x_title: заголовок для оси Ox
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._x_title = x_title
        return self

    def set_y_title(self, y_title: str):
        """Устанавливает заголовок для оси Oy.

        :param y_title: заголовок для оси Oy
        :return: возвращает себя же для реализации паттерна "Builder"
        """
        self._y_title = y_title
        return self
