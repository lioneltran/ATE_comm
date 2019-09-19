
import logging
import numpy as np
import re
import os
from ate_settings import*
from configuration import nanoConfig

SAVE_FILES_LOCAL    = True

if STATION_ID == '1':
    SAVE_FILES_LOCAL = True

if SAVE_FILES_LOCAL:
    # Store Images to Pi Local
    DIANA_IMAGE                 = nanoConfig.DIANA_IMAGE
    CONCENTR_IMAGE              = DIANA_IMAGE + 'concentricity/'
    ALIGNMENT_IMAGE             = DIANA_IMAGE + 'alignment/'
    DEAD_PIXEL_IMAGE            = DIANA_IMAGE + 'deadPixels/'
    LED_UNIFORM_IMAGE           = DIANA_IMAGE + 'LEDUniform/'
    HAND_DETECT_IMAGE           = DIANA_IMAGE + 'handDrag/'
else:
    # Store Images to External USB Disk, "media/pi/ATE_IMAGES/", USB disk name/label must be: "ATE_IMAGES"
    DIANA_IMAGE                 = nanoConfig.DIANA_IMAGE
    CONCENTR_IMAGE              = '/media/pi/ATE_IMAGES/Images/concentricity/'
    ALIGNMENT_IMAGE             = '/media/pi/ATE_IMAGES/Images/alignment/'
    DEAD_PIXEL_IMAGE            = '/media/pi/ATE_IMAGES/Images/deadPixels/'
    LED_UNIFORM_IMAGE           = '/media/pi/ATE_IMAGES/Images/LEDUniform/'
    HAND_DETECT_IMAGE           = '/media/pi/ATE_IMAGES/Images/handDrag/'
    pathImage = os.path.exists(DIANA_IMAGE)
    if not pathImage:
        ateConfig.log.logger.info("Creating storage images folders")
        os.makedirs(DIANA_IMAGE)
    concentr_image = os.path.exists(CONCENTR_IMAGE)
    alignment_image = os.path.exists(ALIGNMENT_IMAGE)
    dead_pixel = os.path.exists(DEAD_PIXEL_IMAGE)
    led_image = os.path.exists(LED_UNIFORM_IMAGE)
    hand_detect = os.path.exists(HAND_DETECT_IMAGE)
    if not concentr_image:
        os.makedirs(CONCENTR_IMAGE)
    if not alignment_image:
        os.makedirs(ALIGNMENT_IMAGE)
    if not led_image:
        os.makedirs(LED_UNIFORM_IMAGE)
    if not hand_detect:
        os.makedirs(HAND_DETECT_IMAGE)
    if not dead_pixel:
        os.makedirs(DEAD_PIXEL_IMAGE)

#Camera Params
EXPOSURE_COMPENSATION_WHITE = 1
EXPOSURE_COMPENSATION_BLACK = -8
CAMERA_RESOLUTION_X         = 2560
CAMERA_RESOLUTION_Y         = 1920
CAMERA_SHARPNESS            = 50
CAMERA_CONTRAST             = 50
CAMERA_BRIGHTNESS           = 50
CAMERA_SATURATION           = -30
CAMERA_ISO                  = 0
CAMERA_STABILIZATION        = True
CAMERA_EXPOSURE_MODE        = 'night'
CAMERA_METER_MODE           = 'average'
CAMERA_MODE                 = 'off'
CAMERA_AWB_GAINS            = 1.2
CAMERA_ROTATION             = 0
CAMERA_HFLIP                = False
CAMERA_VFLIP                = False

#Common vision parameters
BINARY_THRESHOLD            = 40 #20, 30
IMAGE_RESIZE                = 600
RECT_EXTEN_THRES            = 10
BLUR_KSIZE_5                = 5
BLUR_KSIZE_3                = 3
KERNEL1                     = np.ones((1, 1), np.uint8)
KERNEL2                     = np.ones((2, 2), np.uint8)
KERNEL3                     = np.ones((3, 3), np.uint8)
KERNEL5                     = np.ones((5, 5), np.uint8)
KERNEL7                     = np.ones((7, 7), np.uint8)
KERNEL9                     = np.ones((9, 9), np.uint8)
KERNEL11                    = np.ones((11, 11), np.uint8)
KERNEL3x15                  = np.ones((3, 15), np.uint8)
GAUSSIAN_BLUR_KSIZE_9       = (9, 9)
GAUSSIAN_BLUR_KSIZE_5       = (5, 5)
GAUSSIAN_BLUR_KSIZE_3       = (3, 3)
CANNY_THRESHOLD_1           = 100  # first threshold for the hysteresis procedure.
CANNY_THRESHOLD_2           = 200  # second threshold for the hysteresis procedure.
APERTURE_SIZE               = (2, 2)  # aperture size for the Sobel() operator

#======================================================
#Dial platform for each sku with white background color
DIAL_PLATFORM               = ['F102', 'F103', 'F104', 'F105', 'E002']
#======================================================

if STATION_ID == '1' or STATION_ID == '2':
    # Limits paramter
    MAX_DIST_TWO_CENTERS        = 0.2194 #mm
    CONTOUR_MIN_AREA            = 10
    CONTOUR_MAX_AREA            = 1000000
    EINK_ROTATE_ANGLE_UPPER     = 16.60  # (mean + 4*sigma)
    EINK_ROTATE_ANGLE_LOWER     = 13.02  # (mean + 4*sigma)
    PCBA_ROTATE_ANGLE_UPPER     = 12.76  # (mean + 4*sigma)
    PCBA_ROTATE_ANGLE_LOWER     = 9.56   # (mean + 4*sigma)
    CHASSIS_HOLES_HORIZ_ANGLE   = 15  # angle between 2 chassis holes and perfect horizontal is 15 degrees (constant)
    PCBA_HORIZ_ANGLE            = 11.06  # angle between 2 fiducial holes and perfect horizontal is 15 degrees (constant)
    HAND_MINIMUM_POINT          = 350

    # Concentricity Test Params
    CONCENTRICITY_CROP_X1       = 1100
    CONCENTRICITY_CROP_X2       = 1500
    CONCENTRICITY_CROP_Y1       = 800
    CONCENTRICITY_CROP_Y2       = 1150
    PINION_X_CENTER             = 190
    PINION_Y_CENTER             = 160
    PINION_BINARY_THRESHOLD     = [40, 50, 60, 70, 30, 20]
    EINK_BINARY_THRESHOLD       = [40, 50, 60, 70]
    EINK_INNER_RADIUS           = 40
    EINK_OUTER_RADIUS           = 140
    EINK_INNER_RADIUS_MIN       = 65
    EINK_INNER_RADIUS_MAX       = 70
    INNER_CIRCLE_RADIUS_MIN     = 18
    INNER_CIRCLE_RADIUS_MAX     = 23
    OUTER_CIRCLE_RADIUS_MIN     = 67
    OUTER_CIRCLE_RADIUS_MAX     = 70
    PINION_MIN_AREA             = 900
    PINION_MAX_AREA             = 1200
    PINION_RADIUS_MASK          = 45
    EINK_MIN_AREA               = 7000
    EINK_MAX_AREA               = 10000

    # New Math Modeling
    INTERFERENCE_DISTANCE       = 0.1
    PINION_RADIUS               = 0.6   # Pinion Radius = 0.6 as spec
    PINION_TOLERANCE            = 0.016 # Pinion tolerance = 0.016 as spec
    # For station DW.MM.2-Flex.1.ZH
    if ATE_ID == 'DW.MM.2-Flex.1.ZH':
        INTERFERENCE_OFFSET     = 0.034
    # For station DW.MM.2-Flex.2.ZH
    elif ATE_ID == 'DW.MM.2-Flex.2.ZH':
        INTERFERENCE_OFFSET     = 0.019
    # For station DW.MM.2-Flex.3.ZH
    elif ATE_ID == 'DW.MM.2-Flex.3.ZH':
        INTERFERENCE_OFFSET     = 0.03
    # For station DW.MM.2-Flex.4.ZH
    elif ATE_ID == 'DW.MM.2-Flex.4.ZH':
        INTERFERENCE_OFFSET     = 0.05
    # For station DW.MM.2-Flex.5.ZH
    elif ATE_ID == 'DW.MM.2-Flex.5.ZH':
        INTERFERENCE_OFFSET     = 0.05
    # For station DW.MM.2-Flex.6.ZH
    elif ATE_ID == 'DW.MM.2-Flex.6.ZH':
        INTERFERENCE_OFFSET     = 0.06
    # For station DW.MM.2-Flex.1.ZH
    elif ATE_ID == 'DW.MM.2-PT.1.SZ':
        INTERFERENCE_OFFSET     = 0.034

    # For development stations in VN and SF
    else:
        INTERFERENCE_OFFSET     = 0.03


    # Alignment Test Params
    # Rectangle cropped positions
    RECT_THRES_BINARY           = 180
    ALIGN_RECT_CROP_X_1         = 1100
    ALIGN_RECT_CROP_X_2         = ALIGN_RECT_CROP_X_1 + 400
    ALIGN_RECT_CROP_Y_1         = 600
    ALIGN_RECT_CROP_Y_2         = ALIGN_RECT_CROP_Y_1 + 300
    RECT_MIN_AREA               = 100
    BLOCK_SIZE                  = 15
    MIN_EINK_CIRCLE_AREA        = 10000

    # Fiducial and Hole cropped positions
    FIDUCIAL_THRES_BINARY       = [240, 220, 200, 180, 150]
    HOLE_1_THRES_BINARY           = [60, 70, 50, 40, 30, 20, 10]
    HOLE_2_THRES_BINARY           = [40, 30, 20, 10, 60, 70, 50]
    ALIGN_F1_CROP_X_1           = 380
    ALIGN_F1_CROP_X_2           = ALIGN_F1_CROP_X_1 + 200
    ALIGN_F1_CROP_Y_1           = 980
    ALIGN_F1_CROP_Y_2           = ALIGN_F1_CROP_Y_1 + 200
    ALIGN_F2_CROP_X_1           = 1990
    ALIGN_F2_CROP_X_2           = ALIGN_F2_CROP_X_1 + 200
    ALIGN_F2_CROP_Y_1           = 680
    ALIGN_F2_CROP_Y_2           = ALIGN_F2_CROP_Y_1 + 180
    ALIGN_H1_CROP_X_1           = 400
    ALIGN_H1_CROP_X_2           = ALIGN_H1_CROP_X_1 + 200
    ALIGN_H1_CROP_Y_1           = 650
    ALIGN_H1_CROP_Y_2           = ALIGN_H1_CROP_Y_1 + 200
    ALIGN_H2_CROP_X_1           = 2000
    ALIGN_H2_CROP_X_2           = ALIGN_H2_CROP_X_1 + 200
    ALIGN_H2_CROP_Y_1           = 1120
    ALIGN_H2_CROP_Y_2           = ALIGN_H2_CROP_Y_1 + 180
    FIDUCIAL_RADIUS_MAX         = 26
    FIDUCIAL_RADIUS_MIN         = 22
    HOLE_RADIUS_MAX             = 40
    HOLE_RADIUS_MIN             = 30
    FIDUCIAL_MIN_AREA           = 700
    FIDUCIAL_MAX_AREA           = 1300
    FIFUCIAL_MA_ma_RATIO        = 1.6
    HOLE_1_MIN_AREA             = 1400
    HOLE_1_MAX_AREA             = 2100
    HOLE_2_MIN_AREA             = 900
    HOLE_2_MAX_AREA             = 1500
    HOLE_MA_ma_RATIO            = 1.7

    # Dead Pixels Test Params
    BLACK_BINARY_THRESHOLD      = 20
    WHITE_BINARY_THRESHOLD      = 20
    MAX_CIRCLE_RADIUS           = 200
    MIN_CIRCLE_RADIUS           = 100
    RADIUS_THRESHOLD            = 5
    EINK_EDGE_RADIUS            = 770
    ACTIVE_EINK_REGION          = 'activeEInkRegion'
    # LED uniform params
    LED_THRES_BINARY            = 200
    HIST_LOWER_PIXEL_VALUE      = 100
    HIST_AVERAGE_LOWER_LIMIT    = 1300
    HIST_INTERSECT_LOWER_LIMIT  = 27000
    LED_MIN_AREA                = 20000
    MODULE_RADIUS               = 900

    CONCENTRICITY_CIRLCE_CROP_X1 = 800
    CONCENTRICITY_CIRLCE_CROP_X2 = 1450
    CONCENTRICITY_CIRLCE_CROP_Y1 = 630
    CONCENTRICITY_CIRLCE_CROP_Y2 = 1200
    BRAND_MIN_AREA               = 4000
    BRAND_MAX_AREA               = 40000
    BRAND_NAME_RATIO             = 4

    DIAL_BINARY_THRESHOLD        = [30, 40, 50]
    CENTER_CIRCLE_THRESHOLD      = [100, 120]


elif STATION_ID == '3':
        # Hand drag params
        MINIMUM_POINT                = 10
        # LIMIT_ANGLE                  = 3
        DIFF_RADIUS                  = 15
        SIZE_HAND_COMPARE            = 5
        # RADIUS_RATIO                 = 2
        HAND_MINIMUM_POINT           = 350
        # LED uniform params
        LED_THRES_BINARY             = 240
        HIST_LOWER_PIXEL_VALUE       = 200
        HIST_AVERAGE_LOWER_LIMIT     = 200
        HIST_INTERSECT_LOWER_LIMIT   = 100
        HAND_THRES_BINARY            = [30, 40]
        LED_MIN_AREA                 = 50
        MODULE_RADIUS                = 900

        RECT_THRES_BINARY            = 50
        ALIGN_RECT_CROP_X_1          = 1200
        ALIGN_RECT_CROP_X_2          = 1480
        ALIGN_RECT_CROP_Y_1          = 650
        ALIGN_RECT_CROP_Y_2          = 880
        ALIGN_F1_CROP_X_1            = 20
        ALIGN_F1_CROP_X_2            = 260
        ALIGN_F1_CROP_Y_1            = 830
        ALIGN_F1_CROP_Y_2            = 1130
        ALIGN_F2_CROP_X_1            = 2130
        ALIGN_F2_CROP_X_2            = 2280
        ALIGN_F2_CROP_Y_1            = 850
        ALIGN_F2_CROP_Y_2            = 1120
        FIDUCIAL_THRES_BINARY        = [180, 200, 80, 100, 120]
        FIDUCIAL_MIN_AREA            = 5000
        FIDUCIAL_MAX_AREA            = 13000
        FIFUCIAL_MA_ma_RATIO         = 1.6
        HRM_EINK_ALIGN_LOWER_LIMIT   = 10
        ALIGN_H1_CROP_X_1            = 230
        ALIGN_H1_CROP_X_2            = ALIGN_H1_CROP_X_1 + 220
        ALIGN_H1_CROP_Y_1            = 620
        ALIGN_H1_CROP_Y_2            = ALIGN_H1_CROP_Y_1 + 220
        ALIGN_H2_CROP_X_1            = 2060
        ALIGN_H2_CROP_X_2            = ALIGN_H2_CROP_X_1 + 220
        ALIGN_H2_CROP_Y_1            = 1170
        ALIGN_H2_CROP_Y_2            = ALIGN_H2_CROP_Y_1 + 220
        HOLE_RADIUS_MAX              = 40
        HOLE_RADIUS_MIN              = 30
        HOLE_MIN_AREA                = 1100
        HOLE_MAX_AREA                = 1800
        RECT_MIN_AREA                = 100
        HOLE_1_MIN_AREA             = 1300
        HOLE_1_MAX_AREA             = 1800
        HOLE_2_MIN_AREA             = 900
        HOLE_2_MAX_AREA             = 1300
        HOLE_MA_ma_RATIO            = 1.7
        HOLE_1_THRES_BINARY          = [60, 70, 50, 40, 30, 20, 10]
        HOLE_2_THRES_BINARY          = [40, 30, 20, 10, 60, 70, 50]
        # Concentricity Test Params
        MAX_DIST_TWO_CENTERS         = 0.3179 #mm
        CONCENTRICITY_CROP_X1        = 600
        CONCENTRICITY_CROP_X2        = 2050
        CONCENTRICITY_CROP_Y1        = 250
        CONCENTRICITY_CROP_Y2        = 1650
        HAND_WIDTH                   = 170
        HAND_SHIFT                   = 160
        CONCENTRICITY_CIRLCE_CROP_X1 = 1030
        CONCENTRICITY_CIRLCE_CROP_X2 = 1660
        CONCENTRICITY_CIRLCE_CROP_Y1 = 620
        CONCENTRICITY_CIRLCE_CROP_Y2 = 1210
        MAX_CENTER_DISTANCE          = 120
        DIAL_RADIUS_MIN              = 400
        DIAL_RADIUS_MAX              = 600
        EINK_CIRCLE_RADIUS_MIN       = 150
        EINK_CIRCLE_RADIUS_MAX       = 250
        DIAL_BINARY_THRESHOLD        = [30, 40, 50]
        CENTER_CIRCLE_THRESHOLD      = [100, 120]

        # New Math Modeling
        INTERFERENCE_DISTANCE        = 0.1
        INTERFERENCE_OFFSET          = 0.05
        PINION_RADIUS                = 0.6    # Pinion Radius = 0.6 as spec
        PINION_TOLERANCE             = 0.016  # Pinion tolerance = 0.016 as spec

        # RANSAC params
        ITERATION                    = 30
        NUMBER_POINT                 = 50
        RANSAC_THRESHOLD             = 5
        INLINE_THRESHOLD             = 30
        MINIMUM_POINT                = 200
        ELLIPSE_MIN_POINTS           = 5
        # Dead Pixels Test Params
        BLACK_BINARY_THRESHOLD       = 20
        WHITE_BINARY_THRESHOLD       = 40
        CANNY_THRESHOLD_1            = 10  # first threshold for the hysteresis procedure.
        CANNY_THRESHOLD_2            = 10  # second threshold for the hysteresis procedure
        RADIUS_THRESHOLD             = 10
        MIN_RECT_AREA                = 1000
        CONTOUR_MIN_AREA             = 2
        CONTOUR_MAX_AREA             = 1000000
        EINK_EDGE_RADIUS             = 850
        BLOCK_SIZE                   = 15
        PINION_BINARY_THRESHOLD      = [40, 60, 80]
        PINION_MIN_AREA              = 500000
        PINION_MAX_AREA              = 850000
        BRAND_MIN_AREA               = 4000
        BRAND_MAX_AREA               = 40000
        BRAND_NAME_RATIO             = 4
        ACTIVE_EINK_REGION           = 'activeEInkRegion'

#=======================================#
#Watch dial params: Based on histogram to
#define 6 dial platforms:
#black, light gray, gray, more gray,
#light white, white
#=======================================#
# Dial platform mean histogram threshold
DIAL_PLATFORM_THRESHOLD      = 2500
DIAL_MEAN_START_PIXEL        = 20

#Mean histogram level of dial
MEAN_HIST_BLACK             = 500
MEAN_HIST_LIGHT_GRAY        = 1200
MEAN_HIST_GRAY              = 1500
MEAN_HIST_MORE_GRAY         = 2500
MEAN_HIST_LIGHT_WHITE       = 3300
MEAN_HIST_WHITE             = 3600

#Define 5 level binary threshold for dial platform
DIAL_BINARY_LEVEL_1          = [40, 50]         #Histogram's Average < 500
DIAL_BINARY_LEVEL_2          = [60, 70]         #Histogram's Average < 1000
DIAL_BINARY_LEVEL_3          = [90, 100]        #Histogram's Average < 1500
DIAL_BINARY_LEVEL_4          = [100, 110]       #Histogram's Average < 2000
DIAL_BINARY_LEVEL_5          = [40, 60]         #Histogram's Average < 3300
DIAL_BINARY_LEVEL_6          = [100, 80]        #Histogram's Average > 3300
DIAL_BINARY_LEVEL_7          = [120, 80]        #Histogram's Average > 3300
CIRCLE_THRES_INV_BINARY_BLACK= [100]
CIRCLE_THRES_INV_BINARY_WHITE= [80]