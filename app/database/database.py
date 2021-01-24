from app.database import models
from app.database.models import db

def add_measurement():
    measure = models.Measurement

def add_cycle():
    pass


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
        