from minimalmodbus import Instrument
from time import sleep

from config import *


class EUROTHERM_MODULE():
    def __init__(self, path, number, digits):

        self.device = Instrument(path, number)
        self.device.debug = False
        self.device.serial.baudrate = 9600

        self.digits = digits

        self.set_active_setpoint(SP_SELECT_DEFAULT)

    # Writing

    def set_active_setpoint(self, value):
        if 0 <= value and value <= 1:
            self.device.write_register(SP_SELECT_ADDRESS, value, self.digits)

    def set_setpoint(self, value):
        if self.read_setpoint_low_limit() <= value and value <= self.read_setpoint_high_limit():
            self.device.write_register(SP_VALUE_ADDRESS, value, self.digits)

    # Reading

    def read_value(self):
        return self.device.read_register(1, self.digits)

    def read_setpoint_select(self):
        return self.device.read_register(15, self.digits)

    def read_setpoint_value(self):
        return self.device.read_register(SP_VALUE_ADDRESS, self.digits)

    def read_setpoint_high_limit(self):
        return self.device.read_register(111, self.digits)

    def read_setpoint_low_limit(self):
        return self.device.read_register(112, self.digits)

def main():

    device1 = EUROTHERM_MODULE(COM, 1, 1)

    ###########################################################################
    def read_info(device):
        print('Setpoint Select', device.read_setpoint_select(),
              'Value now:',      device.read_value(),
              'Set point value', device.read_setpoint_value(),
              'Set point low:',  device.read_setpoint_low_limit(),
              'Set point high:', device.read_setpoint_high_limit())

    read_info(device1)

    device1.set_setpoint(36)

    read_info(device1)
    ###########################################################################



    ###########################################################################
    device2 = EUROTHERM_MODULE(COM, 3, 1)
    read_info(device2)

    device2.set_setpoint(35)

    read_info(device2)
    ###########################################################################



if __name__ == '__main__':
    main()
