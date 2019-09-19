
import sys
import time
import traceback

from comm.ateSerialUtil import *
from comm.serialApp import SerialApp
from .command import Command
from configuration import ateConfig
from comm.dataObserver import DataObserver
from comm.responseObserver import ResponseObserver


'''
Serial commands to the device
Timeout ensures that we don't hang forever
As this is the lowest level code, all messaging is executed at the command level
'''

# Multiply this value by 5 mSecs to derive timeout period in secconds
SERIAL_TIMEOUT = 200


class SerialCmd(Command):
    # class variable - serial application services shared by all Command instances
    # True = Serial Sim, False = Real Serial HW (default)
    # SerialApp is a singleton object
    serial = SerialApp.Instance()

    def __init__(self, cmd):
        '''
        Init method to to setup command instance attributes
        :param cmd: list, command attributes
        '''
        super().__init__()

        self._cmd = cmd
        self._messageType = cmd['messageType']
        self._commandId = cmd['commandId']
        self._componentId = cmd['componentId']
        self._name = cmd['name']
        self._timeout = int(cmd['timeout'])
        self._type = cmd['type']
        self._feedbackData = cmd['feedbackData']
        self._cmdResult = {}
        self._cmdResult['name'] = cmd['name']

    def _setupObservers(self):
        '''
        Set the observers only prior to executing the serial command, not on SerialCmd instantiation
        :return: None
        '''
        # setup the subject/observer for the ack responses to ATE commands
        self._respObserver = ResponseObserver()
        self._respSubject = SerialCmd.serial.respSubject
        self._respObserver.registerSubject(self._respSubject)
        self._respSubject.registerObserver(self._respObserver)

        # setup the subject/observer for the DUT data responses
        self._dataObserver = DataObserver()
        self._dataSubject = SerialCmd.serial.dataSubject
        self._dataObserver.registerSubject(self._dataSubject)
        self._dataSubject.registerObserver(self._dataObserver)

    def _cleanupObservers(self):
        # clean up this instance's observer objects
        if self._dataObserver:
            self._dataSubject.removeObserver(self._dataObserver)

        if self._respObserver:
            self._respSubject.removeObserver(self._respObserver)
            
        self._contThread = False

    def execute(self):
        '''
        Send command request to the DUT for execution
        :return: command response from DUT: byte list
        '''
        # Create observers prior to serial command execution
        self._setupObservers()

        ateConfig.log.logger.info('Executing command - ' + self._messageType)

        try:
            # Send the DUT request command and then wait for the response to ensure
            # we get it in a reasonable time
            if self._messageType == 'Ping':
                SerialCmd.serial.sendRequest(int(ATE_PING_MSG_ID), int(self._componentId), int(self._commandId))

            elif self._messageType == 'Request':

                if self._componentId == ateConfig.componentID['HT_FILE_TRANSFER']:
                    SerialCmd.serial.sendFileTransferRequest(self._cmd)
                else:
                    SerialCmd.serial.sendRequest(int(ATE_REQ_MSG_ID), int(self._componentId), int(self._commandId), self._payload)

            elif self._messageType == 'Wait':
                pass
            else:
                ateConfig.log.logger.error('   Invalid command - ' + self._messageType)
                return None

            # Configurable timeout in ticks from the command attributes
            respTimeout = self._timeout * SERIAL_TIMEOUT

            # Default - Always wait command timeout period for the returned ack response
            timer = 0
            ateConfig.log.logger.debug('message type: ' + self._messageType)
            while (self._respObserver.gotAck == False) and (timer < respTimeout) and self._messageType != 'Wait':# and (self._messageType != 'Request'):
                time.sleep(MSECS_5)
                timer += 1

            # if expected, wait for the asynchronous DUT feedback data message
            if (self._messageType == 'Request' or self._messageType == 'Wait') \
                    and self._feedbackData and self._respObserver.gotAck:
                timer = 0
                while (self._dataObserver.gotData == False) and (timer < respTimeout):
                    time.sleep(MSECS_5)
                    timer += 1

            # Success if we got a DUT response message
            self._cmdResult['data'] = ''
            if (self._dataObserver.gotData or self._respObserver.gotAck):
                msg = '[' + ', '.join('0x{:02X}'.format(x) for x in SerialCmd.serial.lastResponseMessage) + ']'
                ateConfig.log.logger.debug('   DUT Msg Received - %s' % msg)

                # log the DUT test results
                self._cmdResult['passed'] = True

                if self._messageType == 'Ping':
                    self._cmdResult['msg'] = 'Ping Success!!'

                elif self._messageType == 'Request' or self._messageType == 'Wait':
                    if self._messageType == 'Wait':
                        ateConfig.log.logger.info('GOT WAIT MESSAGE')

                    if self._feedbackData:
                        self._cmdResult['data'] = self.getResponseBody(SerialCmd.serial.lastResponseMessage)
                        SerialCmd.serial.lastResponseMessage = []

                    self._cmdResult['msg'] = 'Request Success!!'

            else:
                # log it
                self._cmdResult['passed'] = False
                self._cmdResult['msg'] = 'ABORT - No Serial Status Response'
                ateConfig.log.logger.error('No DUT test status response')

        except Exception as exc:
            ateConfig.log.logger.error(sys.exc_info())
            ateConfig.log.logger.error('\n'.join(traceback.format_stack()))
            self._cmdResult['passed'] = False

        self._cleanupObservers()
        return self._cmdResult

    def getResponseBody(self, respMessage):
        '''
        Extract any bytes from the message body, if any
        :param respMessage:
        :return: message body data
        '''
        # Messages have min of 5 bytes, anything more indicates messsage body bytes
        if len(respMessage) > 5:
            strData = ''.join(str(chr(data)) for data in respMessage[5:-4])
            return strData
        else:
            return ''


    @property
    def feedbackData(self):
        return self._feedbackData