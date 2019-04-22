from Work.Scripts.src.model.commands import CommandSelect, CommandInsert, \
    CommandUpdate, CommandDelete


class MainTableInteractor:
    def __init__(self):
        pass

    def get_data(self, row_filter, column_filter):
        data = [
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Ласт"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
             "Андрей",
             "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Ласт"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
             "Андрей",
             "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Ласт"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
             "Андрей",
             "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Ласт"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
             "Андрей",
             "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Сулейманов"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Ласт", "Ласт", "Ласт", "Ласт", "Ласт", "Ласт",
             "Ласт",
             "Ласт", "Ласт", "Ласт", "Ласт", "Ласт", "Ласт",
             "Ласт",
             "Ласт", "Ласт"]
        ]
        return data

    def get_columns_by_table(self, table):
        data = []
        if table == "Продукты":
            data = []
        elif table == "Чеки":
            data = []
        return data

    def select(self, command_select: CommandSelect):
        print(command_select)

    def insert(self, command_insert: CommandInsert):
        print(command_insert)

    def update(self, command_update: CommandUpdate):
        print(command_update)

    def delete(self, command_delete: CommandDelete):
        print(command_delete)
