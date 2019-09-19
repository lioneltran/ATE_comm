# import logging
# import os
# class Log:
#
#     def __init__(self, minLevel=logging.INFO, fileOutput=True):
#         self._logger = logging.getLogger('nano')
#         self._logger.setLevel(logging.DEBUG)
#
#         self.setup()
#
#     def setup(self):
#
#         if os.path.isfile('/home/nano/ATE_comm/logs/nano_log.log'):
#             os.remove('/home/nano/ATE_comm/logs/nano_log.log')
#
#         # create a file handler
#         handler = logging.FileHandler('/home/nano/ATE_comm/logs/nano_log.log')
#         handler.setLevel(logging.DEBUG)
#
#         # create a logging format
#         # Sample color
#         # self._formatter = logging.Formatter("\033[31m%(asctime)s;%(levelname)-5s - %(filename)s %(funcName)s(%(lineno)d):  %(message)s\033[0m")
#         self._formatter = logging.Formatter("%(asctime)s;%(levelname)-5s - %(filename)s %(funcName)s(%(lineno)d):  %(message)s")
#         handler.setFormatter(self._formatter)
#
#         terminal_handler = logging.StreamHandler()
#         terminal_handler.setLevel(logging.DEBUG)
#         terminal_handler.setFormatter(self._formatter)
#
#         # add the handlers to the logger
#         self._logger.addHandler(handler)
#         self._logger.addHandler(terminal_handler)
#
#     def reset_handlers(self):
#         handlers = self._logger.handlers
#         for handler in handlers:
#             # Copied from `logging.shutdown`.
#             try:
#                 handler.acquire()
#                 handler.flush()
#                 handler.close()
#             except (OSError, ValueError):
#                 pass
#             finally:
#                 handler.release()
#             self._logger.removeHandler(handler)
#
#         self.setup()
#     # def terminateBackgroundLogger(self):
#     #     '''
#     #     :return:
#     #     '''
#     #     try:
#     #         # Timer to exit loop if timed out
#     #         exitTimerCount = 0
#     #
#     #         # drain the logger queue and close it
#     #         while not self._loggerQueue.empty() and exitTimerCount < SEC_30_TIMER:
#     #             time.sleep(0.001)
#     #             exitTimerCount += 1
#     #
#     #         self._loggerQueue.close()
#     #
#     #         if self._logOutputFileDescriptor:
#     #             self._logOutputFileDescriptor.flush()
#     #             self._logOutputFileDescriptor.close()
#     #
#     #         # kill the background logger queue listener process
#     #         self._backgroundLoggerProcess.terminate()
#     #         self._backgroundLoggerProcess = None
#     #
#     #         # deregister the log handlers - mandatory to ensure everything is cleaned up for next
#     #         # invocation of execute_scenario()
#     #         self._logger.removeHandler(self._conoleStreamHandler)
#     #         self._logger.removeHandler(self._loggerQueueHandler)
#     #
#     #     except Exception as e:
#     #         print(e)
#     #         raise
#
#
#     @property
#     def logger(self):
#         return(self._logger)
#
#     @logger.setter
#     def logger(self, val):
#         self._logger = val
#

import datetime
import gzip
import logging
import logging.handlers
import multiprocessing
import os
import time
import shutil

'''
Usage:  log = Log(); log.logger.info("")

'''

ATE_LOG_PATH = '/home/nano/ATE_comm/logs/'

# number of milliseconds in 30 seconds
SEC_30_TIMER = 30000

'''
The logging module directs all log outputs to registered handlers.  Each handler can be customized to output the log
string in any format and at any log level.

Two handlers supported now:  StreamHandler (to the console), QueueHandler (to the log file)

For the main ATE process, all logs will be output to the console handler at the INFO level.
For the logger process, all logs will be output to the log file at the DEBUG level.

The main ATE process file handler to output at the DEBUG level is optional.  Be aware that this will enable the file
logging within the main process incurring some application overhead.


To set up a handler and it's attributes, you need these calls:

    yourHandlerType = logging.HandlerType()     (HandlerType = Streaming, File, Queue,...)

    yourHandlerType.setLevel([DEBUG, INFO, WARNING, ERROR, CRITICAL])
    yourHandlerType.setFormatter(your logging.Formatter() setup)

    # register your handler with the logger module
    logger.addHandler(yourHandlerType)

'''


class Log:

    def __init__(self, minLevel=logging.INFO, fileOutput=True):
        '''
        Log class initializer to setup at a specific log level and file output preference
        A handler can be Stream (console), File, or Queue.  Each handler is sent the log message stream
        and has its own custom log formatter and log level to define its output.
        :param minLevel:    minimum log level preference
        :param fileOutput:  output logs to file preference
        '''
        self._logger = logging.getLogger('ate')
        self._minLevel = minLevel
        self._logger.setLevel(logging.DEBUG)

        self._currentDefaultLoggerLevel = self._logger.getEffectiveLevel()

        # create formatter
        self._formatter = logging.Formatter(
            "%(asctime)s;%(levelname)-5s - %(filename)s %(funcName)s(%(lineno)d):  %(message)s")

        self._fileOutputFlag = fileOutput

        # name of the logger output file
        self._pathname = ''

        # local logger fileHandler destination
        self._fileHandler = None

        self._consoleStreamHandler = None

        self._backgroundLoggerProcess = None
        self._logOutputFileDescriptor = None
        self._loggerQueue = None
        self._loggerQueueHandler = None

        # Default is to output logs to both the console and log file
        # if fileOutput:
        #     self.createLoggerFile()

    def resetLogLevel(self, logLevel):
        '''
        To reset the logger to a specific log level.
        :param logLevel: int
        :return:
        '''
        self._currentDefaultLoggerLevel = self._logger.getEffectiveLevel()

        # reset the queueHandler log level which streams logs to the process to write to log file
        self._loggerQueueHandler.setLevel(logLevel)
        # print("QueueHandler Current LogLevel - " + str(logLevel))

    def restoreDefaultLogLevel(self):
        '''
        Restores the logger to its default log level, everything on.
        :return:
        '''
        self._logger.setLevel(self._currentDefaultLoggerLevel)
        # print("Enable Current LogLevel - " + str(self._logger.getEffectiveLevel()))

    def createLoggerConsoleHandler(self, minLevel=logging.INFO):
        '''
        Configure the Python logger attributes to stream output to the console
        :return: None
        '''

        # create console handler and set level
        self._conoleStreamHandler = logging.StreamHandler()
        self._conoleStreamHandler.setLevel(minLevel)

        # add formatter with abbreviated log stream for the console
        formatter = logging.Formatter("%(asctime)s;%(levelname)-5s - %(message)s")
        self._conoleStreamHandler.setFormatter(formatter)

        # add console StreamHandler to logger
        self._logger.addHandler(self._conoleStreamHandler)

    def _generateLoggerFilename(self, directory, file=''):
        '''
        Create the complete pathname with the unique test logger filename
        :param file: optional filename
        :return: pathname to logger file
        '''

        # put here to circumvent circular import error dependencies
        # from tests.scenario import Scenario

        pathname = ''

        # Location of the ATE log files
        path = directory

        # Ensure that path exists.  If not, create it with default permissions
        if not os.path.exists(path):
            os.mkdir(path)

        # Use the custom filename if passed as param
        if file:
            pathname = path + file
        else:
            # Log filename to include DUT serial number and test start time
            # filename = 'ATE_{}-{}_{}_{}.log'.format(Scenario.ateTestAttr['station'],
            #                                         Scenario.ateTestAttr['stationIndex'],
            #                                         Scenario.ateTestAttr['internal_serial_number'],
            #                                         Scenario.ateTestAttr['testStartTime'])

            filename = 'ATE_Nano.log'
            pathname = path + filename

        return pathname

    def createLoggerFile(self, file='', logLevel=logging.DEBUG):
        '''
        Setup to write the logs to a file.  Already initialized to write to the console, and this
        will duplicate the same logs to a file; essentially streaming the logs to two places.
        Note - registers a fileHandler to write logs to a file in main ATE logger process
        :param file:          Use non-default filename
        :param logLevel:      Specify another log level besides DEBUG default
        :return: None
        '''

        self._pathname = self._generateLoggerFilename()

        # Setup output file using console output output format attributes
        self._fileHandler = logging.FileHandler(self._pathname)
        self._fileHandler.setLevel(logLevel)
        self._fileHandler.setFormatter(self._formatter)

        # logger is now setup to output to the file at the default application path
        self._logger.addHandler(self._fileHandler)

    def cleanupLogs(self, ageDaysOfLogsToDelete=30):
        '''
        Logging complete, time to cleanup by closing and compressing, and deleting the current log file
        Finally, delete all log files > 30 days old (default)
        This final cleanup method should be final step after controller.executeScenario() prior to exiting ATE
        :param:  ageOfLogsToDelete - int, in days
        :return: None
        '''
        try:
            # Timer to exit loop if timed out
            exitTimerCount = 0

            # drain the logger queue and close it
            while not self._loggerQueue.empty() and exitTimerCount < SEC_30_TIMER:
                time.sleep(0.001)
                exitTimerCount += 1

            self._loggerQueue.close()

            if self._logOutputFileDescriptor:
                self._logOutputFileDescriptor.flush()
                self._logOutputFileDescriptor.close()

            # kill the background logger queue listener process
            self._backgroundLoggerProcess.terminate()
            self._backgroundLoggerProcess = None

            # deregister the log handlers - mandatory to ensure everything is cleaned up for next
            # invocation of execute_scenario()
            self._logger.removeHandler(self._conoleStreamHandler)
            self._logger.removeHandler(self._loggerQueueHandler)

            # Did logger write the logs to an output file?
            if self._pathname:
                # Ensures logger file is closed and ready to compress
                if self._fileHandler:
                    self._fileHandler.close()

                # setup files for compression process
                # origFile = *.log, gzipFile = *.log.gz
                origFilename = self._pathname
                gzipFilename = self._pathname + '.gz'

                inFile = open(origFilename, 'rb')
                outFile = gzip.open(gzipFilename, 'wb')

                # Read all original log data and compress into gzip output file
                # Gzip will read and compress in this single command
                numBytesCompressed = outFile.write(inFile.read())

                inFile.close()
                outFile.close()

                # Did all log file data get compressed?
                if os.path.getsize(origFilename) != numBytesCompressed:
                    print('Error - input file size != gzip bytes read')
                else:
                    self.removeFile(origFilename)

                if self._fileHandler:
                    self._logger.removeHandler(self._fileHandler)

            # Now look to cleanup older logs to reduce filesysem usage
            convertedTodaysDate = datetime.date.fromtimestamp(time.time())

            os.chdir(ATE_LOG_PATH)

            # Search and delete logs > ageOfLogsToDelete (days) in AteExecutionLogs directory
            for file in os.listdir(ATE_LOG_PATH):
                fileDate = os.path.getmtime(file)
                convertedFileDate = datetime.date.fromtimestamp(fileDate)

                # Get number of days since file was created - a datetime.timedelta object
                fileAgeInDays = convertedTodaysDate - convertedFileDate

                # Clean up (remove) any files that are older than the specified age in days
                if (fileAgeInDays.days) >= ageDaysOfLogsToDelete:
                    self.removeFile(file)

        except Exception as e:
            print(e)
            raise

    def removeFile(self, filename):
        '''
        Delete a file specified at the full pathname.
        :param: fileaname: pathname string
        :return: None
        '''
        try:
            # Set permissions to allow all to delete the file
            os.chmod(filename, 0o777)
            os.remove(filename)
            # print('Deleted file - ' + filename)
        except Exception as e:
            print(e)
            raise

    def loggerQueueListenerProcess(self, queue, logOutputFD):
        '''
        The queue listener is a distinct Linux process from the main ATE process to offload the writing of log messages
        to a file in the background.   The idea is to off load the file logging overhead from the main ATE process.
        :param:  queue - multiprocessing.Queue type
        :param:  loggerOutputFD - output file descriptor
        :return: None
        '''

        # the logger process queue listener to manage getting messages from the log message queue
        self._queueListener = logging.handlers.QueueListener(queue)

        # print("Background Logger Process Started - {}, pid - {} ".format(self._backgroundLoggerProcess.name,
        #                                                       str(self._backgroundLoggerProcess.pid)))

        # Run forever blocking on listening for messages on the multiprocessing queue
        while True:
            # blocking call to wait for a message on the logger queue to handle
            logMessage = self._queueListener.dequeue(block=True)

            # format and output the LogRecord (logMessage) to the log file
            # using the logging formatter to just create the output log string for the file, not the log handler
            logOutputFD.write(self._formatter.format(logMessage) + '\n')
            logOutputFD.flush()

            # print('   logMesage Formatted = ' + self._formatter.format(logMessage))

    def startupTheLoggers(self, directory, mpQueue=None):
        '''
        Startup the console StreamHandler and the separate file logger process.
        :return: None
        '''

        # Init the corresponding console StreamHandler for every invocation of the logger process
        self.createLoggerConsoleHandler(self._minLevel)

        # create the logger process input queue; multiprocessing package takes care of reading the queue and
        # piping the log strings from main ATE process to the logger listener process via the loggerQueue
        self._loggerQueue = multiprocessing.Queue(0)

        self._pathname = self._generateLoggerFilename(directory)
        self._logOutputFileDescriptor = open(self._pathname, 'w')

        # this process should not exist, but delete in case the cleanupLogs() did not
        if self._backgroundLoggerProcess:
            self._backgroundLoggerProcess.terminate()

        self._backgroundLoggerProcess = multiprocessing.Process(name='ATELoggerListenerProcess',
                                                                target=self.loggerQueueListenerProcess,
                                                                args=(
                                                                self._loggerQueue, self._logOutputFileDescriptor,))
        self._backgroundLoggerProcess.start()

        # Initialize the logger QueueHandler to handle queued logging messages
        # logger entries written to the queue serviced by the logger's defined QueueHandler
        self._loggerQueueHandler = logging.handlers.QueueHandler(self._loggerQueue)
        self._loggerQueueHandler.setLevel(logging.DEBUG)
        self._loggerQueueHandler.setFormatter(self._formatter)

        # bind the QueueHandler with the logger framework
        self._logger.addHandler(self._loggerQueueHandler)

    def writeToLoggerQueue(self, logMessage):
        '''
        Write log messages to the multiprocessing queue which then pipes the message to the the
        queue listeners to handle.  FOR TEST ONLY.
        :param logMessage: string
        :return: None
        '''
        print("Sending - " + logMessage)
        # self._loggerQueue.put(logMessage)
        self._loggerQueueHandler.enqueue(logMessage)

    def zipAllLogs(self, directory):
        '''
        :param dir_name: File name directory
        :return:
        '''
        try:
            output_filename = directory
            shutil.make_archive(output_filename, 'zip', directory)

            # Remove unzip folder
            shutil.rmtree(directory)
        except Exception as e:
            print(e)
            raise

    def terminateBackgroundLogger(self):
        '''
        :return:
        '''
        try:
            # Timer to exit loop if timed out
            exitTimerCount = 0

            # drain the logger queue and close it
            while not self._loggerQueue.empty() and exitTimerCount < SEC_30_TIMER:
                time.sleep(0.001)
                exitTimerCount += 1

            self._loggerQueue.close()

            if self._logOutputFileDescriptor:
                self._logOutputFileDescriptor.flush()
                self._logOutputFileDescriptor.close()

            # kill the background logger queue listener process
            self._backgroundLoggerProcess.terminate()
            self._backgroundLoggerProcess = None

            # deregister the log handlers - mandatory to ensure everything is cleaned up for next
            # invocation of execute_scenario()
            self._logger.removeHandler(self._conoleStreamHandler)
            self._logger.removeHandler(self._loggerQueueHandler)

        except Exception as e:
            print(e)
            raise

    @property
    def logger(self):
        return (self._logger)

    @logger.setter
    def logger(self, val):
        self._logger = val

