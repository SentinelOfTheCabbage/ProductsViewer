# Метод/функция для получения средних цен по выбранным категориям
# продуктов и выбранному качеству
import random


class ReportsInteractor:

    def __init__(self):
        pass

    def get_prices_by_group_and_quality(self, groups: list, quality: list):
        data = {}
        for group in groups:
            data[group] = [random.randint(10, 100) for _ in range(len(quality))]
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
        pass

