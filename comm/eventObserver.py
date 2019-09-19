
from configuration import ateConfig
from utilities.observer import Observer


class EventObserver(Observer):
    '''
    Returns indicator of receipt of an asynchronous DUT event message.
    '''

    def __init__(self):
        self._gotEvent = False

    def update(self):
        '''
        Callback registered with and called by the eventSubject
        :return: None
        '''
        ateConfig.log.logger.info('   EventObserver- got event')
        self._gotEvent = True

    @property
    def gotEvent(self):
        return self._gotEvent

    @gotEvent.setter
    def gotEvent(self, state):
        self._gotEvent = state
