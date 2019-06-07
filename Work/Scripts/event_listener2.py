from abc import ABC, abstractmethod

from Work.Scripts.db_event import Event


class IEventListener(ABC):

    @abstractmethod
    def notify(self, event: Event):
        pass
