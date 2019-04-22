from abc import ABC, abstractmethod

from Work.Scripts.src.presentation.presenters.db_event import Event


class IEventListener(ABC):

    @abstractmethod
    def notify(self, event: Event):
        pass
