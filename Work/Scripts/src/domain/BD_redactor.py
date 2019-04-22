import os
import pandas

os.chdir('C:/Users/ирбисик/Documents/PYTHON/ProductsViewer/Work/Data')


class DB_Redactor():

    def __init__(self):
        file_name = 'database.txt'
        with open(file_name) as file:
            self.DB_List = [row.strip() for row in file]
            # for i in range(len(data))

    def delete_element(self, source: str, target: int):
        i, database_name = self.find_current_db(source)
        database_name = 'DB_' + database_name
        setattr(self, database_name, pandas.read_csv(self.DB_List[i], sep=';'))
        exec('self.%s=self.%s.drop(%d)' %
             (database_name, database_name, target))
        exec('self.%s.to_csv("%s.csv",index=True,sep=";")' % (
            database_name, source))
        # exec('del(self.%s)' % (database_name))

    def edit_element(self, source: str, target: int, point: int, new_value):
        i, database_name = self.find_corrent_db(source)
        pass

    @staticmethod
    def create_element():
        pass

    def find_current_db(self, current_db_name: str):
        flag = False
        for i in range(len(self.DB_List)):
            database_name = self.DB_List[i].strip('csv')
            database_name = database_name.strip('.')
            if current_db_name == database_name:
                flag = True
                break
        if flag:
            return i, database_name
        else:
            return False
