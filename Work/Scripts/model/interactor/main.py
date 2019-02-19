# Метод/функция для получения средних цен по выбранным категориям
# продуктов и выбранному качеству

# Метод/функция на вход получает список групп продуктов и список категорий качества.
#   Исходя из входных данныx необходимо получить список средних цен
#   по каждой категории качества каждой группы вида
#   [[группа1-качество1, группа1-качество2], [группа2-качество1, группа2-качество2]]
import pandas
import pickle

import os
import datetime
import time
os.chdir('C:/Users/ирбисик/Documents/PYTHON/ProductsViewer/Work/Data')


class ReportsInteractor:
    file_name = 'database.txt'

    def __init__(self):
        DB_Name = 'db.pickle'
        with open(DB_Name,"rb") as DB:
            DataBase = pickle.load(DB)
        for i in range(len(DataBase.keys())):
            db_name=list(DataBase.keys())[i]
            exec('self.%s=DataBase["%s"]' % (db_name,db_name))
        # file_name = 'database.txt'
        # with open(file_name) as file:
        #     self.DB_List = [row.strip() for row in file]

        # for i in range(len(self.DB_List)):
        #     attr_name = self.DB_List[i].strip('csv')
        #     attr_name = attr_name.strip('.')
        #     key_name = attr_name
        #     attr_name = 'DB_' + attr_name
        #     setattr(self, attr_name, pandas.read_csv(self.DB_List[i], sep=';'))

    def get_main_table(self):
        """
        Author: Suleymanov Nail
        Function returns list of lists that contain all needed information for main table
        as: product_id,product_name,product_price,product_producer,product_group,dicsount, quality
        Return[0]==list of headers for table
        """
        Result = [] * 1
        Result.append(list(self.DB_Products.columns))

        def is_discount_works(self, discount_id: int):
            import datetime
            now = time.mktime(datetime.datetime.now().timetuple())
            date_begin = time.mktime(datetime.datetime.strptime(self.DB_Discounts.iloc[
                                     discount_id]['date_begin'], "%d.%m.%Y").timetuple())
            date_end = time.mktime(datetime.datetime.strptime(self.DB_Discounts.iloc[
                                   discount_id]['date_end'], "%d.%m.%Y").timetuple())

            return date_begin <= now <= date_end

        for i in range(len(self.DB_Products)):
            Result.append(list(self.DB_Products.iloc[i]))
            if is_discount_works(self, Result[i + 1][5]):
                Result[i + 1][5] = self.DB_Discounts.iloc[Result[i + 1][5]]['amount']
                Result[i + 1][2] = round(int(Result[i + 1][2])
                                         * (1 - int(Result[i + 1][5]) / 100.0), 2)
            else:
                Result[i + 1][5] = 0

        return Result

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
        """Author: Suleymanov Nail
        output: Result
        Result=[
            {'product[i].name': price[i] },
            ...
        ]
        product[i] is in products and have product[i].group_name == product_group

        """
        Result = {} * 0
        for i in range(len(DB.index)):
            if (DB.iloc[i]['group_name'] == product_group) and (DB.iloc[i]['name'] in products):
                Result.update({DB.iloc[i]['name']: int(DB.iloc[i]['price'])})
        return Result

    def get_box_and_whisker_prices(self, product_group: str, qualities: list, products: list):
        """Author: Suleymanov Nail
        output: Result
        I forgot for what it was created but it works !=)

        """
        def get_quality_pos(quality: str, quality_list: str):
            for i in range(len(quality_list)):
                if quality == quality_list[i]:
                    return i

        database = self.DB_Products
        Result = {}
        List_of_list = [None] * len(qualities)
        for i in range(len(List_of_list)):
            List_of_list[i] = []

        Result = Result.fromkeys(qualities, [])
        for i in range(len(database)):
            if (database.iloc[i]['name'] in products) and (
                    database.iloc[i]['quality'] in qualities) and (
                    database.iloc[i]['group_name'] == product_group):
                current_quality_pos = get_quality_pos(
                    database.iloc[i]['quality'], qualities)
                List_of_list[current_quality_pos].append(
                    int(database.iloc[i]['price']))
        for i in range(len(List_of_list)):
            Result[qualities[i]] = List_of_list[i]

        return Result

    def get_spreading(self, product_group: str, date: str):
        """Author: Suleymanov Nail
        output: Result
        Return information about amount of sold production of product_group and price
        in DD.MM.YYYY date
        Return =[
            {'price': price of 1 object,
             'amount': amount of this product},
            ...
        ]

        """
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
                if first_sale != None:
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
            if (first_sale != None):
                if (first_sale <= int(sales.iloc[i]['check_id']) <= last_sale) and (
                        products.iloc[sales.iloc[i]['products_id']]['group_name'] == product_group):
                    if products.iloc[sales.iloc[i]['products_id']]['name'] not in saved_product_list:
                        saved_product_list.append(
                            products.iloc[sales.iloc[i]['products_id']]['name'])
                        Result.append({'price': products.iloc[sales.iloc[i][
                                      'products_id']]['price'], 'amount': sales.iloc[i]['amount']})
                    else:
                        pos = current_position(saved_product_list, products.iloc[
                                               sales.iloc[i]['products_id']]['name'])
                        Result[pos]['amount'] += sales.iloc[i]['amount']
        return Result

    def get_groups_list(self):
        """Author: Suleymanov Nail
        Returns list of products groups

        """
        return list(self.DB_Groups['name'])

    def get_quality_list(self):
        """Author: Suleymanov Nail
        output: Result
        Returns list of sorted products qualities

        """
        Result = list(set(list(self.DB_Products['quality'])))
        Result.sort()
        return Result

    def get_products_by_group(self, group: str):
        pass
