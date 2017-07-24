from minimalmodbus import Instrument
from time import sleep

from config import configuration


class OVG_MODULE():
    def __init__(self, path, temperature_module_position, sample_flow_module_position):
        self.temperature_module = EUROTHERM_MODULE(path, temperature_module_position, 1)
        self.sample_flow_module = EUROTHERM_MODULE(path, sample_flow_module_position, 0)

    def read_temperature(self):
        return self.temperature_module.read_value()

    def set_temperature(self, temperature):
        self.temperature_module.set_setpoint(float(temperature))

    def get_flow_rate(self):
        return self.sample_flow_module.read_value()

    def set_flow_rate(self, value):
        self.sample_flow_module.set_setpoint(float(value))

    def get_info(self):
        temperature_text = 'Temperature: {}, Target Temperature: {}, Temperature Limit High: {}, Temperature Limit Low: {}'
        temperature_text.format(self.temperature_module.read_value(),
                                self.temperature_module.read_setpoint_value(),
                                self.temperature_module.read_setpoint_high_limit(),
                                self.temperature_module.read_setpoint_low_limit())

        print(temperature_text)



class EUROTHERM_MODULE():
    def __init__(self, path, number, digits):

        self.device = Instrument(path, number)
        self.device.debug = False
        self.device.serial.baudrate = 9600

        self.digits = digits

        self.set_active_setpoint(configuration['sp_select_default'])

    # Writing

    def set_active_setpoint(self, value):
        if 0 <= value and value <= 1:
            self.device.write_register(configuration['sp_select_default'], value, self.digits)

    def set_setpoint(self, value):
        if self.read_setpoint_low_limit() <= value and value <= self.read_setpoint_high_limit():
            self.device.write_register(configuration['sp_select_address'], value, self.digits)

    # Reading

    def read_value(self):
        return self.device.read_register(1, self.digits)

    def read_setpoint_select(self):
        return self.device.read_register(15, self.digits)

    def read_setpoint_value(self):
        return self.device.read_register(configuration['sp_value_address'],
                                         self.digits)

    def read_setpoint_high_limit(self):
        return self.device.read_register(configuration['sp_high_limit'],
                                         self.digits)

    def read_setpoint_low_limit(self):
        return self.device.read_register(configuration['sp_low_limit'],
                                         self.digits)


def main():

    ovg_module_1 = OVG_MODULE(configuration['port'],
                              temperature_module_position = 1,
                              sample_flow_module_position = 2)
    print('Setting temperature to:', 37.0)
    ovg_module_1.set_temperature(37.0)
    ovg_module_1.get_info()


if __name__ == '__main__':
    main()
