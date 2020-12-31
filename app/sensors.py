from app import app
from app import database
from app import comm
from app import utils

import random

class Sensor():
    def __init__(self, id, type, name):
        self.id = id
        self.type = type
        self.name = name
        

    def read(self):
        pass

class SDI12Sensor(Sensor):
    def __init__(self, name, measurement_names):
        self.id = database.get_sensor_id(name)
        super().__init__(self.id, "SDI12", name)
        self.conn = comm.UARTInterface("/dev/ttyACM0", 115200)
        self.bus_id = 0
        self.teros = False
        self.measurement_names = measurement_names
        self.check_if_teros12()
    
    def check_if_teros12(self):
        self.teros = True

    def read(self):
        self.conn.write(f"<SDI12|{ self.bus_id }R0!>")
        return self.conn.read()

    def record_data(self, cycle_id, sensor_id):
        data = self.read()
        
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
            raise ValueError("WTF")

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

    else:
        return None

