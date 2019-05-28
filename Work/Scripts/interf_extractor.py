from abc import ABC


class IDataExtractor(ABC):
    _db_products: dict
    _db_discounts: dict
    _db_vouchers: dict
    _db_sales: dict
    _db_groups: dict
