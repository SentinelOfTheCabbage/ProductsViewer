from Work.Scripts.src.presentation.presenters.stack import Stack


class App:
    __instance = None
    saved_states = Stack(10)

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

