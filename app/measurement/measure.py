from app.sensors.sensor_MPL3115A2 import MPL3115A2
from app.frontend import celery

import time
import datetime

config = {
    "sensor_metadata": {
        0: "MPL3115A2",
    },
    "sample_frequency": 1,
    "duration": 1,
}

@celery.task(name="measurement.cycle")
def start_cycle(config:dict=config):
    # duration is 1 minute minimum
    sensor_metadata = config["sensor_metadata"]
    sample_freq = config["sample_frequency"]
    duration = config["duration"]

    sensors = [new_sensor(s_id, sensor_metadata[s_id]) for s_id in sensor_metadata]

    sample_delay = datetime.timedelta(seconds=float(1 / sample_freq))
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(minutes=duration)

    while(datetime.datetime.now() < end_time):
        target_time = datetime.datetime.now() + sample_delay

        values = query_all(sensors)

        # log to database by id
        print(values)

        # Check if sample collection completed before target time
        if (datetime.datetime.now() < target_time):
            print("Hit Target!")
            time.sleep(target_time - datetime.datetime.now())
        else:
            print("Missed Target! :(")

    print("Cycle Complete!")

def query_all(sensors:list):
    return {s.ID: s.read_all() for s in sensors}

def new_sensor(id, s_type):
    if s_type == "MPL3115A2":
        return MPL3115A2(id)

    elif s_type == "TEROS-12":
        pass