
from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self):
        """Observer updates by pulling data from Subject."""
        pass

    def registerSubject(self, subject):
        """Observer saves reference to Subject."""
        self.subject = subject

    def removeSubject(self):
        """Observer replaces Subject reference to None."""
        self.subject = None
