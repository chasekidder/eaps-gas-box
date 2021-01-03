from os import RTLD_LAZY
from typing import Protocol
from app.views import data
from app import app
from app import database
from app import comm
from app import utils

import random

class Sensor():
    conn = comm.UARTInterface("/dev/ttyACM0", 9600)

    def __init__(self, id, type, name):
        self.id = id
        self.type = type
        self.name = name
        

    def read(self):
        pass


class I2CSensor(Sensor):
    def __init__(self, name, measurement_names, address, cmd_bytes):
        self.id = database.get_sensor_id(name)
        super().__init__(self.id, "I2C", name)
        
        self.device_addr = address
        self.measurement_names = measurement_names
        self.cmd_bytes = cmd_bytes

    def read(self):
        cmd = bytearray(b"<I2C|R")
        cmd.extend(self.device_addr)
        cmd.extend(self.cmd_bytes)
        cmd.extend(bytearray(b">"))

        Sensor.conn.conn.write(cmd)
        return Sensor.conn.conn.readline()


    def record_data(self, cycle_id, sensor_id):
        values = self.read().rstrip()

        #TODO: Refactor this because its a bodge to get the CO2 sensor working
        # Cuts the middle 2 bytes out of the response and adds them 
        rx_bytes = memoryview(values)
        rx_bytes = rx_bytes[1:3]
        values = [int.from_bytes(rx_bytes, byteorder="big")]

        # Combine measurement names and values into a single dictionary
        results = dict(zip(self.measurement_names, values))

        # Addd the final measurements to the database
        for result in results:
            database.add_measurement(cycle_id, sensor_id, results[result], result)
            print(f"{result}: {results[result]}")


class SDI12Sensor(Sensor):
    def __init__(self, name, measurement_names):
        self.id = database.get_sensor_id(name)
        super().__init__(self.id, "SDI12", name)
        
        self.bus_id = 0
        self.teros = False
        self.measurement_names = measurement_names
        self.check_if_teros12()
    
    def check_if_teros12(self):
        self.teros = True

    def read(self):
        Sensor.conn.write(f"<SDI12|{ self.bus_id }R0!>")
        return Sensor.conn.read()

    def record_data(self, cycle_id, sensor_id):
        data = self.read()
        
        # TODO: Refactor this because its awful
        if self.teros:
            # Seperate TEROS-12 response data into its component elements
            # BUS_ID[+-]MOISTURE[+-]TEMPERATURE[+-]EC\r\r\n
            values = utils.parse_regex(data, "([+-])")

            # Remove bus ID element from list
            values.pop(0)

            # Join pos/neg signs with measures and strip whitespace
            for index, _ in enumerate(values):
                values[index:index + 2] = ["".join(values[index:index + 2])
                    .rstrip()]

            # Cast all the values to the appropriate floats
            values = [float(value) for value in values]

        else:
            print("Not TEROS12?")
            values = None

        if values:
            pass
        else:
            raise ValueError("SDI-12 Values was empty!")

        # Combine measurement names and values into a single dictionary
        results = dict(zip(self.measurement_names, values))

        # Addd the final measurements to the database
        for result in results:
            database.add_measurement(cycle_id, sensor_id, results[result], result)
            print(f"{result}: {results[result]}")
        

    def identify_all_sensors(self):
        pass


def new_sensor(sensor_metadata):
    if sensor_metadata.protocol == "SDI12":
        return SDI12Sensor(sensor_metadata.sensor_name, 
            sensor_metadata.measurement_names)

    elif sensor_metadata.protocol == "I2C":
        return I2CSensor(sensor_metadata.sensor_name, 
            sensor_metadata.measurement_names, sensor_metadata.address, 
            sensor_metadata.data_bytes)

    else:
        return None

