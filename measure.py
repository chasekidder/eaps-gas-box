from database import db_utils
import sensors.sensors as sensor
from config import Config

from sensors.sensors import NANO

from webui.ui.measure_routes import celery
#celery = Celery(broker="redis://localhost:6379/0")


import time

CONFIG = None

DB = db_utils.Database()

# Initialize Sensors
SENSORS = {
    "gas pressure": sensor.ABPxx(),
    "teros12": sensor.TEROS12(0),
    "oxygen": sensor.LOX02F(),
    "altitude": sensor.MPL3115A2(),
    "pressure":sensor.ABPxx(),
    "mass flow":sensor.AWM3300V(),
    "co2":sensor.GMP251(),

}

@celery.task(name="measurement.cycle")
def measurement_cycle():
    setup()
    i = 0
    while (i < 1):
        loop()
        i = i + 1
    clean_up()
    

def setup():
    # Open Comms
    # Start WebUI
    # Load Config File
    CONFIG = Config("config.ini")

    # Backup Data Files
    DB.backup()

    # Initialize Data File
    pass

def loop():
    start = time.time()
    end = start + 1

    # Query Sensors
    #responses = {name:sensor.read_all() for (name, sensor) in SENSORS}
    responses = {"gas pressure": SENSORS["gas pressure"].read_all(),
                "teros12": SENSORS["teros12"].read_all(),
                "oxygen": SENSORS["oxygen"].read_all(),
                "altitude": SENSORS["altitude"].read_all(),
                "pressure": SENSORS["pressure"].read_all(),
                "mass flow": SENSORS["mass flow"].read_all(),
                "co2": SENSORS["co2"].read_all(),

    }

    if (time.time() < end):
            print("Hit Target!")
    else:
        print("Missed Target! :(")

    # Record Data to File
    DB.log_data(responses)

    # Control Box (eg pump)

    pass

def clean_up():
    # Verify File Integrity?
    pass

if __name__ == "__main__":
    print("dont run me!")