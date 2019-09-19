#!/usr/bin/python

"""SerialComm module for ATE/DUT serial communications"""

import queue
import threading
import time
import serial

from configuration import ateConfig
from utilities.myThread import MyThread
from .ateSerialUtil import *

# for virtual serial device - testing on MacOS
from .serialSim import TestSerialComm

# ATE/DUT message protocol assumptions
#   1) ATE->DUT command messages are low frequency, command/response based
#   2) ATE->DUT messages are sent only after previous message has completed
#   3) DUT->ATE status messages are asynchronous; ATE can receive them after variable time duration
#   4) DUT->ATE heartbeat messages are sent at a 1hz frequency between commanded tests, not used at this time

class SerialComm:
    '''
    # Support for serial communications on the Raspberry Pi to the device under test (DUT)
    Tasks are of transmitting and receiving messages
    On receive, validate the message and send Ack or Nack
    On transmit, send the message and wait for the Ack or Nack, resend if necessray
    '''

    def __init__(self, appRxQueue=None, test=False):
        '''
        Initialize the queues, instance variables, and serial port attributes
        :param appRxQueue: Application queue to send DUT test status messages
        :param test: True - use Serial Simulator, False - use Serial HW
        '''
        self._seqNum = 0

        self._messageErrors = dict(badTestId=0, badCrc=0, badSyncs=0, timeout=0, resends=0, resendFailed=0)
        self._nackErrors = dict(num=0, badMsgId=0, badCrc=0, badSyncs=0, badMsgSize=0)
        self._messageStats  = dict(received=0, transmitted=0, heartbeats=0, bad=0)

        # put incoming messages here for the serial app to process
        self._rxAppQ = appRxQueue

        # put messages here for the transmit thread
        self._txQ = queue.Queue(5)

        # internal queue to receive and validate message before forwarding to serial app
        self._internalRxQ = queue.Queue(5)
        #self._reqMessageSent = False

        # rx thread puts DUT request ack/nack response messages
        self._rxReqResponseQ = queue.Queue(5)

        # rx thread puts DUT asychronous test status messages
        self._rxTestStatusQ = queue.Queue(5)

        # event flag - indicates an ATE request sent to the DUT, now go wait for the response
        self._reqMsgSentEvent = threading.Event()

        self._lastTxMessage = []

        # serial app request to use SerialComm in test mode, or not
        self._testMode = test

        # flag to terminate all thread while loops, causing the thread to exit and terminate
        self._continue = True

        if self._testMode:
            # use the test loopback serial device
            self._testComm = TestSerialComm()
        else:
            # use the real serial device for testing DUT
            # 19200 baud for compromise of speed vs reliability
            try:
                self._serialDevice = serial.Serial(port='/dev/ttyGS0',
                                                    baudrate=19200,
                                                    parity=serial.PARITY_NONE,
                                                    stopbits=serial.STOPBITS_ONE,
                                                    bytesize=serial.EIGHTBITS,
                                                    timeout=0)
                self._serialDevice.flushInput()
                self._serialDevice.flushOutput()
                ateConfig.log.logger.debug(self._serialDevice.name)
            except Exception as exc:
                ateConfig.log.logger.error("Error creating serialDevice")
                raise

        self._rxThread  = None
        self._rxReqResponseThread = None
        self._rxTestStatusThread = None
        self._txThread  = None

        self.startSerialThreads()

    def startSerialThreads(self):
        '''
        Run all serialComm threads
        :return: none
        '''
        # startup the serial receive thread
        self._rxThread = MyThread(21, 'RxThread', 2, self.receiveThread)
        self._rxThread.start()

        # handle DUT responses to ATE requests
        self._rxReqResponseThread = MyThread(23, 'RxReqResponseThread', 2, self.rxReqResponseThread)
        self._rxReqResponseThread.start()

        # handle asynchronous DUT test status messages
        self._rxTestStatusThread = MyThread(24, 'RxTestStatusThread', 2, self.rxTestStatusThread)
        self._rxTestStatusThread.start()

        # startup the serial transmit thread
        self._txThread = MyThread(25, 'TxThread', 2, self.transmitThread)
        self._txThread.start()

    def closeSerial(self):
        '''
        Shutdown the serial port 
        :return: none
        '''
        if not self._testMode:
            self._serialDevice.close()

    def transmit(self, message):
        '''
        Transmit a message into the transmit queue to ensure
        messages sent in orderly fashion
        :param message: 
        :return: 
        '''
        # copy by value, not by reference to the transmit Q
        self._txQ.put(message[:])

    def transmitThread(self):
        '''
        Transmit a message to the DUT
        :return: none
        '''
        ateConfig.log.logger.debug( "Starting transmitThread")

        # forever loop until the thread is killed
        while self._continue:
            time.sleep(USECS_100)
            # if message received, validate it and check if ack or nack
            if not self._txQ.empty():
                message = self._txQ.get()
                self._lastTxMessage = message

                # if ack or nack sent to DUT, no DUT response expected
                # message_sent flag used in Rx thread to validate DUT response
                if message[0] == ATE_REQ_MSG_ID:
                    self._reqMsgSentEvent.set()

                # delay to allow flag to be read later by receiveThread
                time.sleep(USECS_100)

                if self._testMode:
                    # convert byte array to text string
                    out = ' '.join(str(x) for x in message)

                    # write to the destRx loopback serial device - similuated DUT
                    self._testComm.testAteSend(out)
                else:
                    try:
                        ateConfig.log.logger.debug("   NANO -> ATE Transmit Msg Length - %s" % str(len(message)))
                        # write message (in bytes) out the serial port
                        numBytesWritten = self._serialDevice.write(bytes(message))
                        self._serialDevice.flush()
                        # str(self._serialDevice.out_waiting()))
                    except serial.SerialTimeoutException:
                        ateConfig.log.logger.error('   Serial Error - timeout writing to serial port')


                msg = '[' + ', '.join('0x{:02X}'.format(x) for x in message) + ']'

                ateConfig.log.logger.debug( "NANO -> ATE Transmit - num bytes = " + str(numBytesWritten))
                ateConfig.log.logger.debug( "NANO -> ATE Transmit - %s" % msg)

                self._messageStats['transmitted'] += 1

    def receiveThread(self):
        '''
        This is a separate thread that is running continuously waiting for incoming messages from the DUT.
        Most important serial port thread which needs to always be available to look for incoming messages.
        Queue up received messages into the internal ATE message processing queue for handling later.
        This separate processing thread allows the receive thread to efficiently save incoming messages,
        :return: none
        '''
        ateConfig.log.logger.debug( "Starting receiveThread")

        # forever loop until the thread is killed
        while self._continue:
            rxMessageList = []
            rxMessage = []

            # Minimum time gap between incoming messages - tuned delay, modify with caution
            #time.sleep(MSECS_10)

            # Read from test or real serial device?
            if self._testMode:
                rxMessage = self._testComm.testAteReceive()
            else:
                # number of bytes in current message
                count = 0

                # valid message ID indicating start of message received?
                messageReceived = False
                dutStatusMsgReceived = False
                statusPayloadDataLen = 0
                #ateConfig.log.logger.debug("   Main while loop - messageReceived = " + str(messageReceived))

                # save previous input character to detect end of message sync bytes
                previous_char = ''

                # keep reading serial buffer until whole message received
                contReading = True

                # get all message bytes from the serial port
                readCountTime  = 0

                while contReading:
                    time.sleep(MSECS_5)

                    # reset to start handling first byte of next message segment
                    #if messageReceived == True:
                    #   count = 0

                    # continuously check for bytes in the serial input buffer
                    numBytesWaiting = self._serialDevice.inWaiting()

                    if numBytesWaiting == 0:
                        continue

                    ateConfig.log.logger.debug("ATE -> NANO, Bytes waiting - " + str(numBytesWaiting))

                    serialData = self._serialDevice.read(numBytesWaiting)
                    ateConfig.log.logger.debug(('serialData =  %s' % serialData))

                    numBytesProcessed = 0

                    if serialData:
                        # Look for the start of a new message with valid message ID in first byte
                        # Continue this loop until a complete message detected
                        for ch in serialData:
                            count += 1
                            numBytesProcessed += 1

                            # Look for the message ID for start of new message
                            if not messageReceived:
                                # check if first byte is valid message ID
                                if ch in messageIdList and count == 1:
                                    messageReceived = True
                                    ateConfig.log.logger.debug(('Got Valid Message ID: %r' % str(ch)))

                                    if ch == DUT_STATUS_MSG_ID or ch == DUT_FILE_TRANSFER_STATUS_MSG_ID:
                                        dutStatusMsgReceived = True

                                elif ch in cmdMessageIdList and count == 1:
                                    messageReceived = True
                                    ateConfig.log.logger.debug(('Got Valid Message ID from ATE: %r' % str(ch)))

                                    self._rxAppQ.put(serialData[:])

                                    self.sendAckOrNack(serialData[0], serialData[-4], 0, ACK_MSG_ID)  # Ack

                                else:
                                    ateConfig.log.logger.debug(str(count) + ': Discard %r %r' % (str(ch), str(chr(ch))))
                                    if count > 0:
                                        count -= 1
                                    continue

                            # ateConfig.log.logger.debug(str(count) + ': %r\t%r\t%r' % (str(ch),  str(hex(ch)), str(chr(ch))))
                            rxMessage.append(ch)

                            # For DUT status messages, get the payload count and ingest payload data before
                            # Must first read 3 message bytes - msg ID and two byte payload length
                            # checking for end of message sync bytes
                            if dutStatusMsgReceived and count == 3:
                                statusPayloadDataLen = (rxMessage[1] & 0xFF) | ((rxMessage[2] << 8) & 0xFF00)

                            # If DUT Status Message, bypass sync byte validation until all payload data bytes read
                            elif statusPayloadDataLen > 0 and count > 3:
                                # ateConfig.log.logger.debug("   Payload Data Bypassed = " + str(ch) + ", bytesLeft = " + str(statusPayloadDataLen))
                                statusPayloadDataLen -= 1
                                #continue

                            # end of message sync bytes detected and minimum size message?
                            elif (previous_char == SYNC1 and ch == SYNC2) and count >= 4:
                                ateConfig.log.logger.debug("Got Complete Message Sync Bytes, Msg ID = " + str(rxMessage[0]))
                                rxMessageList.append(rxMessage)

                                ateConfig.log.logger.debug("numBytesWating = {}, numBytesProcessed = {}, msgCount = {}".
                                                          format(str(numBytesWaiting), str(numBytesProcessed), str(count)))

                                # Finished current message, setup for next message
                                rxMessage = []
                                messageReceived = False
                                dutStatusMsgReceived = False

                                # if all message bytes handled, exit processing
                                # Otherwise, we have another message to handle
                                if (numBytesWaiting - numBytesProcessed) == 0:
                                    contReading = False
                                    break
                                else:
                                    # End of current message - reset to start handling first byte of next message segment
                                    count = 0

                            # save previous char to look for two EOM sync bytes
                            previous_char = ch

                    # escape - timeout is one second to read a complete message from start to finish
                    readCountTime += 1
                    if readCountTime > 200:
                        ateConfig.log.logger.warning('Timed out Read Loop')
                        break

            # Message data received, just queue it and valdate in Rx processing thread
            for newMessage in rxMessageList:
                self._messageStats['received'] += 1
                msgId = newMessage[0]

                # buffer the message if not a heartbeat message for processing thread
                if msgId == DUT_HB_MSG_ID:
                    # log the heartbeat message and display it
                    #logger.info("   NANO <- ATE - Received Hearbeat: " + newMessage + ", Hex: " + newMessage.encode('hex'))
                    ateConfig.log.logger.debug("NANO <- ATE - Received Heartbeat: %r" % newMessage)
                    # validate the heartbeat message structure and crc
                    if not self.validateMessage(newMessage):
                        self._rxAppQ.put(newMessage[:])
                        self._messageStats['heartbeats'] += 1

                # status data message with device info - response to ATE request command
                elif msgId == DUT_STATUS_MSG_ID:
                    if self._reqMsgSentEvent.isSet:
                        # Must be an asynchronous DUT test status message
                        self._rxTestStatusQ.put(newMessage[:])
                    else:
                        ateConfig.log.logger.error("NANO <- ATE - Unexpected Message, Discard: %r" % newMessage)
                else:
                    # Check if ack or nack
                    if msgId == ACK_MSG_ID or msgId == NACK_MSG_ID:
                        self._rxReqResponseQ.put(newMessage[:])
                        #ateConfig.log.logger.debug("   reqMsgSentEvent " + str(self._reqMsgSentEvent.is_set()))

                        # Has a ATE request message been sent waiting for the ack/nack?
                        # if self._reqMsgSentEvent.isSet or self._lastTxMessage[0] == ATE_PING_MSG_ID:
                        #     self._rxReqResponseQ.put(newMessage[:])
                        # else:
                        #     ateConfig.log.logger.error("   NANO <- ATE - Ack/Nack Not Expected, Discard: %r" % newMessage)

                msg = '[' + ', '.join('0x{:02X}'.format(x) for x in newMessage) + ']'
                # print(message)

                ateConfig.log.logger.debug( "NANO <- ATE - Received Message: %s" % msg)

    def rxReqResponseThread(self):
        '''
        Background thread to process any queued incoming response ack/nack messages.  Specifically looking for
        responses to ATE requests.  Ensure they come in on time and resend original request, if needed.
        :return: none
        '''
        ateConfig.log.logger.debug( "Starting rxReqResponseThread")

        rxMsg = []
        resendMessageCount = 0  # resend the message max of 3 times

        while self._continue:
            time.sleep(USECS_100)

            if self._rxReqResponseQ.empty():
                continue

            waitLimit = RESPONSE_WAIT_TIMEOUT  # DUT response timeout
            resend_message = False    # resend the message once if response times out

            ateConfig.log.logger.debug('rxReqResponseQ has message')

            # internal DUT response message wait loop - 3 second timeout
            # Either an Ack or Nack is expected
            while waitLimit > 0:

                # if message received, validate it and check if ack or nack
                rxMsg = list(self._rxReqResponseQ.get())
                msg = '[' + ', '.join('0x{:02X}'.format(x) for x in rxMsg) + ']'
                ateConfig.log.logger.debug('NANO <- ATE - From rxReqResponseQ: ' + str(msg))

                # validate the message structure and crc
                if self.validateMessage(rxMsg):
                    ateConfig.log.logger.debug("NANO <- ATE - Invalid DUT Ack/Nack Message CRC")
                    continue

                # ack message
                if rxMsg[0] == ACK_MSG_ID:
                    # self._reqMessageSent = False
                    msg = '[' + ', '.join('0x{:02X}'.format(x) for x in rxMsg) + ']'
                    ateConfig.log.logger.debug('NANO <- ATE - Ack, Orig Id: %s' % msg)
                    break

                # nack message
                elif rxMsg[0] == NACK_MSG_ID:
                    ateConfig.log.logger.debug('NANO <- ATE - Nack, Orig Id: ' + str(rxMsg[1]) + ', Error: ' + str(rxMsg[2]))

                    # save NACK error code stats
                    if rxMsg[3] & 1:
                        self._nackErrors['badMsgId'] += 1
                    if rxMsg[3] & 2:
                        self._nackErrors['badSyncs'] += 1
                    if rxMsg[3] & 4:
                        self._nackErrors['badCrc'] += 1
                    if rxMsg[3] & 8:
                        self._nackErrors['badMsgSize'] += 1

                    # total number of nacks from DUT
                    self._nackErrors['num'] += 1
                    resend_message = True   # got a response, but somethings wrong with orig message
                    break

                waitLimit -= 1
                ateConfig.log.logger.debug('Waiting for Message, Secs = ' + str(waitLimit))

                # wait awhile for DUT response
                time.sleep(SECS_1)

            # This is a bit complex.  Basically handles device responses are correct and received on time.
            # Check what happened after the wait loop terminated
            # Resend msg if 3 second response timeout or resend orig message up to two more times, if needed
            if (waitLimit == 0 or resend_message == True) and resendMessageCount < 2:
                self.incrementSeqNumber()
                self._lastTxMessage[-4] = self._seqNum     # incremented msg seq number
                self._lastTxMessage[-3] = crc8Calc(self._lastTxMessage[:-3])
                self.transmit(self._lastTxMessage)
                resendMessageCount += 1
                self._messageErrors['resends'] += 1
                ateConfig.log.logger.warning('ATE->DUT - Resending Message: ' + str(self._lastTxMessage[0]))

                # set timeout error only in those cases
                if waitLimit == 0:
                    ateConfig.log.logger.error('ATE->DUT - Response Message Timeout')
                    self._messageErrors['timeout'] += 1

            # resend ATE message failed 2 more times, then give it up
            elif resendMessageCount > 2:
                self._reqMsgSentEvent.clear()
                self._messageErrors['resendFailed'] += 1
                resendMessageCount = 0  # reset for next ATE -> DUT message
                ateConfig.log.logger.error('ATE->DUT - Two resends failed to receive valid DUT response')
            else:
                # Success - got valid ACK response from DUT within wait limit time period
                msg = '[' + ', '.join('0x{:02X}'.format(x) for x in rxMsg) + ']'
                ateConfig.log.logger.debug("NANO <- ATE - Got Ack Response Message: %s" % msg)# + str(rxMsg[0]) + ', test Id: ' + str(rxMsg[1]))
                self._rxAppQ.put(rxMsg[:])
                self._reqMsgSentEvent.clear()
                resendMessageCount = 0  # reset for next ATE -> DUT message

    def rxTestStatusThread(self):
        '''
        Thread to process the DUT test status response messages
        :return: None
        '''
        ateConfig.log.logger.debug("Starting rxTestStatusThread")

        # Basicall a forever loop - looking if DUT sent an asynchronous test status message
        while self._continue:
            time.sleep(USECS_100)

            if self._rxTestStatusQ.empty():
                continue

            # get the test results status message, non-blocking call
            rxMsg = self._rxTestStatusQ.get()

            msg = '[' + ', '.join('0x{:02X}'.format(x) for x in rxMsg) + ']'
            ateConfig.log.logger.debug("NANO <- ATE - RxQ Async Response Message: %r" % msg)

            # Should not get acks or nacks from the DUT here, ignore it
            if rxMsg[0] == ACK_MSG_ID or rxMsg[0] == NACK_MSG_ID:
                ateConfig.log.logger.error('No Response to unexpected DUT ack or nacks')
            else:
                # Got a DUT test execution status message
                # validate the message structure and crc and pass message to the serial app
                msgStatus = self.validateMessage(rxMsg)
                if msgStatus == 0:
                    self.sendAckOrNack(rxMsg[0], rxMsg[-4], 0, ACK_MSG_ID)  # Ack
                    self._rxAppQ.put(rxMsg[:])
                    # msg = '[' + ', '.join('0x{:02X}'.format(x) for x in rxMsg) + ']'
                    ateConfig.log.logger.debug("NANO <- ATE - Saved Msg to AppQ: %r" % msg)
                else:
                    self.sendAckOrNack(rxMsg[0], rxMsg[-4], msgStatus, NACK_MSG_ID)  # Nack
                    ateConfig.log.logger.warning("NANO <- ATE - Invalid DUT Test Status Message, Send Nack")

    def killCommThreads(self):
        '''
        Terminate all serialComm threads
        :return: none
        '''
        self._continue = False
        if self._testMode:
            self._testComm.killTestThreads()

    def sendAckOrNack(self, orig_msg_id, orig_seq_num, msg_status, msg_id):
        '''
        Build and send an Ack or Nack message to the device
        :param orig_msg_id:
        :param orig_seq_num:
        :param msg_status:
        :param msg_id:  Ack or Nack
        :return: none
        '''
        crc = 0
        tx_message = []
        self._seqNum = self.incrementSeqNumber()

        if msg_id == ACK_MSG_ID:
            tx_message.extend([msg_id, orig_msg_id, orig_seq_num, self._seqNum])
            crc = crc8Calc(tx_message[:4])
        else:
            tx_message.extend([msg_id, orig_msg_id, orig_seq_num, msg_status, self._seqNum])
            crc = crc8Calc(tx_message[:5])

        tx_message.append(crc)

        tx_message.extend([SYNC1, SYNC2])
        self.transmit(tx_message[:])

    '''
    def createFailureMessage(self, orig_msg_id):
        
        Build a request failure response message to the ATE application
        :param orig_msg_id: 
        :param msg_id: 
        :return: none
        
        failure_message = []
        self._seqNum = self.incrementSeqNumber()

        failure_message.extend([FAIL_MSG_ID, orig_msg_id, self._seqNum])
        crc = crc8Calc(failure_message[:4])
        failure_message.append(crc)

        failure_message.extend([SYNC1, SYNC2])
        return failure_message
    '''

    def validateMessage(self, rxMsg):
        ''' 
        Validate message's sync bytes, message ID, and crc checksum
        :param rxMsg (list): received message 
        :return: (int) bit mask of message errors detected
        '''
        status = 0

        # validate the message id in first byte
        if not rxMsg[0] in messageIdList:
            ateConfig.log.logger.error(('Validate - badTestId: ' + str(rxMsg[0])))
            self._messageErrors['badTestId'] += 1
            status |= 0x01

        # validate two trailing sync bytes
        # '#' = 35 and '$' = 36
        if rxMsg[-2] != SYNC1 and rxMsg[-1] != SYNC2:
            ateConfig.log.logger.error('Valdiate - badSyncs: ' + str(rxMsg[-2]) + ', ' + str(rxMsg[-1]))
            self._messageErrors['badSyncs'] += 1
            status |= 0x02

        # validate crc byte - sum all but last 3 message bytes16
        if rxMsg[-3] != crc8Calc(rxMsg[:-3]):
            ateConfig.log.logger.error(('Validate - badCrc:  %' + str(rxMsg[3])))
            self._messageErrors['badCrc'] += 1
            status |= 0x04

        if status == 0:
            ateConfig.log.logger.debug("ATE Validate - DUT Message Good: " + str(rxMsg[0]))
        else:
            self._messageStats['bad'] += 1

        return status

    def getCommStatus(self):
        '''
        Print the current serial com statistics
        :return: none
        '''
        ateConfig.log.logger.debug( ' Total Messages - Rx: ' + str(self._messageStats['received']) + ', Tx: ' + str(self._messageStats['transmitted']) + ', Bad: ' + \
                str(self._messageStats['bad']))

        ateConfig.log.logger.debug('  Rx Errors:   ' + 'Bad ID: ' + str(self._messageErrors['badTestId']) + \
                                  ', Bad CRC: ' + str(self._messageErrors['badCrc']) + ', Bad Syncs: ' + str(self._messageErrors['badSyncs']) + \
                                  ', Timeout: ' + str(self._messageErrors['timeout']) + ', Resends: ' + str(self._messageErrors['resends']) + \
                                  ', Resend Failed: ' + str(self._messageErrors['resendFailed']))

        ateConfig.log.logger.debug('  Nack Errors: ' + 'Num Nacks: ' + str(self._nackErrors['num']) + \
                                  ', Bad ID: ' + str(self._nackErrors['badMsgId']) +
                                  ', Bad CRC: ' + str(self._nackErrors['badCrc']) + ', Bad Syncs: ' + str(self._nackErrors['badSyncs']) + \
                                  ', Bad Msg Size: ' + str(self._nackErrors['badMsgSize']))

    def getmessageErrors(self):
        return self._messageErrors

    def incrementSeqNumber(self):
        ''' 
        Increment message sequence number with range = 1 to 255
        :return: none
        '''
        if self.seqNum == 255:
            self.seqNum = 1
        else:
            self.seqNum += 1

        return self.seqNum

    # single underscore variables are private class members
    # getters and setters using decorators to access these privates
    @property
    def seqNum(self):
        return self._seqNum

    @seqNum.setter
    def seqNum(self, value):
        self._seqNum = value & 0xFF

    @property
    def rxAppQ(self):
        return self._rxAppQ

    @rxAppQ.setter
    def rxAppQ(self, queue):
        self._rxAppQ = queue

