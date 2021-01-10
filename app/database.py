from app import models
from app import db


def init_new_db():
    db.create_all()

def commit_all():
    db.session.commit()

def add_sample(cycle: int, sensor: int, value, measurement_name: str):
    sample = models.Sample(value=value, sensor=sensor, 
        cycle=cycle, name=measurement_name)
    db.session.add(sample)
    db.session.flush()
    return sample

def add_location(location_name: str):
    location = models.Location(name=location_name)
    db.session.add(location)
    db.session.flush()
    return location
    
def add_sensor(sensor_name: str, protocol: str, measurement_name,
                    address, command):
    measurement_name_id = get_measurement_name_id_by_name(measurement_name)

    sensor = models.Sensor(name=sensor_name, protocol=protocol, 
        measurement_type=measurement_name_id, address=address, command=command)
    db.session.add(sensor)
    db.session.flush()
    return sensor

def add_cycle(site: int):
    cycle = models.Cycle(site=site)
    db.session.add(cycle)
    db.session.flush()
    return cycle

def add_measurement_name(measurement_name):
    measurement_name = models.MeasurementName(name=measurement_name)
    db.session.add(measurement_name)
    db.session.flush()
    return measurement_name

def get_location_id_by_name(location_name: str):
    location = (
        db.session.query(models.Location)
        .filter(models.Location.name == location_name).one_or_none()
    )

    if location is not None:
        return location.id
    else:
        return None

def get_sensor_id_by_name(sensor_name: str) -> int or None:
    sensor= (
        db.session.query(models.Sensor)
        .filter(models.Sensor.name == sensor_name).one_or_none()
    )

    if sensor is not None:
        return sensor.id
    else:
        return None

def get_measurement_name_id_by_name(measurement_name):
    measurement_name = (
        db.session.query(models.MeasurementName)
        .filter(models.MeasurementName.name == 
            measurement_name).one_or_none()
    )

    if measurement_name is not None:
        return measurement_name.id
    else:
        return None

def get_sensor_id(sensor_name: str) -> int:
    sensor_id = get_sensor_id_by_name(sensor_name)
    if sensor_id is not None:
        return sensor_id
    else:
        sensor = add_sensor(sensor_name)
        return sensor.id

def get_location_id(location_name: str) -> int:
    location_id = get_location_id_by_name(location_name)
    if location_id is not None:
        return location_id
    else:
        site = add_location(location_name)
        return site.id

def get_measurement_name_id(measurement_name: str) -> int:
    measurement_name_id = get_measurement_name_id_by_name(measurement_name)
    if measurement_name_id is not None:
        return measurement_name_id
    else:
        measurement_type = add_measurement_name(measurement_name)
        return measurement_type.id