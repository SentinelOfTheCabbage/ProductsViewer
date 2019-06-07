"""
Модуль содержащий слушатели
Автор: Перятин Виталий
Отключены следующие ошибки pylint:
    E0401 - Ошибка экспорта (данный модуль не знает о переназначении папок)
    R0903 - Ошибка количества методов в классе
"""
# pylint: disable=E0401
# pylint: disable=R0903

from abc import ABC, abstractmethod
from Work.Scripts.db_event import Event


class IEventListener(ABC):
    """
    Слушатель событий

    Автор: Перятин Виталий
    """
    @abstractmethod
    def notify(self, event: Event):
        """docstring_peryatin
        """
