#!/usr/bin/env python
"""
circlesConcentricityTest Class
Created: 2019 Aug 29
Description:
Implementation of the circles Concentricity Test class.
This class is the method in which ATE measure distance
between center of pinion and center of eink screen.
"""
import time
from configuration import nanoConfig
from configuration.nanoConfig import *
from configuration.cvConfig import *
# from configuration.bleConfig import *
from tests.test import Test
# from commands.bleCmd import BleCmd
# import tests.scenario
import cv2
import datetime
import numpy
import math
import os

command = {'name': 'Circles Concentricity ATE3 Test Nano',
           'component': 'EInk',
           'commands': [
                        #Find platform dial
                       {'type': 'cv', 'operation': 'findPlatform', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'black_dial_6hour'},

                       # Crop processed image
                       {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'dial_6hour',
                        'y': CONCENTRICITY_CROP_Y1, 'yDist': CONCENTRICITY_CROP_Y2, 'x': CONCENTRICITY_CROP_X1, 'xDist': CONCENTRICITY_CROP_X2,
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'dial_6hour_Crop'},

                       # Crop processed image
                       {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'dial_12hour',
                        'y': CONCENTRICITY_CROP_Y1, 'yDist': CONCENTRICITY_CROP_Y2, 'x': CONCENTRICITY_CROP_X1, 'xDist': CONCENTRICITY_CROP_X2,
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'dial_12hour_Crop'},

                       {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'black_dial_6hour',
                        'y': CONCENTRICITY_CROP_Y1, 'yDist': CONCENTRICITY_CROP_Y2, 'x': CONCENTRICITY_CROP_X1, 'xDist': CONCENTRICITY_CROP_X2,
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'black_dial_6hour_crop'},

                        # Crop processed image
                        {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'black_dial_12hour',
                        'y': CONCENTRICITY_CROP_Y1, 'yDist': CONCENTRICITY_CROP_Y2, 'x': CONCENTRICITY_CROP_X1, 'xDist': CONCENTRICITY_CROP_X2,
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'black_dial_12hour_crop'},

                       # Crop processed image
                       {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'circle_12hour',
                        'y': CONCENTRICITY_CIRLCE_CROP_Y1, 'yDist': CONCENTRICITY_CIRLCE_CROP_Y2, 'x': CONCENTRICITY_CIRLCE_CROP_X1, 'xDist': CONCENTRICITY_CIRLCE_CROP_X2,
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'circle_12hour_Crop'},

                        # Crop processed image
                       {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'circle_6hour',
                        'y': CONCENTRICITY_CIRLCE_CROP_Y1, 'yDist': CONCENTRICITY_CIRLCE_CROP_Y2, 'x': CONCENTRICITY_CIRLCE_CROP_X1, 'xDist': CONCENTRICITY_CIRLCE_CROP_X2,
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'circle_6hour_Crop'},

                        {'type': 'cv', 'operation':'subtract','imageOnePath':DIANA_IMAGE,'imageOneName':'dial_6hour_Crop', 'imageTwoPath':DIANA_IMAGE, 'imageTwoName':'black_dial_6hour_crop',
                        'outImagePath':DIANA_IMAGE, 'outImageName':'subtractImage6hour', 'kernel':KERNEL1},

                        {'type': 'cv', 'operation':'subtract','imageOnePath':DIANA_IMAGE,'imageOneName':'dial_12hour_Crop', 'imageTwoPath':DIANA_IMAGE, 'imageTwoName':'black_dial_12hour_crop',
                        'outImagePath':DIANA_IMAGE, 'outImageName':'subtractImage12hour', 'kernel':KERNEL1},

                        # Find dial circle
                       {'type': 'cv', 'operation': 'findDial', 'imageOnePath': DIANA_IMAGE, 'dialPlatform': 'black', 'threshold': DIAL_BINARY_THRESHOLD,
                        'imageOneName': 'subtractImage6hour', 'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'subtractImage12hour',
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'maskDial', 'kernel': KERNEL3},

                       # Find eInk Circle
                       {'type': 'cv', 'operation': 'findEinkCircle', 'imageOnePath': DIANA_IMAGE, 'threshold': CENTER_CIRCLE_THRESHOLD,
                        'imageOneName': 'circle_12hour_Crop', 'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'circle_6hour_Crop',
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'eInkCircle', 'kernel': KERNEL5, 'dial': ''},

                        # Crop rectangle image
                        {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'rectangle',
                        'y': ALIGN_RECT_CROP_Y_1, 'yDist': ALIGN_RECT_CROP_Y_2, 'x': ALIGN_RECT_CROP_X_1, 'xDist': ALIGN_RECT_CROP_X_2,
                        'outImagePath': DIANA_IMAGE, 'outImageName': 'rect_crop'},

                        {'type': 'cv', 'operation': 'findRect', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'rect_crop',
                        'kernel': KERNEL1, 'outImagePath': ALIGNMENT_IMAGE, 'outImageName': 'Rectangle'},

                   ]
           }


class CirclesConcentricityTestATE3Nano(Test):
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
        :return: The distance between pinion center and eInk center
        '''
        nanoConfig.log.logger.info('=====================================================================')
        nanoConfig.log.logger.info('   Test Started   - ' + self._name)
        nanoConfig.log.logger.info('=====================================================================')
        cmdResponse = ""
        startTime = time.time()
        results = {}
        result = {}
        result['Dial'] = {}
        result['eInk'] = {}
        dialCenter = ''
        testRes = []
        circle_dial = ""
        circle_eInk = ""
        platform = ''
        threshold = ''
        inv_threshold = ''
        image_ratio = 0
        res = {}
        # internal_SN = (tests.scenario.Scenario.ateTestAttr['internal_serial_number'])
        internal_SN = '1234567890'
        filetimestamp = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H%M_%S")

        try:
            # Execute all commands in the command list.
            for cmd in self._cmdList:
                if cmd.operation == 'findEinkCircle':
                    cmd._dial = dialCenter
                    # cmd._threshold = inv_threshold
                # if cmd.operation == 'crop' and cmd._imageOneName == 'dial_6hour' and platform == 'white':
                #     cmd._imageOneName = 'black_dial_6hour'
                # elif cmd.operation == 'crop' and cmd._imageOneName == 'dial_12hour' and platform == 'white':
                #     cmd._imageOneName = 'black_dial_12hour'
                # if cmd.operation == 'findDial':
                #     cmd._dialPlatform = 'black'
                #     cmd._threshold = threshold

                cmdResponse = cmd.execute()
                self._testResult['cmdResults'].append(cmdResponse)

                if type(cmdResponse) == str and 'Error' in cmdResponse:
                    self._testResult['name'] = 'Circles Concentricity ATE3 Test Nano'
                    self._testResult['passed'] = False
                    self._testResult['error'] = cmdResponse
                    self.calcTestDuration(startTime)
                    return self._testResult

                if cmd.type == 'cv' and cmd.operation == 'findDial':
                    result['Dial'] = cmdResponse
                    if result['Dial'] == {}:
                        testRes.append(False)
                        nanoConfig.log.logger.info('Cannot find dial')
                        break
                    else:
                        result['xDial'] = int(result['Dial']['dial'][0][0] + CONCENTRICITY_CROP_X1)
                        result['yDial'] = int(result['Dial']['dial'][0][1] + CONCENTRICITY_CROP_Y1)
                        nanoConfig.log.logger.info('Dial data: %s' % result['Dial'])
                        circle_dial = ((result["xDial"], result['yDial']), result['Dial']['dial'][1])
                        results['rDial'] = result['Dial']['dial'][1]
                        #Get circle center after cropping image
                        xCenter = int(result['xDial'] - CONCENTRICITY_CIRLCE_CROP_X1)
                        yCenter = int(result['yDial'] - CONCENTRICITY_CIRLCE_CROP_Y1)
                        dialCenter = (xCenter, yCenter)
                elif cmd.type == 'cv' and cmd.operation == 'findEinkCircle':
                    result['eInk'] = cmdResponse
                    if result['eInk'] == {}:
                        testRes.append(False)
                        nanoConfig.log.logger.info('Cannot find eInk circle')
                        break
                    else:
                        result["xEInk"] = int(result['eInk']['circle'][0][0] + CONCENTRICITY_CIRLCE_CROP_X1)
                        result['yEInk'] = int(result['eInk']['circle'][0][1] + CONCENTRICITY_CIRLCE_CROP_Y1)
                        circle_eInk = ((result["xEInk"], result['yEInk']), result['eInk']['circle'][1])
                        results['rEInk'] = result['eInk']['circle'][1]
                        nanoConfig.log.logger.info('EInk data: %s' % result['eInk'])
                # elif cmd.type == 'cv' and cmd.operation == 'findPlatform':
                #     res = cmdResponse
                #     platform = res['platform']
                #     threshold = res['threshold']
                #     inv_threshold = res['inv_threshold']

                elif cmd.type == 'cv' and cmd.operation == 'findRect':
                    res['Rect'] = cmdResponse
                    if res['Rect'] == {}:
                        testRes.append(False)
                        nanoConfig.log.logger.info('Cannot detect rectangle')
                        break
                    else:
                        points = res['Rect']['points']
                        dist = []
                        # check left rotation or right rotation via compare distance between 1st-2nd points vs 1st-4th points
                        dist12 = math.sqrt((points[0][0] - points[1][0]) ** 2 + (points[0][1] - points[1][1]) ** 2)
                        dist.append(dist12)
                        dist23 = math.sqrt((points[2][0] - points[1][0]) ** 2 + (points[2][1] - points[1][1]) ** 2)
                        dist.append(dist23)
                        dist34 = math.sqrt((points[2][0] - points[3][0]) ** 2 + (points[2][1] - points[3][1]) ** 2)
                        dist.append(dist34)
                        dist14 = math.sqrt((points[0][0] - points[3][0]) ** 2 + (points[0][1] - points[3][1]) ** 2)
                        dist.append(dist14)
                        dist.sort()
                        #Calculate ratio between real image vs EInk
                        #Length of rectangle: 40 pixel in pixel
                        image_ratio = round(((dist[2]+dist[3])/2)/40, 4)
                        # print(dist)
                        nanoConfig.log.logger.info("ratio: %s" %image_ratio)
                        results['ratio'] = image_ratio

                # BLE command timed out.
                elif cmd.type == 'ble' and cmdResponse['timeout']:
                    self._testResult['error'] = 'BLE connection timed out.'
                    testRes.append(False)
                    result['data'] = None
                    break  # Break out of loop because connection has timed out.
            if result['eInk'] != {} and result['Dial'] != {} and res['Rect'] != {}:
                # Calculate distance between pinion center and eink center
                dist = round(math.sqrt((result['xEInk'] - result['xDial']) ** 2 + (result['yEInk'] - result['yDial']) ** 2), 2)
                results['distance'] = dist
                # Calculat distance in mm
                '''
                EInk: 240 pixels
                Diameter: 27.96mm
                --> 1 pixel: 27.96/240 = 0.1165mm
                --> 1 pixel in image: 0.1165/image_ratio
                '''
                dist_mm = round(dist * 0.1165 / image_ratio, 4)
                results['distance_mm'] = dist_mm
                nanoConfig.log.logger.info('Distance between 2 centers: %s (mm)' % dist_mm)
                if dist_mm >= MAX_DIST_TWO_CENTERS:
                    testRes.append(False)
                else:
                    testRes.append(True)
                    self._testResult['passed'] = True

                # Draw ellipses (approximately circles) in Pinion and eInk Center
                image = cv2.imread(DIANA_IMAGE_RAW + 'circle_12hour.jpeg')
                cv2.circle(image, circle_eInk[0], circle_eInk[1], (0, 0, 255), 2)
                cv2.circle(image, circle_dial[0], circle_dial[1], (0, 0, 255), 2)
                cv2.putText(image, 'Distance: '+str(dist) + '(' + str(results['distance_mm']) +'mm)', (50, 100), cv2.FONT_ITALIC, 2, (255, 255, 255), 2, cv2.LINE_AA)

                # Write image to local
                image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
                # cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "Concentricity_ATE3_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image)
                cv2.imwrite(PROCESSED_IMAGES + "Concentricity_ATE3_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image)
            else:
                testRes.append(False)
                image = cv2.imread(DIANA_IMAGE_RAW + 'circle_12hour.jpeg')
                image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
                cv2.imwrite(PROCESSED_IMAGES + "Concentricity_ATE3_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image)

            nanoConfig.log.logger.debug("File Removed!")

            if False in testRes:
                self._testResult['passed'] = False
            else:
                self._testResult['passed'] = True

            self._testResult['data'] = results
            nanoConfig.log.logger.info('   Test Result: %s ' % self._testResult['data'])
            nanoConfig.log.logger.info('   Test Completed - ' + self._name)

            self.calcTestDuration(startTime)

            return self._testResult


        except Exception as exc:
            result['error'] = str(exc)
            self._testResult['name'] = 'Circles Concentricity ATE3 Test Nano'
            self._testResult['passed'] = False
            self._testResult['data'] = result
            self.calcTestDuration(startTime)
            return self._testResult
