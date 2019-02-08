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

    def close():
        '''
        close()
        Try to close document
        '''
        pass

    def arithmetic_mean_list(self, groups: list, quality: list):
        '''
        output (groups:list,quality: list)
        return arithmetic mean list
        list={
            {   group1_quality1,
                group1_quality2
            },
            {   group2_quality1,
                qroup2_quality2
            },
            ...
        }
        '''

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
            # необходимо удалить лишние параметры качества!
        return Table

        '''
        __dict = dict.fromkeys(groups)
        __arithm_mean = dict.fromkeys(groups)

        for i in range(len(groups)):
            __dict[groups[i]] = dict.fromkeys(quality, [])
            __arithm_mean[groups[i]] = dict.fromkeys(quality, 0)

            for j in range(len(quality)):
                result = []
                summ = 0
                div = 0
                for k in range(len(Prod_List)):

                    if (Prod_List.iloc[k].group_name == groups[i]) and (Prod_List.iloc[k].quality == quality[j]):
                        summ += Prod_List.iloc[k].price
                        div += 1
                if div != 0:
                    __arithm_mean[groups[i]][quality[j]]=summ / div
                else:
                    __arithm_mean[groups[i]][quality[j]]=0

        return __arithm_mean
        '''
# B.groupby('group_name').describe()
