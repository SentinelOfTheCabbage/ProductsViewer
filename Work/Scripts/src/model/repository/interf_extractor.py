from abc import ABC, abstractmethod


class IDataExtractor(ABC):

    @abstractmethod
    def get_db_products(self):
        pass

    @abstractmethod
    def get_db_discounts(self):
        pass

    @abstractmethod
    def get_db_vouchers(self):
        pass

    @abstractmethod
    def get_db_sales(self):
        pass

    @abstractmethod
    def get_db_groups(self):
        pass
