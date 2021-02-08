from app.sensors.sensor_base import Sensor, try_io

import smbus2
import time

ARDUINO_NANO_I2C_ADDRESS = 0x14

class NANO_I2C_CMD():
    CMD_REG_WRITE = 0x00
    A_READ_A0 = 0x10
    A_READ_A1 = 0x11
    A_READ_A2 = 0x12
    A_READ_A3 = 0x13
    A_READ_A4 = 0x14
    A_READ_A5 = 0x15
    SDI12_READ = 0x20
    UART0_READ = 0x30
    UART1_READ = 0x31
    UART0_POLL = 0x32
    UART1_POLL = 0x33

class LOX02F(Sensor):
    def __init__(self, id):
        type = "LOX02F"
        protocol = "UART"
        address = 14
        measurements = [
            "o2_concentration"
        ]
        
        super().__init__(id, type, protocol, address, measurements)
        self.bus = smbus2.SMBus(1)
        self.__initialize_sensor()

    def __initialize_sensor(self):
        command_string = [ord(c) for c in "M 1\r\n"] # \r\n may need to be encoded to send as the correct bytes idk
        try_io(lambda: self.bus.write_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.CMD_REG_WRITE, command_string))
        value = try_io(lambda: self.bus.read_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.UART1_POLL, 1))


    def read_all(self) -> dict:
        return [
            {"measurement": "o2_concentration", "value": self.read_oxygen(), "unit": "percentage"}
        ]

    def read_oxygen(self) -> float:
        command_string = [ord(c) for c in "A\r\n"] # \r\n may need to be encoded to send as the correct bytes idk
        #self.bus.write_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.CMD_REG_WRITE, command_string)
        #value = self.bus.read_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.UART1_POLL, 1)
        #while (value[0] == 0x00):
        #    time.sleep(.01)
        #    value = self.bus.read_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.UART1_READ, 6)
        try_io(lambda: self.bus.write_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.CMD_REG_WRITE, command_string))
        try_io(lambda: self.bus.read_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.UART1_POLL, 1))
        value = try_io(lambda: self.bus.read_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.UART1_READ, 16))


        #TODO: manipulate value! the current return is a raw adc 10bit num
        return value[0]


