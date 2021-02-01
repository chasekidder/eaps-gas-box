from app.sensors.sensor_base import Sensor

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
    SDI12_POLL = 0x21
    UART0_READ = 0x30
    UART1_READ = 0x31
    UART0_POLL = 0x32
    UART1_POLL = 0x33

class TEROS12(Sensor):
    def __init__(self, id):
        type = "TEROS12"
        protocol = "SDI12"
        address = 0 # TODO: THIS NEEDS TO BE DYNAMIC!!!
        measurements = [
            "temperature",
            "electrical_conductivity",
            "moisture"
        ]
        
        super().__init__(id, type, protocol, address, measurements)
        self.bus = smbus2.SMBus(1)

    def read_all(self) -> dict:
        response = self.read_sensor()
        print(response)
        temperature = response
        e_c = 0
        moisture = 0

        return {
            "temperature": temperature,
            "electrical_conductivity": e_c,
            "moisture": moisture
        }

    def read_sensor(self) -> str:
        command_string = [ord(c) for c in f"{ self.ADDRESS }R0!"]
        self.bus.write_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.CMD_REG_WRITE, command_string)
        self.bus.read_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.SDI12_POLL, 1)
        value = self.bus.read_i2c_block_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.SDI12_READ, 16)

        return value