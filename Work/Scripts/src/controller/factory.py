from abc import ABC, abstractmethod

import Work.Scripts.src.model.repository.extractor as prod
import Work.Scripts.src.test.extractor as test


class IDBFactory(ABC):
    @abstractmethod
    def create_table_extractor(self):
        pass


class ProdDbFactory(IDBFactory):
    def create_table_extractor(self):
        return prod.DataExtractor()


class TestDbFactory(IDBFactory):
    def create_table_extractor(self):
        return test.DataExtractor()
