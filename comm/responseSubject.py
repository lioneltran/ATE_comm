
from configuration import nanoConfig
from utilities.subject import Subject

################################################################################
# Concrete Subject class - For Serial Data Response messages
################################################################################
class ResponseSubject(Subject):
    def __init__(self):
        self._observerList = []

    def registerObserver(self, observer):
        '''
        Registers an observer with  if the observer is not already registered.
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
            nanoConfig.log.logger.error("ERROR: Observer already subscribed to Subject!")
            raise ValueError

    def removeObserver(self, observer):
        '''
        Removes an observer from  if the observer is currently subscribed to Serial Data.        
        :param observer 
        :return: None
        '''
        try:
            if observer in self._observerList:
                observer.removeSubject()
                self._observerList.remove(observer)
            else:
                raise ValueError
        except ValueError:
            nanoConfig.log.logger.error("ERROR: Observer currently not subscribed to Subject!")
            raise ValueError

    def notifyObservers(self):
        '''
        Notifies subscribed observers of DUT Ack response received.        
        :return: None
        '''
        for observer in self._observerList:
            nanoConfig.log.logger.debug('   ResponseSubject - notify observers')
            observer.update()

