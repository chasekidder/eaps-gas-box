from app import models
from app import db




def add_measurement(cycle, sensor, value):
    m = models.Measurement(value=value, sensor_id=sensor, collection_id=cycle)
    db.session.add(m)
    db.session.commit()




def test_db():
    site = models.Site(name="TestSite1")
    sensor = models.Sensor(name="TestSensor1")
    db.session.add(site)
    db.session.add(sensor)
    db.session.flush()
    cycle = models.Collection(site_id=site.id)
    db.session.add(cycle)
    db.session.flush()

    add_measurement(cycle.id, sensor.id, 420.69)