#!/usr/bin/env python
"""
EInkScreenPixelTest Class
Created: 2018 May 30
Author: Robert Vo
Updated: 2019 Sep 18 by Lionel Tran

Description:
Implementation of the EInk Screen Pixel Test class.
This class is the method in which ATE can measure detect
dead pixel in EInk Screen.
"""
import time
from configuration import ateConfig
from configuration.ateConfig import *
from configuration.cvConfig import *
from configuration.bleConfig import *
from tests.test import Test
# from commands.bleCmd import BleCmd
# import tests.scenario
import cv2
import datetime
import numpy
import math
import os

command = {'name': 'EInk Screen Pixels ATE3 Test Nano',
           'component': 'EInk',
           'commands': [
                     # Find platform dial
                    {'type': 'cv', 'operation': 'findPlatform', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'black_dial_6hour'},

                    # Crop processed image
                    # Crop rectangle image
                    {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'rectangle',
                    'y': ALIGN_RECT_CROP_Y_1, 'yDist': ALIGN_RECT_CROP_Y_2, 'x': ALIGN_RECT_CROP_X_1, 'xDist': ALIGN_RECT_CROP_X_2,
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'Rect_Crop'},

                    # {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'dial_6hour',
                    # 'y': CONCENTRICITY_CROP_Y1, 'yDist': CONCENTRICITY_CROP_Y2, 'x': CONCENTRICITY_CROP_X1, 'xDist': CONCENTRICITY_CROP_X2,
                    # 'outImagePath': DIANA_IMAGE, 'outImageName': 'Image600_Crop'},
                    #
                    # # Crop processed image
                    # {'type': 'cv', 'operation': 'crop', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'dial_12hour',
                    # 'y': CONCENTRICITY_CROP_Y1, 'yDist': CONCENTRICITY_CROP_Y2, 'x': CONCENTRICITY_CROP_X1, 'xDist': CONCENTRICITY_CROP_X2,
                    # 'outImagePath': DIANA_IMAGE, 'outImageName': 'Image1200_Crop'},

                    {'type': 'cv', 'operation': 'findRect', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'Rect_Crop',
                    'kernel': KERNEL1, 'outImagePath': ALIGNMENT_IMAGE, 'outImageName': 'Rectangle'},

                   # Black image processing
                   {'type': 'cv', 'operation': 'subtract', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'dial_6hour',
                    'imageTwoPath': DIANA_IMAGE_RAW, 'imageTwoName': 'black_dial_6hour',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'subtractImage600', 'kernel': KERNEL1},

                    {'type': 'cv', 'operation': 'subtract', 'imageOnePath': DIANA_IMAGE_RAW, 'imageOneName': 'dial_12hour',
                    'imageTwoPath': DIANA_IMAGE_RAW, 'imageTwoName': 'black_dial_12hour',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'subtractImage1200', 'kernel': KERNEL1},

                    {'type': 'cv', 'operation': 'findDial', 'imageOnePath': DIANA_IMAGE, 'dialPlatform': 'black',
                    'threshold': DIAL_BINARY_THRESHOLD, 'imageOneName': 'subtractImage600', 'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'subtractImage1200',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'watchDial_Mask', 'kernel': KERNEL9},

                    # get white image one without hands
                   {'type': 'cv', 'operation': 'EjectHands', 'imageOnePath': DIANA_IMAGE_RAW,
                    'imageOneName': 'dial_6hour', 'imageTwoPath': DIANA_IMAGE_RAW, 'imageTwoName': 'dial_12hour',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'white', 'dial': ''},

                    # get black image one without hands
                   {'type': 'cv', 'operation': 'EjectHands', 'imageOnePath': DIANA_IMAGE_RAW,
                    'imageOneName': 'black_dial_6hour', 'imageTwoPath': DIANA_IMAGE_RAW, 'imageTwoName': 'black_dial_12hour',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'black', 'dial': ''},

                    # get white image two without hands
                    {'type': 'cv', 'operation': 'EjectHands', 'imageOnePath': DIANA_IMAGE_RAW,
                    'imageOneName': 'whiteImageTwo600', 'imageTwoPath': DIANA_IMAGE_RAW, 'imageTwoName': 'whiteImageTwo1200',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'white2', 'dial': ''},

                    {'type': 'cv', 'operation': 'subtract', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'white',
                    'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'black',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'subtractImage', 'kernel': KERNEL1},

                    {'type': 'cv', 'operation': 'invBinary', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'subtractImage',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'InvBinary', 'threshold': 70, 'kernel': KERNEL1},

                   # {'type': 'cv', 'operation': 'invBinary', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'subtractImage',
                   #  'outImagePath': DIANA_IMAGE, 'outImageName': 'InvBinary_bottom', 'threshold': 50, 'kernel': KERNEL3},
                   #
                   # {'type': 'cv', 'operation': 'bitwiseOr', 'imageOnePath': DIANA_IMAGE,
                   # 'imageOneName': 'InvBinary_top', 'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'InvBinary_bottom',
                   # 'outImagePath': DIANA_IMAGE, 'outImageName': 'InvBinary'},

                    # {'type': 'cv', 'operation': 'invThreshold', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'subtractImage',
                    # 'outImagePath': DIANA_IMAGE, 'outImageName': 'Median_InvBinary', 'threshold': BLOCK_SIZE,
                    # 'kernel': KERNEL1, 'size': [BLOCK_SIZE, BLOCK_SIZE]},
                    #
                    # {'type': 'cv', 'operation': 'bitwiseOr', 'imageOnePath': DIANA_IMAGE,
                    # 'imageOneName': 'InvBinary', 'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'Median_InvBinary',
                    # 'outImagePath': DIANA_IMAGE, 'outImageName': 'binary_active_region'},

                    # {'type': 'cv', 'operation': 'extract', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'binary_and',
                    # 'outImagePath': DIANA_IMAGE, 'outImageName': 'InvBinaryNotBrand', 'kernel': KERNEL5},

                   {'type': 'cv', 'operation': 'eraseCenter', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'watchDial_Mask',
                    'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'InvBinary',
                    'outImagePath': DIANA_IMAGE, 'outImageName': "erodeCenter", 'kernel': KERNEL1},

                   {'type': 'cv', 'operation': 'findDeadPixels', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'erodeCenter',
                    'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'blackImage',
                    'outImagePath': DEAD_PIXEL_IMAGE, 'outImageName': 'DeadPixelWhiteToBlack', 'limits': ['3']},

                   # White image processing
                   {'type': 'cv', 'operation': 'subtract', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'white',
                    'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'white2',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'subtractImageW', 'kernel': KERNEL1},

                   {'type': 'cv', 'operation': 'binary', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'subtractImageW',
                    'threshold': 30, 'kernel': KERNEL2,
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'binary'},

                    {'type': 'cv', 'operation': 'bitwiseAnd', 'imageOnePath': DIANA_IMAGE,
                    'imageOneName': 'binary', 'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'watchDial_Mask',
                    'outImagePath': DIANA_IMAGE, 'outImageName': 'binary_w_active', 'kernel': KERNEL1},

                   # {'type': 'cv', 'operation': 'basicEdgeDetection', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'binary',
                   #  'kernel': KERNEL1, 'outImagePath': DIANA_IMAGE, 'outImageName': 'edgeDetectionW'},

                   # {'type': 'cv', 'operation': 'opening', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'edgeDetectionW',
                   #  'kernel': KERNEL1, 'outImagePath': DIANA_IMAGE, 'outImageName': 'opening'},

                   # {'type': 'cv', 'operation': 'dilation', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'opening',
                   #  'kernel': KERNEL3, 'outImagePath': DIANA_IMAGE, 'outImageName': 'dilation'},

                   {'type': 'cv', 'operation': 'findDeadPixels', 'imageOnePath': DIANA_IMAGE, 'imageOneName': 'binary_w_active',
                    'imageTwoPath': DIANA_IMAGE, 'imageTwoName': 'whiteImageTwo1200',
                    'outImagePath': DEAD_PIXEL_IMAGE, 'outImageName': 'DeadPixelBackToWhite', 'limits': ['3']}

               ]
           }


class EInkDeadPixelTestATE3Nano(Test):
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
        :return: Total error pixel positions
        '''
        ateConfig.log.logger.info('=====================================================================')
        ateConfig.log.logger.info('   Test Started   - ' + self._name)
        ateConfig.log.logger.info('=====================================================================')

        cmdResponse = ''
        startTime = time.time()
        result = {}
        count = 0
        testResult = []
        platform = ''
        threshold = ''
        watch_dial = ''
        image_ratio = 0
        tolerance = 0.04
        # internal_SN = tests.scenario.Scenario.ateTestAttr['internal_serial_number']
        # filetimestamp = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H%M_%S")
        internal_SN = '1234567890'
        filetimestamp = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H%M_%S")
        # Execute all commands in the command list.
        try:
            for cmd in self._cmdList:
                # if cmd.operation == 'crop' and cmd._imageOneName == 'dial_6hour' and platform == 'white':
                #     cmd._imageOneName = 'black_dial_6hour'
                # elif cmd.operation == 'crop' and cmd._imageOneName == 'dial_12hour' and platform == 'white':
                #     cmd._imageOneName = 'black_dial_12hour'
                # elif cmd.operation == 'findDial':
                #     cmd._dialPlatform = platform
                #     cmd._threshold = threshold
                if cmd.operation == 'EjectHands':
                    cmd._dial = watch_dial

                cmdResponse = cmd.execute()
                self._testResult['cmdResults'].append(cmdResponse)

                if type(cmdResponse) == str and 'Error' in cmdResponse:
                    self._testResult['name'] = 'EInk Screen Pixels ATE3 Test Nano'
                    self._testResult['passed'] = False
                    self._testResult['error'] = cmdResponse
                    self.calcTestDuration(startTime)
                    return self._testResult

                elif cmd.type == 'cv' and cmd.operation == 'findDial':
                    res = cmdResponse
                    if res == {}:
                        testResult.append(False)
                        ateConfig.log.logger.info('Cannot find dial')
                        break
                    else:
                        xCenter = int(res['dial'][0][0])
                        yCenter = int(res['dial'][0][1])
                        watch_dial = ((xCenter, yCenter), int(res['dial'][1]))
                        ateConfig.log.logger.info('Watch dial position: %s' %str(watch_dial))
                elif cmd.type == 'cv' and cmd.operation == 'findRect':
                    res = {}
                    res['Rect'] = cmdResponse
                    if res['Rect'] == {}:
                        testResult.append(False)
                        ateConfig.log.logger.info('Cannot detect rectangle')
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
                        ateConfig.log.logger.debug("ratio: %s" %image_ratio)
                        result['ratio'] = image_ratio
                elif cmd.type == 'cv' and cmd.operation == 'eraseText':
                    result['brand_area'] = cmdResponse

                elif cmd.type == 'cv' and cmd.operation == 'findPlatform':
                    res = cmdResponse
                    platform = res['platform']
                    threshold = res['threshold']
                # Check result when it execute findError function.
                elif cmd.type == 'cv' and cmd.operation == 'findDeadPixels':
                    dead_pixel = 0
                    D_cas_pixel = []
                    D_cas_mm    = []
                    defect_02 = []
                    defect_0204 = []
                    defect_04 = []
                    if count == 0:
                        res = {}
                        res = cmdResponse
                        result['areas_black'] = res['areas']
                        # Dead pixel data
                        x = res['xRect']
                        y = res['yRect']
                        w = res['wRect']
                        h = res['hRect']
                        image_b_1 = cv2.imread(DIANA_IMAGE_RAW + 'black_dial_6hour.jpeg')
                        image_b_2 = cv2.imread(DIANA_IMAGE_RAW + 'black_dial_12hour.jpeg')
                        if len(x) > 0:
                            for j in range(0, len(x)):
                                #Calculate as CAS formula
                                D_cas_pixel.append((w[j]+h[j])/2)
                                '''
                                EInk: 240 pixels
                                Diameter: 27.96mm
                                --> 1 pixel: 27.96/240 = 0.1165mm
                                --> 1 pixel in image: 0.1165/image_ratio
                                '''
                                d = round(((w[j]+h[j])/2)*(0.1165/image_ratio), 4)
                                D_cas_mm.append(d)
                                if (d > 0.1) and (d <= 0.2 - tolerance):
                                    defect_02.append(d)
                                elif (d > 0.2 - tolerance) and (d <= 0.4 - tolerance):
                                    defect_0204.append(d)
                                elif d > (0.4 - tolerance):
                                    defect_04.append(d)
                                # Get coordinate before cropping
                                x[j] = x[j] + watch_dial[0][0] - watch_dial[1] - RADIUS_THRESHOLD
                                y[j] = y[j] + watch_dial[0][1] - watch_dial[1] - RADIUS_THRESHOLD
                                if y[j] > watch_dial[0][1]:
                                    cv2.putText(image_b_2, 'D: ' + str(d), (x[j] - RECT_EXTEN_THRES - 50, y[j] - RECT_EXTEN_THRES - 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                    cv2.rectangle(image_b_2, (x[j] - RECT_EXTEN_THRES, y[j] - RECT_EXTEN_THRES), (x[j] + w[j] + RECT_EXTEN_THRES, y[j] + h[j] + RECT_EXTEN_THRES), (0, 0, 255), 2)
                                else:
                                    cv2.putText(image_b_1, 'D: ' + str(d), (x[j] - RECT_EXTEN_THRES - 50, y[j] - RECT_EXTEN_THRES - 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                    cv2.rectangle(image_b_1, (x[j] - RECT_EXTEN_THRES, y[j] - RECT_EXTEN_THRES), (x[j] + w[j] + RECT_EXTEN_THRES, y[j] + h[j] + RECT_EXTEN_THRES), (0, 0, 255), 2)
                        result['black_D_pixel'] = D_cas_pixel
                        result['black_D_mm'] = D_cas_mm
                        ateConfig.log.logger.info("Black image - D in pixels: %s" %str(D_cas_pixel))
                        ateConfig.log.logger.info("Black image - D in mm: %s" % str(D_cas_mm))
                        image_b_1 = cv2.resize(image_b_1, (0, 0), fx=0.5, fy=0.5)
                        image_b_2 = cv2.resize(image_b_2, (0, 0), fx=0.5, fy=0.5)
                        # cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "deadPixel_whiteToBlack_600_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image_b_1)
                        # cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "deadPixel_whiteToBlack_1200_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image_b_2)
                        cv2.imwrite(PROCESSED_IMAGES + "deadPixel_whiteToBlack_600_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image_b_1)
                        cv2.imwrite(PROCESSED_IMAGES + "deadPixel_whiteToBlack_1200_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image_b_2)
                    else:
                        res = {}
                        dead_pixel = 0
                        res = cmdResponse
                        result['areas_white'] = res['areas']
                        # Dead pixel data
                        x = res['xRect']
                        y = res['yRect']
                        w = res['wRect']
                        h = res['hRect']
                        image_w_1 = cv2.imread(DIANA_IMAGE_RAW + 'whiteImageTwo600.jpeg')
                        image_w_2 = cv2.imread(DIANA_IMAGE_RAW + 'whiteImageTwo1200.jpeg')
                        if len(x) > 0:
                            for j in range(0, len(x)):
                                # Calculate as CAS formula
                                D_cas_pixel.append((w[j] + h[j]) / 2)
                                '''
                                EInk: 240 pixels
                                Diameter: 27.96mm
                                --> 1 pixel: 27.96/240 = 0.1165mm
                                --> 1 pixel in image: 0.1165/image_ratio
                                '''
                                d = round(((w[j] + h[j]) / 2) * (0.1165 / image_ratio), 4)
                                if d > 0.1:
                                    D_cas_mm.append(d)
                                if (d > 0.1) and (d <= 0.2 - tolerance):
                                    defect_02.append(d)
                                elif (d > 0.2 - tolerance) and (d <= 0.4 - tolerance):
                                    defect_0204.append(d)
                                elif d > (0.4 - tolerance):
                                    defect_04.append(d)
                                # Get coordinate before cropping
                                x[j] = x[j] + watch_dial[0][0] - watch_dial[1] - RADIUS_THRESHOLD
                                y[j] = y[j] + watch_dial[0][1] - watch_dial[1] - RADIUS_THRESHOLD
                                if y[j] > watch_dial[0][1]:
                                    cv2.putText(image_w_2, 'D: ' + str(d), (x[j] - RECT_EXTEN_THRES - 50, y[j] - RECT_EXTEN_THRES - 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                    cv2.rectangle(image_w_2, (x[j] - RECT_EXTEN_THRES, y[j] - RECT_EXTEN_THRES), (x[j] + w[j] + RECT_EXTEN_THRES, y[j] + h[j] + RECT_EXTEN_THRES), (0, 0, 255), 2)
                                else:
                                    cv2.putText(image_w_1, 'D: ' + str(d), (x[j] - RECT_EXTEN_THRES - 50, y[j] - RECT_EXTEN_THRES - 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                                    cv2.rectangle(image_w_1, (x[j] - RECT_EXTEN_THRES, y[j] - RECT_EXTEN_THRES), (x[j] + w[j] + RECT_EXTEN_THRES, y[j] + h[j] + RECT_EXTEN_THRES), (0, 0, 255), 2)
                        image_w_1 = cv2.resize(image_w_1, (0, 0), fx=0.5, fy=0.5)
                        image_w_2 = cv2.resize(image_w_2, (0, 0), fx=0.5, fy=0.5)
                        # cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "deadPixel_blackToWhite_600_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image_w_1)
                        # cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "deadPixel_blackToWhite_1200_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image_w_2)
                        cv2.imwrite(PROCESSED_IMAGES + "deadPixel_blackToWhite_600_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image_w_1)
                        cv2.imwrite(PROCESSED_IMAGES + "deadPixel_blackToWhite_1200_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image_w_2)

                        result['white_D_pixel'] = D_cas_pixel
                        result['white_D_mm'] = D_cas_mm
                        ateConfig.log.logger.info("White image - D in pixels: %s" % str(D_cas_pixel))
                        ateConfig.log.logger.info("White image - D in mm: %s" % str(D_cas_mm))
                    if len(defect_0204) >= 5:
                        testResult.append(False)
                    if len(defect_04) > 0:
                        testResult.append(False)
                    if dead_pixel <= cmd.limits:
                        testResult.append(True)
                        ateConfig.log.logger.info(self._name + ' passed.')
                    else:
                        testResult.append(False)
                        ateConfig.log.logger.info(self._name + ' failed. Lower limit: [%s]' % (cmd.limits))
                    count += 1
                # BLE command timed out.
                elif cmd.type == 'ble' and cmdResponse['timeout']:
                    self._testResult['error'] = 'BLE connection timed out.'
                    testResult.append(False)
                    result['data'] = None
                    break  # Break out of loop because connection has timed out.

            if watch_dial == '':
                image1 = cv2.imread(DIANA_IMAGE_RAW + 'black_dial_6hour.jpeg')
                image2 = cv2.imread(DIANA_IMAGE_RAW + 'black_dial_12hour.jpeg')
                image1 = cv2.resize(image1, (0, 0), fx=0.5, fy=0.5)
                image2 = cv2.resize(image2, (0, 0), fx=0.5, fy=0.5)
                cv2.imwrite(PROCESSED_IMAGES + "deadPixel_whiteToBlack_600_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image1)
                cv2.imwrite(PROCESSED_IMAGES + "deadPixel_whiteToBlack_1200_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image2)
            #     cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "deadPixel_whiteToBlack_600_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image1)
            #     cv2.imwrite(tests.scenario.Scenario.ateTestAttr['logPath'] + "deadPixel_whiteToBlack_1200_" + internal_SN + "_" + str(filetimestamp) + ".jpeg", image2)

            if False in testResult:
                self._testResult['passed'] = False
            else:
                self._testResult['passed'] = True

            # Remove captured files
            # os.remove(DIANA_IMAGE + 'dial_6hour.jpeg')
            # os.remove(DIANA_IMAGE + 'dial_12hour.jpeg')
            # os.remove(DIANA_IMAGE + 'whiteImageTwo600.jpeg')
            # os.remove(DIANA_IMAGE + 'whiteImageTwo1200.jpeg')
            # os.remove(DIANA_IMAGE + 'black_dial_6hour.jpeg')
            # os.remove(DIANA_IMAGE + 'black_dial_12hour.jpeg')
            if watch_dial != '':
                os.remove(DIANA_IMAGE + 'black.jpeg')
                os.remove(DIANA_IMAGE + 'white.jpeg')
                os.remove(DIANA_IMAGE + 'white2.jpeg')
                os.remove(DIANA_IMAGE + 'watchDial_Mask.jpeg')

            ateConfig.log.logger.debug("Files Removed!")

            self._testResult['data'] = result
            ateConfig.log.logger.info('   Test Result: %s' % result)
            ateConfig.log.logger.info('   Test Completed - ' + self._name)

            self.calcTestDuration(startTime)

            return self._testResult

        except Exception as exc:
            result['error'] = str(exc)
            self._testResult['name'] = 'EInk Screen Pixels ATE3 Test Nano'
            self._testResult['passed'] = False
            self._testResult['data'] = result
            self.calcTestDuration(startTime)
            return self._testResult
