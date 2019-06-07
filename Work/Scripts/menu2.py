from abc import ABC, abstractmethod
from tkinter import Menu

from Work.Scripts.config import COLOR_FG_MENU, \
    COLOR_BG_MENU

LABEL_KEY = 'label'
COMMAND_KEY = 'command'


class MainMenuListener(ABC):

    @staticmethod
    @abstractmethod
    def close_app():
        pass

    @staticmethod
    @abstractmethod
    def create_simple_report():
        pass

    @staticmethod
    @abstractmethod
    def create_statistic_report():
        pass

    @staticmethod
    @abstractmethod
    def create_pivot_report():
        pass

    @staticmethod
    @abstractmethod
    def create_scatter_chart():
        pass

    @staticmethod
    @abstractmethod
    def create_bar_chart():
        pass

    @staticmethod
    @abstractmethod
    def create_box_and_whisker():
        pass

    @staticmethod
    @abstractmethod
    def create_histogram():
        pass

    @staticmethod
    @abstractmethod
    def open_db():
        pass

    @staticmethod
    @abstractmethod
    def save():
        pass

    @staticmethod
    @abstractmethod
    def save_as():
        pass

    @staticmethod
    def edit_db():
        pass

    @staticmethod
    @abstractmethod
    def about_app():
        pass


class MainMenuFactory(ABC):

    def __init__(self, listener: MainMenuListener):
        self.listener = listener

    def get_report_items(self):
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
