import os
import pandas
os.chdir('C:/Users/ирбисик/Documents/PYTHON/ProductsViewer/Work/Data')


class DB_controller():

    def __init__(self):
        file_name = 'database.txt'
        with open(file_name) as file:
            self.DB_List = [row.strip() for row in file]
        for i in range(len(self.DB_List)):
            attr_name = self.DB_List[i].strip('csv')
            attr_name = attr_name.strip('.')
            attr_name = 'DB_' + attr_name
            data = pandas.read_csv(self.DB_List[i], sep=';')
            setattr(self, attr_name, data)
            pattern_name = self.DB_List[i].strip('csv')
            pattern_name = pattern_name.strip('.')
            pattern_name = pattern_name + '_pattern'
            setattr(self, pattern_name, [])
            for i in range(len(data.iloc[0])):
                exec('%s.append(%s)' % ('self.' + pattern_name, 'type(1)' if str(
                    type(data.iloc[1][i])) == "<class 'numpy.int64'>" else 'type("a")'))
            del(data)

    def check_input(self, new_walues: list, destination: str):
        pattern_name = 'self.' + destination + '_pattern'
        loyalty = True
        status = 'good'
        msg = ''
        exec('%s=%s' % ('self.current_file', pattern_name))
        if len(new_walues) == len(self.current_file):
            for i in range(len(self.current_file)):
                if self.current_file[i] != type(new_walues[i]):
                    loyalty = False
                    msg = 'incompatible types of variable on ' + str(i + 1) + ' position. Need ' + str(
                        self.current_file[i]) + ' but ' + str(type(new_walues[i])) + ' given'
                    status = 'error'
                    break
            if loyalty == True:
                print('GJ!')
        else:
            msg = 'Bad len of new element. Need ' + \
                str(len(self.current_file)) + ' but just ' + \
                str(len(new_walues)) + ' given'
            status = 'warning'

        return [status, msg]
