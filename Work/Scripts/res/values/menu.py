from abc import ABC, abstractmethod
from tkinter import Menu

from Work.Scripts.src.view.ui.main_window.config import COLOR_FG_MENU, \
    COLOR_BG_MENU

LABEL_KEY = 'label'
COMMAND_KEY = 'command'


class MainMenuListener(ABC):
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

    def get_change_items(self):
        return [
            {
                LABEL_KEY: "Назад",
                COMMAND_KEY: None
            },
            {
                LABEL_KEY: "Вперёд",
                COMMAND_KEY: None
            },
            {
                LABEL_KEY: "Вырезать",
                COMMAND_KEY: None
            },
            {
                LABEL_KEY: "Копировать",
                COMMAND_KEY: None
            },
            {
                LABEL_KEY: "Вставить",
                COMMAND_KEY: None
            },
            {
                LABEL_KEY: "Найти и заменить",
                COMMAND_KEY: None
            },
        ]

    def get_file_items(self):
        return [
            {
                LABEL_KEY: "Открыть",
                COMMAND_KEY: None
            },
            {
                LABEL_KEY: "Создать копию",
                COMMAND_KEY: None
            },
            {
                LABEL_KEY: "Переименовать",
                COMMAND_KEY: None
            },
            {
                LABEL_KEY: "Сохранить",
                COMMAND_KEY: None
            },
            {
                LABEL_KEY: "Сохранить как...",
                COMMAND_KEY: None
            },
            None,
            {
                LABEL_KEY: "Выйти",
                COMMAND_KEY: None
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
