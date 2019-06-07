from enum import Enum


class TableNameUI(Enum):
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
            ProductColumns.NAME.value: None,
            ProductColumns.PRICE.value: None,
            ProductColumns.PRODUCER_NAME.value: None,
            ProductColumns.GROUP_NAME.value: None,
            ProductColumns.DISCOUNT_NAME.value: None,
            ProductColumns.QUALITY.value: None
        }
