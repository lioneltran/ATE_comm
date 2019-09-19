
from abc import ABC, abstractmethod


'''
Commands to the device
Timeout ensures that we don't hang forever
As this is the lowest level code, all messaging is executed at the command level
'''

class Command(ABC):

    def __init__(self):
        '''
        Init method to to setup command instance attributes
        :param cmd: list, command attributes
        '''
        self._id = ''
        self._name = ''
        self._type = ''
        self._component = ''
        self._timeout = 0
        self._postCmdDelay = 0
        self._cmdResult = ''
        self._operation = ''
        self._pinName = ''
        self._value = ''
        self._payload = None
    
    @abstractmethod
    def execute(self):
        pass

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newId):
        self._id = newId
    
    @property
    def type(self):
        return self._type
    
    @property
    def name(self):
        return self._name
    
    @property
    def component(self):
        return self._component
    
    @property
    def timeout(self):
        return self._timeout
    
    @property
    def operation(self):
        return self._operation
    
    @property
    def pinName(self):
        return self._pinName

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, newValue):
        self._value = newValue

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, newPayload):
        self._payload = newPayload