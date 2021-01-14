from sqlalchemy import Column, String, Date, Integer, Numeric, BLOB, ForeignKey, Table
from sqlalchemy.orm import relationship

from app import db

class Measurement(db.Model):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    timestamp = Column("timestamp", Date)
    value = Column("value", Numeric)

    # many to one
    cycle = Column(Integer, ForeignKey("cycles.id"))
    sensor = Column(Integer, ForeignKey("sensors.id"))
    data_type = Column(Integer, ForeignKey("data_types.id"))

    def __init__(self, timestamp, value, cycle, sensor, data_type):
        self.timestamp = timestamp
        self.value = value
        #self.cycle = cycle
        #self.sensor = sensor
        #self.data_type = data_type


class Cycle(db.Model):
    __tablename__ = "cycles"
    id = Column(Integer, primary_key=True)
    start_time = Column("start_time", Date)
    end_time = Column("end_time", Date)

    # one to many
    measurements = relationship("Measurement", cascade="all, delete, delete-orphan")
    sensors = relationship("Sensor")
    
    # many to one
    site = Column(Integer, ForeignKey("sites.id"))

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
    name = Column("name", String)
    address = Column("address", BLOB)

    # many to one
    protocol = Column(Integer, ForeignKey("protocols.id"))
    
    # one to one
    #commands = relationship("Command", useList=False, back_populates="sensor")
    commands = relationship("Command", back_populates="sensor")

    # many to many
    data_types = relationship("Data_Type", secondary=sensor_datatype_association)

    def __init__(self, name, address, protocol, commands, data_types):
        self.name = name
        self.address = address
        self.protocol = protocol

        # maybe dont init these???
        self.commands = commands
        self.data_types = data_types

    
class Protocol(db.Model):
    __tablename__ = "protocols"
    id = Column(Integer, primary_key=True)
    name = Column("name", String)

    # one to many
    sensors = relationship("Sensor")

    def __init__(self, name):
        self.name = name


class Command(db.Model):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True)
    read = Column("read", BLOB)
    write = Column("write", BLOB)
    calibrate = Column("calibrate", BLOB)

    # one to one
    sensor = relationship("Sensor", back_populates="command")

    def __init__(self, read, write, calibrate):
        self.read = read
        self.write = write
        self.calibrate = calibrate


class Data_Type(db.Model):
    __tablename__ = "data_types"
    id = Column(Integer, primary_key=True)
    name = Column("name", String)
    unit = Column("unit", String)

    # one to many
    measurements = relationship("Measurement")

    # many to many
    sensors = relationship("Sensor")

    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class Site(db.Model):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True)
    name = Column("name", String)

    # one to many
    cycles = relationship("Cycle")

    def __init__(self, name):
        self.name = name