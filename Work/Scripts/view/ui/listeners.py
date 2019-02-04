from abc import ABC, abstractmethod


class IChooserFrameListener(ABC):

    @abstractmethod
    def click_clear(self, event):
        pass

    @abstractmethod
    def click_default(self, event):
        pass


class ISettingsWindowListener(IChooserFrameListener):

    @abstractmethod
    def click_report(self, event):
        pass
