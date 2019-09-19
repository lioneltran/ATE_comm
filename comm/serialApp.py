import struct
from utilities.singleton import Singleton

from .serialComm import *
from utilities.myThread import MyThread
from comm.ateSerialUtil import *
from comm.dataSubject import DataSubject
from comm.responseSubject import ResponseSubject

from configuration.ateConfig import *
from comm.sftpNano import SftpNano
'''
Serial Application class provides an interface to the underlying serial port services.  Applications 
should not use the serial port services directly in case there are future changes to this interface.
Singleton object to ensure that only one SerialApp and SerialComm objects are created
'''

FILE_TRANSFER_HEADER_MSG_ID = 0x2A
FILE_TRANSFER_DATA_MSG_ID = 0x2B
FILE_TRANSFER_COMPLETE_MSG_ID = 0x2C

@Singleton
class SerialApp:
    def __init__(self, testMode=False):
        '''
        Init method to initialize the serial comm port services and object attributes.
        :param testMode: boolean, defaults to False for factory test mode.
        '''
        # should only be a single message in this queue at any time
        self.rxMessageAppQ = queue.Queue(5)
        self._serialComm = SerialComm(self.rxMessageAppQ, testMode)
        self._sftpComm = SftpNano()
        self._sftpComm.create_connection(REMOTE_IP, REMOTE_PORT, REMOTE_USERNAME, REMOTE_PASSWORD)

        self._message = []
        self._txMessage = []

        self._lastMessageSent = 0
        self._continue = True
        self.lastResponseMessage = []

        # Create the DUT ack response event subject
        self._respSubject = ResponseSubject()

        # Create the DUT data response event subject
        self._dataSubject = DataSubject()

        self._fileReceived = {}
        self._fileToSend = {}

        self._startProcessingImages = False
        self._restartController = False

        '''
        Status of 4 vision tests:
        - 0: Did not receive request
        - 1: Received request
        - 2: Started, In progress
        - 3: Done 
        '''
        self._handDragTestNanoStatus = 0
        self._circlesConcentricityTestATE3NanoStatus = 0
        self._eInkDeadPixelTestATE3NanoStatus = 0
        self._LEDUniformingTestATE3NanoStatus = 0

        if not testMode:
            # startup the rx app message queue processing thread
            self._rxAppQThread = MyThread(31, 'AppRxQueueThread', 2, self.processRxQueueThread)
            self._rxAppQThread.start()

    def processRxQueueThread(self):
        '''
        Background application thread to process any queued incoming test status and heartbeat messages
        serialComm Rx thread puts messages in this app queue
        :return: none
        '''
        ateConfig.log.logger.debug("Starting App processRxQueueThread")

        # Wait almost forever loop for messages on the application Rx queue.
        # Exits when the continue flag is False for orderly thread shutdown
        while self._continue:
            # Delay allows thread to periodically sleep and not "hog the system"
            time.sleep(USECS_100)

            # When message in queue, set the received flag for application to handle
            if not self.rxMessageAppQ.empty():
                msg = self.rxMessageAppQ.get()

                if msg[0] == DUT_HB_MSG_ID:
                    ateConfig.log.logger.debug('   SerialApp - DUT Heartbeat Status, Sequence Num: ' + msg[1])

                elif msg[0] == ACK_MSG_ID:
                    # Get ack to indicate command/ack is successful
                    # self.lastResponseMessage = []
                    self._respSubject.notifyObservers()

                elif msg[0] == DUT_STATUS_MSG_ID or msg[0] == DUT_FILE_TRANSFER_STATUS_MSG_ID:
                    # logger.info( 'SerialApp - ATE Rx Queue Message: ' + message  + ", Hex: " + message.encode('hex'))
                    msgHex = '[' + ', '.join('0x{:02X}'.format(x) for x in msg) + ']'
                    ateConfig.log.logger.debug('   SerialApp - ATE RxQueue Message: %r' % msgHex)

                    # serialComm puts a validated message on the rxMessageQ, now go handle it
                    self.lastResponseMessage = msg
                    self._dataSubject.notifyObservers()

                elif msg[0] == ATE_REQ_MSG_ID:
                    ateConfig.log.logger.debug(
                        "Got request msg from Pi: compId: %s, cmdId: %s" % (msg[3], msg[4]))

                    self.processRequest(msg)

                else:
                   ateConfig.log.logger.debug('   SerialApp - Invalid Message ID: ' + str(msg[0]))
            '''
            else:
                no_message_received_count += 1

                # Check that the DUT is still alive - 10 second timeout
                if no_message_received_count > 20:
                    ateConfig.log.logger.warning( "DUT Hearbeat not Received in 10 seconds")
                    # Error
                    break
            '''
    def processRequest(self, message):
        compId = message[3]
        cmdId = message[4]

        if str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_1']:
            ateConfig.log.logger.debug("Got msg to open Nano connection")
            time.sleep(0.1)
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), [78, 65, 78, 79])

        elif str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_2']:
            ateConfig.log.logger.debug("Got Request msg for test Hand Drag Test Nano")
            self._handDragTestNanoStatus = 1
            status = [self._handDragTestNanoStatus]
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

        elif str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_3']:
            ateConfig.log.logger.debug("Got Request msg for test Circles Concentricity Test ATE3 Nano")
            self._circlesConcentricityTestATE3NanoStatus = 1
            status = [self._circlesConcentricityTestATE3NanoStatus]
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

        elif str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_4']:
            ateConfig.log.logger.debug("Got Request msg for test EInk Dead Pixel Test ATE3 Nano")
            self._eInkDeadPixelTestATE3NanoStatus = 1
            status = [self._eInkDeadPixelTestATE3NanoStatus]
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

        elif str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_5']:
            ateConfig.log.logger.debug("Got Request msg for test LED Uniforming Test ATE3 Nano")
            self._LEDUniformingTestATE3NanoStatus = 1
            status = [self._LEDUniformingTestATE3NanoStatus]
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

        elif str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_6']:
            ateConfig.log.logger.debug("Got Check status msg for test Hand Drag Test Nano")
            status = [self._handDragTestNanoStatus]
            ateConfig.log.logger.debug("Current status of test Hand Drag Test Nano: %s" %str(status))
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

        elif str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_7']:
            ateConfig.log.logger.debug("Got Check status msg for test Circles Concentricity Test ATE3 Nano")
            status = [self._circlesConcentricityTestATE3NanoStatus]
            ateConfig.log.logger.debug("Current status of test Circles Concentricity Test ATE3 Nano: %s" %str(status))
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

        elif str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_8']:
            ateConfig.log.logger.debug("Got Check status msg for test EInk Dead Pixel Test ATE3 Nano")
            status = [self._eInkDeadPixelTestATE3NanoStatus]
            ateConfig.log.logger.debug("Current status of test EInk Dead Pixel Test ATE3 Nano: %s" %str(status))
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

        elif str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_9']:
            ateConfig.log.logger.debug("Got Check status msg for test LED Uniforming Test ATE3 Nano")
            status = [self._LEDUniformingTestATE3NanoStatus]
            ateConfig.log.logger.debug("Current status of test LED Uniforming Test ATE3 Nano: %s" %str(status))
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

        elif str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_10']:
            ateConfig.log.logger.debug("Got Start Processing Images Request")
            status = [1]
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

            if self._sftpComm.local_dir_exists(DIANA_IMAGE_RAW):
                self._sftpComm.remove_files_in_local_directory(DIANA_IMAGE_RAW)
            else:
                os.mkdir(DIANA_IMAGE_RAW)
            self._sftpComm.decompress_local_file(DIANA_IMAGE + self._fileReceived['filename'], DIANA_IMAGE)

            self._startProcessingImages = True

        if str(compId) == componentID['HT_NANO'] and str(cmdId) == commandID['HT_NANO_11']:
            ateConfig.log.logger.debug("Got msg to close Nano connection")
            self._handDragTestNanoStatus = 0
            self._circlesConcentricityTestATE3NanoStatus = 0
            self._eInkDeadPixelTestATE3NanoStatus = 0
            self._LEDUniformingTestATE3NanoStatus = 0
            time.sleep(0.1)
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), [78, 65, 78, 79])
            self._restartController = True

        elif str(compId) == componentID['HT_FILE_TRANSFER'] and str(cmdId) == commandID['HT_FILE_TRANSFER_1']:
            ateConfig.log.logger.debug("Got File Transfer Status")
            status = [1] # Continue File Transfer
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId), int(cmdId), status)

        elif str(compId) == componentID['HT_FILE_TRANSFER'] and str(cmdId) == commandID['HT_FILE_TRANSFER_2']:
            ateConfig.log.logger.debug("Got File Transfer Info")
            status = [1] # Continue File Transfer
            payloadLen = message[1]
            filename = "".join(chr(x) for x in message[7:7 + payloadLen - 6])
            ateConfig.log.logger.debug("Got File Name: %s" %str(filename))

            self._fileReceived['filename'] = filename
            self._fileReceived['size_1'] = message[5]
            self._fileReceived['size_2'] = message[6]
            ateConfig.log.logger.debug("Information of received file: %s" % self._fileReceived)
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId),
                             int(cmdId), status)

        elif str(compId) == componentID['HT_FILE_TRANSFER'] and str(cmdId) == commandID['HT_FILE_TRANSFER_3']:
            ateConfig.log.logger.debug("Got File Transfer Complete")
            status = [2]
            if os.path.isfile(DIANA_IMAGE + self._fileReceived['filename']):
                ateConfig.log.logger.debug("File %s exists" % (DIANA_IMAGE + self._fileReceived['filename']))

                size = os.path.getsize(DIANA_IMAGE + self._fileReceived['filename'])

                size_1 = size & 0xFF
                size_2 = (size >> 8) & 0xFF

                if size_1 == self._fileReceived['size_1'] and size_2 == self._fileReceived['size_2']:# and crc32_1 == self._fileReceived['crc32_1'] and crc32_2 == self._fileReceived['crc32_2']:
                    ateConfig.log.logger.info("Perfect File Transfer")
                    status = [3]  # Good checksum

                else:
                    status = [4]  # Bad checksum

            else:
                ateConfig.log.logger.debug("File %s does not exist" % (DIANA_IMAGE +  self._fileReceived['filename']))
                status = [2] # Abort

            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId),
                             int(cmdId), status)

        elif str(compId) == componentID['HT_FILE_TRANSFER'] and str(cmdId) == commandID['HT_FILE_TRANSFER_4']:
            status = []
            ateConfig.log.logger.debug("Got Get File Transfer Status")
            payloadLen = message[1]
            filename = "".join(chr(x) for x in message[5:5 + payloadLen - 4])
            ateConfig.log.logger.debug("Got File Name: %s" %str(filename))

            self._fileToSend['filename'] = filename

            if self._fileToSend['filename'] == 'processed_files.tar':
                if self.sftpComm.local_file_exists(DIANA_IMAGE + 'processed_files.tar'):
                    status = [1]  # Continue File Transfer

                else:
                    status = [2]  # Continue File Transfer

            ateConfig.log.logger.debug("Information of file to send: %s" % self._fileToSend)
            self.sendRequest(int(DUT_STATUS_MSG_ID), int(compId),
                             int(cmdId), status)

            self._fileToSend['filesize'] = os.path.getsize(DIANA_IMAGE + self._fileToSend['filename'])

        elif str(compId) == componentID['HT_FILE_TRANSFER'] and str(cmdId) == commandID['HT_FILE_TRANSFER_5']:
            txMessage = []
            ateConfig.log.logger.debug("Got Get File Transfer Info")
            payloadLen = 6
            fileSize = 0
            ateConfig.log.logger.debug("Information of file to send: %s" % self._fileToSend)

            if self._fileToSend['filename'] == 'processed_files.tar':
                fileSize = self._fileToSend['filesize']

            txMessage.extend([int(DUT_STATUS_MSG_ID), payloadLen & 0xFF, (payloadLen >> 8) & 0xFF,
                                    int(compId), int(cmdId),
                                    fileSize & 0xFF, (fileSize >> 8) & 0xFF])

            # self._txMessage.extend(command['data'])
            txMessage.append(self._serialComm.seqNum)
            crc = crc8Calc(txMessage[:(payloadLen + 2)])

            txMessage.append(crc)
            txMessage.extend([SYNC1, SYNC2])

            self.sendMessage(txMessage)

    def processResponse(self, message):
        '''
        TODO - implement this app method to handle the device response
        :param message:
        :return: none
        '''
        ateConfig.log.logger.debug('   SerialApp - Processing DUT Response: ' + str(message[0]))

    def killThreads(self):
        '''
        Kill all application threads in an orderly manner
        :return: none
        '''
        self._serialComm.killCommThreads()
        self._continue = False
        self._serialComm.closeSerial()

    def sendPingMsg(self):
        '''
        Send a ping message to the DUT to check if it is alive
        :return: none
        '''
        self.sendRequest(ATE_PING_MSG_ID, 0, 0)

    def convertDataToByteList(self, cmdData):
        '''
        Convert the orignal command data of any supported type to a byte list suitable for packing into
        the ATE to DUT request message payload data
        :param cmdData:
        :return: convertedByteData - list of bytes40
        '''

        # put the converted command data bytes here
        convertedByteData = []

        try:
            # Can handle str, int, float, and list types and execute conversions as needed
            # ints and floats packed little endian
            if type(cmdData) == str:
                convertedByteData.extend(cmdData)

            elif type(cmdData) == int:
                # integers are packed as 4 byte values
                convertedByteData.extend(bytearray(struct.pack("I", cmdData)))

            elif type(cmdData) == float:
                # handles single precision floats as 4 byte values
                convertedByteData.extend(bytearray(struct.pack("f", cmdData)))

            elif type(cmdData) == list:
                # just copy the original cmdData list contents
                convertedByteData = cmdData[:]

            elif type(cmdData) == bytes:
                convertedByteData = cmdData

            else:
                ateConfig.log.logger.error('   Invalid cmdData type ' + str(cmdData))
        except:
            return []

        return convertedByteData


    def sendRequest(self, msgId, compId, cmdId, cmdData=None):
        '''
        Send a request to the device
        :param msgId: int, Message ID
        :param compId: int, Component ID
        :param cmdId: int, Command ID
        :return: boolean
        '''
        ateConfig.log.logger.debug("Send NANO ID: " + str(msgId))

        self._txMessage = []
        crc = None

        # TODO - somewhere in here we need to validate the compId and cmdId
        if msgId in cmdMessageIdList or msgId in messageIdList:
            self._serialComm.incrementSeqNumber()

            if msgId == ATE_PING_MSG_ID:
                # Ping message have no compId or cmdId
                self._txMessage.extend([msgId, self._serialComm.seqNum])
                crc = crc8Calc(self._txMessage[:2])
            else:
                # Create the ATE request or ATE execute message
                # self._txMessage.extend([msgId, compId, cmdId])

                # payload data length and data for ATE Request messages only
                if msgId == ATE_REQ_MSG_ID or msgId == DUT_STATUS_MSG_ID:
                    # payloadLen = 16 bits, default length to 4 (compID, cmdID, seqNum, and checksum)
                    # and add cmdData length, if any
                    payloadLen = 4

                    # any payload data to include in the message?
                    if cmdData is not None:
                        # can handle any type of cmdData and convert to list of bytes
                        cmdData = self.convertDataToByteList(cmdData)

                        payloadLen += len(cmdData)

                    self._txMessage.extend([msgId, payloadLen & 0xFF, (payloadLen >> 8) & 0xFF, compId, cmdId])

                    # if any, add the payload data into the message
                    if cmdData is not None:
                        self._txMessage.extend(cmdData)

                else:
                    # non request messages are very short (Ping Message)
                    # payload len is not part of this message, just reusing it for crc calc
                    payloadLen = 3
                    self._txMessage.extend([msgId, compId, cmdId])

                self._txMessage.append(self._serialComm.seqNum)

                # checksum from first message byte thru seqNum byte
                crc = crc8Calc(self._txMessage[:(payloadLen + 2)])

            self._txMessage.append(crc)
            self._txMessage.extend([SYNC1, SYNC2])

            self.sendMessage(self._txMessage)
            return True
        else:
            ateConfig.log.logger.error("Invalid Tx message ID: " + msgId)
            return False


    def sendFileTransferRequest(self, command):
        '''
        For each type of file transfer command, create the serial message and send it to the DUT
        :param command:  All the attributes of the serial commmand
        :return:
        '''
        ateConfig.log.logger.info("Send ATE Message: " + command['name'])

        self._txMessage = []
        crc = None

        self._serialComm.incrementSeqNumber()

        #
        if command['name'] == 'File Transfer Header':
            payloadLen = 14
            fileSize = command['fileSize']
            numPartitions = command['numberPartitions']
            crc32 = command['crc32']

            self._txMessage.extend([ATE_REQ_MSG_ID, payloadLen & 0xFF, (payloadLen >> 8) & 0xFF,
                                    int(command['componentId']), int(command['commandId']), int(command['fileId']),
                                    fileSize & 0xFF, (fileSize >> 8) & 0xFF, (fileSize >> 16) & 0xFF,
                                    numPartitions & 0xFF, (numPartitions >> 8) & 0xFF,
                                    crc32 & 0xFF, (crc32 >> 8) & 0xFF, (crc32 >> 16) & 0xFF, (crc32 >> 24) & 0xFF,
                                    self._serialComm.seqNum])
            crc = crc8Calc(self._txMessage[:(payloadLen + 2)])

        elif command['name'] == 'File Transfer Data':
            payloadLen = command['numberBytes'] + 8
            partitionSize = command['numberBytes']
            partitionNumber = command['partitionNumber']

            fileDataBytes = list(command['data'])

            self._txMessage.extend([ATE_REQ_MSG_ID, payloadLen & 0xFF, (payloadLen >> 8) & 0xFF,
                                    int(command['componentId']), int(command['commandId']),
                                    partitionNumber & 0xFF, (partitionNumber >> 8) & 0xFF,
                                    partitionSize & 0xFF, (partitionSize >> 8) & 0xFF])

            self._txMessage.extend(command['data'])
            self._txMessage.append(self._serialComm.seqNum)
            crc = crc8Calc(self._txMessage[:(payloadLen + 2)])

        elif command['name'] == 'File Transfer Complete':
            payloadLen = 4
            self._txMessage.extend([ATE_REQ_MSG_ID, payloadLen & 0xFF, (payloadLen >> 8) & 0xFF,
                                    int(command['componentId']), int(command['commandId']),
                                    self._serialComm.seqNum])
            crc = crc8Calc(self._txMessage[:6])

        else:
            ateConfig.log.logger.error("Invalid Tx message: " + command['name'])
            return False

        self._txMessage.append(crc)
        self._txMessage.extend([SYNC1, SYNC2])

        self.sendMessage(self._txMessage)
        return True

    def processHeartbeat(self, message):
        '''
        Process the heartbeat message from the device
        :param message:
        :return: none
        '''
        heartbeatStatus = message[1]
        ateConfig.log.logger.debug("DUT Heartbeat Status: " + heartbeatStatus + ", Sequence Num: " + message[2])

    def processTestStatus(self, message):
        '''
        Process the test status message from the device
        :param message:
        :return: none
        '''
        testStatus = message[3:-4]
        ateConfig.log.logger.debug("Test Completion Status" + testStatus)

    def sendMessage(self, message):
        '''
        Request to queue up a message to transmit to the device
        :param message:
        :return: none
        '''
        self._serialComm.transmit(message)

    def getCommStatus(self):
        '''
        Execut the comm status function to get message statistics
        :return: none
        '''
        self._serialComm.getCommStatus()

    # getter/setters
    @property
    def rxMessageQ(self):
        return self._rxMessageQ

    @rxMessageQ.setter
    def rxMessageQ(self, queue):
        self._rxMessageQ = queue

    @property
    def lastResponseMessage(self):
        return self._lastResponseMessage

    @lastResponseMessage.setter
    def lastResponseMessage(self, msg):
        self._lastResponseMessage = msg

    @property
    def serialComm(self):
        return self._serialComm

    @serialComm.setter
    def serialComm(self, comm_obj):
        self._serialComm = comm_obj

    @property
    def respSubject(self):
        return self._respSubject

    @property
    def dataSubject(self):
        return self._dataSubject

    @property
    def startProcessingImages(self):
        return self._startProcessingImages

    @startProcessingImages.setter
    def startProcessingImages(self, value):
        self._startProcessingImages = value

    @property
    def sftpComm(self):
        return self._sftpComm

    @property
    def handDragTestNanoStatus(self):
        return self._handDragTestNanoStatus

    @handDragTestNanoStatus.setter
    def handDragTestNanoStatus(self, value):
        self._handDragTestNanoStatus = value

    @property
    def circlesConcentricityTestATE3NanoStatus(self):
        return self._circlesConcentricityTestATE3NanoStatus

    @circlesConcentricityTestATE3NanoStatus.setter
    def circlesConcentricityTestATE3NanoStatus(self, value):
        self._circlesConcentricityTestATE3NanoStatus = value

    @property
    def eInkDeadPixelTestATE3NanoStatus(self):
        return self._eInkDeadPixelTestATE3NanoStatus

    @eInkDeadPixelTestATE3NanoStatus.setter
    def eInkDeadPixelTestATE3NanoStatus(self, value):
        self._eInkDeadPixelTestATE3NanoStatus = value

    @property
    def LEDUniformingTestATE3NanoStatus(self):
        return self._LEDUniformingTestATE3NanoStatus

    @LEDUniformingTestATE3NanoStatus.setter
    def LEDUniformingTestATE3NanoStatus(self, value):
        self._LEDUniformingTestATE3NanoStatus = value

    @property
    def restartController(self):
        return self._restartController

    @restartController.setter
    def restartController(self, value):
        self._restartController = value
