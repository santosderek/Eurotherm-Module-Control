"""
Created and Written by Derek Santos.

Beginning iteration of controlling and automating an OVG Module. 

"""

from minimalmodbus import Instrument
from time import sleep

from config import configuration

"""

Useful Information:

Setpoints are what the Eurotherm Module is currently targeting. If you desire a
temperature of 35, then the current setpoint must be set to 35. If a setpoint
that is not set as active is changed, the Eurotherm Module will not be set to
the value.

"""


class OVG_MODULE():
    """ Class to manipulate multiple eurotherm_module's at once """

    def __init__(self, path, temperature_module_position, sample_flow_module_position):
        """ Defining both a temperature module and sample flow module. """

        # Path = COM / dev/tty*** Port
        # temperature_module_position = index position of a module; left position is 0, right position is 1
        # sample_flow_module_position = index position of a module; left position is 0, right position is 1
        # Number Of Decimals used by the module. Temperature has 1 decimal while flowrate has 0.
        self.temperature_module = EUROTHERM_MODULE(path,
                                                   temperature_module_position,
                                                   1)
        self.sample_flow_module = EUROTHERM_MODULE(path,
                                                   sample_flow_module_position,
                                                   0)

    def read_temperature(self):
        """ Returns value from the temperature module. """
        return self.temperature_module.read_value()

    def set_temperature(self, temperature):
        """ Sets value desired of the temperature module. """

        # A setpoint is the desired value that you want.
        self.temperature_module.set_setpoint(float(temperature))

    def get_flow_rate(self):
        """ Returns value from the flow rate module. """

        return self.sample_flow_module.read_value()

    def set_flow_rate(self, value):
        """ Sets value desired of the flow rate module. """

        self.sample_flow_module.set_setpoint(float(value))

    def get_info(self):
        # String to return listing all present data.
        temperature_text = 'Temperature: {}, Target Temperature: {}, Temperature Limit High: {}, Temperature Limit Low: {}'
        temperature_text.format(self.temperature_module.read_value(),
                                self.temperature_module.read_setpoint_value(),
                                self.temperature_module.read_setpoint_high_limit(),
                                self.temperature_module.read_setpoint_low_limit())

        print(temperature_text)


class EUROTHERM_MODULE():
    """ Class to manipulate a single Eurotherm Module """

    def __init__(self, path, number, digits):
        """ Instrument class initalizes a connection through the desired port."""

        # Path = COM / dev/tty*** Port
        self.device = Instrument(path, number)
        self.device.debug = False

        # Baudrate for Module is 9600
        self.device.serial.baudrate = 9600

        # Number Of Decimals used by the module. Temperature has 1 decimal while flowrate has 0.
        self.digits = digits

        # Select's the setpoint found in the config file as the active setpoint.
        self.set_active_setpoint(configuration['sp_select_default'])

    # Writing

    def set_active_setpoint(self, value):
        """ Set's the active setpoint to the value specified. """
        if 0 <= value and value <= 1:
            self.device.write_register(
                configuration['sp_select_default'], value, self.digits)

    def set_setpoint(self, value):
        """ Set's the value in the active setpoint to the value given """
        if self.read_setpoint_low_limit() <= value and value <= self.read_setpoint_high_limit():
            self.device.write_register(
                configuration['sp_select_address'], value, self.digits)

    # Reading

    def read_value(self):
        """ Read value from the first register. This is the current value found on the Eurotherm Module. """
        return self.device.read_register(1, self.digits)

    def read_setpoint_select(self):
        """ Reads the active setpoint from the 15th register. """
        return self.device.read_register(15, self.digits)

    def read_setpoint_value(self):
        """ Reads the active setpoint's value from the register specified in the config.py. """
        return self.device.read_register(configuration['sp_value_address'],
                                         self.digits)

    def read_setpoint_high_limit(self):
        """ Reads the active setpoint's high limit value from the register specified in the config.py. """
        return self.device.read_register(configuration['sp_high_limit'],
                                         self.digits)

    def read_setpoint_low_limit(self):
        """ Reads the active setpoint's low limit value from the register specified in the config.py. """
        return self.device.read_register(configuration['sp_low_limit'],
                                         self.digits)


def main():

    # Create an OVG Module while specifying the port, temperature module position, and sample flow module position.
    ovg_module_1 = OVG_MODULE(configuration['port'],
                              temperature_module_position=1,
                              sample_flow_module_position=2)

    # A simple print to show the value we are setting the temperature too.
    print('Setting temperature to:', 37.0)

    # Set the temperature by calling the set_temperature function of the OVG_MODULE.
    ovg_module_1.set_temperature(37.0)

    # Get the latest info about the OVG_MODULE.
    ovg_module_1.get_info()


if __name__ == '__main__':
    main()
