from ate_settings import *
# from commands.dmmCmd import DmmCmd
# from commands.gpioCmd import GpioCmd
# from commands.delayCmd import DelayCmd
from commands.serialCmd import SerialCmd
# from commands.bleCmd import BleCmd
# from commands.audioCmd import AudioCmd
# from commands.logCmd import LogCmd

# If it is ATE 1, import the power supply and flash command classes.
if STATION_ID == '1':
    from commands.psCmd import PsCmd
    from commands.flashCmd import FlashCmd

# If it is ATE 2 or 3, import the camera command classes.
elif STATION_ID == '2' or STATION_ID == '3':
    # from commands.cameraCmd import CameraCmd
    from commands.cvCmd import CVCmd



'''
Factory to create command objects for a specific test
'''


class CommandFactory:
    # class instance counter
    _numCommandObjects = 0

    # Add more object types as needed
    objectTypes = {
        "serial"    : SerialCmd,
        # "io"	    : GpioCmd,
        # "delay"		: DelayCmd,
        # "ble"		: BleCmd,
        # "dmm"       : DmmCmd,
        # "audio"     : AudioCmd,
        # "log"       : LogCmd,

    }

    if STATION_ID == '1':
        # Add the power supply and flash commands.
        objectTypes["ps"]	     = PsCmd
        objectTypes["flash"]     = FlashCmd

    elif STATION_ID == '2' or STATION_ID == '3':
        # Add camera and cv command objects.
        # objectTypes['camera']   = CameraCmd
        objectTypes['cv']       = CVCmd

    def __init__(self):
        '''
        Init method to setup instance
        '''
        self._cmd = None

    def createCmdObject(self, cmd):
        '''
        Create an instance of the command object
        :param cmd: string, name of the command
        :return: Command: object
        '''
        CommandFactory._numCommandObjects += 1

        # create the appropriate command object from objectTypes lookup table
        cmdObject = CommandFactory.objectTypes[cmd['type']](cmd)

        return cmdObject

    def getNumCmdObjects(self):
        '''
        Get how many instances of the command object created
        :return: numCommandObjects: int
        '''
        return CommandFactory._numCommandObjects
