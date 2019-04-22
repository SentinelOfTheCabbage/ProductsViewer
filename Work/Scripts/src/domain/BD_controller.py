# -*- coding: utf-8 -*-

""" PyLinter Sublime Text Plugin

    This is a Pylint plugin for Sublime Text.

    Copyright R. de Laat, Elit 2011-2013

    For more information, go to https://github.com/biermeester/Pylinter#readme
"""
import os
import pandas
os.chdir('C:/Users/Tom/Documents/Python_projects/ProductsViewer/Work/Data')


class db_controller():

    def __init__(self):
        file_name = 'database.txt'
        with open(file_name) as file:
            self._db_list = [row.strip() for row in file]
        for i in range(len(self._db_list)):
            attr_name = self._db_list[i].strip('csv')
            attr_name = attr_name.strip('.')
            attr_name = 'DB_' + attr_name
            data = pandas.read_csv(self._db_list[i], sep=';')
            setattr(self, attr_name, data)
            pattern_name = self._db_list[i].strip('csv')
            pattern_name = pattern_name.strip('.')
            pattern_name = pattern_name + '_pattern'
            setattr(self, pattern_name, [])
            for j in range(len(data.iloc[0])):
                exec('%s.append(%s)' % ('self.' + pattern_name, 'type(1)' if str(
                    type(data.iloc[1][j])) == "<class 'numpy.int64'>" else 'type("a")'))
            del data

    def check_input(self, new_walues: list, destination: str):
        """Lolkek
        """
        pattern_name = 'self.' + destination + '_pattern'
        loyalty = True
        status = 'good'
        msg = ''
        self.current_file = []
        exec('%s=%s' % ('self.current_file', pattern_name))
        if len(new_walues) == len(self.current_file):
            for i in range(len(self.current_file)):
                if self.current_file[i] != type(new_walues[i]):
                    loyalty = False
                    msg = 'incompatible types of variable on ' + \
                        str(i + 1) + ' position. Need ' + str(
                            self.current_file[i]) + ' but ' + str(type(new_walues[i])) + ' given'
                    status = 'error'
                    break
            if loyalty is True:
                print('GJ!')
        else:
            msg = 'Bad len of new element. Need ' + \
                str(len(self.current_file)) + ' but just ' + \
                str(len(new_walues)) + ' given'
            status = 'warning'

        return [status, msg]
