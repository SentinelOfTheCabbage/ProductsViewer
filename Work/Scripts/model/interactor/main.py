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
os.chdir('C:/Users/Tom/Documents/Python_projects/ProductsViewer/Work/Data')


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
        main_table = self._db_products.copy()

        def is_discount_works(discount_id: int):
            now = time.mktime(datetime.datetime.now().timetuple())
            date_begin = time.mktime(datetime.datetime.strptime(
                self._db_discounts['date_begin'].iloc[discount_id], "%d.%m.%Y").timetuple())
            date_end = time.mktime(datetime.datetime.strptime(self._db_discounts['date_end'].iloc[
                discount_id], "%d.%m.%Y").timetuple())
            return date_begin <= now <= date_end

        discount_list = self._db_discounts.id.copy()

        for i in range(len(discount_list)):
            if is_discount_works(discount_list.iloc[i]):
                main_table.loc[main_table.discount_id == discount_list.iloc[
                    i], 'discount_id'] = self._db_discounts.amount.iloc[i]
            else:
                main_table.discount_id.loc[
                    main_table.discount_id == discount_list.iloc[i]] = 0

        main_table.price *= round((1 - main_table.discount_id / 100.0), 2)
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

    def get_prices_by_group_and_quality(self, groups: list, qualities: list):
        """Author: Suleymanov Nail
        output: result,qualities
        result={
            'group1': [q1_value,q2_value,q3_value...],
            ...
        }
        qualities=['q1','q2',...]

        """
        products_table = self._db_products
        result = products_table[(products_table.group_name.isin(groups)) & (
            products_table.quality.isin(qualities))].groupby(
                ['group_name', 'quality'])['price'].mean()
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
        table = self._db_products
        result = table[(table.group_name == product_group)
                       & (table.name.isin(products))].copy()[['name', 'price']]
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
        vouchers = self._db_vouchers[self._db_vouchers.date == date]
        sales = self._db_sales[self._db_sales.check_id.isin(vouchers.id)]

        result = sales.groupby(['products_id'])['amount'].sum()

        # оставить только элементы подходящего типа продукции
        for i in result.keys().tolist():
            if list(self._db_products[self._db_products.id == i].group_name)[0] != product_group:
                result = result.drop(i)
            else:
                # result[i] *= int(
                #     self._db_products[self._db_products.id == i].price)
                result = result.rename({
                    i: list(self._db_products[self._db_products.id == i]['price'])[0]
                })
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
