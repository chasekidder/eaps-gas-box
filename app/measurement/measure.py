#TODO: import all sensors from this module
from app.sensors.sensor_MPL3115A2 import MPL3115A2
from app.sensors.sensor_AWM3300V import AWM3300V
from app.sensors.sensor_TEROS12 import TEROS12

from celery import Celery

import time


# Start Celery Instance
celery = Celery(broker="redis://localhost:6379/0")

config = {
    "sensor_metadata": {
        0: "MPL3115A2",
        1: "AWM3300V",
        2: "TEROS-12"
    },
    "sample_frequency": 1,
    "duration": 0.5,
}

@celery.task(name="measurement.cycle")
def start_cycle(config:dict=config):
    # duration is 1 minute minimum
    sensor_metadata = config["sensor_metadata"]
    sample_freq = config["sample_frequency"]
    duration = config["duration"]

    sensors = [new_sensor(s_id, sensor_metadata[s_id]) for s_id in sensor_metadata]

    sample_delay = 1 / sample_freq
    start_time = time.time()
    end_time = start_time + (60 * duration)

    while(time.time() < end_time):
        target_time = time.time() + sample_delay
        #print(f"Now: {time.time()}, Target: {target_time}")

        responses = query_all(sensors)

        # log to database by id
        log_data(responses)

        # Check if sample collection completed before target time
        if (time.time() < target_time):
            print("Hit Target!")
            time.sleep(target_time - time.time())
        else:
            print("Missed Target! :(")

    print("Cycle Complete!")

def query_all(sensors:list):
    return {s.ID: s.read_all() for s in sensors}

def new_sensor(id, s_type):
    if s_type == "MPL3115A2":
        return MPL3115A2(id)

    elif s_type == "TEROS12":
        return TEROS12(id)

    elif s_type == "AWM3300V":
        return AWM3300V(id)

def log_data(responses:dict):
    for sensor in responses:
        #add_measurement
        pass