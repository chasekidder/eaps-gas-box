from app import models
from app import db


def init_new_db():
    db.create_all()

def add_measurement(cycle_id, sensor_id, value):
    measurement = models.Measurement(value=value, sensor_id=sensor_id, cycle_id=cycle_id)
    db.session.add(measurement)
    db.session.commit()
    return measurement

def add_site(site_name):
    site = models.Site(name=site_name)
    db.session.add(site)
    db.session.flush()
    return site
    
def add_sensor(sensor_name):
    sensor = models.Sensor(name=sensor_name)
    db.session.add(sensor)
    db.session.flush()
    return sensor

def add_cycle(site_id):
    cycle = models.Cycle(site_id=site_id)
    db.session.add(cycle)
    db.session.flush()
    return cycle

def get_site_id_by_name(site_name):
    site = (
        db.session.query(models.Site)
        .filter(models.Site.name == site_name).one_or_none()
    )

    if site is not None:
        return site.id

def get_sensor_id_by_name(sensor_name):
    sensor= (
        db.session.query(models.Sensor)
        .filter(models.Sensor.name == sensor_name).one_or_none()
    )

    if sensor is not None:
        return sensor.id



def test_db():
    #sensor = add_sensor("TestSensor2")
    #site = add_site("TestSite2")
    site = get_site_id_by_name("TestSite2")
    sensor = get_sensor_id_by_name("TestSensor3")

    cycle = add_cycle(site)
    measurement = add_measurement(cycle.id, sensor, 11111.111)
