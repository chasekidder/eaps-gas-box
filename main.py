from database import db_utils
import sensors.sensors as sensor
from config import Config

import time

CONFIG = None
SENSORS = []
DB = db_utils.Database()

def setup():
    # Open Comms
    # Start WebUI
    # Load Config File
    CONFIG = Config("config.ini")

    # Initialize Sensors
    SENSORS = {
        "gas pressure": sensor.ABPxx(),
        "gas flow": sensor.AWM3300V(),

    }

    # Backup Data Files
    DB.backup()

    # Initialize Data File
    pass

def loop():
    start = time.time()
    end = start + 1

    # Query Sensors
    responses = {name:sensor.read_all() for (name, sensor) in SENSORS}

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
    setup()
    loop()
    clean_up()