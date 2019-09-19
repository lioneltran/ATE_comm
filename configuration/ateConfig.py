# from utilities.log import Log
from utilities.log import Log
import logging
import os
DEBUG_MODE = '10000'
# global logging variable
# instantiated once first time this module is loaded
# Five log levels - CRITICAL, ERROR, WARNING, INFO, and DEBUG
# For development, set to DEBUG.  For production, set to WARNING.
if DEBUG_MODE == '10000':
    log = Log(logging.DEBUG)
elif DEBUG_MODE == '20000':
    log = Log(logging.INFO)
elif DEBUG_MODE == '30000':
    log = Log(logging.WARN)
elif DEBUG_MODE == '40000':
    log = Log(logging.ERROR)

PROCESSED_IMAGES = '/home/nano/misfit/ShineProduction/newATE/Images/processed/'
PROJECT_PATH    = '/home/nano/misfit/ShineProduction/newATE/'
TRANSFER_PATH   = '/home/nano/misfit/ShineProduction/newATE/Images/transfer/'
DIANA_IMAGE     = '/home/nano/misfit/ShineProduction/newATE/Images/'
DIANA_IMAGE_RAW = '/home/nano/misfit/ShineProduction/newATE/Images/raw/'
LOCAL_IMAGE_PROCESSING_RESULT = PROCESSED_IMAGES + 'image_processing_result.json'
LOCAL_PASSWORD          = 'root'

LOGPATH                 = '/home/nano/misfit/ShineProduction/newATE/logs/'

if not os.path.isdir(PROCESSED_IMAGES):
    os.makedirs(PROCESSED_IMAGES)
if not os.path.isdir(TRANSFER_PATH):
    os.makedirs(TRANSFER_PATH)
if not os.path.isdir(DIANA_IMAGE):
    os.makedirs(DIANA_IMAGE)
if not os.path.isdir(DIANA_IMAGE_RAW):
    os.makedirs(DIANA_IMAGE_RAW)

os.chmod(PROCESSED_IMAGES, 0o777)
os.chmod(TRANSFER_PATH, 0o777)
os.chmod(DIANA_IMAGE, 0o777)
os.chmod(DIANA_IMAGE_RAW, 0o777)
# For SFTP
# For SFTP
REMOTE_IP               = '10.0.1.1'
REMOTE_USERNAME         = 'pi'
REMOTE_PASSWORD         = 'root'
REMOTE_PORT             = 22
REMOTE_DIANA_IMAGE      = '/home/pi/misfit/ShineProduction/newATE/Images/'
REMOTE_TRANSFER_PATH    = REMOTE_DIANA_IMAGE + 'Transfer/'
REMOTE_IMAGE_PROCESSING_RESULT = '/home/pi/misfit/ShineProduction/newATE/image_processing_result.json'
REMOTE_PROJECT_PATH    = '/home/pi/misfit/ShineProduction/newATE/'

# LOCAL_DIR       = PROJECT_PATH + 'sftp/'
# REMOTE_IMAGE     = '/home/nano/misfit/ShineProduction/newATE/'
# REMOTE_IMAGE_TRANSFER    = '/home/nano/misfit/ShineProduction/newATE/images/transfer/'

componentID = {
    'HT_ACCEL'          : '161',    #0xA1
    'HT_HAPTICS'        : '162',    #0xA2
    'HT_MOV'            : '163',    #0xA3
    'HT_MCU'            : '164',    #0xA4
    'HT_FL'             : '165',    #0xA5
    'HT_PMU'            : '166',    #0xA6
    'HT_DISPLAY'        : '167',    #0xA7
    'HT_MSP'            : '168',    #0xA8
    'HT_PUSH'           : '169',    #0xA9
    'HT_EXT_FLASH'      : '170',    #0xAA
    'HT_RADIO'          : '171',    #0xAB
    'HT_MIC'            : '172',    #0xAC
    'HT_FILE_TRANSFER'  : '173',    #0xAD
    'HT_NANO'           : '174',    #0xAE
}
commandID ={
    'HT_ACCEL_1'          : '1',
    'HT_ACCEL_2'          : '2',
    'HT_ACCEL_3'          : '3',
    'HT_ACCEL_4'          : '4',
    'HT_HAPTICS_1'        : '1',
    'HT_HAPTICS_2'        : '2',
    'HT_HAPTICS_3'        : '3',
    'HT_HAPTICS_4'        : '4',
    'HT_MOV_1'            : '1',
    'HT_MOV_2'            : '2',
    'HT_MOV_3'            : '3',
    'HT_MOV_4'            : '4',
    'HT_MOV_5'            : '5',
    'HT_MCU_1'            : '1',
    'HT_MCU_2'            : '2',
    'HT_MCU_3'            : '3',
    'HT_MCU_4'            : '4',
    'HT_MCU_5'            : '5',
    'HT_MCU_6'            : '6',
    'HT_MCU_7'            : '7',
    'HT_MCU_8'            : '8',
    'HT_MCU_9'            : '9',
    'HT_MCU_10'           : '10',
    'HT_MCU_11'           : '11',
    'HT_FL_1'             : '1',
    'HT_FL_2'             : '2',
    'HT_FL_3'             : '3',
    'HT_PMU_1'            : '1',
    'HT_PMU_2'            : '2',
    'HT_PMU_3'            : '3',
    'HT_PMU_4'            : '4',
    'HT_PMU_5'            : '5',
    'HT_PMU_6'            : '6',
    'HT_PMU_7'            : '7',
    'HT_PMU_8'            : '8',
    'HT_PMU_9'            : '9',
    'HT_PMU_10'           : '10',
    'HT_DISPLAY_1'        : '1',
    'HT_DISPLAY_2'        : '2',
    'HT_DISPLAY_3'        : '3',
    'HT_DISPLAY_4'        : '4',
    'HT_DISPLAY_5'        : '5',
    'HT_DISPLAY_6'        : '6',
    'HT_DISPLAY_7'        : '7',
    'HT_MSP_1'            : '1',
    'HT_MSP_2'            : '2',
    'HT_MSP_3'            : '3',
    'HT_MSP_4'            : '4',
    'HT_PUSH_1'           : '1',
    'HT_PUSH_2'           : '2',
    'HT_PUSH_3'           : '3',
    'HT_EXT_FLASH_1'      : '1',
    'HT_EXT_FLASH_2'      : '2',
    'HT_EXT_FLASH_3'      : '3',
    'HT_EXT_FLASH_4'      : '4',
    'HT_EXT_FLASH_5'      : '5',
    'HT_RADIO_1'          : '1',
    'HT_RADIO_2'          : '2',
    'HT_RADIO_3'          : '3',
    'HT_MIC_1'            : '1',
    'HT_MIC_2'            : '2',
    'HT_FILE_TRANSFER_1'  : '1', # File Transfer Status
    'HT_FILE_TRANSFER_2'  : '2', # Send File info: file name and file size
    'HT_FILE_TRANSFER_3'  : '3', # When file transfer completed, send to notify
    'HT_FILE_TRANSFER_4'  : '4', # Get File Transfer Status
    'HT_FILE_TRANSFER_5'  : '5', # Get File Transfer Info: wait for file name and file size

    'HT_NANO_1'           : '1', # For Open Nano Connection
    'HT_NANO_2'           : '2', # For Start Hand Drag Test Nano
    'HT_NANO_3'           : '3', # For Start Circles Concentricity Test ATE3 Nano
    'HT_NANO_4'           : '4', # For Start EInk Dead Pixel Test ATE3 Nano
    'HT_NANO_5'           : '5', # For Start LED Uniforming Test ATE3 Nano
    'HT_NANO_6'           : '6', # For Get status of Hand Drag Test Nano
    'HT_NANO_7'           : '7', # For Get status of Circles Concentricity Test ATE3 Nano
    'HT_NANO_8'           : '8', # For Get status of EInk Dead Pixel Test ATE3 Nano
    'HT_NANO_9'           : '9', # For Get status of LED Uniforming Test ATE3 Nano
    'HT_NANO_10'          : '10',# For starting processing images
    'HT_NANO_11'          : '11',  # For restart controller

}