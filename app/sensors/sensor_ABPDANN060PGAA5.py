from app.sensors.sensor_base import Sensor

import smbus2

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

class ABPxx(Sensor):
    def __init__(self, id):
        type = "ABPxxx"
        protocol = "ANALOG"
        address = 14
        measurements = [
            "pressure"
        ]
        
        super().__init__(id, type, protocol, address, measurements)
        self.bus = smbus2.SMBus(1)

    def read_all(self) -> list:
        return [
            {"measurement": "pressure", "value": self.read_pressure(), "unit": "mbar"}
        ]

    def read_pressure(self) -> float:
        # TODO: Make sure to receive 2 bytes instead of one because the nano is
        # supposed to be sending a 16-bit number!
        value = self.bus.read_byte_data(ARDUINO_NANO_I2C_ADDRESS, NANO_I2C_CMD.A_READ_A2)
        
        #TODO: manipulate value! the current return is a raw adc 10bit num
        return value

