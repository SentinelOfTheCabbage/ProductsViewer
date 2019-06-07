"""docstring_peryatin
"""
from enum import Enum


class TableName(Enum):
    """docstring_peryatin
    """
    PRODUCTS = "Products"
    VOUCHERS = "Vouchers"


class ProductsColumn(Enum):
    """docstring_peryatin
    """
    ID = "id"
    NAME = "name"
    PRICE = "price"
    PRODUCER_NAME = "producer_name"
    GROUP_NAME = "group_name"
    DISCOUNT_NAME = "discount_id"
    QUALITY = "quality"

    @staticmethod
    def get_columns():
        """docstring_peryatin
        """
        return [
            ProductsColumn.ID.value,
            ProductsColumn.NAME.value,
            ProductsColumn.PRICE.value,
            ProductsColumn.PRODUCER_NAME.value,
            ProductsColumn.GROUP_NAME.value,
            ProductsColumn.DISCOUNT_NAME.value,
            ProductsColumn.QUALITY.value
        ]


class VouchersColumn(Enum):
    """docstring_peryatin
    """
    ID = "id"
    DATE = "date"
    TIME = "time"
    TOTAL = "total"

    @staticmethod
    def get_columns():
        """docstring_peryatin
        """
        return [
            VouchersColumn.ID.value,
            VouchersColumn.DATE.value,
            VouchersColumn.TIME.value,
            VouchersColumn.TOTAL.value
        ]
