
import sys
import traceback

from commands.command import Command
from configuration import ateConfig
from utilities.cvController import CVController


class CVCmd(Command):
    _cv = CVController()
    def __init__(self, cmd):
        '''
        Init method to to setup command instance attributes
        :param cmd: list, command attributes
        '''
        super().__init__()

        self._type         = cmd['type']
        self._operation    = cmd['operation']
        self._imageOnePath = cmd['imageOnePath']
        self._imageOneName = cmd['imageOneName']
        if cmd['operation'] == 'crop':
            self.y = int(cmd['y'])
            self.yDist = int(cmd['yDist'])
            self.x = int(cmd['x'])
            self.xDist = int(cmd['xDist'])
        elif cmd['operation'] == 'andWithMask':
            self._xCenter = int(cmd['xCenter'])
            self._yCenter = int(cmd['yCenter'])
            self._rMask   = cmd['rMask']
        elif cmd['operation'] == 'intersect':
            self._point_1 = cmd['point_1']
            self._point_2 = cmd['point_2']
            self._point_3 = cmd['point_3']
            self._point_4 = cmd['point_4']
            self._position = cmd['position']
        elif cmd['operation'] == 'findHand':
            self._number_hand = int(cmd['hands'])
        elif cmd['operation'] == 'EjectHands':
            self._dial = cmd['dial']
        elif cmd['operation'] == 'findHole':
            self._minArea = cmd['minArea']
            self._maxArea = cmd['maxArea']

        if 'threshold' in cmd:
            self._threshold = cmd['threshold']
        if 'kernel' in cmd:
            self._kernel = cmd['kernel']
        if 'size' in cmd:
            self._size = cmd['size']
        if 'limits' in cmd:
            self._limits = cmd['limits']
            if len(self._limits) == 1:
                self._limits = float(self._limits[0])
            elif len(self._limits) == 2:
                self._lowerLimit = float(self._limits[0])
                self._upperLimit = float(self._limits[1])
            else:
                ateConfig.log.logger.error('Incorrect number of limits specified. There must only be a lower.')
        if 'imageTwoPath' in cmd:
            self._imageTwoPath = cmd['imageTwoPath']
            self._imageTwoName = cmd['imageTwoName']

        if 'outImagePath' in cmd:
            self._outImagePath = cmd['outImagePath']
            self._outImageName = cmd['outImageName']

        if 'dialPlatform' in cmd:
            self._dialPlatform = cmd['dialPlatform']

    def execute(self):
        '''
        Send command request to the DUT for execution
        :return: command response from DUT: byte list
        '''
        ateConfig.log.logger.debug('Executing CV command')
        result = None

        try:
            if self._operation == 'read':
                image = CVCmd._cv.readImage(self._imageOnePath, self._imageOneName)
            elif self._operation == 'write':
                CVCmd._cv.writeImage(self._imageOnePath, self._imageOneName)
            elif self._operation == 'show':
                CVCmd._cv.showImage(self._imageOnePath, self._imageOneName)
            elif self._operation == 'subtract':
                CVCmd._cv.subtractImages(self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName, self._outImagePath, self._outImageName)
            elif self._operation == 'dilation':
                CVCmd._cv.dilationImage(self._imageOnePath, self._imageOneName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'opening':
                CVCmd._cv.openingImagewithPath(self._imageOnePath, self._imageOneName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'closing':
                CVCmd._cv.closingImagewithPath(self._imageOnePath, self._imageOneName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'resize':
                CVCmd._cv.resizeImage(self._imageOnePath, self._imageOneName, self._outImagePath, self._outImageName)
            elif self._operation == 'blur':
                CVCmd._cv.blurImage(self._imageOnePath, self._imageOneName, self._outImagePath, self._outImageName)
            elif self._operation == 'invBinary':
                CVCmd._cv.convertImagetoInvBinary(self._imageOnePath, self._imageOneName, self._threshold, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'binary':
                CVCmd._cv.convertImagetoBinary(self._imageOnePath, self._imageOneName, self._threshold, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'edgeDetection':
                CVCmd._cv.edgesDetection(self._imageOnePath, self._imageOneName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'basicEdgeDetection':
                CVCmd._cv.basicEdgesDetection(self._imageOnePath, self._imageOneName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'erodeCenter':
                CVCmd._cv.erodeCenterCircle(self._imageOnePath, self._imageOneName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'bitwiseAnd':
                CVCmd._cv.bitwise_and_two_images(self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'bitwiseOr':
                CVCmd._cv.bitwise_or_two_images(self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName, self._outImagePath,self._outImageName)
            elif self._operation == 'findContours':
                contours = CVCmd._cv.findContoursinImage(self._imageOnePath, self._imageOneName)
            elif self._operation == 'findDeadPixels':
                result = CVCmd._cv.errorPositionDetection(self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName, self._outImagePath, self._outImageName)
            elif self._operation =='correlation':
                result = CVCmd._cv.correlationTwoImages(self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName)
            elif self._operation == 'crop':
                CVCmd._cv.cropImage(self._imageOnePath, self._imageOneName, self.y, self.yDist, self.x, self.xDist, self._outImagePath, self._outImageName)
            elif self._operation =='findRect':
                result = CVCmd._cv.rectangleDetection(self._imageOnePath, self._imageOneName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'findFudical':
                result = CVCmd._cv.fiducialDetection(self._imageOnePath, self._imageOneName, self._outImagePath, self._outImageName)
            elif self._operation == 'findHole':
                result = CVCmd._cv.chassisHoleDetection(self._imageOnePath, self._imageOneName, self._threshold, self._minArea, self._maxArea, self._outImagePath, self._outImageName)
            elif self._operation == 'findPinion':
                result = CVCmd._cv.pinionDetection(self._imageOnePath, self._imageOneName, self._outImagePath, self._outImageName)
            elif self._operation == 'findEink':
                result = CVCmd._cv.eInkCenterCirleDetection(self._imageOnePath, self._imageOneName, self._outImagePath, self._outImageName)
            elif self._operation == 'andWithMask':
                CVCmd._cv.imageWithMask(self._imageOnePath, self._imageOneName, self._rMask, self._xCenter, self._yCenter, self._outImagePath, self._outImageName)
            elif self._operation == 'analyzeHist':
                result = CVCmd._cv.histogramAnalysis(self._imageOnePath, self._imageOneName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'intersect':
                result = CVCmd._cv.intersection(self._point_1, self._point_2, self._point_3, self._point_4)
            elif self._operation == 'findHand':
                result = CVCmd._cv.handDetection(self._imageOnePath, self._imageOneName, self._kernel, self._number_hand, self._imageTwoPath, self._imageTwoName)
            elif self._operation == 'findDial':
                result = CVCmd._cv.dialCircleDetection(self._dialPlatform, self._threshold, self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'findEinkCircle':
                result = CVCmd._cv.eInkCircleDetection(self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName, self._kernel, self._outImagePath, self._outImageName, self._dial, self._threshold)
            elif self._operation == 'EjectHands':
                CVCmd._cv.ejectHands(self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName, self._outImagePath, self._outImageName, self._dial)
            elif self._operation == 'eraseCenter':
                CVCmd._cv.eraseCenterCircle(self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'eraseText':
                result = CVCmd._cv.deleteText(self._imageOnePath, self._imageOneName, self._imageTwoPath, self._imageTwoName, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'invThreshold':
                CVCmd._cv.medianInvThreshold(self._imageOnePath, self._imageOneName, self._size, self._kernel, self._outImagePath, self._outImageName)
            elif self._operation == 'findPlatform':
                result = CVCmd._cv.dialPlatformDetection(self._imageOnePath, self._imageOneName)
            elif self._operation == 'extract':
                CVCmd._cv.extractBrand(self._imageOnePath, self._imageOneName, self._kernel, self._outImagePath, self._outImageName)
        except Exception as exc:
            ateConfig.log.logger.error(sys.exc_info())
            ateConfig.log.logger.error('\n'.join(traceback.format_stack()))
            message = 'Error message: ' + 'Operation: ' + self._operation + ' | Image Name: '+ self._imageOneName + ' | Info: ' + str(exc)
            return message

        return result

    @property
    def limits(self):
        return self._limits

    @property
    def lowerLimit(self):
        return self._lowerLimit

    @property
    def upperLimit(self):
        return self._upperLimit