#!/usr/bin/env python
"""
LEDUniformingTestATE3 Class
Author: Robert Vo
Created: 2018 May 15
Updated: 2018 Dec 3

Description:
Implementation of the LED Uniforming Test class.
This class is the method in which ATE detect
LED uniform in FL.
"""
import time
from configuration import nanoConfig
from configuration.nanoConfig import *
from configuration.cvConfig import *
# from configuration.bleConfig import *
from tests.test import Test
# import tests.scenario
import cv2
import datetime
import numpy
import os

command = {'name': 'LED Uniforming ATE3 Test Nano',
           'component': 'LED',
           'commands': [
               # Process images and determine if any LEDs are malfunctioning.
               {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'LEDOn', 'y': 0,
                'yDist': CAMERA_RESOLUTION_Y / 2, 'x': 0, 'xDist': CAMERA_RESOLUTION_X / 2, 'outImagePath': DIANA_IMAGE,'outImageName': '1stCrop'},
               {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'LEDOn',
                'y': CAMERA_RESOLUTION_Y / 2, 'yDist': CAMERA_RESOLUTION_Y, 'x': 0, 'xDist': CAMERA_RESOLUTION_X / 2,'outImagePath': DIANA_IMAGE, 'outImageName': '2ndCrop'},
               {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'LEDOn', 'y': 0,
                'yDist': CAMERA_RESOLUTION_Y / 2, 'x': CAMERA_RESOLUTION_X / 2, 'xDist': CAMERA_RESOLUTION_X, 'outImagePath': DIANA_IMAGE, 'outImageName': '3rdCrop'},
               {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'LEDOn',
                'y': CAMERA_RESOLUTION_Y / 2, 'yDist': CAMERA_RESOLUTION_Y, 'x': CAMERA_RESOLUTION_X / 2, 'xDist': CAMERA_RESOLUTION_X, 'outImagePath': DIANA_IMAGE, 'outImageName': '4thCrop'},

               # Analyze histogram each section image
                {'type': 'cv', 'operation': 'analyzeHist', 'imageOnePath': DIANA_IMAGE, 'imageOneName': '1stCrop',
                'outImagePath': DIANA_IMAGE, 'outImageName': '1stCropHist', 'kernel':KERNEL5, 'limits':['0', '18']},
                {'type': 'cv', 'operation': 'analyzeHist', 'imageOnePath': DIANA_IMAGE, 'imageOneName': '2ndCrop',
                'outImagePath': DIANA_IMAGE, 'outImageName': '2ndCropHist', 'kernel':KERNEL5, 'limits':['0', '18']},
                {'type': 'cv', 'operation': 'analyzeHist', 'imageOnePath': DIANA_IMAGE, 'imageOneName': '3rdCrop',
                'outImagePath': DIANA_IMAGE, 'outImageName': '3rdCropHist', 'kernel':KERNEL5, 'limits':['0', '18']},
                {'type': 'cv', 'operation': 'analyzeHist', 'imageOnePath': DIANA_IMAGE, 'imageOneName': '4thCrop',
                'outImagePath': DIANA_IMAGE, 'outImageName': '4thCropHist', 'kernel':KERNEL5, 'limits':['0', '18']},
           ]
           }


class LEDUniformingTestATE3Nano(Test):
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
        :return: histogram correlation between image sections
        '''
        nanoConfig.log.logger.info('=====================================================================')
        nanoConfig.log.logger.info('   Test Started   - ' + self._name)
        nanoConfig.log.logger.info('=====================================================================')

        cmdResponse = ''
        startTime = time.time()
        result = {}
        res = {}
        testRes = []
        hist_value = []
        # internal_SN = (tests.scenario.Scenario.ateTestAttr['internal_serial_number'])
        internal_SN = '1234567890'
        filetimestamp = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H%M_%S")
        i = 1
        average_led1 = 0
        average_led2 = 0
        average_led3 = 0
        average_led4 = 0
        average_values = []

        try:
            # Execute all commands in the command list.
            for cmd in self._cmdList:
                cmdResponse = cmd.execute()

                # Don't append histogram: it's data is so long
                if cmd.operation != 'analyzeHist':
                    self._testResult['cmdResults'].append(cmdResponse)

                if type(cmdResponse) == str and 'Error' in cmdResponse:
                    self._testResult['name'] = 'LED Uniforming Test ATE3'
                    self._testResult['passed'] = False
                    self._testResult['error'] = cmdResponse
                    self.calcTestDuration(startTime)
                    return self._testResult

                elif cmd.type == 'cv' and cmd.operation == 'analyzeHist':
                    if cmdResponse == {}:
                        nanoConfig.log.logger.info('LED_' + str(i) + ' is failed')
                        result['average_led'+str(i)] = 0
                        nanoConfig.log.logger.info('Average of LED_' + str(i) + ' : 0')
                        average_values.append(result['average_led' + str(i)])
                        testRes.append(False)
                    else:
                        res['LED_' + str(i)] = cmdResponse
                        # mean_hist = numpy.mean(res['LED_' + str(i)]['hist'])
                        # res['LED_' + str(i) + '_mean_hist'] = round(float(mean_hist), 2)
                        average = 0
                        if i == 1:
                            img_led1 = cv2.imread(DIANA_IMAGE + '1stCropHist.jpeg')
                            average_led1 = np.mean(img_led1)
                            average = average_led1
                        elif i == 2:
                            img_led2 = cv2.imread(DIANA_IMAGE + '2ndCropHist.jpeg')
                            average_led2 = np.mean(img_led2)
                            average = average_led2
                        elif i == 3:
                            img_led3 = cv2.imread(DIANA_IMAGE + '3rdCropHist.jpeg')
                            average_led3 = np.mean(img_led3)
                            average = average_led3
                        else:
                            img_led4 = cv2.imread(DIANA_IMAGE + '4thCropHist.jpeg')
                            average_led4 = np.mean(img_led4)
                            average = average_led4
                        result['average_led'+str(i)] = round(float(average), 2)
                        average_values.append(result['average_led'+str(i)])
                        nanoConfig.log.logger.info('Average of LED_' + str(i)+ ' : %s' %average)
                        if average > cmd.lowerLimit and average <= cmd.upperLimit:
                            testRes.append(True)
                        else:
                            nanoConfig.log.logger.info('LED_' + str(i) + ' failed. Average of image: %s. Range: [%s, %s]' % (average, cmd.lowerLimit, cmd.upperLimit))
                            testRes.append(False)
                    # hist_value.append(res['LED_' + str(i) + '_mean_hist'])
                    i += 1
                # BLE command timed out.
                elif cmd.type == 'ble' and cmdResponse['timeout']:
                    self._testResult['error'] = 'BLE connection timed out.'
                    testRes.append(False)
                    result['data'] = None
                    break  # Break out of loop because connection has timed out.

            #Calculate average, percentage between led regions
            min_average = min(average_values)
            max_average = max(average_values)
            nanoConfig.log.logger.info('Min of LED: %s' %min_average)
            nanoConfig.log.logger.info('Max of LED: %s' %max_average)

            if max_average > 0 and min_average > 0:
                #Comparision
                percentage = round(min_average/max_average*100)
                nanoConfig.log.logger.info('Ratio between min and max: %s' %percentage + '%')
                result['average_per']= percentage
                #If the smallest value >= 80% the biggest value --> Pass
                if percentage >= 1:
                    testRes.append(True)
                else:
                    testRes.append(False)
            else:
                testRes.append(False)
                result['average_per'] = 0

            # Draw LED position and save image to local
            image = cv2.imread(DIANA_IMAGE_RAW + 'LEDOn.jpeg')
            if average_led1 > 0:
                # 1st LED location
                LED_1 = res['LED_1']['led']
                cv2.ellipse(image, LED_1, (0, 0, 255), 2)

            if average_led2 > 0:
                # 2nd LED location
                x2 = int(res['LED_2']['led'][0][0])
                y2 = int(res['LED_2']['led'][0][1] + CAMERA_RESOLUTION_Y / 2)
                LED_2 = ((x2, y2), res['LED_2']['led'][1], res['LED_2']['led'][2])
                cv2.ellipse(image, LED_2, (0, 0, 255), 2)
            if average_led3 > 0:
                # 3rd LED location
                x3 = int(res['LED_3']['led'][0][0] + CAMERA_RESOLUTION_X / 2)
                y3 = int(res['LED_3']['led'][0][1])
                LED_3 = ((x3, y3), res['LED_3']['led'][1], res['LED_3']['led'][2])
                cv2.ellipse(image, LED_3, (0, 0, 255), 2)
            if average_led4 > 0:
                # 4th LED location
                x4 = int(res['LED_4']['led'][0][0] + CAMERA_RESOLUTION_X / 2)
                y4 = int(res['LED_4']['led'][0][1] + CAMERA_RESOLUTION_Y / 2)
                LED_4 = ((x4, y4), res['LED_4']['led'][1], res['LED_4']['led'][2])
                cv2.ellipse(image, LED_4, (0, 0, 255), 2)
            cv2.putText(image, 'LED 1: %s' % result['average_led1'], (50, 100), cv2.FONT_ITALIC, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, 'LED 2: %s' % result['average_led2'], (50, 170), cv2.FONT_ITALIC, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, 'LED 3: %s' % result['average_led3'], (50, 240), cv2.FONT_ITALIC, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, 'LED 4: %s' % result['average_led4'], (50, 310), cv2.FONT_ITALIC, 2, (255, 255, 255), 2, cv2.LINE_AA)
            image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
            cv2.imwrite(PROCESSED_IMAGES + "LED_Uniform_ATE3_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image)

            # Remove captured file
            # os.remove(DIANA_IMAGE + 'LEDOn.jpeg')
            os.remove(DIANA_IMAGE + '1stCrop.jpeg')
            os.remove(DIANA_IMAGE + '2ndCrop.jpeg')
            os.remove(DIANA_IMAGE + '3rdCrop.jpeg')
            os.remove(DIANA_IMAGE + '4thCrop.jpeg')

            nanoConfig.log.logger.debug("File Removed!")

            if False in testRes:
                self._testResult['passed'] = False
                nanoConfig.log.logger.info(self._name + ' failed.')
            else:
                self._testResult['passed'] = True
                nanoConfig.log.logger.info(self._name + ' passed.')

            self._testResult['data'] = result
            nanoConfig.log.logger.info('   Test Result: %s' % result)
            nanoConfig.log.logger.info('   Test Completed - ' + self._name)

            self.calcTestDuration(startTime)

            return self._testResult

        except Exception as exc:
            result['error'] = str(exc)
            self._testResult['name'] = 'LED Uniforming ATE3 Test Nano'
            self._testResult['passed'] = False
            self._testResult['data'] = result
            self.calcTestDuration(startTime)
            return self._testResult
