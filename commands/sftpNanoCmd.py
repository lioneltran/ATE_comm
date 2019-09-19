import sys
import traceback

from .command import Command
from configuration import ateConfig
from comm.sftpNano import SftpNano

'''
Serial commands to the device
Timeout ensures that we don't hang forever
As this is the lowest level code, all messaging is executed at the command level
'''


class SftpNanoCmd(Command):
    # class variable - serial application services shared by all Command instances
    # True = Serial Sim, False = Real Serial HW (default)
    # SerialApp is a singleton object
    _sftfNano = SftpNano()

    def __init__(self, cmd):
        '''
        Init method to to setup command instance attributes
        :param cmd: list, command attributes
        '''
        super().__init__()

        self._name = cmd['name']
        self._operation = cmd['operation']

        if self._operation == 'create_connection':
            self._host = cmd['host']
            self._port = cmd['port']
            self._username = cmd['username']
            self._password = cmd['password']

        if self._operation == 'put_file' or self._operation == 'get_file':
            self._localFilePath = cmd['localFilePath']
            self._remoteFilePath = cmd['remoteFilePath']

    def execute(self):
        '''
        Send command request to the DUT for execution
        :return: command response from DUT: byte list
        '''
        # Create observers prior to serial command execution
        ateConfig.log.logger.info('Executing command - ' + self._operation)

        try:
            if self._operation == 'create_connection':
                SftpNanoCmd._sftfNano.create_connection(self._host, self._port, self._username, self._password)

            if self._operation == 'put_file':
                SftpNanoCmd._sftfNano.put_file(self._localFilePath, self._remoteFilePath)

            if self._operation == 'get_file':
                SftpNanoCmd._sftfNano.get_file(self._remoteFilePath, self._localFilePath)

            if self._operation == 'close_connection':
                SftpNanoCmd._sftfNano.close_connection()

        except Exception as exc:
            ateConfig.log.logger.error(sys.exc_info())
            ateConfig.log.logger.error('\n'.join(traceback.format_stack()))
            message = 'Error message: ' + 'Operation: ' + self._operation+ ' | Info: ' + str(exc)
            return message