from app.database import models
from app.database.models import db

import datetime

def log_measurement(value, sensor, cycle):
    #TODO: THIS WILL ERROR I NEED THE ID HERE
    s = getsensorbyid(sensor)
    m = add_measurement(value, s.id, cycle, sensor)
    return m

def add_measurement(value, data_type, cycle, sensor):
    timestamp = datetime.datetime.now()
    measure = models.Measurement(timestamp=timestamp, value=value,
        data_type_id=data_type, cycle_id=cycle, sensor_id=sensor)
    db.session.flush()
    return measure.id

def add_cycle(site: int) -> int:
    start = datetime.datetime.now()
    cycle = models.Cycle(start_time=start, site_id=site)
    db.session.flush()
    return cycle.id

def add_site(name:str)- > int:
    site = models.Site(name)
    db.session.flush()
    return site.id

def add_sensor(name:str, address, data_type:int) -> int:
    sensor = Sensor(name=name, address=address, data_type_id=data_type)
    db.session.flush()
    return sensor.id

def add_data_type():
    d_type = models.Date_Type(name:str, unit:str)
    db.session.flush()
    return d_type.id


# Shouldn't need this if the id comes from the web ui
def get_id_by_name(name: str, type: str) -> int:
    if type == "sensor":
        result = db.session.query(models.Sensor).filter(
            models.Sensor.name == name).one_or_none()

    elif type == "site":
        result = db.session.query(models.Site).filter(
            models.Site.name == name).one_or_none()
        
    elif type == "data_type":
        result = db.session.query(models.Data_Type).filter(
            models.Data_Type.name == name).one_or_none()

    else:
        result = None


    if result is not None:
        return result
    
    elif type == "sensor":
        new_item = models.Sensor()

    elif type == "site":
        new_item = models.Site()
    
    elif type == "data_type":
        new_item = models.Data_Type()

    else:
        raise ValueError("Invalid Type")

    
    if new_item is not None:
        db.session.add(new_item)
        db.session.flush()
        return new_item
        