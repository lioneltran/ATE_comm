

from abc import ABC, abstractmethod
import time

from commands.commandFactory import CommandFactory
from configuration import ateConfig


class Test(ABC):
    '''
    Abstract Base Test class.  Derive to create component specific test class
    Mandatory that setup() and execute() be implemented in derived class
    '''
    def __init__(self, setup):
        self._name = setup['name']
        self._component = setup['component']
        self._configuraton = []
        self._cmdFactory = CommandFactory()
        self._cmdList = []
        self._commands = setup['commands']
        self._testResult = dict(name=self._name, passed=False, startTime=0, duration=0, data='', cmdResults=[])

        # test start time in unix epochs
        self._testResult['startTime'] = time.time()

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    def calcTestDuration(self, startTime):
        '''
        Common method to all Test instances to calculate the test execution time
        :param startTime:
        :return:
        '''
        duration = time.time() - startTime
        self._testResult['duration'] = duration
        ateConfig.log.logger.info('   Test duration (epochs) = ' + str(duration))
        return duration

    def createTestCmdObjects(self):
        '''
        Create each command object ready to execute the whole test
        :return: None
        '''
        for cmd in self._commands:
            # create the new Cmd object
            tempCmdObject = self._cmdFactory.createCmdObject(cmd)

            # support list of handle values each of which is associated with a separate commmand object
            # for example, setup characteristcs command uses a value list
            if isinstance(tempCmdObject.message.handle, list):
                handleList = tempCmdObject.message.handle
                #newCmd = cmd

                # Create each command with a distinct value from the list
                for handle in handleList:
                    cmdObject = self._cmdFactory.createCmdObject(cmd)
                    cmdObject.message.handle = handle

                    self._cmdList.append(cmdObject)
                    ateConfig.log.logger.info("Created newCmd - " + str(cmdObject))
            else:
                #cmdObject = self._cmdFactory.createCmdObject(cmd)
                self._cmdList.append(tempCmdObject)
                ateConfig.log.logger.info("Created cmd - " + str(cmd))

    @property
    def name(self):
        return self._name

    @property
    def component(self):
        return self._component
