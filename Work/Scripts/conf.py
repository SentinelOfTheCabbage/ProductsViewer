"""
Модуль для дополнительный надстроек проекта

Автор: Перятин Виталий
"""

import os


def parent_dir(path):
    """
    Возвращает путь к родителю текущей директории

    :param path: текущая директория
    :return: путь к родителю текущей директории

    Автор: Перятин Виталий
    """
    return os.path.dirname(path)


ROOT_DIR = parent_dir(parent_dir(__file__))
