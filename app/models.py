import sqlalchemy.schema as schema
import sqlalchemy.types as types
import sqlalchemy.orm as orm

from datetime import datetime


# Reference Tables
sensor_measurements = schema.Table('sensor_measurements',
    schema.Column('measurement_name_id', types.Integer, schema.ForeignKey('measurementname.id')),
    schema.Column('sensor_id', types.Integer, schema.ForeignKey('sensor.id'))
)

class MeasurementName(types.Model):
    __tablename__ = "measurement_names"
    id = schema.Column(types.Integer, primary_key=True)
    name = schema.Column(types.Text, nullable=False)

class Location(types.Model):
    __tablename__ = "locations"
    id = schema.Column(types.Integer, primary_key=True)
    name = schema.Column(types.Text, nullable=False)

# Potential Tables:
#   - Protocols



# Data Tables
class Sensor(types.Model):
    __tablename__ = "sensors"
    id = schema.Column(types.Integer, primary_key=True)
    name = schema.Column(types.Text, nullable=False)
    protocol = schema.Column(types.Text, nullable=False)
    address = schema.Column(types.BLOB)
    command= schema.Column(types.BLOB)

    meaurement_names = orm.relationship("MeasurementName", secondary=sensor_measurements, 
        lazy="subquery", backref=orm.backref("measurement_names", lazy=True))

class Cycle(types.Model):
    __tablename__ = "cycles"
    id = schema.Column(types.Integer, primary_key=True)
    start_time = schema.Column(types.DateTime, nullable=False,
        default=datetime.utcnow)
    duration = schema.Column(types.Integer, nullable=False)
    frequency = schema.Column(types.Integer, nullable=False)
    
    site = schema.Column(types.Integer, schema.ForeignKey("site.id"), nullable=False)
    samples = orm.relationship("Sample", backref=orm.backref(
        "cycle"))

class Sample(types.Model):
    __tablename__ = "samples"
    id = schema.Column(types.Integer, primary_key=True)
    timestamp = schema.Column(types.DateTime, nullable=False,
        default=datetime.utcnow)
    value = schema.Column(types.Numeric, nullable=False)
    name = schema.Column(types.Text, nullable=False)

    sensor = schema.Column(schema.ForeignKey("sensor.id"))
    cycle = schema.Column(schema.ForeignKey("cycle.id"))