# -*- coding: utf-8 -*-

""" PyLinter Sublime Text Plugin

    This is a Pylint plugin for Sublime Text.

    Copyright R. de Laat, Elit 2011-2013

    For more information, go to https://github.com/biermeester/Pylinter#readme
"""
# Метод функция для получения средних цен по выбранным категориям
# продуктов и выбранному качеству

# Метод/функция на вход получает список групп продуктов и список категорий качества.
#   Исходя из входных данныx необходимо получить список средних цен
#   по каждой категории качества каждой группы вида
#   [[группа1-качество1, группа1-качество2], [группа2-качество1, группа2-качество2]]
import pickle

import os
import datetime
import time

import pandas
os.chdir('C:/Users/ирбисик/Documents/PYTHON/ProductsViewer/Work/Data')


class ReportsInteractor:
    """
    docstring
    """
    file_name = 'database.txt'

    def __init__(self):
        with open('db.pickle', "rb") as open_data_base:
            data_base = pickle.load(open_data_base)

        self._db_products = data_base['_db_products']
        self._db_discounts = data_base['_db_discounts']
        self._db_vouchers = data_base['_db_vouchers']
        self._db_sales = data_base['_db_sales']
        self._db_groups = data_base['_db_groups']

    def get_main_table(self):
        """
        Author: Suleymanov Nail
        Function returns list of lists that contain all needed information for main table
        as: product_id,product_name,product_price,product_producer,product_group,dicsount, quality
        Return[0]==list of headers for table
        """
        # result = [] * 1
        # result.append(list(self._db_products.columns))
        main_table = self._db_products

        def is_discount_works(self, discount_id: int):
            now = time.mktime(datetime.datetime.now().timetuple())
            date_begin = time.mktime(datetime.datetime.strptime(
                self._db_discounts['date_begin'].iloc[discount_id], "%d.%m.%Y").timetuple())
            date_end = time.mktime(datetime.datetime.strptime(self._db_discounts['date_end'].iloc[
                discount_id], "%d.%m.%Y").timetuple())

            return date_begin <= now <= date_end

        for i in range(len(main_table)):
            if is_discount_works(self, main_table['discount_id'].iloc[i]):
                main_table['discount_id'].iloc[i] = self._db_discounts.iloc[
                    main_table['discount_id'].iloc[i]]['amount']
                main_table['price'].iloc[i] = int(main_table['price'].iloc[
                    i]) * (1 - int(main_table['discount_id'].iloc[
                        i]) / 100.0)
            else:
                main_table['discount_id'].iloc[i] = 0
        main_table = main_table.rename(columns={
            'id': 'Id',
            'name': 'Product name',
            'price': 'Price',
            'producer_name': 'Producer name',
            'group_name': 'Category',
            'discount_id': 'Discount',
            'quality': 'Quality'
        })
        return main_table

    def get_prices_by_group_and_quality(self, groups: list, quality: list):
        """Author: Suleymanov Nail
        output: result,qualities
        result={
            'group1': [q1_value,q2_value,q3_value...],
            ...
        }
        qualities=['q1','q2',...]

        """

        def arithmetic_mean_series(groups: list, quality: list):
            products_list = self._db_products
            sorted_series_table = products_list.groupby(['group_name', 'quality'])[
                'price'].mean()
            changes = True
            table_group_keys_list = list(
                sorted_series_table.index.levels[0])
            while changes is True:
                changes = False

                for i in table_group_keys_list:
                    if i not in groups:
                        sorted_series_table = sorted_series_table.drop(
                            labels=i, level=0)
                        table_group_keys_list.remove(i)
                        changes = True
                        break

            del table_group_keys_list
            table_quality_keys_list = list(
                sorted_series_table.index.levels[1])
            changes = True
            while changes is True:
                changes = False

                for i in table_quality_keys_list:
                    if i not in quality:
                        sorted_series_table = sorted_series_table.drop(
                            labels=i, level=1)
                        table_quality_keys_list.remove(i)
                        changes = True
                        break
            return sorted_series_table

        sorted_series_table = arithmetic_mean_series(
            groups, quality)  # Получение DataFrame
        result = dict.fromkeys(groups)  # Создание будущего dict of list
        for i in groups:
            result[i] = [0] * len(quality)

        # Вспомогательная функция для быстрого определения позиций в листах
        def group_pos(groups, needle: str):
            for i in groups:
                if i == needle:
                    return i
            return None

        def table_pos(table, needle: str):
            for i, item in enumerate(table):
                if item == needle:
                    return i
            return None

        for i in range(len(sorted_series_table.index.codes[0])):
            #  взять key продукта и соотнести с позицией в groups
            groups_position = group_pos(groups, sorted_series_table.index.levels[
                0][sorted_series_table.index.codes[0][i]])

            #  взять key качества и соотнести с позицией в quality
            quality_position = table_pos(quality, sorted_series_table.index.levels[
                1][sorted_series_table.index.codes[1][i]])

            # записать в нужную ячейку инфомрацию
            if (groups_position is not None) and (quality_position is not None):
                result[groups_position][
                    quality_position] = sorted_series_table[i]

        return result

    def get_prices_by_group(self, product_group: str, products: list):
        """Author: Suleymanov Nail
        output: result
        result=[
            {'product[i].name': price[i] },
            ...
        ]
        product[i] is in products and have product[i].group_name == product_group

        """
        result = {}
        for i in range(len(self._db_products.index)):
            if self._db_products.iloc[i]['group_name'] == product_group:
                if self._db_products.iloc[i]['name'] in products:
                    result.update({self._db_products.iloc[i]['name']: int(
                        self._db_products.iloc[i]['price'])})
        return result

    def get_box_and_whisker_prices(self, product_group: str, qualities: list, products: list):
        """Author: Suleymanov Nail
        output: result
        I forgot for what it was created but it works !=)

        """
        def get_quality_pos(quality: str, quality_list: str):
            for i, item in enumerate(quality_list):
                if quality == item:
                    return i
            return None

        database = self._db_products
        result = {}
        list_of_list = [None] * len(qualities)
        for i, item in enumerate(list_of_list):
            item = []

        result = result.fromkeys(qualities, [])
        for i in range(len(database)):
            if (database.iloc[i]['name'] in products) and (
                    database.iloc[i]['quality'] in qualities) and (
                        database.iloc[i]['group_name'] == product_group):
                current_quality_pos = get_quality_pos(
                    database.iloc[i]['quality'], qualities)
                list_of_list[current_quality_pos].append(
                    int(database.iloc[i]['price']))
        for i, item in enumerate(list_of_list):
            result[qualities[i]] = item

        return result

    def get_spreading(self, product_group: str, date: str):
        """Author: Suleymanov Nail
        output: result
        Return information about amount of sold production of product_group and price
        in DD.MM.YYYY date
        Return =[
            {'price': price of 1 object,
             'amount': amount of this product},
            ...
        ]

        """
        vouchers = self._db_vouchers
        sales = self._db_sales
        products = self._db_products
        first_sale = None
        last_sale = None
        result = []
        for i in vouchers.index:
            if vouchers.iloc[i]['date'] == date:
                if first_sale is None:
                    first_sale = i
                if first_sale is not None:
                    last_sale = i
            elif last_sale is not None:
                break

        def current_position(source: list, needle: str):
            for i in len(source):
                if source[i] == needle:
                    return i
            return None

        for i in sales.index:
            save_product_list = []
            result = []
            if first_sale is not None:
                if (first_sale <= int(sales.iloc[i]['check_id']) <= last_sale) and (
                        products.iloc[sales.iloc[i]['products_id']]['group_name'] == product_group):
                    if products.iloc[sales.iloc[i]['products_id']]['name'] not in save_product_list:
                        save_product_list.append(
                            products.iloc[sales.iloc[i]['products_id']]['name'])
                        result.append({'price': products.iloc[sales.iloc[i][
                            'products_id']]['price'], 'amount': sales.iloc[i]['amount']})
                    else:
                        pos = current_position(save_product_list, products.iloc[
                            sales.iloc[i]['products_id']]['name'])
                        result[pos]['amount'] += sales.iloc[i]['amount']
        return result

    def get_groups_list(self):
        """Author: Suleymanov Nail
        Returns list of products groups

        """
        return list(self._db_groups['name'])

    def get_quality_list(self):
        """Author: Suleymanov Nail
        output: result
        Returns list of sorted products qualities

        """
        result = list(set(list(self._db_products['quality'])))
        result.sort()
        return result
