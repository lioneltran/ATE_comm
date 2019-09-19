#!/usr/bin/env python
"""
HandDragTest Class
Created: 2018 May 14
Author: Robert Vo
Updated: 2019 Sep 18 by Lionel Tran

Description:
Implementation of HandDragTest class.
This class is the method in which ATE detect
hand position after moving to specific position.
"""
import time as time
from configuration.ateConfig import *
from configuration.cvConfig import *
# from configuration import nanoConfig
# from configuration.bleConfig import *
from tests.test import Test
import cv2
import datetime
# import tests.scenario
import os
import math

command = {'name': 'Hand Drag Test Nano',
           'component': 'Movement',
           'commands': [
                        #Subtract white background image to baclk background image to get dial position
                       {'type': 'cv', 'operation': 'subtract', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'dial_12hour',
                        'imageTwoPath': DIANA_IMAGE_RAW, 'imageTwoName': 'hand_drag_12hour',
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'getDial', 'kernel': KERNEL1},

                        # Find watch dial region based on pinion detect (find white color area with bigger area)
                        {'type': 'cv', 'operation': 'findPinion', 'imageOnePath': DIANA_IMAGE,
                        'imageOneName': 'getDial', 'outImagePath': DIANA_IMAGE, 'outImageName': 'watchDial'},

                       #Subtract original image to 6:00 image
                       {'type': 'cv', 'operation': 'subtract', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'hand_drag_12hour',
                        'imageTwoPath': DIANA_IMAGE_RAW, 'imageTwoName': 'black_dial_6hour',
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'subtractOrginal', 'kernel': KERNEL1},

                       # Detect hand position
                       {'type': 'cv', 'operation': 'findHand', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'subtractOrginal',
                        'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'handDialMask',
                        'kernel': KERNEL11, 'hands': '1'},

                       #Subtract 6:00 image to original image
                       {'type': 'cv', 'operation': 'subtract', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'black_dial_6hour',
                        'imageTwoPath': DIANA_IMAGE_RAW, 'imageTwoName': 'hand_drag_12hour',
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'subtract6hour', 'kernel': KERNEL1},

                       # Detect hand position
                       {'type': 'cv', 'operation': 'findHand', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'subtract6hour',
                        'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'handDialMask',
                        'kernel': KERNEL11, 'hands': '2', 'limits':['177', '183']},

                       # Subtract 12:00 image to original image
                       {'type': 'cv', 'operation': 'subtract', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'black_dial_12hour',
                        'imageTwoPath': DIANA_IMAGE_RAW, 'imageTwoName': 'hand_drag_12hour',
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'subtract12hour', 'kernel': KERNEL1},

                       # Detect hand position
                       {'type': 'cv', 'operation': 'findHand', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'subtract12hour',
                        'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'handDialMask',
                        'kernel': KERNEL9, 'hands': '2', 'limits':['3']},

                       ]
           }


class HandDragTestNano(Test):
    def __init__(self):
        '''
        This function initializes the class and sets up the command flow.
        '''

        super().__init__(command)
        self.setup()

    def setup(self):
        '''
        This function creates the command objects and appends them to the command list.
        :return: None
        '''

        self._name = command['name']
        self._commands = command['commands']

        # Create each command object and append it to the command list.
        for cmd in self._commands:
            cmdObject = self._cmdFactory.createCmdObject(cmd)
            self._cmdList.append(cmdObject)

    def execute(self):
        '''
        This function executes each function in the command list.
        The results are stored into a result dictionary containing
        all of the information of the test.
        :return:
        - Distance from fudical and test point to Rectangle edge
        - Angle between rectangle bottom edge and horizontal
        '''
        ateConfig.log.logger.info('=====================================================================')
        ateConfig.log.logger.info('   Test Started   - ' + self._name)
        ateConfig.log.logger.info('=====================================================================')
        cmdResponse = ''
        startTime = time.time()
        # internal_SN = (tests.scenario.Scenario.ateTestAttr['internal_serial_number'])
        internal_SN = '1234567890'
        filetimestamp = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H%M_%S")
        result = {}
        testRes = []
        original_hand = {}
        offset_angle = 0
        try:
            # Execute all commands in the command list.
            for cmd in self._cmdList:

                cmdResponse = cmd.execute()

                self._testResult['cmdResults'].append(cmdResponse)

                if type(cmdResponse) == str and 'Error' in cmdResponse:
                    self._testResult['name'] = 'Hand Drag Test Nano'
                    self._testResult['passed'] = False
                    self._testResult['error'] = cmdResponse
                    self.calcTestDuration(startTime)
                    return self._testResult

                if cmd.type == 'cv' and cmd.operation == 'findPinion':
                    if cmdResponse != {}:
                        ellipse = cmdResponse['pinion']
                        #Create a dial mask to remove noise outside dial
                        mask = np.zeros((int(CAMERA_RESOLUTION_Y), int(CAMERA_RESOLUTION_X)), np.uint8)
                        cv2.circle(mask, (int(ellipse[0][0]), int(ellipse[0][1])), int(ellipse[1][1] / 2), (255, 255, 255), -1)
                        cv2.imwrite(DIANA_IMAGE+'handDialMask.jpeg', mask)

                elif cmd.type == 'cv' and cmd.operation == 'findHand' and cmd._imageOneName == 'subtractOrginal':
                    # result['original'] = cmdResponse
                    if len(cmdResponse['hand_angle']) == 1:
                        # get hand angle at orginal
                        if cmdResponse['hand_angle'][0] < 90:
                            offset_angle = round(cmdResponse['hand_angle'][0], 2)
                        else:
                            offset_angle = round(cmdResponse['hand_angle'][0] - 360, 2)
                        result['offset_angle'] = offset_angle
                        ellipse = cmdResponse['ellipse']
                        original_hand['ellipse'] = ellipse
                        ateConfig.log.logger.info('Offset angle: %s' %offset_angle)
                        # draw hands and write hand angle on image
                        image = cv2.imread(DIANA_IMAGE_RAW + 'hand_drag_12hour.jpeg')
                        cv2.ellipse(image, ellipse[0], (0, 0, 255), 4)
                        cv2.putText(image, 'offset_angle: %s' % offset_angle, (50, 50), cv2.FONT_ITALIC, 2,(255, 255, 255), 2, cv2.LINE_AA)
                        # save image
                        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
                        # cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "HandDrag_Offset_" + internal_SN + "_" + str(filetimestamp) + ".jpeg",image)
                        cv2.imwrite(PROCESSED_IMAGES + "HandDrag_Offset_" + internal_SN + "_" + str(filetimestamp) + ".jpeg",image)
                    else:
                        testRes.append(False)
                        ateConfig.log.logger.info('Cannot detect hands. Hands may be not move')
                        image = cv2.imread(DIANA_IMAGE_RAW + 'hand_drag_12hour.jpeg')
                        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
                        # cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "HandDrag_Offset_" + internal_SN + "_" + str(filetimestamp) + ".jpeg",image)
                        cv2.imwrite(PROCESSED_IMAGES + "HandDrag_Offset_" + internal_SN + "_" + str(filetimestamp) + ".jpeg",image)
                        break

                elif cmd.type == 'cv' and cmd.operation == 'findHand' and cmd._imageOneName == 'subtract6hour':
                    image = cv2.imread(DIANA_IMAGE_RAW + 'black_dial_6hour.jpeg')
                    #SW cannot detect hands
                    if (len(cmdResponse['hand_angle'])) == 0:
                        testRes.append(False)
                        ateConfig.log.logger.info('Cannot detect hands')
                        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
                        cv2.imwrite(PROCESSED_IMAGES + "HandDrag_6hour_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image)
                    #SW detect hands
                    else:
                        #Get hands angles
                        minute_hand = round(abs(cmdResponse['hand_angle'][0] - offset_angle), 2)
                        hour_hand = round(abs(cmdResponse['hand_angle'][1] - offset_angle), 2)
                        ateConfig.log.logger.info('Minute hand : %s' % (minute_hand))
                        ateConfig.log.logger.info('Hour hand   : %s' % (hour_hand))
                        result['6_00_hands_angle'] = [hour_hand, minute_hand]
                        if ((abs(minute_hand) < cmd.lowerLimit or abs(minute_hand) > cmd.upperLimit)) or ((abs(hour_hand) < cmd.lowerLimit or abs(hour_hand) > cmd.upperLimit)):
                            testRes.append(False)
                            ateConfig.log.logger.info('Hand at wrong position')
                        else:
                            testRes.append(True)
                            ateConfig.log.logger.info('Hand at 6:00 position')

                        cv2.putText(image, 'Minute Angle: %s' % minute_hand, (50, 50), cv2.FONT_ITALIC, 2, (0, 0, 255),2, cv2.LINE_AA)
                        cv2.putText(image, 'Hour   Angle: %s' % hour_hand, (50, 120), cv2.FONT_ITALIC, 2, (0, 0, 255), 2, cv2.LINE_AA)
                        for i in range(len(cmdResponse['ellipse'])):
                            cv2.ellipse(image, cmdResponse['ellipse'][i], (0, 0, 255), 4)
                        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
                        # cv2.imwrite( tests.scenario.Scenario.ateTestAttr['logPath'] + "HandDrag_6hour_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image)
                        cv2.imwrite( PROCESSED_IMAGES + "HandDrag_6hour_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image)
                    # Remove files
                    os.remove(DIANA_IMAGE + 'subtract6hour.jpeg')

                elif cmd.type == 'cv' and cmd.operation == 'findHand' and cmd._imageOneName == 'subtract12hour':
                    image = cv2.imread(DIANA_IMAGE_RAW + 'black_dial_12hour.jpeg')
                    if (len(cmdResponse['hand_angle'])) == 0:
                        testRes.append(True)
                        result['12_00_hands_angle'] = [0, 0]
                        ateConfig.log.logger.info('Minute hand : 0')
                        ateConfig.log.logger.info('Hour hand   : 0')
                        ateConfig.log.logger.info('Hand at 12:00 position')
                        cv2.putText(image, 'Minute Angle: 0', (50, 50), cv2.FONT_ITALIC, 2, (0, 0, 255),2, cv2.LINE_AA)
                        cv2.putText(image, 'Hour   Angle: 0', (50, 120), cv2.FONT_ITALIC, 2, (0, 0, 255), 2, cv2.LINE_AA)
                        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
                        # cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "HandDrag_12hour_" + internal_SN + "_" + str(filetimestamp) + ".jpeg",image)
                        cv2.imwrite(PROCESSED_IMAGES + "HandDrag_12hour_" + internal_SN + "_" + str(filetimestamp) + ".jpeg",image)
                    else:
                        minute_hand = round(abs(cmdResponse['hand_angle'][0] - offset_angle), 2)
                        hour_hand = round(abs(cmdResponse['hand_angle'][1] - offset_angle), 2)
                        if minute_hand > 270:
                            minute_hand = round(360 - minute_hand, 2)
                        if hour_hand > 270:
                            hour_hand = round(360 - hour_hand, 2)
                        ateConfig.log.logger.info('Minute hand : %s' % (minute_hand))
                        ateConfig.log.logger.info('Hour hand   : %s' % (hour_hand))
                        result['12_00_hands_angle'] = [hour_hand, minute_hand]
                        if abs(minute_hand) > cmd.limits or abs(hour_hand) > cmd.limits:
                            testRes.append(False)
                            ateConfig.log.logger.info('Hands at wrong position')
                        else:
                            testRes.append(True)
                            ateConfig.log.logger.info('Hands at 12:00 position')
                        for i in range(len(cmdResponse['ellipse'])):
                            cv2.ellipse(image, cmdResponse['ellipse'][i], (0, 0, 255), 4)

                        cv2.putText(image, 'Minute Angle: %s' % minute_hand, (50, 50), cv2.FONT_ITALIC, 2, (0, 0, 255),2, cv2.LINE_AA)
                        cv2.putText(image, 'Hour   Angle: %s' % hour_hand, (50, 120), cv2.FONT_ITALIC, 2, (0, 0, 255), 2, cv2.LINE_AA)
                        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
                        cv2.imwrite(PROCESSED_IMAGES + "HandDrag_12hour_" + internal_SN + "_" + str(filetimestamp) + ".jpeg",image)
                    #Remove image
                    os.remove(DIANA_IMAGE + 'subtract12hour.jpeg')
                # BLE command timed out.
                elif cmd.type == 'ble' and cmdResponse['timeout']:
                    self._testResult['error'] = 'BLE connection timed out.'
                    testRes.append(False)
                    result['data'] = None
                    break  # Break out of loop because connection has timed out.

            # Remove captured file
            # os.remove(DIANA_IMAGE + 'hand_drag_12hour.jpeg')
            # os.remove(DIANA_IMAGE + 'dial_12hour.jpeg')
            # os.remove(DIANA_IMAGE + '6hour.jpeg')
            # os.remove(DIANA_IMAGE + '12hour.jpeg')
            os.remove(DIANA_IMAGE + 'subtractOrginal.jpeg')
            ateConfig.log.logger.debug("File Removed!")

            if False in testRes:
                self._testResult['passed'] = False
                ateConfig.log.logger.info(self._name + ' failed')
            else:
                self._testResult['passed'] = True
                ateConfig.log.logger.info(self._name + ' passed.')

            self._testResult['data'] = result
            ateConfig.log.logger.info('   Test Result: %s' % result)
            ateConfig.log.logger.info('   Test Completed - ' + self._name)

            self.calcTestDuration(startTime)

            return self._testResult


        except Exception as exc:
            result['error'] = str(exc)
            self._testResult['name'] = 'Hand Drag Test Nano'
            self._testResult['passed'] = False
            self._testResult['data'] = result
            self.calcTestDuration(startTime)
            return self._testResult