from app.sensors.sensor_base import Sensor

import smbus2
import time

def try_io(call, tries=10):
    assert tries > 0
    error = None
    result = None

    while tries:
        try:
            result = call()
        except IOError as e:
            error = e
            tries -= 1
        else:
            break

    if not tries:
        raise error

    return result

MPL3115A2_I2C_ADDRESS = 0x60
MPL3115A2_REGISTER_STATUS_ADDRESS = 0x00
MPL3115A2_REGISTER_PRESSURE_MSB = 0x01
MPL3115A2_REGISTER_ALTITUDE_MSB = 0x01
MPL3115A2_REGISTER_TEMP_MSB = 0x04
MPL3115A2_BAR_IN_MSB = 0x14

class MPL3115A2_CTRL_REG1:
    ADDRESS = 0x26
    SBYB = 0x01
    OST = 0x02
    RST = 0x04
    OS0 = 0x08
    OS1 = 0x10
    OS2 = 0x20
    RAW = 0x40
    ALT = 0x80

class MPL3115A2_PT_DATA_CFG:
    ADDRESS = 0x13
    TDEFE = 0x01
    PDEFE = 0x02
    DREM = 0x04

class MPL3115A2(Sensor):
    def __init__(self, id):
        type = "MPL3115A2"
        protocol = "I2C"
        address = MPL3115A2_I2C_ADDRESS
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
        byteVal = MPL3115A2_CTRL_REG1.OS0 | MPL3115A2_CTRL_REG1.OS1 \
            | MPL3115A2_CTRL_REG1.OS2 | MPL3115A2_CTRL_REG1.SBYB
        try_io(lambda: self.bus.write_byte_data(MPL3115A2_I2C_ADDRESS, MPL3115A2_CTRL_REG1.ADDRESS, byteVal))
        time.sleep(.001)

        # 0x07 (7) Enable data ready events Altitude, Pressure, Temperature
        byteVal = MPL3115A2_PT_DATA_CFG.TDEFE | MPL3115A2_PT_DATA_CFG.PDEFE | MPL3115A2_PT_DATA_CFG.DREM
        try_io(lambda: self.bus.write_byte_data(MPL3115A2_I2C_ADDRESS, MPL3115A2_PT_DATA_CFG.ADDRESS, byteVal))

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
        byteVal = MPL3115A2_CTRL_REG1.OS0 | MPL3115A2_CTRL_REG1.OS1 \
            | MPL3115A2_CTRL_REG1.OS2 | MPL3115A2_CTRL_REG1.SBYB
        self.bus.write_byte_data(MPL3115A2_I2C_ADDRESS, MPL3115A2_CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # Read barometric pressure (3 bytes)
        # Pressure MSB, Pressure CSB, Pressure LSB
        data = self.bus.read_i2c_block_data(MPL3115A2_I2C_ADDRESS, MPL3115A2_REGISTER_PRESSURE_MSB, 3)

        # Convert to 20-bit integer
        pressure_pa = (((data[0]<<16) + (data[1]<<8) + (data[2] & 0xF0)) / 16) / 4.0
        pressure_kpa = pressure_pa / 1000.0

        return pressure_kpa

    def read_altitude(self) -> float:
        # 0xB9 (185) Active Mode, OSR = 128, Altimeter Mode
        byteVal = MPL3115A2_CTRL_REG1.OS0 | MPL3115A2_CTRL_REG1.OS1 \
            | MPL3115A2_CTRL_REG1.OS2 | MPL3115A2_CTRL_REG1.SBYB | MPL3115A2_CTRL_REG1.ALT
        self.bus.write_byte_data(MPL3115A2_I2C_ADDRESS, MPL3115A2_CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # Read altitude (3 bytes)
        # Altitude MSB, Altitude CSB, Altitude LSB
        data = self.bus.read_i2c_block_data(MPL3115A2_I2C_ADDRESS, MPL3115A2_REGISTER_ALTITUDE_MSB, 3)

        # Convert to 20-bit integer
        altitude = (((data[0]<<16) + (data[1]<<8) + (data[2] & 0xF0)) / 16) / 16.0

        return altitude

    def read_temperature_c(self) -> float:
        # 0x39 (57) Active Mode, OSR = 128, Barometer Mode
        byteVal = MPL3115A2_CTRL_REG1.OS0 | MPL3115A2_CTRL_REG1.OS1 \
            | MPL3115A2_CTRL_REG1.OS2 | MPL3115A2_CTRL_REG1.SBYB
        self.bus.write_byte_data(MPL3115A2_I2C_ADDRESS, MPL3115A2_CTRL_REG1.ADDRESS, byteVal)
        time.sleep(.001)

        # Read ambiant temperature (2 bytes)
        # Temperature MSB, Temperature LSB
        data = self.bus.read_i2c_block_data(MPL3115A2_I2C_ADDRESS, MPL3115A2_REGISTER_TEMP_MSB, 2)

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
        self.bus.write_i2c_block_data(MPL3115A2_I2C_ADDRESS, MPL3115A2_BAR_IN_MSB, data)
