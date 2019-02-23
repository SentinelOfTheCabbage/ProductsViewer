from abc import ABC, abstractmethod

from Work.Scripts.src.controller.db_event import Event


class IEventListener(ABC):

    @abstractmethod
    def notify(self, event: Event):
        pass
