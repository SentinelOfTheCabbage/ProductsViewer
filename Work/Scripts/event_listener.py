"""
Модуль содержащий слушатели

Автор: Перятин Виталий
"""

from abc import ABC, abstractmethod
from Work.Scripts.db_event import Event


class IEventListener(ABC):
    """
    Слушательь событий

    Автор: Перятин Виталий
    """
    @abstractmethod
    def notify(self, event: Event):
        pass
