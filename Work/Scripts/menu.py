"""
Содержит абстрактную реализацию мсобытий меню

Автор: Перятин Виталий
"""

from abc import ABC, abstractmethod
from tkinter import Menu

from Work.Scripts.config import COLOR_FG_MENU, \
    COLOR_BG_MENU

LABEL_KEY = 'label'
COMMAND_KEY = 'command'


class MainMenuListener(ABC):
    """
    Слушатель событий меню

    Автор: Перятин Виталий
    """

    @staticmethod
    @abstractmethod
    def close_app():
        """
        Закрывает приложение

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def create_simple_report():
        """
        Создаёт простой текстовый отчёт

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def create_statistic_report():
        """
        Создаёт текстовый статистический  отчёт

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def create_pivot_report():
        """
        Создаёт сводную таблицу

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def create_scatter_chart():
        """
        Создаёт диаграмму рассеивания

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def create_bar_chart():
        """
        Создаёт столбчатую диаграмму

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def create_box_and_whisker():
        """
        Создаёт диаграмму "Ящик с усами"

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def create_histogram():
        """
        Создаёт гистограмму

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def open_db():
        """
        Открывает Бд

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def save():
        """
        Сохраняет БД

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def save_as():
        """
        Сохраняет БД в выбранную дирекотрию

        Автор: Перятин Виталий
        """

    @staticmethod
    def edit_db():
        """
        Редактирует БД

        Автор: Перятин Виталий
        """

    @staticmethod
    @abstractmethod
    def about_app():
        """
        Открывет информацию "О приложении"

        Автор: Перятин Виталий
        """


class MainMenuFactory(ABC):
    """
    Фабрика для создания элементов меню

    Автор: Перятин Виталий
    """

    def __init__(self, listener: MainMenuListener):
        self.listener = listener

    def get_report_items(self):
        """
        Возвращает список элементов словаря со слушателями для отчётов
        :return: список элементов словаря со слушателями

        Автор: Перятин Виталий
        """
        return [
            {
                LABEL_KEY: "Простой отчёт",
                COMMAND_KEY: self.listener.create_simple_report
            },
            {
                LABEL_KEY: "Статистика",
                COMMAND_KEY: self.listener.create_statistic_report
            },
            {
                LABEL_KEY: "Сводная таблица",
                COMMAND_KEY: self.listener.create_pivot_report
            },
            None,
            {
                LABEL_KEY: "Столбчатая диаграмма",
                COMMAND_KEY: self.listener.create_bar_chart
            },
            {
                LABEL_KEY: "Гистограмма",
                COMMAND_KEY: self.listener.create_histogram
            },
            {
                LABEL_KEY: "Диаграмма 'Ящика с усами'",
                COMMAND_KEY: self.listener.create_box_and_whisker
            },
            {
                LABEL_KEY: "Диаграмма рассеивания",
                COMMAND_KEY: self.listener.create_scatter_chart
            }
        ]

    def get_file_items(self):
        """
        Возвращает список элементов словаря со слушателями пункта "Файл"
        :return: список элементов словаря со слушателями

        Автор: Перятин Виталий
        """
        return [
            {
                LABEL_KEY: "Открыть",
                COMMAND_KEY: self.listener.open_db
            },
            {
                LABEL_KEY: "Сохранить",
                COMMAND_KEY: self.listener.save
            },
            {
                LABEL_KEY: "Сохранить как...",
                COMMAND_KEY: self.listener.save_as
            },
            {
                LABEL_KEY: "Редактировать БД",
                COMMAND_KEY: self.listener.edit_db
            },
            {
                LABEL_KEY: "О программе",
                COMMAND_KEY: self.listener.about_app
            },
            None,
            {
                LABEL_KEY: "Выйти",
                COMMAND_KEY: self.listener.close_app
            },
        ]

    @staticmethod
    def get_menu(name: str, items: list):
        """
        Создаёт и возвращает список основных элементов меню

        :param name: заголовок меню
        :param items: список элементов меню
        :return: Основной пункт меню

        Автор: Перятин Виталий
        """
        menu = Menu(tearoff=0, bg=COLOR_BG_MENU, fg=COLOR_FG_MENU)
        for item in items:
            if item is None:
                menu.add_separator()
            else:
                menu.add_command(item)
        return {
            'label': name,
            'menu': menu
        }
