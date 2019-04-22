# -*- coding: utf-8 -*-

""" PyLinter Sublime Text Plugin

    This is a Pylint plugin for Sublime Text.

    Copyright R. de Laat, Elit 2011-2013

    For more information, go to https://github.com/biermeester/Pylinter#readme
"""
import pickle
import os
import pandas
os.chdir('C:/Users/Tom/Documents/Python_projects/ProductsViewer/Work/Data')


class DbRedactor:
    """LOL!
    """
    def __init__(self):
        with open('db.pickle', "rb") as db_from_pickle:
            self.database = pickle.load(db_from_pickle)
        self.db_list = list(self.database.keys())
            # for i in range(len(data))

    def delete_element(self, source: str, target: int):
        """LOL!
        """
        return None
        # i, database_name = self.find_current_db(source)
        # database_name = 'DB_' + database_name
        # setattr(self, database_name, pandas.read_csv(self.db_list[i], sep=';'))
        # exec('self.%s=self.%s.drop(%d)' %
        #      (database_name, database_name, target))
        # exec('self.%s.to_csv("%s.csv",index=True,sep=";")' % (database_name, source))
        # exec('del(self.%s)' % (database_name))

    def edit_element(self, source: str, target: int, point: int, new_value):
        """LOLA!
        """
        # i, database_name = find_corrent_db(source)
        return None

    def create_element(self):
        """LOLLA!
        """
        return None

    def find_current_db(self, current_db_name: str):
        """ALSFDS
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
        else:
            return False
