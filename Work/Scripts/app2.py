
class App:
    __instance = None

    @staticmethod
    def getInstance():
        if App.__instance is None:
            App.__instance = App()

        return App.__instance

    def __init__(self):
        if App.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            App.__instance = self

