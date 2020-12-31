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
        print(data)
        
        if self.teros:
            values = utils.parse_regex(data, "[+-]")
        else:
            print("Not TEROS12?")
            values = []

        if values:
            pass
        else:
            raise ValueError("WTF")

        return

        results = {self.measurement_names[i]: values[i] for i 
            in range(len(self.measurement_names))} 

        for result in results:
            database.add_measurement(cycle_id, sensor_id, result)
        

    def identify_all_sensors(self):
        pass


def new_sensor(sensor_metadata):
    if sensor_metadata.protocol == "SDI12":
        return SDI12Sensor(sensor_metadata.sensor_name, 
            sensor_metadata.measurement_names)

    else:
        return None

