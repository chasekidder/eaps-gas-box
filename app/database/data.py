from app import app
from app import database
from app import sensors as s
import time

# --------------------------------------------------------------------------
# TEMPORARY TESTING CLASS
class SensorMetadata():
    def __init__(self, protocol, measurement_names, sensor_name, address = None, data_bytes = None):
        self.protocol = protocol
        self.measurement_names = measurement_names
        self.sensor_name = sensor_name
        self.data_bytes = data_bytes
        self.address = address

# --------------------------------------------------------------------------

def collect_data():

    # ----------------------------------------------------------------------
    # TEMPORARY TESTING OBJECT
    settings = {
        "freq": 1, # samples per second
        "duration": 10, # seconds
        "site_name": "TestSite1",
        "sensors": [
            #SensorMetadata("SDI12", ["Moisture", "Temperature", "Electrical Conductivity"], "Sensor1"),
            #SensorMetadata("I2C", ["CO2"], "I2CSensor2", bytearray.fromhex("68"), bytearray.fromhex("04 04 22 00 08 2A"))
            SensorMetadata("ANALOG", ["CO2"], "CO2_Sensor", 1),
        ]
        
    }

    # TODO: Need to store sensor config data in database
    sensors = [s.new_sensor(sensor) for sensor in settings["sensors"]]
    # ----------------------------------------------------------------------



    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # Begin the sampling

    num_of_samples = settings["freq"] * settings["duration"]
    sec_delay = 1 / settings["freq"]

    site_id = database.get_site_id(settings["site_name"])
    cycle = database.add_cycle(site_id)


    for _ in range(num_of_samples):
        print(f"========= Iteration: {_} ===========")
        temp = True
        time_start = time.time()
        time_target = time_start + sec_delay
        #print("Target: " + str(time_target))

        for sensor in sensors:
            sensor.record_data(cycle.id, sensor.id)
        
        database.commit_all()
        while (time.time() < time_target):
            if temp:
                temp = u'\u2713'
                print(f"Target Time Met: {temp}")
                temp = False
            time.sleep(.001)



