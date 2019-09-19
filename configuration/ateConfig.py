
from utilities.log import Log
import logging
import numpy as np
from ate_settings import*
import re

DEBUG_MODE = False
# global logging variable
# instantiated once first time this module is loaded
# Five log levels - CRITICAL, ERROR, WARNING, INFO, and DEBUG
# For development, set to DEBUG.  For production, set to WARNING.
if DEBUG_MODE == True:
    log = Log(logging.DEBUG)
else:
    log = Log(logging.INFO)

DEVICE_TYPE = 'Diana'
MCU = 'Apollo2'
FONT_FILE_PATH ='/home/pi/misfit/ShineProduction/newATE/tests/diana_fonts_unhinted_cjk.fmp'
PROJECT_PATH = '/home/pi/misfit/ShineProduction/newATE/'
DESKTOP_PATH = "/home/pi/Desktop/"
# projects
projectList=["Diana"]

#===============================================================================
# STATION SOFTWARE VERSION
#===============================================================================
#Version scheme is defined as
#<station_type>.<product>.<major>.<minor>.<internal_rev>.<prod | dev>

STATION = "ATE"             # Can be either ATE or RMA
PRODUCT = DEVICE_TYPE       # The product type
MAJOR = "1"                 # Major version
MINIOR = "1"                # Minior version
INTERNAL = "1"             # Internal version - used for development.
RELEASE_TYPE = "prod"        # Can be either prod or dev - prod indicates that it is used on the production floor.  dev indicates it's used for development.
BUILD = 'PV'
STATION_SOFTWARE_VERSION = STATION + "." + PRODUCT + "." + MAJOR + "." + MINIOR + "." + INTERNAL + "." + RELEASE_TYPE

#===============================================================================
# SUPPORTED DEVICE FIRMWARE VERSIONS
#===============================================================================
FW_VERSIONS=['DN1.0.2.3r.prod.v7', 'DN1.0.2.3r.prod.v8', 'DN1.0.2.3r.prod.v9']

# ===============================================================================
# MANUFACTURER INFORMATION
# ===============================================================================
MANUFACTURER_NAME = 'Endor'
TEST_LOCATION = 'China'

DIR = "/home/pi/Desktop/FlexFlow/"
UMOUNT_CMD = "umount " + DIR
MOUNT_CMD = ""
MOUNT_TEST_FOLDER = False
if re.search("FDT", STATION_INDEX):  # Set up command to connect to FDT network folder for uploading test files.
    MOUNT_CMD = 'sudo mount.cifs //10.10.13.10/ATE_TestReport ' + DIR + ' -o rw,dir_mode=0777,file_mode=0777,username=pi,password=pi'
    MOUNT_TEST_FOLDER = True
    # print("Mounting FDT network folder for test files.")
elif re.search("PT", STATION_INDEX):  # Set up command to connect to PT network folder for uploading test files.
    MOUNT_CMD = 'sudo mount.cifs //192.168.5.33/ATE_TestReport ' + DIR + ' -o rw,dir_mode=0777,file_mode=0777,domain=FOSSIL,username=qcyou,password=Qc@999999,sec=ntlm'
    MOUNT_TEST_FOLDER = True
    # print("Mounting PT network folder for test files.")
else:  # Set up command to connect to Flex network folder for uploading test files.
    MOUNT_CMD = "sudo mount.cifs //172.30.31.21/TestFile/RebelTestFile/ATE" + str(STATION_ID) + " " + DIR + " -o user=rebelte,password=rebel@123,sec=ntlm,uid=pi,gid=pi"
    MOUNT_TEST_FOLDER = True
    # print("Mounting FlexFlow network folder for test files.")
#===============================================================================
# DEVICE PHYSICAL INFORMATION
#===============================================================================



#===============================================================================
#===============================================================================
# Common pathnames
#Log file path
ATE_LOG_UPLOAD_PATH = '/home/pi/Desktop/ateTestUploads/'

pathCommon = {
    'usbRadioPath': '/dev/ttyACM0',
    'serialPort': '/dev/ttyAMA0',
    'isPiRunning': '/home/pi',
    'pathtoLogs': '/home/pi/misfit/ShineProduction/src/',
    'statusFile': '/home/pi/misfit/ShineProduction/src/prev_test_data/status.txt',
    'batteryPassedFile': '/home/pi/misfit/ShineProduction/src/prev_test_data/battery_passed.txt',
    'testJsonFile': '/home/pi/misfit/ShineProduction/src/prev_test_data/test_json',
    'imagePathFile': '/home/pi/misfit/ShineProduction/src/view/images/batteryPlot.png'
}

# Bluetooth common settings
# Timeouts are in seconds
bluetoothCommon = {
    'btMaxNumRetries': 3,
    'btTimeout': 10,
    # 10 seconds is maximum time we will wait from issuing a BT command to receiving a response
    'btStateMachineTimeout': 10,
    'btScanForDut': False,
    # Delay between BLE tests.  If the commands are issued too quickly, it's possible there could be a BLE timeout
    'btDelay': 0.5
}

# Database common settings
# Timeouts are in seconds
dbCommon = {
    'dbMaxPostAttempts': 10,
    'dbPostTimeout': 5,
    'dbMaxReadAttempts': 10,
    'dbReadTimeout': 2,
    'checkInternetWithRetries': 3,
    'maxInternetConnectAttempts': 3
}

devicePhysicalInfo = {

}

# Test Parameters, current values in milliamps

defaultTestParams = {
    'numReadings', 1,
    'numReadingsBaseline', 100,
    'baselineWindowSize', 4,
    'defaultCurrentRange', 0.1,
    'maxInvalidRssiCount', 10,
    'serialTimeout', 0.1,
    'buttonToggleTime', 0.1,
    'piVoltageLower', 2.0,
    'piVoltageUpper', 5.0
}

U7 =   { 'name'        :'TCA9539',
          'address'       :'0x74',
          'registerMap'   :   { 'Input_Port_0'              :'0x00',
                                'Input_Port_1'              :'0x01',
                                'Output_Port_0'             :'0x02',
                                'Output_Port_1'             :'0x03',
                                'Polarity_Inversion_Port_0' :'0x04',
                                'Polarity_Inversion_Port_1' :'0x05',
                                'Configuration_Port_0'      :'0x06',
                                'Configuration_Port_1'      :'0x07',
                              },
        }


U13 =   { 'name'        :'TCA9539',
          'address'       :'0x75',
          'registerMap'   :   { 'Input_Port_0'              :'0x00',
                                'Input_Port_1'              :'0x01',
                                'Output_Port_0'             :'0x02',
                                'Output_Port_1'             :'0x03',
                                'Polarity_Inversion_Port_0' :'0x04',
                                'Polarity_Inversion_Port_1' :'0x05',
                                'Configuration_Port_0'      :'0x06',
                                'Configuration_Port_1'      :'0x07',
                              },
        }

if STATION_ID == '3':
    gpioControllerConfig = [
        {'name': 'VIN_VCC',                     'type': 'pi',   'physical': '7',    'wPi': '7',     'BCM': '4',     'mode': 'out',  'value': '1'},
        {'name': 'VIN_GND',                     'type': 'pi',   'physical': '11',   'wPi': '0',     'BCM': '17',    'mode': 'out',  'value': '1'},
        {'name': 'VCC_LED',                     'type': 'pi',   'physical': '16',   'wPi': '4',     'BCM': '23',    'mode': 'out',  'value': '1'},
    ]
else:
    gpioControllerConfig = [
        {'name': 'GPIO2_I2C_SDA',               'type': 'pi',   'physical': '3',    'wPi': '8',     'BCM': '2',     'mode': 'alt0', 'value': '0'},
        {'name': 'GPIO3_I2C_SCL',               'type': 'pi',   'physical': '5',    'wPi': '9',     'BCM': '3',     'mode': 'alt0', 'value': '0'},
        {'name': 'GPIO14_UART_TXD0',            'type': 'pi',   'physical': '8',    'wPi': '15',    'BCM': '14',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO15_UART_RXD0',            'type': 'pi',   'physical': '10',   'wPi': '16',    'BCM': '15',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO17_TEST',                 'type': 'pi',   'physical': '11',   'wPi': '0',     'BCM': '17',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO18_CE1_N_ALT',            'type': 'pi',   'physical': '12',   'wPi': '1',     'BCM': '18',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO27_FLASHER_OK',           'type': 'pi',   'physical': '13',   'wPi': '2',     'BCM': '27',    'mode': 'in',   'value': '1'},
        {'name': 'GPIO23_REV_DRIVE',            'type': 'pi',   'physical': '16',   'wPi': '4',     'BCM': '23',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO24_EXPAND_INT2_N',        'type': 'pi',   'physical': '18',   'wPi': '5',     'BCM': '24',    'mode': 'out',  'value': '1'},
        {'name': 'GPIO10_SPI_MOSI',             'type': 'pi',   'physical': '19',   'wPi': '12',    'BCM': '10',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO9_SPI_MISO',              'type': 'pi',   'physical': '21',   'wPi': '13',    'BCM': '9',     'mode': 'in',   'value': '0'},
        {'name': 'GPIO25_FLASHER_START',        'type': 'pi',   'physical': '22',   'wPi': '6',     'BCM': '25',    'mode': 'out',  'value': '0'},
        {'name': 'GPIO11_SPI_SCLK',             'type': 'pi',   'physical': '23',   'wPi': '14',    'BCM': '11',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO8_SPI_CE0_N',             'type': 'pi',   'physical': '24',   'wPi': '10',    'BCM': '8',     'mode': 'in',   'value': '0'},
        {'name': 'GPIO7_SPI_CE1_N',             'type': 'pi',   'physical': '26',   'wPi': '11',    'BCM': '7',     'mode': 'in',   'value': '0'},
        {'name': 'GPIO0_ID_SD',                 'type': 'pi',   'physical': '27',   'wPi': '30',    'BCM': '0',     'mode': 'out',  'value': '0'},
        {'name': 'GPIO1_ID_SC',                 'type': 'pi',   'physical': '28',   'wPi': '31',    'BCM': '1',     'mode': 'out',  'value': '0'},
        {'name': 'GPIO5_EXPAND_INT_N',          'type': 'pi',   'physical': '29',   'wPi': '21',    'BCM': '5',     'mode': 'out',  'value': '1'},
        {'name': 'GPIO6_CE0_N_ALT',             'type': 'pi',   'physical': '31',   'wPi': '22',    'BCM': '6',     'mode': 'in',   'value': '0'},
        {'name': 'GPIO12_MCU_RST_N',            'type': 'pi',   'physical': '32',   'wPi': '26',    'BCM': '12',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO13_EXPAND_RST_N',         'type': 'pi',   'physical': '33',   'wPi': '23',    'BCM': '13',    'mode': 'out',  'value': '1'},
        {'name': 'GPIO19_SPI_MISO',             'type': 'pi',   'physical': '35',   'wPi': '24',    'BCM': '19',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO16_DIFF_TRANS_EN',        'type': 'pi',   'physical': '36',   'wPi': '27',    'BCM': '16',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO26_FLASHER_BUSY',         'type': 'pi',   'physical': '37',   'wPi': '25',    'BCM': '26',    'mode': 'in',   'value': '1'},
        {'name': 'GPIO20_SPI_MOSI',             'type': 'pi',   'physical': '38',   'wPi': '28',    'BCM': '20',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO21_SPI_SCLK',             'type': 'pi',   'physical': '40',   'wPi': '29',    'BCM': '21',    'mode': 'in',   'value': '0'},
        {'name': 'GPIO4',                       'type': 'pi',   'physical': '7',    'wPi': '7',     'BCM': '4',     'mode': 'in',   'value': '0'},
        {'name': 'GPIO22_TRANS_EN',             'type': 'pi',   'physical': '15',   'wPi': '3',     'BCM': '22',    'mode': 'out',  'value': '0'},

        {'name': 'EXP1_JTAG_PRO_EN_N',          'type': 'exp1', 'device': U7, 'physical': 'P00', 'port': '0', 'bit': '0',   'mode': 'out', 'value': '1'},
        {'name': 'EXP1_DUT_VCC_1_EN',           'type': 'exp1', 'device': U7, 'physical': 'P01', 'port': '0', 'bit': '1',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_DUT_VCC_2_EN',           'type': 'exp1', 'device': U7, 'physical': 'P04', 'port': '0', 'bit': '4',   'mode': 'out', 'value': '0'},
        {'name': 'EXP2_DUT_VCC_3_EN',           'type': 'exp2', 'device': U13,'physical': 'P14', 'port': '1', 'bit': '4',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_DUT_MFG_TX_RX_EN_N',     'type': 'exp1', 'device': U7, 'physical': 'P02', 'port': '0', 'bit': '2',   'mode': 'out', 'value': '1'},
        {'name': 'EXP1_DUT_MFG_TEST_EN_N',      'type': 'exp1', 'device': U7, 'physical': 'P03', 'port': '0', 'bit': '3',   'mode': 'out', 'value': '1'},
        {'name': 'EXP1_VSENSE_EN_N',            'type': 'exp1', 'device': U7, 'physical': 'P05', 'port': '0', 'bit': '5',   'mode': 'out', 'value': '1'},
        {'name': 'EXP1_VSENSE_A0',              'type': 'exp1', 'device': U7, 'physical': 'P06', 'port': '0', 'bit': '6',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_VSENSE_A1',              'type': 'exp1', 'device': U7, 'physical': 'P07', 'port': '0', 'bit': '7',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_VSENSE_A2',              'type': 'exp1', 'device': U7, 'physical': 'P10', 'port': '1', 'bit': '0',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_VSENSE_SEL',             'type': 'exp1', 'device': U7, 'physical': 'P11', 'port': '1', 'bit': '1',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_XTAL_CAL_CTL',           'type': 'exp1', 'device': U7, 'physical': 'P12', 'port': '1', 'bit': '2',   'mode': 'out', 'value': '1'},

        {'name': 'EXP2_TRANS_POWER_EN',         'type': 'exp2', 'device': U13, 'physical': 'P00', 'port': '0', 'bit': '0',  'mode': 'out', 'value': '1'},
        {'name': 'EXP2_DIFF_LS_EN',             'type': 'exp2', 'device': U13, 'physical': 'P01', 'port': '0', 'bit': '1',  'mode': 'out', 'value': '0'},
        {'name': 'EXP2_VIN_REVERSE_POL_EN_1',   'type': 'exp2', 'device': U13, 'physical': 'P02', 'port': '0', 'bit': '2',  'mode': 'out', 'value': '0'},
        {'name': 'EXP2_VIN_REVERSE_POL_EN_2',   'type': 'exp2', 'device': U13, 'physical': 'P03', 'port': '0', 'bit': '3',  'mode': 'out', 'value': '0'},
        {'name': 'EXP2_SWITCH_MR_EN_N',         'type': 'exp2', 'device': U13, 'physical': 'P04', 'port': '0', 'bit': '4',  'mode': 'out', 'value': '1'},
        {'name': 'EXP2_PUSHER_EN_1',            'type': 'exp2', 'device': U13, 'physical': 'P05', 'port': '0', 'bit': '5',  'mode': 'out', 'value': '0'},
        {'name': 'EXP2_PUSHER_EN_2',            'type': 'exp2', 'device': U13, 'physical': 'P06', 'port': '0', 'bit': '6',  'mode': 'out', 'value': '0'},
        {'name': 'EXP2_PUSHER_EN_3',            'type': 'exp2', 'device': U13, 'physical': 'P07', 'port': '0', 'bit': '7',  'mode': 'out', 'value': '0'},
        {'name': 'EXP2_SWITCH_REV_DRIVE_EN_N',  'type': 'exp2', 'device': U13, 'physical': 'P10', 'port': '1', 'bit': '0',  'mode': 'out', 'value': '1'},
        {'name': 'EXP2_SWITCH_DA_RST_EN_N',     'type': 'exp2', 'device': U13, 'physical': 'P11', 'port': '1', 'bit': '1',  'mode': 'out', 'value': '1'},
        {'name': 'EXP2_SWITCH_CE1_N_ALT_EN_N',  'type': 'exp2', 'device': U13, 'physical': 'P12', 'port': '1', 'bit': '2',  'mode': 'out', 'value': '1'},
        {'name': 'EXP2_SWITCH_CE0_N_ALT_EN_N',  'type': 'exp2', 'device': U13, 'physical': 'P13', 'port': '1', 'bit': '3',  'mode': 'out', 'value': '1'},
        {'name': 'EXP2_DUT_RST_EN_N',           'type': 'exp2', 'device': U13, 'physical': 'P15', 'port': '1', 'bit': '5',  'mode': 'out', 'value': '1'},
        {'name': 'EXP2_XTAL_GEN_EN_N',          'type': 'exp2', 'device': U13, 'physical': 'P16', 'port': '1', 'bit': '6',  'mode': 'out', 'value': '1'},
        {'name': 'EXP2_EXT_SYS_CTL',            'type': 'exp2', 'device': U13, 'physical': 'P17', 'port': '1', 'bit': '7',  'mode': 'out', 'value': '0'},

        {'name': 'EXP1_PRE_EN_SW1',             'type': 'exp1', 'device': U7, 'physical': 'P13', 'port': '1', 'bit': '3',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_PRE_EN_SW2',             'type': 'exp1', 'device': U7, 'physical': 'P14', 'port': '1', 'bit': '4',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_PRE_EN_SW3',             'type': 'exp1', 'device': U7, 'physical': 'P15', 'port': '1', 'bit': '5',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_PRE_EN_LD01',            'type': 'exp1', 'device': U7, 'physical': 'P16', 'port': '1', 'bit': '6',   'mode': 'out', 'value': '0'},
        {'name': 'EXP1_PRE_EN_LD02',            'type': 'exp1', 'device': U7, 'physical': 'P17', 'port': '1', 'bit': '7',   'mode': 'out', 'value': '0'},
    ]

testCommand = {
    'MCU_LDO_ENABLED_CURRENT_TEST'  : '1',
    'MCU_BUCK_ENABLED_CURRENT_TEST' : '2',
    'MAC_ADDRESS_TEST'              : '3',
    'DRV_ID_TEST'                   : '4',
    'ACCEL_ORIENTATION_TEST'        : '5',
    'ACCEL_PART_ID_TEST'            : '6',
    'ACCEL_CURRENT_TEST'            : '7',
    'CRYSTAL_CALIBRATION'           : '8',
    'HARDWARE_REV_TEST'             : '9',
    'CRYSTAL_TEST'                  : '10',
    'MVMT1_CW_CURRENT_TEST'         : '11',
    'MVMT1_CCW_CURRENT_TEST'        : '12',
    'MVMT2_CW_CURRENT_TEST'         : '13',
    'MVMT2_CCW_CURRENT_TEST'        : '14',
    'MVMT3_CW_CURRENT_TEST'         : '15',
    'MVMT3_CCW_CURRENT_TEST'        : '16',
    'LOWEST_POWER_MODE_CURRENT_TEST': '17',
    'BOOST_TEST'                    : '18',
    'VIBE_CURRENT_TEST'             : '19',
    'VIBE_TEST'                     : '20',
    'PUSHER_PUSH_TEST'              : '21',
    'EXT_FLASH_PART_ID_TEST'        : '23',
    'GET_MODE'                      : '99',
    'ERASE_DEVICE'                  : '255',
}

testComponent = {
    'LEGACY':'255'
}

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
    'HT_FILE_TRANSFER_1'  : '1',
    'HT_FILE_TRANSFER_2'  : '2',
    'HT_FILE_TRANSFER_3'  : '3',

}

# Misc
OFFSET_CURRENT_SCALING_FACTOR = 1e11
RATED_VOLTAGE_2V2             = 100 # 0x64
OVERDRIVE_VOLTAGE_2V2         = 108 # 0x6C
OVERDRIVE_VOLTAGE_2V5         = 129 # 0x81

VOLUME_DB_500Hz  = '-12.61dB'
VOLUME_DB_1000Hz = '-19.21dB'
VOLUME_DB_4000Hz = '-17.94dB'

### Whitenoise test limits ###
#ATE2
MIN_DUT_AVG_POWER   = -80.0
MAX_DUT_STDEV       = 5.0

#ATE3
MIN_NORMALIZED_AVG_POWER    = -16.5
MAX_NORMALIZED_AVG_POWER    = 3.0
MAX_NORMALIZED_STDEV        = 7.8

# Codec setup
AUDIO_CODEC_ADPCM   = 0
AUDIO_CODEC_SBC     = 1
AUDIO_CODEC_USED    = AUDIO_CODEC_ADPCM

if AUDIO_CODEC_USED == AUDIO_CODEC_ADPCM:
    AUDIO_STREAM_FILTER = '04.FF.1C.1B.05.00.00.00.16.65.00.'   # 20 bytes
    # As the audio is 4s long, it's 4*8000 = 32KBytes of audio data. BLE throughput ~ 2000 bytes/s will requires ~16s to stream all the data
    AUDIO_STREAM_DELAY  = '20'
else:
    AUDIO_STREAM_FILTER = '04.FF.1A.1B.05.00.00.00.14.65.00.'   # 18 bytes
    AUDIO_STREAM_DELAY = '5'

### Volume level to play whitenoise file ###
# Default
VOLUME_DB_WHITE_NOISE       = '0dB'
# ATE2
if STATION_ID == '2':
    # Station 1 (ATE2.1)
    if STATION_INDEX == '1':
        VOLUME_DB_WHITE_NOISE = '-0.1dB'
    # Station 1 (ATE2.2)
    elif STATION_INDEX == '2':
        VOLUME_DB_WHITE_NOISE = '0dB'
    # Station 1 (ATE2.3)
    elif STATION_INDEX == '3':
        VOLUME_DB_WHITE_NOISE = '-0.2dB'
# ATE 3
if STATION_ID == '3':
    VOLUME_DB_WHITE_NOISE = '-6.29dB'


#RSSI params for each station
if STATION_ID == '1':
    RSSI_AVERAGE_LOWER        = -45
    RSSI_AVERAGE_UPPER        = -20
elif STATION_ID == '2':
    RSSI_AVERAGE_LOWER        = -60 # 3 sigma
    RSSI_AVERAGE_UPPER        = -20
elif STATION_ID == '3':
    RSSI_AVERAGE_LOWER        = -70
    RSSI_AVERAGE_UPPER        = -20

# Power supply initialization sequence. This can be used by any test.
PS_INIT =   [
    {'type': 'ps', 'name': 'Open power supply connection', 'operation': 'open'},
    {'type': 'ps', 'name':'Set voltage', 'operation':'configure', 'setting':'Voltage', 'value':'3.8'},
    {'type': 'ps', 'name':'Set current limit', 'operation':'configure', 'setting':'Current', 'value':'0.5'},
    {'type': 'ps', 'name':'Set current range', 'operation':'configure', 'setting':'CurrentRange', 'value':'1'},
    {'type': 'ps', 'name':'Set sense sweep points', 'operation':'configure', 'setting':'SenseSweepPoints', 'value':'4096'},
    {'type': 'ps', 'name':'Enable power supply', 'operation':'enable'},
            ]

# This puts all GPIOs in a safe state. This also safely powers off device under test.
GPIO_INIT = [
    # Turn disconnect 7V relay from DUT.
    {'type': 'io', 'pinName': 'EXP2_DUT_VCC_3_EN', 'mode': 'out', 'value': '0', 'operation': 'write'},

    # Configure communication lines for MFG and SPI on Raspberry Pi as inputs.
    {'type': 'io', 'pinName': 'GPIO14_UART_TXD0',       'mode': 'out', 'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO15_UART_RXD0',       'mode': 'out', 'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO14_UART_TXD0',       'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO15_UART_RXD0',       'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO17_TEST',            'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO10_SPI_MOSI',        'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO9_SPI_MISO',         'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO11_SPI_SCLK',        'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO8_SPI_CE0_N',        'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO7_SPI_CE1_N',        'mode': 'in',  'value': '0', 'operation': 'configure'},

    # Configure Rev drive pins, spare pins, and reset pin  as inputs
    {'type': 'io', 'pinName': 'GPIO6_CE0_N_ALT',        'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO18_CE1_N_ALT',       'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO23_REV_DRIVE',       'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO16_DIFF_TRANS_EN',   'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO12_MCU_RST_N',       'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO19_SPI_MISO',        'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO20_SPI_MOSI',        'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO21_SPI_SCLK',        'mode': 'in',  'value': '0', 'operation': 'configure'},

    # Set translator load switch and enable pins and GPIO Expander Reset and INT pins high
    {'type': 'io', 'pinName': 'GPIO5_EXPAND_INT_N',     'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'GPIO13_EXPAND_RST_N',    'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'GPIO24_EXPAND_INT2_N',   'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'GPIO4',                  'mode': 'in',  'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO22_TRANS_EN',        'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP2_TRANS_POWER_EN',    'mode': 'out', 'value': '1', 'operation': 'write'},

    # Disconnect MFG Pins
    {'type': 'io', 'pinName': 'EXP1_DUT_MFG_TX_RX_EN_N', 'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP1_DUT_MFG_TEST_EN_N',  'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP2_DUT_RST_EN_N',       'mode': 'out', 'value': '1', 'operation': 'write'},

    # Disconnect Flasher Pins
    {'type': 'io', 'pinName': 'EXP1_JTAG_PRO_EN_N',      'mode': 'out', 'value': '1', 'operation': 'write'},

    # Disconnect MR, Rev Drive and Spare pins
    {'type': 'io', 'pinName': 'EXP2_SWITCH_REV_DRIVE_EN_N',     'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP2_SWITCH_DA_RST_EN_N',        'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP2_SWITCH_CE1_N_ALT_EN_N',     'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP2_SWITCH_CE0_N_ALT_EN_N',     'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP2_SWITCH_MR_EN_N',            'mode': 'out', 'value': '1', 'operation': 'write'},

    # Disable Voltage Sense Mux
    {'type': 'io', 'pinName': 'EXP1_VSENSE_EN_N',               'mode': 'out', 'value': '1', 'operation': 'write'},

    # Set Voltage Sense switch to LV Vsense
    {'type': 'io', 'pinName': 'EXP1_VSENSE_SEL',                'mode': 'out', 'value': '0', 'operation': 'write'},

    # Disconnect RTC Cal pins
    {'type': 'io', 'pinName': 'EXP2_XTAL_GEN_EN_N',     'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP1_XTAL_CAL_CTL',      'mode': 'out', 'value': '1', 'operation': 'write'},

    # Disable reverse polarity circuitry
    {'type': 'io', 'pinName': 'EXP2_VIN_REVERSE_POL_EN_1',   'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP2_VIN_REVERSE_POL_EN_2',   'mode': 'out', 'value': '0', 'operation': 'write'},

    # Disable HV System Relay
    {'type': 'io', 'pinName': 'EXP2_EXT_SYS_CTL',   'mode': 'out', 'value': '0', 'operation': 'write'},

    # Turn off load switches
    {'type': 'io', 'pinName': 'EXP1_DUT_VCC_2_EN',   'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP1_DUT_VCC_1_EN',   'mode': 'out', 'value': '0', 'operation': 'write'},

    # Power down LDOs and power supplies
    {'type': 'io', 'pinName': 'EXP1_PRE_EN_LD01',   'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP1_PRE_EN_LD02',   'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP1_PRE_EN_SW3',    'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP1_PRE_EN_SW2',    'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'io', 'pinName': 'EXP1_PRE_EN_SW1',    'mode': 'out', 'value': '0', 'operation': 'write'},
    ]

ENTER_HT_SEQUENCE = [
    # Enable loadswitch for level translator.
    {'type': 'io', 'pinName': 'EXP2_TRANS_POWER_EN', 'mode': 'out', 'value': '1', 'operation': 'write'},

    # Configure Tx as input.
    {'type': 'io', 'pinName': 'GPIO14_UART_TXD0', 'mode': 'out', 'value': '0', 'operation': 'write'},
    # Configure Rx as input.
    {'type': 'io', 'pinName': 'GPIO15_UART_RXD0', 'mode': 'out', 'value': '0', 'operation': 'write'},
    # Configure TEST as output low.
    # {'type': 'io', 'pinName': 'GPIO17_TEST', 'mode': 'out', 'value': '0', 'operation': 'write'},

    # Enable Translators
    {'type': 'io', 'pinName': 'GPIO22_TRANS_EN', 'mode': 'out', 'value': '1', 'operation': 'write'},

    # Connect Tx and Rx pins between ATE and Device.
    {'type': 'io', 'pinName': 'EXP1_DUT_MFG_TX_RX_EN_N', 'mode': 'out', 'value': '0', 'operation': 'write'},
    # Connect TEST pin between ATE and Device
    {'type': 'io', 'pinName': 'EXP1_DUT_MFG_TEST_EN_N', 'mode': 'out', 'value': '0', 'operation': 'write'},

    # Pulse EXP2_SWITCH_MR_EN_N low for 160 ms to wake up.
    {'type': 'io', 'pinName': 'EXP2_SWITCH_MR_EN_N', 'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'delay', 'delay': '0.160'},
    {'type': 'io', 'pinName': 'EXP2_SWITCH_MR_EN_N', 'mode': 'out', 'value': '1', 'operation': 'write'},

    # Control of MCU reset.
    {'type': 'io', 'pinName': 'GPIO12_MCU_RST_N', 'mode': 'out', 'value': '1', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'EXP2_DUT_RST_EN_N', 'mode': 'out', 'value': '0', 'operation': 'write'},
    # Toggle Ambiq reset pin.
    # Pull down ABQ MCU Reset pin.
    {'type': 'io', 'pinName': 'GPIO12_MCU_RST_N', 'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'delay', 'delay': '0.1'},
    # Pull up ABQ MCU Reset pin.Remove control of MCU reset.
    {'type': 'io', 'pinName': 'GPIO12_MCU_RST_N', 'mode': 'out', 'value': '1', 'operation': 'write'},
    # Disable DUT RESET from Pi
    {'type': 'io', 'pinName': 'EXP2_DUT_RST_EN_N', 'mode': 'out', 'value': '1', 'operation': 'write'},

    {'type': 'io', 'pinName': 'GPIO17_TEST', 'mode': 'in', 'value': '0', 'operation': 'poll', 'readDelay':'0.01', 'timeout':'5'},
    {'type': 'io', 'pinName': 'GPIO17_TEST', 'mode': 'out', 'value': '0', 'operation': 'write'},

    # Enter Hardware Test Sequence
    {'type': 'delay', 'delay': '0.16'},
    {'type': 'io', 'pinName': 'GPIO15_UART_RXD0', 'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'io', 'pinName': 'GPIO14_UART_TXD0', 'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'GPIO17_TEST', 'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'delay', 'delay': '0.15'},
    {'type': 'io', 'pinName': 'GPIO15_UART_RXD0', 'mode': 'out', 'value': '1', 'operation': 'write'},
    {'type': 'io', 'pinName': 'GPIO14_UART_TXD0', 'mode': 'out', 'value': '0', 'operation': 'write'},
    {'type': 'delay', 'delay': '0.15'},
    {'type': 'io', 'pinName': 'GPIO15_UART_RXD0', 'mode': 'alt0', 'value': '0', 'operation': 'configure'},
    {'type': 'io', 'pinName': 'GPIO14_UART_TXD0', 'mode': 'alt0', 'value': '0', 'operation': 'configure'},

    {'type': 'io', 'pinName': 'EXP1_DUT_MFG_TEST_EN_N', 'mode': 'out', 'value': '1', 'operation': 'write'},

    # Delay to allow init to complete before querying for mode.
    {'type': 'delay', 'delay': '1'},

    # Request HT MODE to ensure device is in Hardware test mode.
    {'type': 'serial', 'name': 'Check Mode', 'messageType': 'Request',
     'componentId': componentID['HT_MCU'],
     'commandId': commandID['HT_MCU_10'],
     'timeout': '3', 'postCmdDelay': '0', 'feedbackData': True},
]
#Serial number validation params
#========================================================
SERIAL_NUMBER_LENGTH = 10
if STATION_ID == '1' or STATION_ID == '2':
    SMT_SN_REQUIRED = True # For ATE 2, this is actually the E-Ink lot number and this is required.
elif  STATION_ID == '3':
    SMT_SN_REQUIRED = False

if STATION_ID == '1' or STATION_ID == '2':
    HEARTRATE_SN_REQUIRED = False
    INTERNAL_SN_REQUIRED = True
    PACKAGING_SN_REQUIRED = False
    MATCHSTR_INTERNAL_REGEX = 'D00ZZ[^BbOoSsIi]{5}'
    MATCHSTR_REGEX = ''

if STATION_ID == '3':
    HEARTRATE_SN_REQUIRED = True
    INTERNAL_SN_REQUIRED = True
    PACKAGING_SN_REQUIRED = True
    MATCHSTR_HEARTRATE_REGEX = 'D00HR[^BbOoSsIi]{5}'
    MATCHSTR_INTERNAL_REGEX = 'D00ZZ[^BbOoSsIi]{5}'
    MATCHSTR_REGEX = 'D0[FE][0-9][0-9A-Z]{2}[^BbOoSsIi]{4}'
# Mapping of ATE Test class name to ID to report failures to ATE operator
# Test numbers are logially grouped by functionality
# NOTE - the test name must match the actual class name or the test ID lookup will fail
# Test ID - xxyy, where xx = test group, yy = test sub ID

ateTestIdMap = { \
        # System Group - 00
        'EraseDevice'                                   : '0001',
        'ProgramDevice'                                 : '0002',
        'EnterHardwareTestMode'                         : '0003',
        'EnterHardwareTestModeATE2'                     : '0004',
        'ExitHardwareTestModeATE2'                      : '0005',
        'PowerOnDevice'                                 : '0006',
        'PowerOffDevice'                                : '0007',
        'InitRadioAndMsp'                               : '0008',
        'CrystalCalibration'                            : '0009',
        'CrystalTest'                                   : '0010',
        'GetMacAddressTest'                             : '0011',
        'McuRunCurrentTest'                             : '0012',
        'McuRunCurrentTestVIn'                          : '0013',
        'LowestPowerModeCurrentTest'                    : '0014',
        'PmuActiveCurrentTestVIn'                       : '0015',
        'HardwareRevisionTest'                          : '0016',
        'TransferLutFile'                               : '0017',

        # Accelerometer Group - 01
        'AccelOrientTest'                               : '0101',
        'AccelPartIdTest'                               : '0102',
        'AccelerometerCurrentTest'                      : '0103',

        # Movement Group - 02
        'Movement1CounterClockwiseCurrentTest'          : '0201',
        'Movement1ClockwiseCurrentTest'                 : '0202',
        'Movement2CounterClockwiseCurrentTest'          : '0203',
        'Movement2ClockwiseCurrentTest'                 : '0204',
        'Movement1ClockwiseCurrentTestVIn'              : '0205',
        'Movement1CounterClockwiseCurrentTestVIn'       : '0206',
        'Movement2ClockwiseCurrentTestVIn'              : '0207',
        'Movement2CounterClockwiseCurrentTestVIn'       : '0208',

        # Haptics Group - 03
        'DrvIdTest'                                     : '0301',
        'VibeCurrentTest'                               : '0302',

        # Power Management Unit Group - 04
        'VsysTest'                                      : '0401',
        'VldoTest'                                      : '0402',
        'VpmidTest'                                     : '0403',
        'ChargeCutoffTest'                              : '0404',
        'PositivePolarityChargingTest'                  : '0405',
        'NegativePolarityChargingTest'                  : '0406',
        'PositivePolarityChargingTestVIn'               : '0407',
        'NegativePolarityChargingTestVIn'               : '0408',
        'ShipModeCurrentTest'                           : '0409',
        'WakeFromShipMode'                              : '0410',

        # External Flash Group - 05
        'ExtFlashPartIdTest'                            : '0501',
        'ProgramExternalFlash'                          : '0502',
        'ExtFlashReadWriteSpeedTest'                    : '0503',

        # Microphone Group - 06
        'MicrophoneCurrentTestVIn'                      : '0601',
        'Microphone500HzTest'                           : '0602',
        'Microphone1KhzTest'                            : '0603',
        'Microphone4KhzTest'                            : '0604',
        'MicrophoneCurrentTest'                         : '0605',
        'MicrophoneWhiteNoiseTest1'                     : '0606',
        'MicrophoneWhiteNoiseTestATE3'                  : '0607',
        'MicrophoneCollectChamberAudio'                 : '0608',

        # Pusher Group - 07
        'PusherTest'                                    : '0701',

        # BLE Group - 08
        'OpenBleConnection'                             : '0801',
        'CloseBleConnection'                            : '0802',
        'GetFirmwareVersion'                            : '0803',
        'AverageRssiTest'                               : '0804',
        'SetTimeTest'                                   : '0805',
        'GetAccelerometerStreaming'                     : '0806',
        'SetPMUChargeCutoff'                            : '0807',
        'VibeDiagnosticTest'                            : '0808',
        'EnterShipModeWhiteBackground'                  : '0809',
        'PacketErrorRateTest'                           : '0810',
        'HRMBPMTest'                                    : '0811',
        'ChargePadContactTest'                          : '0812',
        'VibeBTCalibrationTest'                         : '0813',
        'HandDragTest'                                  : '0814',
        'HRMeInkMovementTest'                           : '0815',
        'SetHandShippingPositions'                      : '0817',
        'GetBatteryVoltageTest'                         : '0818',
        'UpdateModuleSerialNumber'                      : '0819',
        'HrmLedCurrentTest'                             : '0820',
        'WriteHRSerialNumberTest'                       : '0821',
        'WriteSerialNumberTest'                         : '0822',
        'SetPMUChargeCurrentTermination'                : '0823',
        'DeviceUpdate'                                  : '0824',

        # E-Ink Group - 09
        'StoreEInkLotNumber'                            : '0901',
        'InitEInkScreen'                                : '0902',
        'DisplayCurrentTestVIn'                         : '0903',
        'LEDUniformingTest'                             : '0904',
        'circlesConcentricityTest'                      : '0905',
        'eInkAlignmentTest'                             : '0906',
        'EInkScreenPixelTest'                           : '0907',
        'DisplayFrontLightCurrentTestVIn'               : '0908',
        'CirclesConcentricityTestATE3'                  : '0909',
        'EInkDeadPixelTestATE3'                         : '0910',
        'LEDUniformingTestATE3'                         : '0911',

        #Security Group - 10
        'Activation'                                    :'1001',
        'InternetConnection'                            :'1002'

}
