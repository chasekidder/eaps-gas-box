import smbus2
import time
import re

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
    A_READ_A2 = 0x12 # ABPxx Pressure Sensor
    A_READ_A3 = 0x13 # GMP 251 CO2 Sensor
    A_READ_A4 = 0x14 # I2C SCL
    A_READ_A5 = 0x15 # I2C SDA
    A_READ_A6 = 0x16 
    A_READ_A7 = 0x17 # AWM3300V Mass Flow Sensor

    SDI12_READ = 0x20
    SDI12_POLL = 0x21

    UART0_READ = 0x30
    UART1_READ = 0x31

    UART0_POLL = 0x32
    UART1_INIT = 0x33

    PUMP_CTRL_REG = 0x50

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
        time.sleep(0.01)

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
        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.A_READ_A2, 2)
        
        value = value[1] << 8 | value[0]

        return value


class AWM3300V(Sensor):
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)

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
        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.A_READ_A7, 2)
        
        value = value[1] << 8 | value[0]
        return value

class GMP251(Sensor):
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)

    def read_all(self) -> dict:
        return [
            {
                "timestamp": time.time(),
                "type": "co2 concentration", 
                "value": self.read_co2_concentration(), 
                "unit": "percent"
            }
        ]

    def read_co2_concentration(self) -> float:
        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.A_READ_A3, 2)
        
        value = value[1] << 8 | value[0]
        return value

class LOX02F(Sensor):
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)
        self.__initialize_sensor()

    def __initialize_sensor(self):
        # Configure to oneshot serial measurement mode
        command_string = "M 1\r\n"
        command_bytes = [ord(c) for c in command_string] 

        # Send command to Nano cmd register
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_bytes)

        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
        while (value[0] == 0x0F):
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
            time.sleep(0.1)

        print(value)


    def read_all(self) -> dict:
        o2_pressure = self.read_oxygen_pressure()
        o2_pressure = ''.join([chr(x) for x in o2_pressure])
        print("Oxygen Pressure:" + str(o2_pressure))


        o2_concentration = self.read_oxygen_percent()
        o2_concentration = ''.join([chr(x) for x in o2_concentration])
        print("Oxygen Concentration:" + str(o2_concentration))


        #resp_components = re.split("[+-][\d\.]+", response)

        return [
            {
                "timestamp": time.time(),
                "type": "pp02",
                "value": o2_pressure,
                "unit": "mbar",
            },
            # {
            #     "timestamp": time.time(),
            #     "type": "oxygen concentration",
            #     "value": o2_concentration,
            #     "unit": "percent",
            # },
        ]
       

    def read_oxygen_pressure(self) -> float:
        command_string = "O\r\n"
        command_bytes = [ord(c) for c in command_string] 
        
        # Send command to Nano cmd register
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_bytes)

        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
        while (value[0] == 0x0F):
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
            time.sleep(0.1)
        print(value)

        if (value[0] == 0x0F):
            print("0x0F response!")
            raise ValueError

        return value

    def read_oxygen_percent(self) -> float:
        command_string = "P\r\n"
        command_bytes = [ord(c) for c in command_string] 
        
        # Send command to Nano cmd register
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_bytes)

        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
        while (value[0] == 0x0F):
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.UART1_READ, 32)
            time.sleep(0.1)
        print(value)

        if (value[0] == 0x0F):
            print("0x0F response!")
            raise ValueError

        return value


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

    def __init__(self):
        address = MPL3115A2.I2C_ADDRESS

        self.bus = smbus2.SMBus(1)
        time.sleep(0.01)
        self.__initialize_sensor()

    def __initialize_sensor(self):
        
        # 0x39 (57) Active Mode, OSR = 128, Barometer Mode
        byteVal = MPL3115A2.CTRL_REG1.OS0 | MPL3115A2.CTRL_REG1.OS1 \
            | MPL3115A2.CTRL_REG1.OS2 | MPL3115A2.CTRL_REG1.SBYB
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # 0x07 (7) Enable data ready events Altitude, Pressure, Temperature
        byteVal = MPL3115A2.PT_DATA_CFG.TDEFE | MPL3115A2.PT_DATA_CFG.PDEFE | MPL3115A2.PT_DATA_CFG.DREM
        self.bus.write_byte_data(MPL3115A2.I2C_ADDRESS, MPL3115A2.PT_DATA_CFG.ADDRESS, byteVal)

    def read_all(self) -> dict:
        kpa = try_io(lambda: self.read_pressure())

        return [
            {
                "timestamp": time.time(),
                "type": "barometric pressure",
                "value": kpa,
                "unit": "kpa",
            },
            {
                "timestamp": time.time(),
                "type": "altitude",
                "value": (44330.77 * (1 - pow(((kpa * 1000) / 101326), (0.1902632)))),
                "unit": "meters",
            },
            {
                "timestamp": time.time(),
                "type": "temperature",
                "value": self.read_temperature_c(),
                "unit": "celcius",
            },
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
        time.sleep(0.01)

    def read_all(self) -> dict:
        response = self.read_sensor()
        response = ''.join([chr(x) for x in response])

        resp_components = re.findall("([+-][\d\.]+)", response)

        moisture = float(resp_components[0])
        temperature = float(resp_components[1])
        e_c = float(resp_components[2])
        

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
                "unit": "mS/cm",
            },
            {
                "timestamp": time.time(),
                "type": "volumetric water content",
                "value": moisture,
                "unit": "calibrated counts VWC",
            },
        ]


    def read_sensor(self) -> str:
        # Write TEROS-12 Command to the Nano's Command Register
        command_string = f"{ self.address }R0!"
        command_bytes = [ord(c) for c in command_string]
        self.bus.write_i2c_block_data(NANO_I2C_ADDR, NANO.CMD_REG_WRITE, command_bytes)

        value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.SDI12_READ, 32)
        while (value[0] == 0x0F):
            value = self.bus.read_i2c_block_data(NANO_I2C_ADDR, NANO.SDI12_READ, 32)
            time.sleep(0.1)


        if (value[0] == 0x0F):
            print("0x0F response!")
            print(value)
            raise ValueError

        return value