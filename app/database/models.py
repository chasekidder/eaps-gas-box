from sqlalchemy import Column, String, Date, Integer, Numeric, BLOB, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from app.frontend import app
from flask_sqlalchemy import SQLAlchemy

# Open the DB Connection
db = SQLAlchemy(app)

class Measurement(db.Model):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    timestamp = Column("timestamp", Date, nullable=False)
    value = Column("value", Numeric, nullable=False)

    cycle_id = Column(Integer, ForeignKey("cycles.id"), nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    data_type_id = Column(Integer, ForeignKey("data_types.id"), nullable=False)

    cycle = relationship("Cycle", backref="measurement")
    sensor = relationship("Sensor", backref="measurement")
    data_type = relationship("Data_Type", backref="measurement")

    def __init__(self, timestamp, value, cycle, sensor, data_type):
        self.timestamp = timestamp
        self.value = value
        self.cycle = cycle
        self.sensor = sensor
        self.data_type = data_type


class Cycle(db.Model):
    __tablename__ = "cycles"
    id = Column(Integer, primary_key=True)
    start_time = Column("start_time", Date, nullable=False)
    end_time = Column("end_time", Date)

    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)

    site = relationship("Site", backref="cycle")

    def __init__(self, start_time, site, sensors):
        self.start_time = start_time
        self.site = site
        #self.sensors = sensors


sensor_datatype_association = Table("sensors_datatypes", db.Model.metadata,
    Column('sensor_id', Integer, ForeignKey('sensors.id')),
    Column('data_type_id', Integer, ForeignKey("data_types.id"))
    )


class Sensor(db.Model):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    address = Column("address", BLOB, nullable=False)

    # many to one
    protocol_id = Column(Integer, ForeignKey("protocols.id"), nullable=False)
    data_type_id = Column(Integer, ForeignKey("data_types.id"), nullable=False)
    command_id = Column(Integer, ForeignKey("commands.id"), nullable=False)

    protocol = relationship("Protocol", backref="sensor")

    data_types = relationship("Data_Type", 
        secondary=sensor_datatype_association, backref="sensors")

    command = relationship("Command", 
        #backref=backref("sensor", useList=False))
        backref="sensor")

    def __init__(self, name, address, protocol, commands, data_types):
        self.name = name
        self.address = address
        self.protocol = protocol

        self.command = commands
        self.data_types = data_types

    
class Protocol(db.Model):
    __tablename__ = "protocols"
    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=False)

    def __init__(self, name):
        self.name = name


class Command(db.Model):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True)
    read = Column("read", BLOB, nullable=False)
    write = Column("write", BLOB)
    calibrate = Column("calibrate", BLOB)

    def __init__(self, read, write, calibrate):
        self.read = read
        self.write = write
        self.calibrate = calibrate


class Data_Type(db.Model):
    __tablename__ = "data_types"
    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    unit = Column("unit", String, nullable=False)

    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class Site(db.Model):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=False)

    def __init__(self, name):
        self.name = name