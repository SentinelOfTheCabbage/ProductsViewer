from enum import Enum


class TableName(Enum):
    PRODUCTS = "Продукты"
    VOUCHERS = "Чеки"


class IColumnsName(Enum):
    pass


class VoucherColumns(IColumnsName):
    NAME = "Наименование"
    TOTAL = "Итого"


class ProductColumns(IColumnsName):
    NAME = "Наименование"
    PRICE = "Цена"
    PRODUCER_NAME = "Производитель"
    GROUP_NAME = "Группа продукта"
    DISCOUNT_NAME = "Скидка"
    QUALITY = "Категория качества"

    @staticmethod
    def get_empty_row():
        return {
            ProductColumns.NAME: None,
            ProductColumns.PRICE: None,
            ProductColumns.PRODUCER_NAME: None,
            ProductColumns.GROUP_NAME: None,
            ProductColumns.DISCOUNT_NAME: None,
            ProductColumns.QUALITY: None
        }
