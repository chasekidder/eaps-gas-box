from app import db

from datetime import datetime

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    
    site_id = db.Column(db.Integer, db.ForeignKey("site.id"), nullable=False)
    measurements = db.relationship("Measurement", backref=db.backref(
        "cycle"))

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    value = db.Column(db.Numeric, nullable=False)
    name = db.Column(db.Text, nullable=False)

    sensor_id = db.Column(db.ForeignKey("sensor.id"))
    cycle_id = db.Column(db.ForeignKey("cycle.id"))