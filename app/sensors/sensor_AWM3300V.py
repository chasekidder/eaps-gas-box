from app.sensors.sensor_base import Sensor

import smbus2

ARDUINO_NANO_I2C_ADDRESS = 0x14

class NANO_I2C_CMD():
    COMMAND_REG = 0x00
    A_READ_A0 = 0x10
    A_READ_A1 = 0x11
    A_READ_A2 = 0x12
    A_READ_A3 = 0x13
    A_READ_A4 = 0x14
    A_READ_A5 = 0x15
    SDI12_READ = 0x20
    UART_READ = 0x30

class AWM3300V(Sensor):
    def __init__(self, id):
        type = "MPL3115A2"
        protocol = "ANALOG"
        address = 14
        measurements = [
            "mass_flow"
        ]
        
        super().__init__(id, type, protocol, address, measurements)
        self.bus = smbus2.SMBus(1)
        self.arduino_addr = 0x14

    def read_all(self) -> dict:
        return {
            "mass_flow": self.read_mass_flow()
        }

    def read_mass_flow(self) -> float:
        #command_string = [ord(c) for c in "0R0!"]
        #self.bus.write_i2c_block_data(NANO_I2C.ADDRESS, NANO_I2C.COMMAND_REG, command_string)
        #value = self.bus.read_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.A_READ_A0, 1)
        value = self.bus.read_byte_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.A_READ_A0)
        print(value)
        return value


