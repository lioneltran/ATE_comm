import sys
import json
import os
sys.path.append('/home/nano/misfit/ShineProduction/newATE/')
import glob
import shutil
import time
from configuration import ateConfig
from configuration.ateConfig import *
import subprocess
import threading
import netifaces as ni

from utilities.myThread import MyThread
import RPi.GPIO as GPIO
# from commands.serialCmd import SerialCmd
from comm.serialApp import SerialApp

import pexpect
import stat
import errno
class Controller():
    def __init__(self):
        testResult = []
        self._testRunning = False

        self._controlPin = 18
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
        GPIO.setup(self._controlPin, GPIO.IN)  # button pin set as input

        self._password = LOCAL_PASSWORD

        self._GPIOStateThread  = None
        self._connectionStatusThread = None
        self._visionTestsThread = None
        self._serialConnectionStatusGood = False
        self._serialNetworkStatusGood = False

        self.serial = None

        log.startupTheLoggers(LOGPATH)

        self.interfaceInitialize()
        self.startThreads()

    def startThreads(self):
        self._GPIOStateThread = MyThread(31, 'GPIOStateThread', 2, self.GPIOStateThread)
        self._GPIOStateThread.start()

        self._connectionStatusThread = MyThread(32, 'connectionStatusThread', 2, self.connectionStatusThread)
        self._connectionStatusThread.start()

        self._controllerThread = MyThread(33, 'visionTestsThread', 2, self.controllerThread)
        self._controllerThread.start()

    def GPIOStateThread(self):
        while True:
            ateConfig.log.logger.debug('Waiting for GPIO state changes')
            GPIO.wait_for_edge(self._controlPin, GPIO.FALLING)
            ateConfig.log.logger.debug('Rebooting..')
            try:
                child = pexpect.spawn("sudo reboot now", timeout=14400)
                # child = pexpect.spawn("bash /home/nano/Desktop/interface_script.sh", timeout=14400)

                self._handle_sftp_prompt(child)
                child.expect(pexpect.EOF)

            finally:
                if child:
                    child.close()
                    if child.isalive():
                        ateConfig.log.logger.debug('Child did not exit gracefully.')
                    else:
                        ateConfig.log.logger.debug('Child exited gracefully.')

            # if child:
            #     if child.status > 0:
            #         raise Exception('')
            #     else:
            #         ateConfig.log.logger.info('Putting file completed')

    def connectionStatusThread(self):
        connection_HB = threading.Event()
        while not connection_HB.wait(10):
            status = self.ping(REMOTE_IP)
            if status:
                if self.serial:
                    ateConfig.log.logger.debug("HB: USB network connection is Good | %s | %s | %s | %s | %s |"
                                                %( self._testRunning, self.serial.handDragTestNanoStatus,
                                                   self.serial.circlesConcentricityTestATE3NanoStatus,
                                                   self.serial.eInkDeadPixelTestATE3NanoStatus,
                                                   self.serial.LEDUniformingTestATE3NanoStatus) )
                else:
                    ateConfig.log.logger.debug("HB: USB network connection is Good")
                self.createConnection()
                self._serialNetworkStatusGood = True
            else:
                ateConfig.log.logger.debug("USB network connection is Bad")
                self._serialNetworkStatusGood = False

                import netifaces as ni
                ni.ifaddresses('usb0')
                ip = ni.ifaddresses('usb0')[ni.AF_INET][0]['addr']
                if ip == '10.0.1.2':
                    ateConfig.log.logger.debug("Pi'IP is not set yet")

                else:
                    ateConfig.log.logger.debug("Running the initialization script")
                    self.interfaceInitialize()

    def controllerThread(self):
        while True:
            if self._serialNetworkStatusGood:
                if self.serial:
                    if self.serial.restartController == True and self._testRunning == False:
                        self.serial.restartController = False
                        time.sleep(2)
                        self.restartConnection()

                if self.serial.startProcessingImages:
                    self.sftp.remove_files_in_local_directory(PROCESSED_IMAGES)
                    self._testRunning = True
                    self.serial.startProcessingImages = False

                if self._testRunning == True:
                    if self.sftp.local_dir_exists(DIANA_IMAGE_RAW):
                        jpegCounter = len(glob.glob1(DIANA_IMAGE_RAW, "*.jpeg"))
                        if jpegCounter == 11:
                            testResult = self.visionTests()

                            data_string = json.dumps(testResult)
                            data_json = json.loads(data_string)

                            with open(LOCAL_IMAGE_PROCESSING_RESULT, 'w', encoding='utf-8') as f:
                                json.dump(data_json, f, ensure_ascii=False, indent=4)

                            shutil.copyfile('/home/nano/ATE_comm/logs/ATE_Nano.log', PROCESSED_IMAGES + 'ATE_Nano.log')

                            self.sftp.compress_local_folder(PROCESSED_IMAGES,DIANA_IMAGE + 'processed_files.tar')
                            # os.chmod(DIANA_IMAGE + 'processed_files.tar', stat.S_IRWXU)
                            self._testRunning = False

    def createConnection(self):
        try:
            self.serial = SerialApp.Instance()

            self.sftp = self.serial.sftpComm
            self.sftp.create_connection(REMOTE_IP, REMOTE_PORT, REMOTE_USERNAME, REMOTE_PASSWORD)
        except ImportError:
            pass

    def restartConnection(self):
        try:
            os.chmod(DIANA_IMAGE + 'processed_files.tar', stat.S_IRWXU)
            self.sftp.remove_local_file(DIANA_IMAGE+'raw_images.tar')
            self.sftp.remove_local_file(DIANA_IMAGE + 'processed_files.tar')
            log.terminateBackgroundLogger()
            log.startupTheLoggers(LOGPATH)

            # self.serial = None
            # self.sftp = None
            #
            # self.createConnection()

        except Exception as e:
            ateConfig.log.logger.error("Error: %s" %e)
            pass

        # except IOError as e:
        #     if e.errno == errno.EPIPE:
        #         time.sleep(1)
        #         log.terminateBackgroundLogger()
        #         log.startupTheLoggers(LOGPATH)


    def interfaceInitialize(self):
        try:
            # child = pexpect.spawn("sudo reboot now", timeout=14400)
            child = pexpect.spawn("bash /home/nano/Desktop/interface_script.sh", timeout=14400)

            self._handle_sftp_prompt(child)
            child.expect(pexpect.EOF)

        finally:
            if child:
                child.close()
                if child.isalive():
                    ateConfig.log.logger.debug('Child did not exit gracefully.')
                else:
                    ateConfig.log.logger.debug('Child exited gracefully.')
        #
        # if child:
        #     if child.status > 0:
        #         raise Exception('')
        #     else:
        #         ateConfig.log.logger.info('Putting file completed')


    def visionTests(self):
        from tests.vision.circlesConcentricityTestATE3Nano import CirclesConcentricityTestATE3Nano
        from tests.vision.EInkdeadPixelTestATE3Nano import EInkDeadPixelTestATE3Nano
        from tests.vision.handDragTestNano import HandDragTestNano
        from tests.vision.LEDUniformingTestATE3Nano import LEDUniformingTestATE3Nano
        testResult = []

        # 1st test
        if self.serial.handDragTestNanoStatus == 1:
            classInstance = HandDragTestNano()
            self.serial.handDragTestNanoStatus = 2
            result = classInstance.execute()

            if result:
                self.serial.handDragTestNanoStatus = 3
                testResult.append(result)


        # 2nd test
        if self.serial.circlesConcentricityTestATE3NanoStatus == 1:
            classInstance = CirclesConcentricityTestATE3Nano()
            self.serial.circlesConcentricityTestATE3NanoStatus = 2
            result = classInstance.execute()

            if result:
                self.serial.circlesConcentricityTestATE3NanoStatus = 3
                testResult.append(result)

        # 3rd test
        if self.serial.eInkDeadPixelTestATE3NanoStatus == 1:
            classInstance = EInkDeadPixelTestATE3Nano()
            self.serial.eInkDeadPixelTestATE3NanoStatus = 2
            result = classInstance.execute()

            if result:
                self.serial.eInkDeadPixelTestATE3NanoStatus = 3
                testResult.append(result)

        # 4th test
        if self.serial.LEDUniformingTestATE3NanoStatus == 1:
            classInstance = LEDUniformingTestATE3Nano()
            self.serial.LEDUniformingTestATE3NanoStatus = 2
            result = classInstance.execute()

            if result:
                self.serial.LEDUniformingTestATE3NanoStatus = 3
                testResult.append(result)

        return testResult

    def _handle_sftp_prompt(self, child):
        # ateConfig.log.logger.debug('Expecting prompt...')
        i = child.expect(['.*password:.*', pexpect.EOF])
        # ateConfig.log.logger.debug(child.after)
        if i == 0:
            ateConfig.log.logger.debug('Supplying pass to sftp server')
            child.sendline(self._password)
            ateConfig.log.logger.debug('sent pw')
            self._handle_sftp_prompt(child)

        if i == 1:
            ateConfig.log.logger.debug('EOF')

        else:
            ateConfig.log.logger.debug('Invalid case')

    def ping(self, ip):
        # ping_command = ['ping', ip, '-n', '1'] instead of ping_command = ['ping', ip, '-n 1'] for Windows
        ping_command = ['ping', ip, '-c 1']
        ping_output = subprocess.run(ping_command, shell=False, stdout=subprocess.PIPE)
        success = ping_output.returncode
        return True if success == 0 else False



controller = Controller()
