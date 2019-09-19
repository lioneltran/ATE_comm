from abc import ABC, abstractmethod


class Subject(ABC):
    @abstractmethod
    def registerObserver(self, observer):
        """Registers an observer with Subject."""
        pass

    @abstractmethod
    def removeObserver(self, observer):
        """Removes an observer from Subject."""
        pass

    @abstractmethod
    def notifyObservers(self):
        """Notifies observers that Subject data has changed."""
        pass
