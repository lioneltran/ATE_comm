#!/usr/bin/env python
"""
Cumputer Vision Class
Created: 2017 Oct 15
Author: Thien Doan

Description:
Implementation of the Computer Vision class.
This class is the interface between application and cv.
"""
from utilities import cv
from configuration import ateConfig

class CVController():

    # Initialize the instrument
    def __init__(self):
        self.cv = cv.CV()

    def readImage(self, path, name):
        image = self.cv.readImage(path, name)
        return image

    def writeImage(self, image, path, name):
        self.cv.writeImage(image, path, name)

    def showImage(self, path, name):
        ateConfig.log.logger.info('Show image: %s' %name)
        self.cv.showImage(path, name)

    def subtractImages(self, pathOne, nameOne, pathTwo, nameTwo, writePath, writeName):
        # ateConfig.log.logger.info('Subtract two images')
        self.cv.subtractImages(pathOne, nameOne, pathTwo, nameTwo, writePath, writeName)

    def dilationImage(self, path, name, kernel, writePath, writeName):
        # ateConfig.log.logger.info('Image Dilation')
        self.cv.dilationImage(path, name, kernel, writePath, writeName)

    def openingImagewithPath(self, path, name, kernel, writePath, writeName):
        # ateConfig.log.logger.info('Do image openning')
        self.cv.openingImagewithPath(path, name, kernel, writePath, writeName)

    def openingImagewithoutPath(self, image, kernel):
        # ateConfig.log.logger.info('Do image openning')
        image = self.cv.openingImagewithoutPath(image, kernel)
        return image

    def closingImagewithPath(self, path, name, kernel, writePath, writeName):
        # ateConfig.log.logger.info('Do image closing')
        self.cv.closingImagewithPath(path, name, kernel, writePath, writeName)

    def closingImagewithoutPath(self, image, kernel):
        # ateConfig.log.logger.info('Do image closing')
        image = self.cv.closingImagewithoutPath(image, kernel)
        return image

    def resizeImage(self, path, name, writePath, writeName):
        # ateConfig.log.logger.info('Resize image')
        image = self.cv.resizeImage(path, name, writePath, writeName)
        return image

    def blurImage(self, path, name, writePath, writeName):
        # ateConfig.log.logger.info('Blur Image')
        self.cv.blurImage(path, name, writePath, writeName)

    def convertImagetoInvBinary(self, path, name, threshold, kernel, writePath, writeName):
        # ateConfig.log.logger.info('Convert image to binary image via invert binary method')
        self.cv.convertImagetoInvBinary(path, name, threshold, kernel, writePath, writeName)

    def convertImagetoBinary(self, path, name, threshold, kernel, writePath, writeName):
        # ateConfig.log.logger.info('Convert image to binary image via binary method')
        self.cv.convertImagetoBinary(path, name, threshold, kernel, writePath, writeName)

    def edgesDetection(self, path, name, kernel, writePath, writeName):
        # ateConfig.log.logger.info('Edge Detection in the image')
        self.cv.edgesDetection(path, name, kernel, writePath, writeName)

    def basicEdgesDetection(self, path, name, kernel, writePath, writeName):
        # ateConfig.log.logger.info('Edge Detection in the image')
        self.cv.basicEdgesDetection(path, name, kernel, writePath, writeName)

    def erodeCenterCircle(self, path, name, kernel, writePath, writeName):
        # ateConfig.log.logger.info('Find and draw overlap circle center')
        self.cv.erodeCenterCircle(path, name, kernel, writePath, writeName)

    def bitwise_and_two_images(self, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName):
        # ateConfig.log.logger.info('Bitwise_And two images')
        self.cv.bitwise_and_two_images(pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName)

    def bitwise_or_two_images(self, pathOne, nameOne, pathTwo, nameTwo, writePath, writeName):
        self.cv.bitwise_or_two_images(pathOne, nameOne, pathTwo, nameTwo, writePath, writeName)

    def positionDetection(self, x, y):
        # ateConfig.log.logger.info('Finding coordinates of error pixel')
        (quadrant1, quadrant2, quadrant3, quadrant4) = self.cv.positionDetection(x, y)
        return (quadrant1, quadrant2, quadrant3, quadrant4)

    def findContoursinImage(self, binImagePath, binImageName):
        contours = self.findContoursinImage(binImagePath, binImageName)
        return contours

    def errorPositionDetection(self, binImagePath, binImageName, oriImagePath, oriImageName, writePath, writeName):
        # ateConfig.log.logger.info('Finding error pixel')
        result = self.cv.errorPositionDetection(binImagePath, binImageName, oriImagePath, oriImageName, writePath, writeName)
        return result

    def correlationTwoImages(self, pathOne, nameOne, pathTwo, nameTwo):
        # ateConfig.log.logger.info('Finding histogram correlation between two images')
        result = self.cv.correlationTwoImages(pathOne, nameOne, pathTwo, nameTwo)
        return result

    def cropImage(self, path, name, y, yDist, x, xDist, writePath, writeName):
        # ateConfig.log.logger.info('Cropping image')
        self.cv.cropImage(path, name, y, yDist, x, xDist, writePath, writeName)

    def rectangleDetection(self, path, name, kernel, writePath, writeName):
        result = self.cv.rectangleDetection(path, name, kernel, writePath, writeName)
        return result

    def fiducialDetection(self, path, name, writePath, writeName):
        result = self.cv.fiducialDetection(path, name, writePath, writeName)
        return result

    def chassisHoleDetection(self, path, name, threshold, min_area, max_area, writePath, writeName):
        result = self.cv.chassisHoleDetection(path, name, threshold, min_area, max_area, writePath, writeName)
        return result

    def eInkCenterCirleDetection(self, path, name, writePath, writeName):
        result = self.cv.eInkCenterCirleDetection(path, name, writePath, writeName)
        return result

    def pinionDetection(self, path, name, writePath, writeName):
        result = self.cv.pinionDetection(path, name, writePath, writeName)
        return result

    def imageWithMask(self, path, name, rMask, xcenter, ycenter, writePath, writeName):
        result = self.cv.imageWithMask(path, name, rMask, xcenter, ycenter, writePath, writeName)
        return result

    def histogramAnalysis(self, path, name, kernel, writePath, writeName):
        result = self.cv.histogramAnalysis(path, name, kernel, writePath, writeName)
        return  result

    def intersection(self, p1, p2, p3, p4):
        result = self.cv.intersection(p1, p2, p3, p4)
        return result

    def handDetection(self, path, name, kernel, number_hand, maskPath, maskName):
        result = self.cv.handDetection(path, name, kernel, number_hand, maskPath, maskName)
        return result

    def dialCircleDetection(self, dialPlatform, binaryThreshold, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName):
        result = self.cv.dialCircleDetection(dialPlatform, binaryThreshold, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName)
        return result

    def eInkCircleDetection(self, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName, dial, binaryThreshold):
        result = self.cv.eInkCircleDetection(pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName, dial, binaryThreshold)
        return result

    def ejectHands(self, pathOne, nameOne, pathTwo, nameTwo, writePath, writeName, dial):
        self.cv.HandsEject(pathOne, nameOne, pathTwo, nameTwo, writePath, writeName, dial)

    def eraseCenterCircle(self, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName):
        self.cv.eraseCenterCircle(pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName)

    def deleteText(self, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName):
        result = self.cv.deleteText(pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName)
        return result

    def medianInvThreshold(self, path, name, size, kernel, writePath, writeName):
        self.cv.medianInvThreshold(path, name, size, kernel, writePath, writeName)

    def dialPlatformDetection(self, path, name):
        result = self.cv.dialPlatformDetection(path, name)
        return result

    def extractBrand(self, path, name, kernel, writePath, writeName):
        self.cv.extractBrand(path, name, kernel, writePath, writeName)


