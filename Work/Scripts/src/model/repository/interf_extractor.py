from abc import ABC, abstractmethod


class IDataExtractor(ABC):

    @abstractmethod
    def get_data(self):
        pass
