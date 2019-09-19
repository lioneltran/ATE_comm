

import os
import pty
import queue
import serial
import time

from configuration import ateConfig
from .ateSerialUtil import *
from utilities.myThread import MyThread


# DUT Simulator - use the local MacOS loopback serial device for module testing
# the message protocols without using the real DUT hardware
class TestSerialComm(object):

    def __init__(self):

        # to access some of the comm methods
        #self.__comm = comm

        # general thread continuation flag - set to False to terminate all threads
        self.__continue = True

        self.__seq_num = 0

        # init source loopback interface - ATE
        # srclb_master - ATE receive
        # srclb_ser    - ATE transmit by writing to this descriptor
        self.__srclb_master, self.__srclb_slave = pty.openpty()
        self.__srclb_s_name = os.ttyname(self.__srclb_slave)
        self.__srclb_ser = serial.Serial(self.__srclb_s_name)

        self.__test_txQ = queue.Queue(10)

        # init destination loopback interface - simulated DUT
        # destlb_master - DUT receive
        # destlb_ser  - DUT transmit by writing to this descriptor
        self.__destlb_master, self.__destlb_slave = pty.openpty()
        self.__destlb_s_name = os.ttyname(self.__destlb_slave)
        self.__destlb_ser = serial.Serial(self.__destlb_s_name)

        # startup the simDUT serial receive thread - wait for messsages from master
        self.__rxThread = MyThread(11, 'TestDestRxThread', 2, self.test_dut_receive_thread)
        self.__rxThread.start()

        # startup the simDUT heartbeat thread, disabled during some tests
        #self.__hbThread = MyThread(12, 'TestHeartbeatThread', 2, self.test_heartbeat_transmit_thread)
        #self.__hbThread.start()

        # startup the simDUT serial transmit queue thread
        self.__txQThread = MyThread(13, 'TestTransmitQThread', 2, self.test_transmitQ_thread)
        self.__txQThread.start()

    # TEST - loopback ATE receive interface
    # this can be in (or called from) a separate thread that is running all the time
    # waiting for incoming messages.
    def testAteReceive(self):
        # Read from the virtual srcTx serial device
        new_message = os.read(self.__srclb_master, 20)
        ateConfig.log.logger.info( 'ATE<-SimDUT - Receive Message - %r' % new_message)
        return new_message

    # TEST - write the message to the simDUT receive loopback serial port
    def testAteSend(self, message):
        self.__destlb_ser.write(str.encode(message))
        ateConfig.log.logger.info( "   ATE->SimDUT Transmit - " + message)

    # TEST - loopback simDUT receive thread
    # this should be in a separate thread that is running all the time blocking on incoming messages.
    def test_dut_receive_thread(self):
        ateConfig.log.logger.info( "Starting testDutReceiveThread")

        # Pretty much an infinite loop waiting for incoming messages
        while self.__continue:
            new_message = []
            msg = []
            time.sleep(0.1)

            #  temporary bypass for testing
            # continue

            # Read from the virtual serial device input
            new_message = os.read(self.__destlb_master, 20)
            ateConfig.log.logger.info( 'SimDUT<-ATE - Rx Thread: %r' % new_message)

            msg = list(new_message[:].split())

            # Must be a valid message ID in first byte
            if (msg[0] != b'33') and (msg[0] != b'40'):
                ateConfig.log.logger.info('ATE->SimDUT - Rx Thread, Bad Msg ID: %r' % msg)
                continue

            # ATE request message received, ignore any acks and nacks
            if new_message and (msg[0] != ACK_MSG_ID and msg[0] != NACK_MSG_ID):
                # setup ack message, return orig message ID in ACK
                self.__seq_num += 1
                resp = [ACK_MSG_ID, int(msg[0]), self.__seq_num]   # ack
                #resp = [NACK_MSG_ID, msg[0], self.__seq_num]   # nack
                crc = crc8_calc(resp[:4])
                resp.append(crc)
                resp.extend([SYNC1, SYNC2])

                # transmit the response to the ATE Rx thread
                out = ' '.join(str(x) for x in resp)
                ateConfig.log.logger.info( 'SimDUT->ATE - Rx Thread, Queue Ack: %r' % out)
                # self.srclb_ser.write(out)
                #self.__test_txQ.put(out)
                self.__test_txQ.put(resp[:])

                # setup test completed status message
                self.__seq_num += 1
                resp = [STATUS_MSG_ID, int(msg[1]), self.__seq_num]

                crc = crc8_calc(resp[:4])
                resp.append(crc)
                resp.extend([SYNC1, SYNC2])

                # transmit the response to the srcRx thread (ATE)
                out = ' '.join(str(x) for x in resp)
                ateConfig.log.logger.info( 'SimDUT->ATE - Rx Thread, Queue Status Response: %r' % out)
                # self.srclb_ser.write(out)
                #self.__test_txQ.put(out)
                self.__test_txQ.put(resp[:])
            else:
                ateConfig.log.logger.info( 'SimDUT<-ATE - Rx Thread, Ignore Ack or Nack, id = %r' % msg[0])

    # TEST - Send out 1hz heartbeat message from DUT to ATE
    def test_heartbeat_transmit_thread(self):
        ateConfig.log.logger.info( "Starting testHeartbeatThread")
        hb_seq_num = 1

        # Pretty much an infinite loop waiting for incoming messages
        while self.__continue:
            # TODO - reset to 1 second intervals later
            time.sleep(2)

            # setup 1 hz heartbeat message
            resp = [HB_MSG_ID, hb_seq_num]
            hb_seq_num += 1

            crc = crc8_calc(resp[:3])
            resp.append(crc)
            resp.extend([SYNC1, SYNC2])

            # transmit the response to the srcRx thread (ATE)
            out = ''
            out = ' '.join(str(x) for x in resp)
            ateConfig.log.logger.info( 'SimDUT->ATE - HB Thread, Queue Heartbeat: %r' % out)
            # self.srclb_ser.write(out)
            self.__test_txQ.put(out)

    # background thread to process any queued messages to transmit to ATE
    # ensures that messages are sent out in order one at a time
    def test_transmitQ_thread(self):
        ateConfig.log.logger.info( "Starting testTransmitQThread")

        while self.__continue:
            time.sleep(0.1)
            # if message received, validate it and check if ack or nack
            if not self.__test_txQ.empty():
                message = self.__test_txQ.get()

                out = ' '.join(str(x) for x in message)
                #ateConfig.log.logger.info( '\nSimDUT->ATE - Transmit Q Thread: %r' % message)
                ateConfig.log.logger.info('\nSimDUT->ATE - Transmit Q Thread: %r' % out)
                self.__srclb_ser.write(bytes(message))

    def killTestThreads(self):
        self.__continue = False

