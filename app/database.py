from app import models
from app import db


def init_new_db():
    db.create_all()

def commit_all():
    db.session.commit()

def add_measurement(cycle_id: int, sensor_id: int, value, measurement_name: str):
    measurement = models.Measurement(value=value, sensor_id=sensor_id, 
        cycle_id=cycle_id, name=measurement_name)
    db.session.add(measurement)
    db.session.flush()
    return measurement

def add_site(site_name: str):
    site = models.Site(name=site_name)
    db.session.add(site)
    db.session.flush()
    return site
    
def add_sensor(sensor_name: str):
    sensor = models.Sensor(name=sensor_name)
    db.session.add(sensor)
    db.session.flush()
    return sensor

def add_cycle(site_id: int):
    cycle = models.Cycle(site_id=site_id)
    db.session.add(cycle)
    db.session.flush()
    return cycle

def get_site_id_by_name(site_name: str):
    site = (
        db.session.query(models.Site)
        .filter(models.Site.name == site_name).one_or_none()
    )

    if site is not None:
        return site.id
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

def get_sensor_id(sensor_name: str) -> int:
    sensor_id = get_sensor_id_by_name(sensor_name)
    if sensor_id is not None:
        return sensor_id
    else:
        sensor = add_sensor(sensor_name)
        return sensor.id

def get_site_id(site_name: str) -> int:
    site_id = get_site_id_by_name(site_name)
    if site_id is not None:
        return site_id
    else:
        site = add_site(site_name)
        return site.id



def test_db():
    #sensor = add_sensor("TestSensor2")
    #site = add_site("TestSite2")
    site = get_site_id_by_name("TestSite2")
    sensor = get_sensor_id_by_name("TestSensor3")

    cycle = add_cycle(site)
    measurement = add_measurement(cycle.id, sensor, 11111.111)
