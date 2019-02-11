# Метод/функция для получения средних цен по выбранным категориям
# продуктов и выбранному качеству

# Метод/функция на вход получает список групп продуктов и список категорий качества.
#   Исходя из входных данныx необходимо получить список средних цен по каждой категории качества каждой группы вида
#   [[группа1-качество1, группа1-качество2], [группа2-качество1, группа2-качество2]]
import pandas

import os
os.chdir('C:/Users/ирбисик/Documents/PYTHON/ProductsViewer/Work/Data')


class ReportsInteractor:
    file_name = 'database.txt'

    def __init__(self):
        file_name = 'database.txt'
        with open(file_name) as file:
            DB_List = [row.strip() for row in file]
        self.DB_Products = pandas.read_csv(DB_List[0], sep=';')
        self.DB_Producer = pandas.read_csv(DB_List[2], sep=';')
        self.DB_Vouchers = pandas.read_csv(DB_List[5], sep=';')
        self.DB_Sales = pandas.read_csv(DB_List[1], sep=';')
        self.DB_Groups = pandas.read_csv(DB_List[3], sep=';')
        self.DB_Discount = pandas.read_csv(DB_List[4], sep=';')

    def get_prices_by_group_and_quality(self, groups: list, quality: list):
        """Author: Suleymanov Nail
        output: Result,qualities
        Result={
            'group1': [q1_value,q2_value,q3_value...],
            ...
        }
        qualities=['q1','q2',...]

        """

        def arithmetic_mean_series(groups: list, quality: list):
            products_list = self.DB_Products
            sorted_series_table = products_list.groupby(['group_name', 'quality'])[
                'price'].mean()
            changes = True
            print(sorted_series_table)
            table_group_keys_list = list(sorted_series_table.index.levels[0])
            while changes == True:
                changes = False

                for i in range(len(table_group_keys_list)):
                    if table_group_keys_list[i] not in groups:
                        sorted_series_table = sorted_series_table.drop(
                            labels=table_group_keys_list[i], level=0)
                        table_group_keys_list.remove(table_group_keys_list[i])
                        changes = True
                        break

            del(table_group_keys_list)

            table_quality_keys_list = list(sorted_series_table.index.levels[1])
            changes = True
            while changes == True:
                changes = False

                for i in range(len(table_quality_keys_list)):
                    if table_quality_keys_list[i] not in quality:
                        sorted_series_table = sorted_series_table.drop(
                            labels=table_quality_keys_list[i], level=1)
                        table_quality_keys_list.remove(
                            table_quality_keys_list[i])
                        changes = True
                        break
            return sorted_series_table

        sorted_series_table = arithmetic_mean_series(
            groups, quality)  # Получение DataFrame
        Result = dict.fromkeys(groups)  # Создание будущего dict of list
        for i in range(len(groups)):
            Result[groups[i]] = [0] * len(quality)

        # Вспомогательная функция для быстрого определения позиций в листах
        def table_pos(groups, needle):
            for i in range(len(groups)):
                if groups[i] == needle:
                    return i

        for i in range(len(sorted_series_table.index.codes[0])):
            #  взять key продукта и соотнести с позицией в groups
            groups_position = table_pos(groups, sorted_series_table.index.levels[
                0][sorted_series_table.index.codes[0][i]])

            #  взять key качества и соотнести с позицией в quality
            quality_position = table_pos(quality, sorted_series_table.index.levels[
                1][sorted_series_table.index.codes[1][i]])

            #  записать в нужную ячейку инфомрацию
            Result[groups[groups_position]][
                quality_position] = sorted_series_table[i]

        return Result

    def get_prices_by_group(self, product_group: str, products: list):
        Result = {} * 0
        for i in range(len(DB.index)):
            if (DB.iloc[i]['group_name'] == product_group) and (DB.iloc[i]['name'] in products):
                Result.update({DB.iloc[i]['name']: int(DB.iloc[i]['price'])})
        return Result

    def get_box_and_whisker_prices(self, product_group: str, qualities: list, products: list):
        database = self.DB_Products
        Result = {}
        Result.fromkeys(qualities, [])
        for i in range(len(database)):
            if (database.iloc[i]['name'] in products) and (
                    database.iloc[i]['quality'] in qualities) and (
                    database.iloc[i]['group_name'] == product_group):
                Result[database.iloc[i]['quality']].append(
                    int(database.iloc[i]['price']))
        return Result

    def get_spreading(self, product_group: str, date: str):
        vouchers = self.DB_Vouchers
        sales = self.DB_Sales
        products = self.DB_Products
        first_sale = None
        last_sale = None
        Result = []
        for i in vouchers.index:
            if vouchers.iloc[i]['date'] == date:
                if first_sale == None:
                    first_sale = i
                else:
                    last_sale = i
            elif last_sale != None:
                break

        def current_position(source: list, needle: str):
            for i in len(source):
                if source[i] == needle:
                    return i

        for i in sales.index:
            saved_product_list = []
            Result = []
            if (first_sale <= int(sales.iloc[i]['check_id']) <= last_sale) and (
                    products.iloc[sales.iloc[i]['products_id'] - 1]['group_name'] == product_group):
                if products.iloc[sales.iloc[i]['products_id'] - 1]['name'] not in saved_product_list:
                    saved_product_list.append(
                        products.iloc[sales.iloc[i]['products_id'] - 1]['name'])
                    Result.append({'price': products.iloc[sales.iloc[i][
                                  'products_id'] - 1]['price'], 'amount': sales.iloc[i]['amount']})
                else:
                    pos = current_position(saved_product_list, products.iloc[
                                           sales.iloc[i]['products_id'] - 1]['name'])
                    Result[pos]['amount'] += sales.iloc[i]['amount']
        return Result
