import smbus2
import time

from config import Config
from sensors.utils import try_io

CONFIG = Config("config.ini")

# Arduino Nano I2C Address
NANO_I2C_ADDR = CONFIG.NANO_I2C_ADDR

# Arduino Nano I2C Command Registers
class NANO():
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

class Sensor():
    def __init__(self):
        pass
        
    def read_all(self):
        raise NotImplementedError

    def calibrate(self):
        raise NotImplementedError


class ABPxx(Sensor):
    def __init__(self):
        self.bus = smbus2.SMBus(1)

    def read_all(self) -> list:
        return [
            {
                "timestamp": time.time(),
                "type": "pressure",
                "value": self.read_pressure(),
                "unit": "mbar",
            }
        ]

    def read_pressure(self) -> float:
        # TODO: Make sure to receive 2 bytes instead of one because the nano is
        # supposed to be sending a 16-bit number!
        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.A_READ_A2, 2)
        
        #TODO: manipulate value! the current return is a raw adc 10bit num
        value = value[1] << 8 | value[0]

        return value


class AWM3300V(Sensor):
    def __init__(self, name):
        self.bus = smbus2.SMBus(1)

    def read_all(self) -> dict:
        return [
            {
                "timestamp": time.time(),
                "type": "mass flow", 
                "value": self.read_mass_flow(), 
                "unit": "asdf"
            }
        ]

    def read_mass_flow(self) -> float:
        # TODO: Make sure to receive 2 bytes instead of one because the nano is
        # supposed to be sending a 16-bit number!
        value = self.bus.read_byte_data(NANO_I2C_ADDR, NANO.A_READ_A0)
        
        #TODO: manipulate value! the current return is a raw adc 10bit num
        return value

class GMP251(Sensor):
    def __init__(self, id):
        type = "GMP251"
        protocol = "ANALOG"
        address = 14
        measurements = [
            "co2_concentration"
        ]
        
        super().__init__(id, type, protocol, address, measurements)
        self.bus = smbus2.SMBus(1)

    def read_all(self) -> dict:
        return {
            "sensor":self.name,
            "data":{"measurement": "co2_concentration", "value": self.read_co2_concentration(), "unit": "percent"}
        }

    def read_co2_concentration(self) -> float:
        # TODO: Make sure to receive 2 bytes instead of one because the nano is
        # supposed to be sending a 16-bit number!
        value = self.bus.read_byte_data(NANO_I2C_ADDR, NANO.A_READ_A1)
        
        #TODO: manipulate value! the current return is a raw adc 10bit num
        return value

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
        try_io(lambda: self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_string))
        value = try_io(lambda: self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_POLL, 1))


    def read_all(self) -> dict:
        return [
            {"measurement": "o2_concentration", "value": self.read_oxygen(), "unit": "percentage"}
        ]

    def read_oxygen(self) -> float:
        command_string = [ord(c) for c in "A\r\n"] # \r\n may need to be encoded to send as the correct bytes idk
        #self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_string)
        #value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_POLL, 1)
        #while (value[0] == 0x00):
        #    time.sleep(.01)
        #    value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 6)
        try_io(lambda: self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_string))
        try_io(lambda: self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_POLL, 1))
        value = try_io(lambda: self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 16))


        #TODO: manipulate value! the current return is a raw adc 10bit num
        return value[0]

class MPL3115A2(Sensor):
    I2C_ADDRESS = 0x60
    REGISTER_STATUS_ADDRESS = 0x00
    REGISTER_PRESSURE_MSB = 0x01
    REGISTER_ALTITUDE_MSB = 0x01
    REGISTER_TEMP_MSB = 0x04
    BAR_IN_MSB = 0x14

    class CTRL_REG1:
        ADDRESS = 0x26
        SBYB = 0x01
        OST = 0x02
        RST = 0x04
        OS0 = 0x08
        OS1 = 0x10
        OS2 = 0x20
        RAW = 0x40
        ALT = 0x80

    class PT_DATA_CFG:
        ADDRESS = 0x13
        TDEFE = 0x01
        PDEFE = 0x02
        DREM = 0x04

    def __init__(self, id):
        type = "MPL3115A2"
        protocol = "I2C"
        address = MPL3115A2.I2C_ADDRESS
        measurements = [
            "barometric_pressure",
            "altitude",
            "temperature_celcius",
            "temperature_farenheit"
        ]
        
        super().__init__(id, type, protocol, address, measurements)
        self.bus = smbus2.SMBus(1)
        self.__initialize_sensor()

    def __initialize_sensor(self):
        
        # 0x39 (57) Active Mode, OSR = 128, Barometer Mode
        byteVal = MPL3115A2.CTRL_REG1.OS0 | MPL3115A2.CTRL_REG1.OS1 \
            | MPL3115A2.CTRL_REG1.OS2 | MPL3115A2.CTRL_REG1.SBYB
        try_io(lambda: self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.CTRL_REG1.ADDRESS, byteVal))
        time.sleep(.001)

        # 0x07 (7) Enable data ready events Altitude, Pressure, Temperature
        byteVal = MPL3115A2.PT_DATA_CFG.TDEFE | MPL3115A2.PT_DATA_CFG.PDEFE | MPL3115A2.PT_DATA_CFG.DREM
        try_io(lambda: self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.PT_DATA_CFG.ADDRESS, byteVal))

    def read_all(self) -> dict:
        kpa = try_io(lambda: self.read_pressure())
        return [
            {"measurement": "barometric_pressure", "value": kpa, "unit": "kpa"},
            {"measurement": "altitude", "value": (44330.77 * (1 - pow(((kpa * 1000) / 101326), (0.1902632)))), "unit": "meters"},
            {"measurement": "temperature_celcius", "value": try_io(lambda: self.read_temperature_c()), "unit": "celcius"},
            {"measurement": "temperature_farenheit", "value": try_io(lambda: self.read_temperature_f()), "unit": "farenheit"},
        ]

    def read_pressure(self) -> float:
        # 0x39 (57) Active Mode, OSR = 128, Barometer Mode
        byteVal = MPL3115A2.CTRL_REG1.OS0 | MPL3115A2.CTRL_REG1.OS1 \
            | MPL3115A2.CTRL_REG1.OS2 | MPL3115A2.CTRL_REG1.SBYB
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # Read barometric pressure (3 bytes)
        # Pressure MSB, Pressure CSB, Pressure LSB
        data = self.bus.read_i2c_block_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.REGISTER_PRESSURE_MSB, 3)

        # Convert to 20-bit integer
        pressure_pa = (((data[0]<<16) + (data[1]<<8) + (data[2] & 0xF0)) / 16) / 4.0
        pressure_kpa = pressure_pa / 1000.0

        return pressure_kpa

    def read_altitude(self) -> float:
        # 0xB9 (185) Active Mode, OSR = 128, Altimeter Mode
        byteVal = MPL3115A2.CTRL_REG1.OS0 | MPL3115A2.CTRL_REG1.OS1 \
            | MPL3115A2.CTRL_REG1.OS2 | MPL3115A2.CTRL_REG1.SBYB | MPL3115A2.CTRL_REG1.ALT
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # Read altitude (3 bytes)
        # Altitude MSB, Altitude CSB, Altitude LSB
        data = self.bus.read_i2c_block_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.REGISTER_ALTITUDE_MSB, 3)

        # Convert to 20-bit integer
        altitude = (((data[0]<<16) + (data[1]<<8) + (data[2] & 0xF0)) / 16) / 16.0

        return altitude

    def read_temperature_c(self) -> float:
        # 0x39 (57) Active Mode, OSR = 128, Barometer Mode
        byteVal = MPL3115A2.CTRL_REG1.OS0 | MPL3115A2.CTRL_REG1.OS1 \
            | MPL3115A2.CTRL_REG1.OS2 | MPL3115A2.CTRL_REG1.SBYB
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # Read ambiant temperature (2 bytes)
        # Temperature MSB, Temperature LSB
        data = self.bus.read_i2c_block_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.REGISTER_TEMP_MSB, 2)

        # Convert to 20-bit integer
        altitude = (((data[0]<<8) + (data[1] & 0xF0)) / 16) / 16.0

        return altitude

    def read_temperature_f(self) -> float:
        temp_c = self.read_temperature_c()
        temp_f = (temp_c * 1.8) + 32

        return temp_f

    def calibrate_sea_level(self, pascal:float = 101326):
        if ((pascal / 2) > 65535):
            raise ValueError("Calibration Number Too Large")

        bar_hg = pascal / 2
        data = [int(bar_hg) >> 8, int(bar_hg) & 0xF0 ]
        self.bus.write_i2c_block_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.BAR_IN_MSB, data)

class TEROS12(Sensor):
    def __init__(self, address):
        self.address = address

        self.bus = smbus2.SMBus(1)

    def read_all(self) -> dict:
        response = self.read_sensor()
        print(response)
        print(''.join([chr(x) for x in response]))
        temperature = 0
        e_c = 0
        moisture = 0

        return [
            {
                "timestamp": time.time(),
                "type": "temperature",
                "value": temperature,
                "unit": "celcius",
            },
            {
                "timestamp": time.time(),
                "type": "electrical conductivity",
                "value": e_c,
                "unit": "v",
            },
            {
                "timestamp": time.time(),
                "type": "moisture",
                "value": moisture,
                "unit": "mmhg?",
            },
        ]


    def read_sensor(self) -> str:
        command_string = [ord(c) for c in f"{ self.address }R0!"]
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_string)
        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.SDI12_READ, 64)
        while (value[0] == 0x00):
            time.sleep(0.001)
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.SDI12_READ, 64)

        return value