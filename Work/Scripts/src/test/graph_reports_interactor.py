# Метод/функция для получения средних цен по выбранным категориям
# продуктов и выбранному качеству
import random


class ReportsInteractor:

    def __init__(self):
        pass

    def get_prices_by_group_and_quality(self, groups: list, quality: list):
        data = {}
        for group in groups:
            data[group] = [random.randint(10, 100) for _ in
                           range(len(quality))]
        return data

    def get_prices_by_group(self, product_group: str, products: list):
        data = [random.randint(10, 100) for _ in range(len(products))]
        return data

    def get_box_and_whisker_prices(self, product_group: str, qualities: list,
                                   products: list):
        data = {}
        for quality in qualities:
            data[quality] = [random.randint(10, 100) for _ in range(20)]
        print(data)
        return data

    def get_spreading(self, product_group: str, date: str):

        def get_random_point():
            return {
                'price': random.randint(10, 100),
                'amount': random.randint(10, 100)
            }

        data = [get_random_point() for _ in range(20)]
        return data

    def get_products_groups(self):
        data = ["Ягоды", "Картошка", "Зёрна",
                "Мясо", "Для беременных",
                "Деликатесы",
                "Птица", "Рыба", "Хлеб",
                "Молочное", "Овощи",
                "Фрукты и ягоды"]
        return data

    def get_quality_categories(self):
        data = ["ГОСТ", "СТО", "ТУ"]
        return data

    def get_products_by_group(self, group: str):
        data = ["Молоко 'М'", "Молоко 'Простоквашино' ",
                "Кефир 'Домик в деревне'", "Творог 'Домик в деревне' "]
        return data
