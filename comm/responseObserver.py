
from configuration import ateConfig
from utilities.observer import Observer

class ResponseObserver(Observer):
    '''
    Returns the got DUT ack response to the latest ATE command
    '''
    def __init__(self):
        self._gotAck = False

    def update(self):
        '''
        Callback registered witht the ack/nack responseSubject
        :return: None
        '''
        if ateConfig.log._fileOutputFlag == True:
            ateConfig.log.logger.debug('   ResponseObserver- got ack')
        self._gotAck = True
        
    @property
    def gotAck(self):
        return self._gotAck