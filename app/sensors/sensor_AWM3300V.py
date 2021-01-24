from app.sensors.sensor_base import Sensor

import smbus2

class AWM3300V(Sensor):
    def __init__(self, id):
        type = "MPL3115A2"
        protocol = "ANALOG"
        address = 0x14
        measurements = [
            "mass_flow"
        ]
        
        super().__init__(id, type, protocol, address, measurements)
        self.bus = smbus2.SMBus(1)

    def read_all(self) -> dict:
        return {
            "mass_flow": self.read_mass_flow()
        }

    def read_mass_flow(self) -> float:
        command = "ANALOG|0"
        cmd = [ord(c) for c in command]
        self.bus.write_i2c_block_data(self.ADDRESS, 0x00, cmd)
        value = self.bus.read_byte_data(self.ADDRESS, 0)
        return value


