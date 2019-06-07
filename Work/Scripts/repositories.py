"""
Данный модуль содержит классы:
    class MainTableRepository - для контакта с БД
    class ReportsInteractor - класс для создания отчётов
Отключены следующие ошибки pylint:
    W0212 - Ошибка доступа к защищённым данным
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)
    W0702 - Ошибка отсутствия точного exception'а
"""
# pylint: disable=W0212
# pylint: disable=E0401
# pylint: disable=W0702
import copy

import datetime
import time

import pandas
import pandas as pd

from Work.Scripts.commands import CommandDelete, CommandUpdate, \
    CommandInsert, CommandSelect
from Work.Scripts.key_words import CompareOp
from Work.Scripts.interf_extractor import IDataExtractor
from Work.Scripts.config import NAME_TITLES


class MainTableRepository:
    """
    Класс для импорта основной информации из базы данных

    Автор: Сулейманов Наиль
    """
    extractor: IDataExtractor
    df = pd.DataFrame()
    select_df = pd.DataFrame()

    def __init__(self, extractor: IDataExtractor):
        self.extractor = extractor

    def get_data(self):
        """
        Возвращает основную таблицу, получаемую функцией get_main_table

        Автор: Сулейманов Наиль
        """
        return self.get_main_table()

    def get_main_table(self):
        """
        Функция возвращает список списков, которые содержат всю необходимую информацию для основной таблицы
        как: product_id, product_name, product_price, product_producer, product_group, dicsount, качество

        :return: список заголовков таблицы

        Автор: Сулейманов Наиль
        """
        main_table: pandas.DataFrame = self.extractor._db_products.copy()
        self.discount_list: pandas.DataFrame = self.extractor._db_discounts.copy()
        self.discount_list: pandas.DataFrame = self.extractor._db_discounts.copy()
        self.producer_list: pandas.DataFrame = self.extractor._db_producers.copy()
        self.group_list: pandas.DataFrame = self.extractor._db_groups.copy()
        main_table = pandas.merge(
            main_table, self.discount_list, left_on='discount_id', right_on='discount_id')
        main_table = pandas.merge(
            main_table, self.group_list, left_on='group_id', right_on='group_id')
        main_table = pandas.merge(
            main_table, self.producer_list, left_on='producer_id', right_on='producer_id')
        columns = ['id','name','price','producer_id','producer_name','group_id','group_name','discount_id','amount','date_begin','date_end','quality']
        main_table=main_table[columns]
        discounts_id = self.discount_list.discount_id.copy()
        for i in range(len(discounts_id)):
            if not self.is_discount_works(discounts_id.iloc[i]):
                change_list = main_table.discount_id == discounts_id.iloc[i]
                main_table.amount.loc[change_list] = 0
                main_table.date_end.loc[change_list] = 'XX.XX.XXXX'

        main_table = main_table.rename(columns={
            'name': NAME_TITLES[0],
            'price': NAME_TITLES[1],
            'producer_name': NAME_TITLES[2],
            'group_name': NAME_TITLES[3],
            'amount': NAME_TITLES[4],
            'quality': NAME_TITLES[5]
        })
        main_table['Скидка'] = main_table['Скидка'].astype(str)+'% ['+main_table['date_end']+']'
        del main_table['date_begin']
        del main_table['date_end']
        main_table= main_table.sort_values('id')
        self.df = main_table
        self.select_df = main_table
        return main_table

    def is_discount_works(self, discount_id: int):
        now = time.mktime(datetime.datetime.now().timetuple())
        date_begin = time.mktime(datetime.datetime.strptime(
            self.discount_list['date_begin'].iloc[discount_id],
            "%d.%m.%Y").timetuple())
        date_end = time.mktime(
            datetime.datetime.strptime(
                self.discount_list['date_end'].iloc[
                    discount_id],
                "%d.%m.%Y").timetuple())
        return date_begin <= now <= date_end

    def set_data(self, data: pd.DataFrame):
        """
        Устанавливает новую БД в виде DataFrame
        :param data: новые данные для записи

        Автор: Перятин Виталий
        """
        self.d_f = data

    def get_products_groups(self):
        """
        Функция возвращает группы товаров

        Автор: Сулейманов Наиль
        """
        return self.extractor._db_groups["group_name"].unique()

    def get_qualities(self):
        """Return quality_list"""
        return self.extractor._db_products['quality'].unique()

    def get_producers(self):
        """
        Возвращает список производителей
        :return: список производителей

        Автор: Перятин Виталий
        """
        return self.extractor._db_producers['producer_name'].unique()

    def get_products_names(self):
        """
        Возвращает названия продуктов из БД
        :return: названия продуктов из БД

        Автор: Перятин Виталий
        """
        return self.extractor._db_products['name'].unique()

    def get_max_price(self):
        """
        Возращает максимальную цену проуктов
        :return: максимальная цена проуктов

        Автор: Перятин Виталий
        """
        return max(list(self.extractor._db_products['price']))

    def get_max_discount(self):
        """
        Возвращает макасимальную скидку продуктов
        :return: макасимальная скидка продуктов

        Автор: Перятин Виталий
        """
        return max(list(self.extractor._db_discounts['amount']))

    def select(self, command_select: CommandSelect = None):
        """
        Выбирает данные из БД по переданным командам извне

        :param command_select: команды для выборки данных из БД
        :return: Отфильтрованная БД в виде DataFrame

        Автор: Перятин Виталий
        """
        if not command_select is None:
            self.selector = command_select
        drop_list = [item for item in self.d_f.columns.values if item not in
                     self.selector.get_columns()]
        self.select_df = self.d_f.drop(drop_list, axis=1)
        for col, o_p, val in self.selector.items():
            self.select_df = self.select_df[self._filter(
                self.d_f, col, o_p, val)]
        return self.select_df

    @staticmethod
    def _filter(df: pd.DataFrame, field, compare_op: str,
                value, reverse=False):
        """
        Фильтрует записи таблицы. Проверяет удовлетвоярет ли строка
        в DataFrame переданному значению
        :param d_f: таблица для фильтрации
        :param field: поле, которое проверяется при фильтрации
        :param compare_op: операнд сравнения
        :param value: значение, относительно которого фильтруются данные
        :param reverse: True при необходимости перевернуть операцию сравнения
        :return: отфильтрованная БД

        Автор: Перятин Виталий
        """
        def get_type_of(series: pd.Series):
            """
            Получает тип значений, которые хранятся в колонке
            :param series: список значений столбца
            :return: тип значений столбца

            Автор: Перятин Виталий
            """
            if series.array:
                try:
                    float(series.array[0])
                    float(value)
                    return float
                except:
                    return str
            return None

        def reverse_op(op):
            """
            Переворачивает операцию сравнения
            :return: перевернутая операция сравнения

            Автор: Перятин Виталий
            """
            return {
                CompareOp.EQUAL: CompareOp.NOT_EQUAL,
                CompareOp.NOT_EQUAL: CompareOp.EQUAL,
                CompareOp.LESS: CompareOp.MORE_OR_EQUAL,
                CompareOp.LESS_OR_EQUAL: CompareOp.MORE,
                CompareOp.MORE: CompareOp.LESS_OR_EQUAL,
                CompareOp.MORE_OR_EQUAL: CompareOp.LESS
            }[op]

        data_type = get_type_of(df[field])
        value = data_type(value)
        field_val = df[field].astype(data_type)
        if reverse:
            compare_op = reverse_op(compare_op)
        return {
            CompareOp.EQUAL: field_val == value,
            CompareOp.NOT_EQUAL: field_val != value,
            CompareOp.LESS: field_val < value,
            CompareOp.LESS_OR_EQUAL: field_val <= value,
            CompareOp.MORE: field_val > value,
            CompareOp.MORE_OR_EQUAL: field_val >= value
        }[compare_op]

    def insert(self, command_insert: CommandInsert):
        """
        Получает строки для вставки в БД
        :return: строки для вставки в БД

        Автор: Перятин Виталий
        """
        row = command_insert.get_row()
        self.df = self.df.append(row, ignore_index=True)
        return row.values()

    def update(self, command_update: CommandUpdate):
        """
        Получает обновленные строки по переданной команеде
        :return: обновленные строки по переданной команеде

        Автор: Перятин Виталий
        """
        command_update.get_values()
        for col, op, val in command_update.items():
            for field, set_val in command_update.get_values().items():
                self.df.loc[self._filter(
                    self.df, col, op, val
                ), field] = set_val
        return self.select(self.selector)

    def delete(self, command_delete: CommandDelete):
        """
        Получает таблицу с удалёными строками
        :return: таблица с удалёными строками

        Автор: Перятин Виталий
        """
        for col, o_p, val in command_delete.items():
            self.d_f = self.d_f[self._filter(self.d_f, col, o_p, val, True)]
        return self.select(self.selector)

    def get_vals_by_col(self, column: str):
        """
        Получает список значений по названию столбца
        :param column: название столбца
        :return: список значений по названию столбца

        Автор: Перятин Виталий
        """
        vals = list(set(self.d_f[column].tolist()))
        vals.sort()
        return vals

    def get_db_copy(self):
        """
        Получает копию базы данных
        :return: копия базы данных

        Автор: Перятин Виталий
        """
        return copy.deepcopy(self.df)

    def get_quality_list(self):
        """
        Получает список категорий качества
        :return: список категорий качества

        Автор: Перятин Виталий
        """
        result = list(self.extractor._db_products['quality'].unique())
        return result
    def get_producers_list(self):
        """
        Получает список производителей
        :return: список производителей

        Автор: Перятин Виталий
        """
        producers = self.extractor._db_producers.copy()
        producer_list = list(producers['name'])
        return producer_list

    def get_group_list(self):
        """
        Получает список групп
        :return: список групп

        Автор: Перятин Виталий
        """
        groups = self.extractor._db_groups.copy()
        producer_list = list(groups['name'])
        return producer_list

    def get_discount_list(self):
        """
        Получает список скидок
        :return: список скидок

        Автор: Перятин Виталий
        """
        discounts = self.extractor._db_discounts.copy()
        date_list = list(discounts['date_end'])
        discount_list = list(discounts['amount'])
        for i,j in enumerate(discount_list):
            discount_list[i]=str(j)+'% ['+date_list[i]+']'
        return discount_list


class ReportsInteractor:
    """
    Класс для работы с базой данных и преобразования типов

    Автор: Сулейманов Наиль
    """
    extractor: IDataExtractor

    def __init__(self, extractor: IDataExtractor):
        self.extractor = extractor

    def get_prices_by_group_and_quality(self, groups: list, qualities: list):
        """
        :return: таблица, содержащая таблицу со средней ценой
        каждого качества и группы от входа

        Автор: Сулейманов Наиль
        """
        products_table = self.extractor._db_products
        result = []
        # products_table[(products_table.group_name.isin(groups)) & (
        #     products_table.quality.isin(qualities))].groupby(
        #     ['group_name', 'quality'])['price'].mean()
        for i in range(len(groups)):
            result.append([0] * len(qualities))
            for j in range(len(qualities)):
                group_mean_prices = None
                try:
                    group_mean_prices = list(products_table[(products_table.group_name.isin([groups[i]])) & (
                        products_table.quality.isin([qualities[j]]))].groupby(
                            ['group_name', 'quality'])['price'].mean())
                except IndexError:
                    pass
                if group_mean_prices:
                    result[i][j] = group_mean_prices[0]
        return result

    def get_prices_by_group(self, product_group: str, products: list):
        """
        Возвращает список словарей, где ключ - название столбца, а значение словаря - сзанчение столбца.
        Список словарей - список цен по выбранной группе
        :return: список цен по выбранной группе

        Автор: Сулейманов Наиль
        """
        result = {}
        table = self.extractor._db_products
        result = table[(table.group_name == product_group)
                       & (table.name.isin(products))].copy()[['name', 'price']]
        return result

    def get_products_groups(self):
        """
        Функция возвращает Series со всеми группами продукции

        Автор: Сулейманов Наиль
        """
        return self.extractor._db_groups["group_name"]

    def get_products_by_group(self, group: str):
        """
        Функция возвращает список Series с продуктами,
        принадлежащими заданной группе товаров.

        Автор: Сулейманов Наиль
        """
        db_products = self.extractor._db_products
        return db_products[db_products["group_name"] == group]["name"]

    def get_box_and_whisker_prices(self, product_group: str, qualities: list, products: list):
        """
        Функция принимает на вход тип продукции, лист качеств и лист продуктов
        Возвращает лист листов, где каждая ячейка содержит стоимости всех продуктов данного качества

        Автор: Сулейманов Наиль
        """
        temp_db = self.extractor._db_products.copy()
        temp_db = temp_db.loc[temp_db.group_name == product_group]
        result = []

        for _, item in enumerate(qualities):
            slice_of_db = temp_db.price.loc[
                (temp_db.quality == item) & (temp_db.name.isin(products))]
            result.append(list(slice_of_db))

        return result

    def get_spreading(self, product_group: str, date: str):
        """
        Возвращает информацию о количестве проданной продукции группы товаров и цене
        в формате ДД.ММ.ГГГГ
        :return: список словарей по распылению исходя из переданных параметров

        Автор: Сулейманов Наиль
        """
        vouchers = self.extractor._db_vouchers[
            self.extractor._db_vouchers.date == date]
        sales = self.extractor._db_sales[
            self.extractor._db_sales.check_id.isin(vouchers.id)]

        intermediate_result = sales.groupby(['products_id'])['amount'].sum()

        # оставить только элементы подходящего типа продукции
        for i in intermediate_result.keys().tolist():
            if list(self.extractor._db_products[self.extractor._db_products.id == i].group_name)[0] != product_group:
                intermediate_result = intermediate_result.drop(i)
            else:
                # intermediate_result[i] *= int(
                #     self._db_products[self._db_products.id == i].price)
                intermediate_result = intermediate_result.rename({
                    i: list(self.extractor._db_products[self.extractor._db_products.id == i]['price'])[0]
                })
        price_list = intermediate_result.keys().tolist()
        amount_list = intermediate_result.values.tolist()

        result = []
        for i, current_amount in enumerate(amount_list):
            result.append({'price': price_list[i]})
            result[i]['amount'] = current_amount

        return result

    def get_quality_list(self):
        """
        Получает список значений качества продукции

        Автор: Сулейманов Наиль
        """
        result = list(self.extractor._db_products['quality'].unique())
        return result
