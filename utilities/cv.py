#!/usr/bin/env python
"""
Computer Vision Class
Created: 2017 Oct 15
Author: Thien Doan

Description:
Implementation of the Computer Vision class.
"""
import numpy
import numpy as np
import time
import cv2
import math
import random
from configuration import ateConfig
from configuration.ateConfig import *
from configuration.cvConfig import *

class CV():
    # Initialize the instrument
    def __init__(self):
        self.binary_threshold = BINARY_THRESHOLD

    def readImage(self, path, name):
        '''
        Read an image from local
        :param path:
        :param name:
        :return:
        '''
        ateConfig.log.logger.debug('Read image: %s' % (path+name+'.jpeg'))
        image = cv2.imread(path+name+'.jpeg')
        return image

    #Write image into local
    def writeImage(self, image, path, name):
        '''
        The function writes image to local as path and name
        :param image:
        :param path:
        :param name:
        :return: None
        '''
        ateConfig.log.logger.debug('Write image to:%s' % (path+name+'.jpeg'))
        cv2.imwrite(path+name+'.jpeg', image)

    def showImage(self, path, name):
        '''
        Show an image
        :param path:
        :param name:
        :return: None
        '''
        ateConfig.log.logger.info('Show image: %s' %name)
        img = self.readImage(path, name)
        cv2.imshow(name, img)
        k = cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cropImage(self, path, name, y, yDist, x, xDist, writePath, writeName):
        '''

        :param path:
        :param name:
        :param y: Initial position
        :param yDist: Destination position
        :param x: Initial position
        :param xDist: Destination position
        :param writePath:
        :param writeName:
        :return: None
        '''
        ateConfig.log.logger.info('Cropping image')
        image = self.readImage(path, name)
        crop_image = image[y:yDist, x:xDist]
        self.writeImage(crop_image, writePath, writeName)

    #subtract two color images
    def subtractImages(self, pathOne, nameOne, pathTwo, nameTwo, writePath, writeName):
        '''
        Subtract two images
        :param pathOne:
        :param nameOne:
        :param pathTwo:
        :param nameTwo:
        :param writePath:
        :param writeName:
        :return: None
        '''
        ateConfig.log.logger.info('Subtract two images')
        imageOne = self.readImage(pathOne, nameOne)
        imageTwo = self.readImage(pathTwo, nameTwo)
        img1_gray = cv2.cvtColor(imageOne, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(imageTwo, cv2.COLOR_BGR2GRAY)
        sub_img = cv2.subtract(img1_gray, img2_gray)
        self.writeImage(sub_img, writePath, writeName)

    def dilationImage(self, path, name, kernel, writePath, writeName):
        '''
        Perform dilation of image
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Image Dilation')
        image = self.readImage(path, name)
        image = cv2.dilate(image, kernel, iterations=3)
        self.writeImage(image, writePath, writeName)

    def erosionImage(self, path, name, kernel, writePath, writeName):
        '''
        Perform erosion of image
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Image Erosion')
        image = self.readImage(path, name)
        image = cv2.erode(image, kernel, iterations=1)
        self.writeImage(image, writePath, writeName)

    def openingImagewithPath(self, path, name, kernel, writePath, writeName):
        '''
        Perform openning of image: Erosion followed by dilation with a read image
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Do image openning')
        image = self.readImage(path, name)
        img_erosion = cv2.erode(image, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
        self.writeImage(img_dilation, writePath, writeName)

    def openingImagewithoutPath(self, image, kernel):
        '''
        Perform openning of image: Erosion followed by dilation
        :param image:
        :param kernel:
        :return:
        '''
        ateConfig.log.logger.info('Do image openning')
        img_erosion = cv2.erode(image, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
        return img_dilation

    def closingImagewithPath(self, path, name, kernel, writePath, writeName):
        '''
        Perform closing of image: dilation followed by erosion
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Do image closing')
        image = self.readImage(path, name)
        img_dilation = cv2.dilate(image, kernel, iterations=1)
        img_closing = cv2.erode(img_dilation, kernel, iterations=1)
        self.writeImage(img_closing, writePath, writeName)

    def closingImagewithoutPath(self, image, kernel):
        '''
        Perform closing of image: dilation followed by erosion with read image
        :param image:
        :param kernel:
        :return:
        '''
        ateConfig.log.logger.info('Do image closing')
        img_dilation = cv2.dilate(image, kernel, iterations=1)
        img_closing = cv2.erode(img_dilation, kernel, iterations=1)
        return img_closing

    def resizeImage(self, path, name, writePath, writeName):
        '''
        Resize an image with IMAGE_SIZE
        :param path:
        :param name:
        :return:
        '''
        ateConfig.log.logger.info('Resize image')
        image = self.readImage(path, name)
        r = IMAGE_RESIZE / image.shape[1]
        dim = (IMAGE_RESIZE, int(image.shape[0] * r))
        img_resize = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        self.writeImage(img_resize, writePath, writeName)

    def blurImage(self, path, name, writePath, writeName):
        '''
        Blur image with MedianBlur
        :param path:
        :param name:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Blur Image')
        image = self.readImage(path, name)
        img_blur = cv2.medianBlur(image, BLUR_KSIZE_3)
        self.writeImage(img_blur, writePath, writeName)

    def convertImagetoInvBinary(self, path, name, threshold, kernel, writePath, writeName):
        '''
        Convert an image to invert binary image
        :param path:
        :param name:
        :param threshold:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Convert image to binary image via invert binary method')
        image = self.readImage(path, name)
        # Convert image to binary image using invert binary
        ret, image_inv_binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
        image_inv_binary_opening = self.openingImagewithoutPath(image_inv_binary, kernel)
        self.writeImage(image_inv_binary_opening, writePath, writeName)

    def convertImagetoBinary(self, path, name, threshold, kernel, writePath, writeName):
        '''
        Convert image to binary image
        :param path:
        :param name:
        :param threshold:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Convert image to binary image via binary method')
        image = self.readImage(path, name)
        ret, image_binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        image = cv2.erode(image_binary, kernel, iterations=1)
        image = cv2.dilate(image, kernel, iterations=1)


        self.writeImage(image, writePath, writeName)

    def edgesDetection(self, path, name, kernel, writePath, writeName):
        '''
        find all egdes in an image using Canny Edge detection
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Edge Detection in the image')
        image = self.readImage(path, name)
        edges_img = cv2.Canny(image, CANNY_THRESHOLD_1, CANNY_THRESHOLD_2, APERTURE_SIZE)
        # edge_opening = self.openingImagewithoutPath(edges_img, kernel)
        self.writeImage(edges_img, writePath, writeName)

    def erodeCenterCircle(self, path, name, kernel, writePath, writeName):
        '''
        Erode a center circle
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Find and draw overlap circle center...')
        image = self.readImage(path, name)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        height, width = image_gray.shape

        dept, contours, hierarchy = cv2.findContours(image_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Find the index of the largest contour
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        ellipse = cv2.fitEllipse(cnt)
        #Reduce MA, ma to make inner radius of overlap circle smaller than edge of circle
        MA = ellipse[1][0]-RADIUS_THRESHOLD
        ma = ellipse[1][1]-RADIUS_THRESHOLD
        overlap_ellipse = ((ellipse[0][0], ellipse[0][1]), (MA, ma),ellipse[2])

        #Get center info
        rMask = int(ellipse[1][0]/2)-RADIUS_THRESHOLD*2
        ycenter = int(ellipse[0][1])
        xcenter = int(ellipse[0][0])
        center = 255 * cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rMask, 2 * rMask))
        mask = np.zeros((int(height), int(width)), np.uint8)
        mask[ycenter - rMask:ycenter + rMask, xcenter - rMask:xcenter + rMask] = center
        if DEBUG_MODE:
            self.writeImage(mask, path, "maskEInk")

        #Draw overlap ellipse with width = 2*radius
        cv2.ellipse(image, overlap_ellipse, (0, 0, 0), RADIUS_THRESHOLD*2)
        if DEBUG_MODE:
            self.writeImage(image, path, "overlapOuterEdge")

        if DEBUG_MODE:
            ateConfig.log.logger.debug('Ellipse: ' + str(ellipse))

        #Crop only center of eink
        crop_image = image_gray[CONCENTRICITY_CROP_Y1: CONCENTRICITY_CROP_Y2, CONCENTRICITY_CROP_X1:CONCENTRICITY_CROP_X2]
        # image_gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
        if DEBUG_MODE:
            self.writeImage(crop_image, path, "centerOriginal")

        dept, contours, hierarchy = cv2.findContours(crop_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Find the index of the largest contour
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        ellipse = cv2.fitEllipse(cnt)
        if DEBUG_MODE:
            ateConfig.log.logger.debug('Ellipse: ' +str(ellipse))
        #Get ellipse data
        (x,y) = ellipse[0]
        (MA, ma) = ellipse[1]
        #Calculate average of circle via MA, ma of ellipse
        radius = ((MA+ma)/4)

        # mask = cv2.ellipse(mask, ellipse, (0, 0, 0), 1)
        cv2.circle(mask, (int(x + CONCENTRICITY_CROP_X1), int(y+CONCENTRICITY_CROP_Y1)), int(radius) + RADIUS_THRESHOLD, (0, 0, 0), -1)
        self.writeImage(mask, DIANA_IMAGE, ACTIVE_EINK_REGION)

        #Draw overlap circle to remove inner circle
        cv2.circle(image, (int(x + CONCENTRICITY_CROP_X1), int(y+CONCENTRICITY_CROP_Y1)), int(radius) + RADIUS_THRESHOLD, (0, 0, 0), -1)
        if DEBUG_MODE:
            self.writeImage(image, path, "overlapInnerEdge")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.bitwise_and(image, mask)

        #Do openning error pixels
        image = cv2.dilate(image, kernel, iterations=2)
        image = cv2.erode(image, kernel, iterations=1)

        self.writeImage(image, writePath, writeName)

    def bitwise_and_two_images(self, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName):
        '''
        Perform bitwise and two images
        :param pathOne:
        :param nameOne:
        :param pathTwo:
        :param nameTwo:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Bitwise_And two images')
        imageOne = self.readImage(pathOne, nameOne)
        imageTwo = self.readImage(pathTwo, nameTwo)
        img_and = cv2.bitwise_and(imageOne, imageTwo)
        # image = cv2.dilate(img_and, kernel, iterations=1)
        self.writeImage(img_and, writePath, writeName)

    def bitwise_or_two_images(self, pathOne, nameOne, pathTwo, nameTwo, writePath, writeName):
        '''
        Perform bitwise or two images
        :param pathOne:
        :param nameOne:
        :param pathTwo:
        :param nameTwo:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Bitwise or two images')
        imageOne = self.readImage(pathOne, nameOne)
        imageTwo = self.readImage(pathTwo, nameTwo)
        img_and = cv2.bitwise_or(imageOne, imageTwo)
        # image = cv2.dilate(img_and, kernel, iterations=1)
        self.writeImage(img_and, writePath, writeName)

    def positionDetection(self, x, y):
        '''
        Find pixels in 4 quadrants
        :param x:
        :param y:
        :return:
        '''
        ateConfig.log.logger.info('Finding coordinates of error pixel')
        quadrant1=0
        quadrant2=0
        quadrant3=0
        quadrant4=0
        for i in range(0, len(x)):
            if x[i] >= CAMERA_RESOLUTION_X/2 and y[i] < CAMERA_RESOLUTION_Y/2:
                quadrant1+=1
            elif x[i] < CAMERA_RESOLUTION_X/2 and y[i] < CAMERA_RESOLUTION_Y/2:
                quadrant2+=1
            elif x[i] < CAMERA_RESOLUTION_X/2 and y[i] >= CAMERA_RESOLUTION_Y/2:
                quadrant3+=1
            else:
                quadrant4+=1
        return (quadrant1, quadrant2, quadrant3, quadrant4)

    def errorPositionDetection(self, binImagePath, binImageName, oriImagePath, oriImageName, writePath, writeName):
        '''
        Find all error pixels in image
        :param binImagePath:
        :param binImageName:
        :param oriImagePath:
        :param oriImageName:
        :param writePath:
        :param writeName:
        :return: Total error positions and total erros in each quadrant
        '''
        ateConfig.log.logger.info('Finding dead pixel on image...')
        binary_image = self.readImage(binImagePath, binImageName)
        # contours = self.findContoursinImage(binImagePath, binImageName)
        binary_image = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)
        ret, binary_image = cv2.threshold(binary_image, self.binary_threshold, 255, cv2.THRESH_BINARY)
        if DEBUG_MODE:
            self.writeImage(binary_image, binImagePath, "contourBinary")
        dept, contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        original_image = self.readImage(oriImagePath, oriImageName)
        errorCount = 0
        areas      = []
        quadrant1  = 0
        quadrant2  = 0
        quadrant3  = 0
        quadrant4  = 0
        x = []
        y = []
        w = []
        h = []
        result ={}
        for cnt in contours:
            # if DEBUG_MODE:
            #     print(cv2.contourArea(cnt))
            #Ger all positions with area >= lower limit
            if cv2.contourArea(cnt) >= CONTOUR_MIN_AREA and cv2.contourArea(cnt) <= CONTOUR_MAX_AREA :
                # if DEBUG_MODE:
                #     print(cv2.contourArea(cnt))
                areas.append(cv2.contourArea(cnt))
                errorCount += 1
                x1, y1, w1, h1 = cv2.boundingRect(cnt)
                x.append(int(x1))
                y.append(int(y1))
                w.append(int(w1))
                h.append(int(h1))
        (quadrant1, quadrant2, quadrant3, quadrant4) = self.positionDetection(x, y)
        if DEBUG_MODE:
            if len(x) > 0:
                #Draw a red rectanlge in each error position
                for j in range(0, len(x)):
                    cv2.rectangle(original_image, (x[j]-RECT_EXTEN_THRES, y[j]-RECT_EXTEN_THRES), (x[j] + w[j]+RECT_EXTEN_THRES, y[j] + h[j]+RECT_EXTEN_THRES), (0, 0, 255), 2)

        result_image = original_image
        self.writeImage(result_image, writePath, writeName)

        # result['errorPositions'] = errorCount
        # result['quad1'] = quadrant1
        # result['quad2'] = quadrant2
        # result['quad3'] = quadrant3
        # result['quad4'] = quadrant4
        result['areas'] = areas
        result['xRect'] = x
        result['yRect'] = y
        result['wRect'] = w
        result['hRect'] = h
        # ateConfig.log.logger.info('Dead pixel result: ' + str(result))
        return result

    def correlationTwoImages(self, pathOne, nameOne, pathTwo, nameTwo):
        '''
        find Histogram correlation of two images
        :param pathOne:
        :param nameOne:
        :param pathTwo:
        :param nameTwo:
        :return: correlation value
        '''
        result ={}
        imageOne = self.readImage(pathOne, nameOne)
        imageTwo = self.readImage(pathTwo, nameTwo)
        imageOne = cv2.cvtColor(imageOne, cv2.COLOR_BGR2GRAY)
        imageTwo = cv2.cvtColor(imageTwo, cv2.COLOR_BGR2GRAY)
        hist1 = cv2.calcHist([imageOne], [0], None, [256], [0,256])
        hist2 = cv2.calcHist([imageTwo], [0], None, [256], [0,256])
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        result['correlation'] = correlation
        return result

    def rectangleDetection(self, path, name, kernel, writePath, writeName):
        '''
        Find rectangle shape in image
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return: coordinate of left bottom point of rectangle and angle between rectangle with horizontal
        '''
        result = {}
        max_index = 0
        max_area  = RECT_MIN_AREA
        ateConfig.log.logger.info('Finding Rectangle in eInk...')
        image = self.readImage(path, name)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # img_blur = cv2.medianBlur(img_gray, BLUR_KSIZE_3)

        #Convert image to binary
        ret, binary_img = cv2.threshold(img_gray, RECT_THRES_BINARY, 255, cv2.THRESH_BINARY)
        if DEBUG_MODE:
            self.writeImage(binary_img, path, "alignBinary")
        #Closing to make rectangle smoothly
        img_erode = cv2.erode(binary_img, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erode, kernel, iterations=2)

        #Find contour of rectangle
        dept, contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #Get rectangle positions
        for i in range(0, len(contours)):
            if cv2.contourArea(contours[i]) > max_area:
                max_area = cv2.contourArea(contours[i])
                max_index = i
        if max_area > RECT_MIN_AREA:
            cnt = contours[max_index]
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            points=[]
            for p in box:
                pt = (int(p[0]), int(p[1]))
                points.append(pt)
            result['points'] = points
            if DEBUG_MODE:
                self.writeImage(image, writePath, writeName)

        return result

    def fiducialDetection(self, path, name, writePath, writeName):
        '''
        Find Fiducial center coordinate in image
        :param path:
        :param name:
        :param writePath:
        :param writeName:
        :return: data of ellipse: (x, y), (MA, ma)
        '''
        ateConfig.log.logger.info('Find Fiducial ...')
        image = self.readImage(path, name)
        result = {}

        #Do smooth image
        # image = cv2.medianBlur(image, BLUR_KSIZE_5)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for threshold in FIDUCIAL_THRES_BINARY:
            ret, image_binary = cv2.threshold(image_gray, threshold, 255, cv2.THRESH_BINARY)
            image_binary = cv2.dilate(image_binary, KERNEL2, iterations=1)
            if DEBUG_MODE:
                self.writeImage(image_binary, DIANA_IMAGE, "fiducialToBinary")
            dept, contours, hierarchy = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            max_index = 0
            best_area = 0
            # Find the index of the largest contour
            areas = [cv2.contourArea(c) for c in contours]
            for i in range(0, len(areas)):
                if areas[i]> FIDUCIAL_MIN_AREA and areas[i] < FIDUCIAL_MAX_AREA:
                    cnt = contours[i]
                    (x, y), (MA, ma), angle = cv2.fitEllipse(cnt)
                    #check the ratio between ma vs MA to avoid wrong detection ellipse
                    if ma/MA < FIFUCIAL_MA_ma_RATIO:
                        max_index = i
                        best_area = areas[i]
                        ateConfig.log.logger.debug('Area: %s' % areas[i])
            if best_area != 0:
                # max_index = np.argmax(areas)
                cnt = contours[max_index]
                ellipse = cv2.fitEllipse(cnt)
                result['fiducial'] = ellipse
                result['area'] = best_area
                result['threshold'] = threshold
                if DEBUG_MODE:
                    #Draw ellipse and save to local
                    img = cv2.ellipse(image, ellipse, (0, 0, 255), 2)
                    print(ellipse)
                    self.writeImage(img, DIANA_IMAGE, "fiducialEllipse")
                break
            ateConfig.log.logger.debug('Try next binary threshold')
        return result

    def chassisHoleDetection(self, path, name, min_area, max_area, writePath, writeName):
        '''
        Find chassis hole
        :param path:
        :param name:
        :param writePath:
        :param writeName:
        :return: coordinates of 2 centers and radius value
        '''
        ateConfig.log.logger.info('Finding chassis hole')
        image = self.readImage(path, name)
        result = {}

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for threshold in HOLE_THRES_BINARY:
            ret, image_binary = cv2.threshold(image_gray, threshold, 255, cv2.THRESH_BINARY_INV)
            # image_binary = cv2.erode(image_binary, KERNEL2, iterations=1)
            image_binary = cv2.dilate(image_binary, KERNEL2, iterations=1)
            if DEBUG_MODE:
                self.writeImage(image_binary, DIANA_IMAGE, "HoleBinary")
            dept, contours, hierarchy = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # Find the index of the largest contour
            best_area = 0
            max_index = 0
            areas = [cv2.contourArea(c) for c in contours]
            for i in range(0, len(areas)):
                if areas[i] > min_area and areas[i] < max_area:
                    cnt = contours[i]
                    (x, y), (MA, ma), angle = cv2.fitEllipse(cnt)
                    # #Only get ellipse ~ circle to remove edge of E-Ink
                    if ma/MA < HOLE_MA_ma_RATIO:
                        max_index = i
                        best_area = areas[i]
                        ateConfig.log.logger.debug('Area: %s' % areas[i])
            if best_area != 0:
                # max_index = np.argmax(areas)
                cnt = contours[max_index]
                ellipse = cv2.fitEllipse(cnt)
                result['hole'] = ellipse
                result['area'] = best_area
                result['threshold'] = threshold
                if DEBUG_MODE:
                    # Draw ellipse and save to local
                    img = cv2.ellipse(image, ellipse, (0, 0, 255), 2)
                    self.writeImage(img, DIANA_IMAGE, name+"_holeEllipse")
                break
            ateConfig.log.logger.debug('Try next binary threshold')
        return result

    def pinionDetection(self, path, name, writePath, writeName):
        '''
        Finding Pinion position
        :param path:
        :param name:
        :param writePath:
        :param writeNam:
        :return:
        '''
        result  = {}

        ateConfig.log.logger.info('Finding Pinion...')
        image = self.readImage(path, name)

        image_blur = cv2.GaussianBlur(image, GAUSSIAN_BLUR_KSIZE_3, 0)
        image_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
        for threshold in PINION_BINARY_THRESHOLD:
            ret, image_binary = cv2.threshold(image_gray, threshold, 255, cv2.THRESH_BINARY)
            #Enhance edge of circle
            image_binary = cv2.dilate(image_binary, KERNEL2, iterations=1)
            image_binary = cv2.erode(image_binary, KERNEL2, iterations=1)
            if DEBUG_MODE:
                self.writeImage(image_binary, DIANA_IMAGE, "pinionToBinary")
            dept, contours, hierarchy = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # Find the index of the largest contour
            areas = [cv2.contourArea(c) for c in contours]
            max_index = 0
            best_area = 0
            for i in range(0, len(areas)):
                if areas[i] > PINION_MIN_AREA and areas[i] < PINION_MAX_AREA:
                    max_index = i
                    best_area = areas[i]
                    ateConfig.log.logger.debug('Area: %s' % areas[i])
            if best_area != 0:
                # max_index = np.argmax(areas)
                cnt = contours[max_index]
                ellipse = cv2.fitEllipse(cnt)
                result['pinion'] = ellipse
                result['area']  = best_area
                result['threshold'] = threshold
                if DEBUG_MODE:
                    ateConfig.log.logger.debug('Ellipse: ' + str(ellipse))
                    cv2.ellipse(image, ellipse, (0, 0, 255), 2)
                    self.writeImage(image, DIANA_IMAGE, "testPinion")
                break
            ateConfig.log.logger.debug('Try next binary threshold')
        return result

    def eInkCenterCirleDetection(self, path, name, writePath, writeName):
        '''
        Finding outer cirle of EInk center
        :param path:
        :param name:
        :param writePath:
        :param writeNam:
        :return:
        '''
        result  = {}

        ateConfig.log.logger.info('Finding EInk Outer Center Circle...')
        image = self.readImage(path, name)

        image = cv2.GaussianBlur(image, GAUSSIAN_BLUR_KSIZE_3, 0)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for threshold in EINK_BINARY_THRESHOLD:
            #convert to binary image
            ret, image_binary = cv2.threshold(image_gray, threshold, 255, cv2.THRESH_BINARY)
            if DEBUG_MODE:
                self.writeImage(image_binary, DIANA_IMAGE, "eInkCenterToBinary")

            #Do edge detection to find inner circle and outer cirle of eink center
            edges_img = cv2.Canny(image_binary, CANNY_THRESHOLD_1, CANNY_THRESHOLD_2, APERTURE_SIZE)
            if DEBUG_MODE:
                self.writeImage(edges_img, DIANA_IMAGE, "eInkCenterToEdge")
            #Do opening image to enhance edge of circle
            edges_img = cv2.dilate(edges_img, KERNEL2, iterations=1)
            edges_img = cv2.erode(edges_img, KERNEL2, iterations=1)

            dept, contours, hierarchy = cv2.findContours(edges_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # Find the index of the largest contour
            areas = [cv2.contourArea(c) for c in contours]
            max_index = 0
            best_area = 0
            for i in range(0, len(areas)):
                if areas[i] > EINK_MIN_AREA and areas[i] < EINK_MAX_AREA:
                    max_index = i
                    best_area = areas[i]
                    ateConfig.log.logger.debug('Area: %s' %areas[i])
            if best_area != 0:
                # max_index = np.argmax(areas)
                cnt = contours[max_index]
                ellipse = cv2.fitEllipse(cnt)
                result['eInk'] = ellipse
                result['area'] = best_area
                result['threshold'] = threshold
                result['cnt'] = cnt
                if DEBUG_MODE:
                    ateConfig.log.logger.debug('Ellipse: ' + str(ellipse))
                    cv2.ellipse(image, ellipse, (0, 0, 255), 2)
                    self.writeImage(image, DIANA_IMAGE, "testeInkCenter")
                break
            ateConfig.log.logger.debug('Try next binary threshold')
        return result

    def imageWithMask(self, path, name, rMask, xcenter, ycenter, writePath, writeName):
        '''

        :param path:
        :param name:
        :param writePath:
        :param writeName:
        :return: and image
        '''
        ateConfig.log.logger.info('Do bitwise_and image with mask...')
        img = self.readImage(path, name)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height, width = gray_image.shape
        kernel = 255 * cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*rMask, 2*rMask))
        mask = np.zeros((int(height), int(width)), np.uint8)
        mask[ycenter - rMask:ycenter + rMask, xcenter - rMask:xcenter + rMask] = kernel
        if DEBUG_MODE:
            self.writeImage(mask, path, "mask")
        masked_image = cv2.bitwise_and(gray_image, mask)
        self.writeImage(masked_image, writePath, writeName)

    def histogramAnalysis(self, path, name, kernel, writePath, writeName):
        '''
        :param path:
        :param name:
        :param writePath:
        :param writeName:
        :return: number pixel of max brightness and LED posision coordinate
        '''
        result = {}
        max_index = 0
        max_area  = LED_MIN_AREA
        ateConfig.log.logger.info('Analyzing image histogram...')
        image = self.readImage(path, name)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # change to binary image
        ret, image_binary = cv2.threshold(gray_image, LED_THRES_BINARY, 255, cv2.THRESH_BINARY)

        # implement opening
        erosion = cv2.erode(image_binary, kernel, iterations=1)
        opening_img = cv2.dilate(erosion, kernel, iterations=1)
        height, width = gray_image.shape
        black_image = np.zeros((int(height), int(width)), np.uint8)

        if DEBUG_MODE:
            self.writeImage(opening_img, writePath, name+"_histBinary")
        # find contour from binary image
        dept, contours, hierarchy = cv2.findContours(opening_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0, len(contours)):
            #Only get area >= lower limit area
            if cv2.contourArea(contours[i]) > max_area:
                max_area = cv2.contourArea(contours[i])
                max_index = i
        if max_area > LED_MIN_AREA:
            result['area'] = max_area
            ateConfig.log.logger.debug('Max LED active region: %s' %max_area)
            cnt = contours[max_index]
            ellipse = cv2.fitEllipse(cnt)
            result['led'] = ellipse
            mask = cv2.ellipse(black_image, ellipse, (255, 255, 255), -1)
            if DEBUG_MODE:
                # Draw ellipse and save to local
                img = cv2.ellipse(image, ellipse, (0, 255, 0), 2)
                self.writeImage(img, DIANA_IMAGE, name+"_ellipse")

            masked_image = cv2.bitwise_and(gray_image, mask)
            self.writeImage(masked_image, writePath, writeName)
            # calculate histogram of led imaged
            hist = cv2.calcHist([masked_image], [0], mask, [256], [0, 256])
            sort_hist = hist[HIST_LOWER_PIXEL_VALUE:256]
            result['hist'] = sort_hist

        return result

    def intersection(self, p1, p2, p3, p4):
        '''
        Get intersection coordinates between two lines from 2 points/line
        :param L1:
        :param L2:
        :return:
        '''
        ateConfig.log.logger.debug("Find intersection point between 2 lines from 4 points")
        result = {}
        A1 = (p1[1] - p2[1])
        B1 = (p2[0] - p1[0])
        C1 = (p1[0] * p2[1] - p2[0] * p1[1])
        L1 = (A1, B1, -C1)

        A2 = (p3[1] - p4[1])
        B2 = (p4[0] - p3[0])
        C2 = (p3[0] * p4[1] - p4[0] * p3[1])
        L2 = (A2, B2, -C2)

        D = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            result['x'] = int(x)
            result['y'] = int(y)
            ateConfig.log.logger.debug("Intersection coordinate: (%s, %s)" %(int(x), int(y)))

        return result

    def handDetection(self, path, name, kernel, number_hand, maskPath, maskName):
        '''
        :param path:
        :param name:
        :return: angle of two hands
        '''
        result = {}
        ateConfig.log.logger.debug("Finding hands position...")

        image = self.readImage(path, name)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = gray_image.shape
        mask = self.readImage(maskPath, maskName)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.bitwise_and(gray_image, mask)

        for threshold in HAND_THRES_BINARY:
            ret, image_binary = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

            erode_image = cv2.erode(image_binary, kernel)
            dilate_image = cv2.dilate(erode_image, kernel)
            if DEBUG_MODE:
                self.writeImage(dilate_image, path, 'hand_binary_'+str(threshold))

            img, cnts, hierarchy = cv2.findContours(dilate_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:number_hand]
            hand_angle = []
            ellipse = []
            if len(cnts) > 0:
                ellip = cv2.fitEllipse(cnts[0])
                #Get MA of maximun ellipse
                MA = ellip[1][0]
                for cnt in cnts:
                    ateConfig.log.logger.debug("Hand size: %s" %cnt.size)
                    if cnt.size > HAND_MINIMUM_POINT:
                        ellip = cv2.fitEllipse(cnt)
                        angle = ellip[2]
                        '''
                        #Re-calculation ellipse angle with upper horizontal
                        Note: ellipse angle is the angle between MA with horizontal in Clock-wise direction
                        '''
                        #Case 1: Hands are above center
                        if ellip[0][1] < h / 2:
                            angle = angle
                            #Hand at Quadrant II and ellipse angle is the angle MA with lower horizontal
                            #So + 180 to create an angle with the upper horizontal
                            if angle > 90:
                                angle = angle + 180
                        #Case 2: Hands are above center
                        else:
                            # Hand at Quadrant III and ellipse angle is the angle MA with lower horizontal
                            # So + 180 to create an angle with the upper horizontal
                            if angle < 90:
                                angle = angle + 180
                        '''
                        The sencond hand must meet the below requirements:
                        1. MA > ma*SIZE_HAND_COMPARE
                        2. The difference between the first MA and the current MA must be smaller than DIFF_RADIUS
                        '''
                        if ellip[1][1] > SIZE_HAND_COMPARE * ellip[1][0] and abs(ellip[1][0] - MA) < DIFF_RADIUS:
                            hand_angle.append(angle)
                            ellipse.append(ellip)
            if ellipse != []:
                # Detect 2 hands at the same position
                if len(hand_angle) == 1 and number_hand == 2:
                    hand_angle.append(hand_angle[0])
                if DEBUG_MODE:
                    if ellipse != []:
                        for e in ellipse:
                            image = cv2.ellipse(image, e, (0, 255, 0), 2)
                        self.writeImage(image, path, 'hand_detected_'+str(threshold))
                result['hand_angle'] = hand_angle
                result['ellipse'] = ellipse
                if DEBUG_MODE:
                    ateConfig.log.logger.debug('Hands angle: %s' %hand_angle)
                break
            else:
                result['hand_angle'] = hand_angle
                result['ellipse'] = ellipse
                ateConfig.log.logger.debug('Try next binary threshold')
        return result

    def RANSAC_circledetection(self, cnt, inline_threshold, number_point):
        '''
        :param cnt:
        :param inline_threshold:
        :param number_point:
        :return:
        '''

        p_num = 0
        best_circle = []
        for k in range(ITERATION):

            # Choose random 3 points
            id1 = random.randint(0, len(cnt) - 1)
            id2 = random.randint(0, len(cnt) - 1)
            while id2 == id1:
                id2 = random.randint(0, len(cnt) - 1)
            id3 = random.randint(0, len(cnt) - 1)
            while id2 == id1 or id3 == id1:
                id3 = random.randint(0, len(cnt) - 1)

            # Fit circle from three point
            x1 = float(cnt[id1][0][0])
            y1 = float(cnt[id1][0][1])
            x2 = float(cnt[id2][0][0])
            y2 = float(cnt[id2][0][1])
            x3 = float(cnt[id3][0][0])
            y3 = float(cnt[id3][0][1])

            a1 = 2 * (x1 - x2)
            b1 = 2 * (y1 - y2)
            c1 = x1 ** 2 - x2 ** 2 + y1 ** 2 - y2 ** 2
            a2 = 2 * (x3 - x2)
            b2 = 2 * (y3 - y2)
            c2 = x3 ** 2 - x2 ** 2 + y3 ** 2 - y2 ** 2

            if (b2 * a1 - b1 * a2) == 0:
                continue
            y = (c2 * a1 - c1 * a2) / (b2 * a1 - b1 * a2)
            x = (c2 * b1 - c1 * b2) / (a2 * b1 - a1 * b2)
            r = math.sqrt((cnt[id1][0][0] - x) ** 2 + (cnt[id1][0][1] - y) ** 2)

            # Consider number_point point
            num_inline = 0
            n = int(len(cnt) / number_point)
            for i in range(int(len(cnt) / n)):
                dist = abs(math.sqrt((cnt[n * i][0][0] - x) ** 2 + (cnt[n * i][0][1] - y) ** 2) - r)
                # Check point is inline
                if dist < RANSAC_THRESHOLD:
                    num_inline += 1

            # Check it is best circle
            if num_inline > p_num and num_inline > inline_threshold:
                best_circle = ((int(x), int(y)), int(r))
                p_num = num_inline

        return best_circle

    def dialCircleDetection(self, dialPlatform, binaryThreshold, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName):
        '''
        Finding dial circle
        :param pathOne:
        :param nameOne:
        :param pathTwo:
        :param nameTwo:
        :param kernel:
        :param writePath:
        :param writeNam:
        :return:
        '''

        result = {}

        ateConfig.log.logger.info('Finding Dial Watch...')
        # read two image
        imageOne = self.readImage(pathOne, nameOne)
        imageTwo = self.readImage(pathTwo, nameTwo)

        # convert image to gray
        img1_gray = cv2.cvtColor(imageOne, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(imageTwo, cv2.COLOR_BGR2GRAY)

        # get size of image
        h, w = img1_gray.shape
        best_circle = []

        for threshold in binaryThreshold:
            # apply threshold to convert image to binary
            if dialPlatform == 'white':
                ret, img1_binary = cv2.threshold(img1_gray, threshold, 255, cv2.THRESH_BINARY_INV)
                ret, img2_binary = cv2.threshold(img2_gray, threshold, 255, cv2.THRESH_BINARY_INV)
            elif dialPlatform == 'black' or dialPlatform == 'gray':
                ret, img1_binary = cv2.threshold(img1_gray, threshold, 255, cv2.THRESH_BINARY)
                ret, img2_binary = cv2.threshold(img2_gray, threshold, 255, cv2.THRESH_BINARY)

            # add two image to remove hands
            image_binary = cv2.add(img1_binary, img2_binary)
            image_binary = cv2.erode(image_binary, kernel, iterations=1)
            image_binary = cv2.dilate(image_binary, kernel, iterations=1)

            if DEBUG_MODE:
                self.writeImage(image_binary, pathOne, 'binary_dial')

            # find contour and sorted contour according to area
            im1, cnts, hierarchy = cv2.findContours(image_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

            if len(cnts) > 0:
                dials = []
                i = 0
                for cnt in cnts:
                    if len(cnt) > MINIMUM_POINT:
                        # ellipse approximation
                        circle = self.RANSAC_circledetection(cnt, INLINE_THRESHOLD, NUMBER_POINT)
                        if len(circle) > 0:
                            # check circle is concentricity
                            dist = math.sqrt((w / 2 - circle[0][0]) ** 2 + (h / 2 - circle[0][1]) ** 2)
                            if dist < MAX_CENTER_DISTANCE:
                                dials.append(circle)
                                # ateConfig.log.logger.debug("Found cirles: %s" %circle)
                for dial in dials:
                    if dial[1] > DIAL_RADIUS_MIN and dial[1] < DIAL_RADIUS_MAX:
                        best_circle = dial
                        if DEBUG_MODE:
                            imageOne = cv2.circle(imageOne, best_circle[0], best_circle[1], (0, 255, 0), 2)
                            self.writeImage(imageOne, pathOne, 'dial_circle')

                        # calculate dial radius
                        rMask = best_circle[1] - RADIUS_THRESHOLD
                        # get a mask is dial
                        kernel = 255 * cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * int(rMask), 2 * int(rMask)))
                        mask = np.zeros((int(h), int(w)), np.uint8)
                        mask = cv2.circle(mask, best_circle[0], best_circle[1]-2*RADIUS_THRESHOLD, (255, 255, 255), -1)

                        # mask[int(best_circle[0][1] - rMask):int(best_circle[0][1] + rMask), int(best_circle[0][0] - rMask):int(best_circle[0][0] + rMask)] = kernel

                        # Crop area inner dial
                        mask = mask[int(best_circle[0][1] - rMask - 2*RADIUS_THRESHOLD):int(best_circle[0][1] + rMask + 2*RADIUS_THRESHOLD), int(best_circle[0][0] - rMask - 2*RADIUS_THRESHOLD):int(best_circle[0][0] + rMask + 2*RADIUS_THRESHOLD)]
                        self.writeImage(mask, writePath, writeName)
                        result['dial'] = best_circle
                        result['threshold'] = threshold
                        break
            if best_circle != []:
                break

        return result

    def eInkCircleDetection(self, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName, dialCenter, binaryThreshold):
        '''
        Finding circle on dial
        :param pathOne:
        :param nameOne:
        :param pathTwo:
        :param nameTwo:
        :param kernel:
        :param writePath:
        :param writeNam:
        :return:
        '''

        result = {}

        ateConfig.log.logger.info('Finding EInk Circle...')

        # read two image
        imageOne = self.readImage(pathOne, nameOne)
        imageTwo = self.readImage(pathTwo, nameTwo)

        # convert image to gray
        img1_gray = cv2.cvtColor(imageOne, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(imageTwo, cv2.COLOR_BGR2GRAY)

        # get size of image
        h, w = img1_gray.shape

        for threshold in binaryThreshold:
            # threshold to convert image to binary
            ret, image1_binary = cv2.threshold(img1_gray, threshold, 255, cv2.THRESH_BINARY_INV)
            ret, image2_binary = cv2.threshold(img2_gray, threshold, 255, cv2.THRESH_BINARY_INV)

            if DEBUG_MODE:
                self.writeImage(image1_binary, pathOne, 'binary_eInkCircle_1_'+str(threshold))
                self.writeImage(image2_binary, pathOne, 'binary_eInkCircle_2_'+str(threshold))

            # delete hands via masks
            image1_binary[int(0):int(dialCenter[1]+HAND_SHIFT), int(dialCenter[0] - HAND_WIDTH/2):int(dialCenter[0] + HAND_WIDTH/2)] = 0
            image2_binary[int(dialCenter[1]-HAND_SHIFT):int(h), int(dialCenter[0] - HAND_WIDTH/2):int(dialCenter[0] + HAND_WIDTH/2)] = 0

            #Write image to debug and calibration in the factory
            if DEBUG_MODE:
                self.writeImage(image1_binary, pathOne, 'binary_eInkCircle_1_remove_hand'+str(threshold))
                self.writeImage(image2_binary, pathOne, 'binary_eInkCircle_2_remove_hand' + str(threshold))

            #Add 2 images to create a complete circle
            image_binary = cv2.add(image1_binary, image2_binary)

            image_binary = cv2.dilate(image_binary, kernel, iterations=1)
            image_binary = cv2.erode(image_binary, kernel, iterations=2)

            if DEBUG_MODE:
                self.writeImage(image_binary, pathOne, 'eInk_circle_mask')

            # find contour and sorted contours according to area
            dept, contours, hierarchy = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            circle = ''
            for cnt in contours:
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                radius = int(radius)
                if radius > EINK_CIRCLE_RADIUS_MIN and radius < EINK_CIRCLE_RADIUS_MAX:
                    circle = ((x, y), radius)
                    result['circle'] = circle
                    result['threshold'] = threshold
                    if DEBUG_MODE:
                        cv2.circle(imageOne, (int(x), int(y)), radius, (0, 255, 0), 3)
                        self.writeImage(imageOne, pathOne, 'eInk_circle_' + str(radius))
                    break
            if circle != '':
                break
            else:
                ateConfig.log.logger.debug('Try next binary threshold')

        return result

    def HandsEject(self, pathOne, nameOne, pathTwo, nameTwo, writePath, writeName, dial):
        '''
        Eject Hands on dial
        :param pathOne:
        :param nameOne:
        :param pathTwo:
        :param nameTwo:
        :param kernel:
        :param writePath:
        :param writeNam:
        :return:
        '''

        ateConfig.log.logger.info('Removing hands...')

        # read two image
        imageOne = self.readImage(pathOne, nameOne)
        imageTwo = self.readImage(pathTwo, nameTwo)

        # convert image to gray
        img1_gray = cv2.cvtColor(imageOne, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(imageTwo, cv2.COLOR_BGR2GRAY)

        # get size of image
        h, w = img1_gray.shape

        # eject hands
        img1_gray[dial[0][1]:int(h), 0:int(w)] = img2_gray[dial[0][1]:int(h), 0:int(w)]

        # apply mask to get dial area
        rMask = dial[1]
        kernel = 255 * cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * int(rMask), 2 * int(rMask)))
        mask = np.zeros((int(h), int(w)), np.uint8)
        mask[int(dial[0][1] - rMask):int(dial[0][1] + rMask), int(dial[0][0] - rMask):int(dial[0][0] + rMask)] = kernel
        img_gray = cv2.bitwise_and(img1_gray, mask)

        #Crop dial area
        crop_image = img_gray[int(dial[0][1] - rMask - RADIUS_THRESHOLD):int(dial[0][1] + rMask + RADIUS_THRESHOLD), int(dial[0][0] - rMask - RADIUS_THRESHOLD):int(dial[0][0] + rMask + RADIUS_THRESHOLD)]

        # img_blur = cv2.medianBlur(crop_image, BLUR_KSIZE_3)
        self.writeImage(crop_image, writePath, writeName)


    def eraseCenterCircle(self, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName):
        '''
        Erode a center circle
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Find and draw overlap circle center...')

        # Read image and convert to gray
        image1 = self.readImage(pathOne, nameOne)  # mask
        image2 = self.readImage(pathTwo, nameTwo)

        image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        # Get size of image
        h, w = image1_gray.shape

        image2 = cv2.bitwise_and(image1_gray, image2_gray)
        if DEBUG_MODE:
            self.writeImage(image2, pathTwo, "overlapOuterEdge")

        mask = np.zeros((int(h), int(w)), np.uint8)

        # Get only center of eink
        mask[int(h / 2) - EINK_CIRCLE_RADIUS_MIN:int(h / 2) + EINK_CIRCLE_RADIUS_MIN,
        int(w / 2) - EINK_CIRCLE_RADIUS_MIN:int(w / 2) + EINK_CIRCLE_RADIUS_MIN] = image2_gray[int(h / 2) - EINK_CIRCLE_RADIUS_MIN:int(h / 2) + EINK_CIRCLE_RADIUS_MIN, int(w / 2) - EINK_CIRCLE_RADIUS_MIN:int(w / 2) + EINK_CIRCLE_RADIUS_MIN]

        if DEBUG_MODE:
            self.writeImage(mask, pathTwo, "centerOriginal")
        # Continue find contour and get contour have max area
        dept, cnts, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # cv2.fillPoly(image2, [cnts[0]], (0, 0, 0))

        ellipse = cv2.fitEllipse(cnts[0])
        if DEBUG_MODE:
            ateConfig.log.logger.debug('Ellipse: ' + str(ellipse))
        # Get ellipse data
        (x, y) = ellipse[0]
        (MA, ma) = ellipse[1]
        # Calculate average of circle via MA, ma of ellipse
        radius = ((MA + ma) / 4)

        # Draw overlap circle to remove inner circle
        cv2.circle(image2, (int(x), int(y)),int(radius)+3, (0, 0, 0), -1)

        if DEBUG_MODE:
            self.writeImage(image2, pathTwo, "overlapInnerEdge")
        # #Do openning error pixels
        # image = cv2.dilate(image2, kernel, iterations=2)
        # image = cv2.erode(image, kernel, iterations=1)
        self.writeImage(image2, writePath, writeName)

    def deleteText(self, pathOne, nameOne, pathTwo, nameTwo, kernel, writePath, writeName):
        '''
        Erase Text on dial
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        result = {}
        ateConfig.log.logger.info('Erase brand text on watch face...')

        # Read image and convert to binary
        image1 = self.readImage(pathOne, nameOne)
        image2 = self.readImage(pathTwo, nameTwo)
        image_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        ret, image_gray = cv2.threshold(image_gray, WHITE_BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

        # Implement closing with long rectangle to get text area are rectangles
        image_gray = cv2.dilate(image_gray, kernel)
        image_gray = cv2.erode(image_gray, kernel)
        image_gray = cv2.dilate(image_gray, KERNEL3)

        # Implement opening to eject rectangles with short edge
       # image_gray = cv2.erode(image_gray, kernel)
       # image_gray = cv2.dilate(image_gray, kernel)

        if DEBUG_MODE:
            self.writeImage(image_gray, pathOne, "dilateText")

        # Find contour and sorted according to area
        dept, cnts, hierarchy = cv2.findContours(image_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[1:]

        # Get contours are rectangles and have area larger than min area.
        for cnt in cnts:
            # Get contour arclength
            peri = cv2.arcLength(cnt, True)

            # Approximate polygon
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            # Check polygon is a rectangle
            if len(approx) == 4:
                if cv2.contourArea(cnt) > MIN_RECT_AREA:
                    result['brand_area'] = cv2.contourArea(cnt)
                    # Approximate rectangle
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    # Erase text region
                    cv2.fillPoly(image2, [box], (0, 0, 0))
        self.writeImage(image2, writePath, writeName)

        return result

    def basicEdgesDetection(self, path, name, kernel, writePath, writeName):
        '''
        find all edges in an image using basic edge detection
        :param path:
        :param name:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Edge Detection in the image')

        # Read image and convert to gary
        image = self.readImage(path, name)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Erode operating
        erode = cv2.erode(image_gray, kernel)

        # Subtract to get edge
        edges_img = cv2.absdiff(erode, image_gray)

        # Save image
        self.writeImage(edges_img, writePath, writeName)

    def medianInvThreshold(self, path, name, size, kernel, writePath, writeName):
        '''
        :param path:
        :param name:
        :param size:
        :param kernel:
        :param writePath:
        :param writeName:
        :return:
        '''
        ateConfig.log.logger.info('Convert image to binary image via adaptive threshold method')
        image = self.readImage(path, name)
        # Convert image to binary image using invert binary
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_inv_binary = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, size[0], size[1])
        # image_inv_binary = cv2.dilate(image_inv_binary, kernel)
        # image_inv_binary = cv2.erode(image_inv_binary, kernel)
        self.writeImage(image_inv_binary, writePath, writeName)

    def dialPlatformDetection(self, path, name):
        '''
        Base on image to find dial platform
        :param path:
        :param name:
        :return: platform
        '''
        result = {}
        image = self.readImage(path, name)
        mask = self.readImage(DIANA_IMAGE, 'dialMask')
        and_image = cv2.bitwise_and(image, mask)
        image_gray = cv2.cvtColor(and_image, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([image_gray], [0], None, [256], [0, 256])
        #only get mean from pixel has value 20 since most of image is black
        mean_hist = np.mean(hist[DIAL_MEAN_START_PIXEL:])
        ateConfig.log.logger.debug('Average of histogram: %s' %mean_hist)
        '''
        Based on dial histogram:
            - Clarify dial platform: black or white
            - Choose the proper binary threshold going along with dial platform
        '''
        if mean_hist <= DIAL_PLATFORM_THRESHOLD:
            result['platform'] = 'black'
            result['inv_threshold'] = CIRCLE_THRES_INV_BINARY_BLACK
            if mean_hist <= MEAN_HIST_BLACK:
                result['threshold'] = DIAL_BINARY_LEVEL_1
            elif mean_hist > MEAN_HIST_BLACK and mean_hist < MEAN_HIST_LIGHT_GRAY:
                result['threshold'] = DIAL_BINARY_LEVEL_2
            elif mean_hist >= MEAN_HIST_LIGHT_GRAY and mean_hist < MEAN_HIST_GRAY:
                result['threshold'] = DIAL_BINARY_LEVEL_3
            elif mean_hist >= MEAN_HIST_GRAY and mean_hist < MEAN_HIST_MORE_GRAY:
                result['threshold'] = DIAL_BINARY_LEVEL_4
        else:
            result['platform'] = 'white'
            result['inv_threshold'] = CIRCLE_THRES_INV_BINARY_WHITE
            if mean_hist < MEAN_HIST_LIGHT_WHITE:
                result['threshold'] = DIAL_BINARY_LEVEL_5
            elif mean_hist >= MEAN_HIST_LIGHT_WHITE and mean_hist < MEAN_HIST_WHITE:
                result['threshold'] = DIAL_BINARY_LEVEL_6
            else:
                result['threshold'] = DIAL_BINARY_LEVEL_7
        ateConfig.log.logger.info('Dial platform: %s' % result['platform'])

        return result

    def extractBrand(self, path, name, kernel, writePath, writeName):
        '''

        :param path:
        :param name:
        :return: image without brand name
        '''
        ateConfig.log.logger.info('Extracting Brand Name...')
        result = {}
        image = self.readImage(path, name)
        image_cp = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        height, width = gray.shape
        xIcon = []
        yIcon = []
        wIcon = []
        hIcon = []

        binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        binary_image_erode = cv2.erode(binary_image, KERNEL3, iterations=1)
        binary_image_dilate = cv2.dilate(binary_image_erode, kernel, iterations=3)

        dept, cnts, hierarchy = cv2.findContours(binary_image_dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[1:]
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            # if DEBUG_MODE:
            #     ateConfig.log.logger.debug("area icon: %s" % (w * h))
            #Get the brand area
            if w * h > BRAND_MIN_AREA and w * h < BRAND_MAX_AREA and w/h > BRAND_NAME_RATIO:
                xIcon.append(x)
                yIcon.append(y)
                wIcon.append(w)
                hIcon.append(h)
        if len(xIcon) > 0:
            # Save all icons in list
            for i in range(0, len(xIcon)):
                icon = binary_image_dilate[yIcon[i]:yIcon[i] + hIcon[i] + 5, xIcon[i]:xIcon[i] + wIcon[i] + 5]
                cv2.rectangle(image_cp, (xIcon[i], yIcon[i]), (xIcon[i] + wIcon[i], yIcon[i] + hIcon[i]),(0, 255, 0), 2)
                cv2.rectangle(image, (xIcon[i]-5, yIcon[i]-5), (xIcon[i] + wIcon[i]+5, yIcon[i] + hIcon[i]+5),(0, 0, 0), -1)
                # self.writeImage(icon, path, 'test' + '_' + str(i))
            if DEBUG_MODE:
                self.writeImage(image_cp, path, 'brand_extract')
        self.writeImage(image, writePath, writeName)