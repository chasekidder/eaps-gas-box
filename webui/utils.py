import os
import random
import datetime
import re


def get_files_in_dir(path:str) -> list:
    return os.listdir(path)


def get_live_data():
    return {
            "timestamp": datetime.datetime.now(),
            "Electrical Conductivity": {
                        "Sensor1": random.randint(1,10),
                        "Sensor2": random.randint(1,10),
                        "Sensor3": random.randint(1,10),
                        },
            "Moisture": {
                        "Sensor1": random.randint(1,10),
                        "Sensor2": random.randint(1,10),
                        "Sensor3": random.randint(1,10),
                        },
            "Temperature": {
                        "Sensor1": random.randint(1,10),
                        "Sensor2": random.randint(1,10),
                        "Sensor3": random.randint(1,10),
                        },
            "Carbon Dioxide": random.randint(1,10),
            "Oxygen": random.randint(1,10),
            "Gas Pressure": random.randint(1,10)
            }



def str_to_bytes(data: str) -> bytes:
    return data.encode()

def bytes_to_str(data: bytes, encoding: str="utf-8") -> str:
    return data.decode(encoding)

def parse_regex(data: str, pattern: str) -> list:
    return re.split(pattern, data)