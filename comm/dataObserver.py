
from configuration import nanoConfig
from utilities.observer import Observer

class DataObserver(Observer):
    '''
    Returns an event flag of the data being observed.  In this case, it is the 
    DUT data message has been received.
    '''
    def __init__(self):
        self._gotData = False

    def update(self):
        '''
        Callback registered with and called by the dataSubject
        :return: None
        '''
        nanoConfig.log.logger.debug('   DataObserver - got data')
        self._gotData = True
        
    @property
    def gotData(self):
        return self._gotData


