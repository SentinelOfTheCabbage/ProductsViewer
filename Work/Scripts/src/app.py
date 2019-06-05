"""
"""
import pickle


class App:
    """
    """
    __instance = None

    def get_database(self):
        database = None
        with open('db.pickle', 'rb') as db_pickle:
            database = pickle.load(db_pickle)
        database = database['_db_products']
        return database

    @staticmethod
    def getInstance():
        """
        """
        if App.__instance is None:
            App.__instance = App()

        return App.__instance

    def __init__(self):
        """
        """
        if App.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            App.__instance = self
