"""
Модуль для управления базой даных

Отключены следующие ошибки pylint:
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)
    R1705 - Нет необходимости в elif/else после return

Автор: Перятин Виталий
"""
# pylint: disable=E0401
# pylint: disable=R1705
from enum import Enum

from Work.Scripts.ui_table_constants import \
    ProductColumns, TableNameUI
from Work.Scripts.extractor import DataExtractor
from Work.Scripts.repositories import ReportsInteractor, \
    MainTableRepository
from Work.Scripts.commands import CommandSelect, CommandInsert, \
    CommandUpdate, CommandDelete
from Work.Scripts.db_event import Event

EMPTY_EXPRS = "Не заполнены условия"
EMPTY_COLS = "Не выбраны колонки"
EMPTY_VALS = "Не заполнены значения"


class EditDbError(Enum):
    """
    Перечисления ошибок при изменении БД

    Автор: Перятин Виталий
    """
    EMPTY_FIELDS = 1
    INCORRECT_DATA = 2
    NO_SELECTOR = 3


class MainTableController:
    """
    Класс для управления основной таблицей,
    лежащей в базе данных

    Автор: Перятин Виталий
    """

    def __init__(self, save_curr_state=False):
        self.repository = MainTableRepository(DataExtractor())
        self.selector = CommandSelect(TableNameUI.PRODUCTS)
        if save_curr_state:
            self._save_state()

    def get_data_frame(self):
        """
        Получает основную таблицу из базы данных
        для отображения пользователю
        :return: основная таблица из базы данных

        Автор: Перятин Виталий
        """
        return self.repository.get_main_table()

    def get_products_groups(self):
        """
        Поллучает список групп продуктов

        Автор: Перятин Виталий
        """
        return self.repository.get_products_groups()

    def get_qualities(self):
        """
        Получает список категорий качества

        Автор: Перятин Виталий
        """
        return self.repository.get_qualities()

    def get_producers(self):
        """
        Получает список производителей

        Автор: Перятин Виталий
        """
        return self.repository.get_producers()

    def get_products_names(self):
        """
        Получает список имён продуктов

        Автор: Перятин Виталий
        """
        return self.repository.get_products_names()

    def get_max_price(self):
        """
        Получает максимальную цену продукта

        Автор: Перятин Виталий
        """
        return self.repository.get_max_price()

    def get_max_discouжnt(self):
        """
        Получает максимальную скидку

        Автор: Перятин Виталий
        """
        return self.repository.get_max_discount()

    def select(self, column_choices: dict, expressions):
        """
        Фильтрует таблицу и возвращает результат фильтрации

        Автор: Перятин Виталий
        """
        columns = []

        def get_text():
            """
            Получает текст для результата выборки данных

            Автор: Перятин Виталий
            """
            col_text = 'По столбцам: ' + ', '.join(columns)
            exprs = []
            for expr in expressions:
                field, o_p, val = expr.get_expression()
                exprs.append(str(field) + str(o_p) + str(val))
            if exprs:
                expr_text = '\nПо условиям: ' + '; '.join(exprs)
            else:
                expr_text = ''
            return 'Таблица отфильтрована\n' + col_text + expr_text

        for col, var in column_choices.items():
            if var.get():
                columns.append(col)

        is_full_exprs = True
        for expr in expressions:
            if expr.get_expression()[2] == '':
                is_full_exprs = False
                break

        if not columns:
            err = EditDbError.EMPTY_FIELDS
            return Event(err, EMPTY_COLS)
        elif not is_full_exprs:
            err = EditDbError.EMPTY_FIELDS
            return Event(err, EMPTY_EXPRS)
        else:
            self.selector = CommandSelect(TableNameUI.PRODUCTS)
            self.selector.set_columns(columns)
            self.selector.set_conditions(expressions)
            data = self.repository.select(self.selector)
            self._save_state()
            return Event(0, get_text(), data)

    def insert(self, col_to_values: dict):
        """
        Вставляет новые строки в базу данных и
        врзвращает рузультат вставки

        Автор: Перятин Виталий
        """

        def get_text(cut_row: list):
            """
            Получает текст для результата вставки

            Автор: Перятин Виталий
            """
            return "В БД добавлена следующая строка... \n" + ", ".join(cut_row)

        is_full_row = True
        row = {}
        for col, val in col_to_values.items():
            if not val.get():
                is_full_row = False
            else:
                row[col] = val.get()

        if is_full_row:
            inserter = CommandInsert()
            inserter.add_row(row)
            row_list = self.repository.insert(inserter)
            titled_row = dict(zip(ProductColumns.get_empty_row().keys(),
                                  row_list))
            cutted_row = [val for col, val in titled_row.items()
                          if col in list(self.selector.get_columns())]
            self._save_state()
            return Event(0, get_text(cutted_row), cutted_row)
        else:
            return Event(EditDbError.EMPTY_FIELDS.value, EMPTY_VALS)

    def update(self, set_frames: list, expressions: list):
        """
        Обновялет строки и возвращает результат обновления

        Автор: Перятин Виталий
        """
        def get_text():
            """
            Получает текст для результата обновления

            Автор: Перятин Виталий
            """
            return "Обновлены строки"

        values = {}
        updater = CommandUpdate()
        is_full_vals = True
        for set_frame in set_frames:
            col_to_val = set_frame.get_col_to_value()
            if list(col_to_val.values())[0] != '':
                values.update(set_frame.get_col_to_value())
            else:
                is_full_vals = False
                break

        if (not is_full_vals) or (not values):
            return Event(EditDbError.EMPTY_FIELDS, EMPTY_VALS)
        elif not expressions:
            return Event(EditDbError.EMPTY_FIELDS, EMPTY_EXPRS)
        else:
            updater.update_values(values)
            updater.set_conditions(expressions)
            data = self.repository.update(updater)
            self._save_state()
            return Event(0, get_text(), data)

    def delete(self, expressions):
        """
        Удаляет строки и возвращает результат удаления

        Автор: Перятин Виталий
        """
        def get_text():
            """
            Получает текст для результата обновления

            Автор: Перятин Виталий
            """
            return "Удалены записи"

        is_full_exprs = True
        for expr in expressions:
            if expr.get_expression()[2] == '':
                is_full_exprs = False
                break

        if (expressions is None) or (not is_full_exprs) or (not expressions):
            return Event(EditDbError.EMPTY_FIELDS, EMPTY_EXPRS)
        else:
            deleter = CommandDelete()
            deleter.set_conditions(expressions)
            data = self.repository.delete(deleter)
            self._save_state()
            return Event(0, get_text(), data)

    def get_vals_by_col(self, column):
        """
        Получает значения по названию столбцу
        :param column: название столбца

        Автор: Перятин Виталий
        """
        return self.repository.get_vals_by_col(column)


class ReportsController:
    """
    Класс для управления данными,
    которые необходимы для отчётов
    """

    def __init__(self):
        self.reports_interactor = ReportsInteractor(DataExtractor())

    def get_products_groups(self):
        """
        Получает список групп

        Автор: Перятин Виталий
        """
        return self.reports_interactor.get_products_groups()

    def get_quality_categories(self):
        """
        Получает список категорий качества

        Автор: Перятин Виталий
        """
        return self.reports_interactor.get_quality_list()

    def get_prices_by_group_and_quality(self, groups: list, quality: list):
        """
        Получает список цен по группе и категории качества
        :param groups: группы
        :param quality: категории качества

        Автор: Перятин Виталий
        """
        return self.reports_interactor.get_prices_by_group_and_quality(
            groups, quality)

    def get_products_by_group(self, group: str):
        """
        Получает списико продуктов по группе
        :param group: группа

        Автор: Перятин Виталий
        """
        return self.reports_interactor.get_products_by_group(group)

    def get_box_and_whisker_prices(self, product_group: str, qualities: list,
                                   products: list):
        """
        Получает разброс цен для диаграммы "Ящик с усами"

        Автор: Перятин Виталий
        """
        return self.reports_interactor.get_box_and_whisker_prices(
            product_group, qualities, products)

    def get_prices_by_group(self, product_group: str, products: list):
        """
        Получает список цен продуктоа по группе
        :param products: список продуктов
        :param product_group: название группы

        Автор: Перятин Виталий
        """
        return self.reports_interactor.get_prices_by_group(product_group,
                                                           products)

    def get_spreading(self, product_group: str, date: str):
        """
        Получает разброс цен по группе в определённый день
        :param product_group: название группы
        :param date: дата

        Автор: Перятин Виталий
        """
        return self.reports_interactor.get_spreading(product_group,
                                                     date)
