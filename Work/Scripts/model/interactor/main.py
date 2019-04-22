# -*- coding: utf-8 -*-

""" PyLinter Sublime Text Plugin

    This is a Pylint plugin for Sublime Text.

    Copyright R. de Laat, Elit 2011-2013

    For more information, go to https://github.com/biermeester/Pylinter#readme
"""
import pickle

import os
import datetime
import time

import pandas
os.chdir('C:/Users/Tom/Documents/Python_projects/ProductsViewer/Work/Data')


class ReportsInteractor:
    """Данный класс никак не изменяет исходной БД и лишь достаёт необходимые данные
    """

    def __init__(self, pickle_db_filename: str = 'db.pickle'):
        """Считывание pickle файла и создание каждой таблицы

        """
        with open(pickle_db_filename, "rb") as open_data_base:
            data_base = pickle.load(open_data_base)

        self._db_products = data_base['_db_products']
        self._db_discounts = data_base['_db_discounts']
        self._db_vouchers = data_base['_db_vouchers']
        self._db_sales = data_base['_db_sales']
        self._db_groups = data_base['_db_groups']

    def get_main_table(self):
        """Эта функция возвращает DataFrame с основной таблицей, с конвертированными заголовками:
            discount_id -> Dicsount (при чём теперь тут значения скидки, 
                                        а не id, если эта скидка ещё активна)
            group_name  -> Category
            price       -> Price (цена пересчитана с  учётом скидки)
        ... и т.д
        """
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
                main_table.discount_id[main_table.discount_id ==
                                       self._db_discounts.id.iloc[
                                           i]] = self._db_discounts.amount.iloc[i]
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
        """На вход подаётся лист групп товаров (Овощи, Мясное, к примеру)
        и лист качеств (ГОСТ, ТУ, например).
        Функция возвращает DataFrame содержащий отсортированную таблицу вида:
            Группа -> Качество -> СС
        Где СС - средняя стоимость товаров данной группы и качества
        """
        products_table = self._db_products
        result = products_table[(products_table.group_name.isin(groups)) & (
            products_table.quality.isin(qualities))].groupby(
                ['group_name', 'quality'])['price'].mean()
        return result

    def get_prices_by_group(self, product_group: str, products: list):
        """Функция принимает на вход тип продукции и лист продуктов
        Возвращает Dataframe с колонками:
            name -> наименование продукта
            price -> стоимость единицы данного товара 
        """
        result = {}
        table = self._db_products
        result = table[(table.group_name == product_group)
                       & (table.name.isin(products))].copy()[['name', 'price']]
        return result

    def get_box_and_whisker_prices(self, product_group: str, qualities: list, products: list):
        """Функция принимает на вход тип продукции, лист качеств и лист продуктов
        Возвращает лист листов, где каждая ячейка содержит стоимости всех продуктов данного качества
        Т.е к примеру, если qualities = ['ГОСТ','ТУ']
        То  result[0] сожержит стоимости продуктов из листа productsкачества 'ГОСТ',
            result[1] ->'ТУ'  
        """
        temp_db = self._db_products.copy()
        temp_db = temp_db.loc[temp_db.group_name == product_group]
        result = []
        
        for _, item in enumerate(qualities):
            slice_of_db = temp_db.price.loc[
                (temp_db.quality == item) & (temp_db.name.isin(products))]
            result.append(list(slice_of_db))
        
        return result

    def get_spreading(self, product_group: str, date: str):
        """Функция принимает на вход наименование типа продукции и дату
        Возвращает лист словарей вида:
        Return =[
            {'price': стоимость единицы товара данного типа проданного в этот день,
             'amount': кол-во продаж этого товара},
            ...
        ]
        Где содержатся все товары данного типа, проданные в этот день
        """
        vouchers = self._db_vouchers[self._db_vouchers.date == date]
        sales = self._db_sales[self._db_sales.check_id.isin(vouchers.id)]

        intermediate_result = sales.groupby(['products_id'])['amount'].sum()

        for i in intermediate_result.keys().tolist():
            if list(self._db_products[self._db_products.id == i].group_name)[0] != product_group:
                intermediate_result = intermediate_result.drop(i)
            else:
                intermediate_result = intermediate_result.rename({
                    i: list(self._db_products[self._db_products.id == i]['price'])[0]
                })
        price_list = intermediate_result.keys().tolist()
        amount_list = intermediate_result.values.tolist()

        result = []
        for i, current_amount in enumerate(amount_list):
            result.append({'price': price_list[i]})
            result[i]['amount'] = current_amount

        return result

    def get_groups_list(self):
        """Возвращает лист, содержащий все возможные категории продукции
        """
        return list(self._db_groups['name'])

    def get_quality_categories(self):
        """Возвращает все возможные категории качества
        """
        result = list(self._db_products['quality'].unique())
        return result
