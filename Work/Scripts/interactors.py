"""
Модуль дял трансформирования типов на стороне базы данных к типу,
    который испоьзуется на стороне визуального интерфейса

Отключены следующие ошибки pylint:
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)
    R0201 - Ошибка использования self в некоторых методах класса

Автор: Перятин Виталий
"""
# pylint: disable=E0401
# pylint: disable=R0201
from pandas import DataFrame, Series

from Work.Scripts.db_controller import MainTableController, \
    ReportsController


class ListMainTableInteractor(MainTableController):
    """
    Класс для трансформирования типов на стороне базы данных к типу,
    который испоьзуется на стороне визуального интерфейса

    Автор: Перятин Виталий
    """
    def __init__(self, save_curr_state=False):
        super().__init__(save_curr_state)

    def tolist(self, d_f: DataFrame):
        """
        Преобразует DataFrame в список списков
        :return: список списков для отображения таблицы пользователю

        Автор: Перятин Виталий
        """
        if (d_f is not None) and (isinstance(d_f, DataFrame)):
            full_list = d_f.values.tolist()
            full_list.insert(0, d_f.columns.tolist())
            return full_list
        return None

    def select(self, column_choices: dict, expressions):
        """
        Фильтрует таблицу по переданным выражениям и
        возвращает результат при фильтрации таблицы
        :param column_choices: список столбцов
        :param expressions: список выражений для фильтрации

        Автор: Перятин Виталий
        """
        event = super().select(column_choices, expressions)
        event.data = self.tolist(event.data)
        return event

    def get_products_groups(self):
        """
        Получает список групп

        Автор: Перятин Виталий
        """
        return list(super().get_products_groups())

    def get_qualities(self):
        """
        Получает список категорий качества

        Автор: Перятин Виталий
        """
        return list(super().get_qualities())

    def get_producers(self):
        """
        Получает список производителей

        Автор: Перятин Виталий
        """
        return list(super().get_producers())

    def get_products_names(self):
        """
        Получает сипсок названий продуктов

        Автор: Перятин Виталий
        """
        return list(super().get_products_names())

    def get_max_price(self):
        """
        Получает максимальную цену продуктов

        Автор: Перятин Виталий
        """
        return super().get_max_price()

    def get_max_discount(self):
        """
        Получает максимальную скидку

        Автор: Перятин Виталий
        """
        return super().get_max_discount()

    def update(self, set_frames: list, expressions: list):
        """
        Обновляет таблицу и получает результат операции

        Автор: Перятин Виталий
        """
        event = super().update(set_frames, expressions)
        event.data = self.tolist(event.data)
        return event

    def delete(self, expressions):
        """
        Удаляет записи в таблице и возвращает результат удаления

        Автор: Перятин Виталий
        """
        event = super().delete(expressions)
        event.data = self.tolist(event.data)
        return event

    def get_data(self):
        """
        Получает итоговую таблицу для отображени пользователю

        Автор: Перятин Виталий
        """
        return self.tolist(super().get_data_frame())[:100]


class ListReportsAdapter(ReportsController):
    """
    Адапер для преобразования данных из DataFrame в
    инртерфейсы удобные для работы на стороне интерфейса

    Автор: Перятни Виталий
    """
    def __init__(self):
        super().__init__()

    def tolist(self, series: Series):
        """
        Преобразует тип Series к списку

        Автор: Перятин Виталий
        """
        if (series is not None) and (isinstance(series, Series)):
            return series.tolist()
        return None

    def get_products_groups(self):
        """
        Получает сипсок групп продуктов

        Автор: Перятин Виталий
        """
        return self.tolist(super().get_products_groups())
