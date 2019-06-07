"""Author: Suleymanov Nail
Отключены следующие ошибки pylint:
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)
"""
# pylint: disable=E0401
# -*- coding: utf-8 -*-
import os
import pickle

from Work.Scripts.conf import ROOT_DIR

os.chdir(ROOT_DIR + '/Work/Data')


class DbRedactor:
    """Author: Suleymanov Nail
    Класс для редактирования Базы данных
    """

    def __init__(self):
        with open('db.pickle', "rb") as db_from_pickle:
            self.database = pickle.load(db_from_pickle)
        self.db_list = list(self.database.keys())

    # def delete_element(self, source: str, target: int):
    #     """Author: Suleymanov Nail
    #     Функция удаляет элемент в таблице
    #     """
    #     i, database_name = self.find_current_db(source)
    #     database_name = 'DB_' + database_name
    #     setattr(self, database_name, pandas.read_csv(self.db_list[i], sep=';'))
    #     exec('self.%s=self.%s.drop(%d)' %
    #          (database_name, database_name, target))
    #     exec('self.%s.to_csv("%s.csv",index=True,sep=";")' % (database_name, source))
    #     exec('del(self.%s)' % (database_name))
    #     return None

    def edit_element(self, source: str, target: int, point: int, new_value):
        """Author: Suleymanov Nail
        Функция редактирует элемент в таблице
        """
        # i, database_name = find_corrent_db(source)

    def create_element(self):
        """Author: Suleymanov Nail
        Функция создаёт элемент в таблице
        """

    def find_current_db(self, current_db_name: str):
        """Author: Suleymanov Nail
        Функция находит database по заданному имени файла.
        """
        flag = False
        for i in range(len(self.db_list)):
            database_name = self.db_list[i].strip('csv')
            database_name = database_name.strip('.')
            if current_db_name == database_name:
                flag = True
                break
        if flag is True:
            return i, database_name
        return False
