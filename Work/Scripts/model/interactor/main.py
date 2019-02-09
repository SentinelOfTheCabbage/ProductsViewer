# Метод/функция для получения средних цен по выбранным категориям
# продуктов и выбранному качеству

# Метод/функция на вход получает список групп продуктов и список категорий качества.
#   Исходя из входных данныx необходимо получить список средних цен по каждой категории качества каждой группы вида
#   [[группа1-качество1, группа1-качество2], [группа2-качество1, группа2-качество2]]
import pandas

import os
os.chdir('C:/Users/ирбисик/Documents/PYTHON/ProductsViewer/Work/Scripts/model/interactor/')


class DataBase:
    file_name = 'database.txt'

    def connect(self):
        file_name = 'database.txt'
        with open(file_name) as file:
            DB_List = [row.strip() for row in file]
        self.DB_Products = pandas.read_csv(DB_List[0], sep=';')
        self.DB_Producer = pandas.read_csv(DB_List[2], sep=';')
        self.DB_Vouchers = pandas.read_csv(DB_List[5], sep=';')
        self.DB_Sales = pandas.read_csv(DB_List[1], sep=';')
        self.DB_Groups = pandas.read_csv(DB_List[3], sep=';')
        self.DB_Discount = pandas.read_csv(DB_List[4], sep=';')

    def AMD(self, groups: list, quality: list):

        def arithmetic_mean_series(self, groups: list, quality: list):
        """Author: Suleymanov Nail' BIV181

        input (groups:list,quality: list)
        return arithmetic mean list

        list={
            {   groups[0]_quality[0]_value,
                groups[0]_quality[1]_value,
                ...
            },
            ...
            {   groups[n-1]_quality[0]_value,
                groups[n-1]_quality[1]_value
                ...
            },
        }

        """

        Prod_List = self.DB_Products
        Table = Prod_List.groupby(['group_name', 'quality'])['price'].mean()
        Group_List = self.DB_Groups
        changes = True
        L = list(Table.index.levels[0])
        while changes == True:
            changes = False

            for i in range(len(L)):
                if L[i] not in groups:
                    Table = Table.drop(labels=L[i], level=0)
                    L.remove(L[i])
                    changes = True
                    break

        L = list(Table.index.levels[1])
        changes = True
        while changes == True:
            changes = False

            for i in range(len(L)):
                if L[i] not in quality:
                    Table = Table.drop(labels=L[i], level=1)
                    L.remove(L[i])
                    changes = True
                    break
        return Table

        Table = self.arithmetic_mean_series(
            groups, quality)  # Получение DataFrame
        R = dict.fromkeys(groups)  # Создание будущего dict of list
        for i in range(len(groups)):
            R[groups[i]] = [0] * len(quality)

        # Вспомогательная функция для быстрого определения позиций в листах
        def table_pos(groups, needle):
            for i in range(len(groups)):
                if groups[i] == needle:
                    return i

        for i in range(len(Table.index.codes[0])):
            #  взять key продукта и соотнести с позицией в groups
            G = table_pos(groups, Table.index.levels[
                          0][Table.index.codes[0][i]])

            #  взять key качества и соотнести с позицией в quality
            Q = table_pos(quality, Table.index.levels[
                          1][Table.index.codes[1][i]])

            #  записать в нужную ячейку инфомрацию
            R[groups[G]][Q] = Table[i]

        return R, quality
