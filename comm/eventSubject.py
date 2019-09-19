
from configuration import ateConfig
from utilities.subject import Subject

################################################################################
# Concrete Subject class - DUT Event Message receivied
################################################################################
class EventSubject(Subject):
    def __init__(self):
        self._observerList = []

    def registerObserver(self, observer):
        '''
        Registers an observer if the observer is not already registered.
        :param observer: 
        :return: None
        '''
        
        try:
            if observer not in self._observerList:
                self._observerList.append(observer)
                observer.registerSubject(self)
            else:
                raise ValueError
        except ValueError:
            ateConfig.log.logger.error("ERROR: Observer already subscribed to Subject!")
            raise ValueError

    def removeObserver(self, observer):
        '''
        Removes an observer if the observer is currently subscribed.
        :param observer: 
        :return: None
        '''
        try:
            if observer in self._observerList:
                observer.removeSubject()
                self._observerList.remove(observer)
            else:
                raise ValueError
        except ValueError:
            ateConfig.log.logger.error("ERROR: Observer currently not subscribed to Subject!")
            raise ValueError

    def notifyObservers(self):
        '''
        Notifies subscribed observers if received event message.
        :return: None
        '''
        for observer in self._observerList:
            ateConfig.log.logger.info('   EventSubject - notify observers')
            observer.update()