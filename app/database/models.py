from sqlalchemy import Column, String, Date, Integer, Numeric, BLOB, ForeignKey, Table
from sqlalchemy.orm import relationship, backref


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


class Cycle(db.Model):
    __tablename__ = "cycles"
    id = Column(Integer, primary_key=True)
    start_time = Column("start_time", Date, nullable=False)
    end_time = Column("end_time", Date)

    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)

    site = relationship("Site", backref="cycle")


sensor_datatype_association = Table("sensors_datatypes", db.Model.metadata,
    Column('sensor_id', Integer, ForeignKey('sensors.id')),
    Column('data_type_id', Integer, ForeignKey("data_types.id"))
    )

class Sensor(db.Model):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    address = Column("address", BLOB, nullable=False)

    # This might not work! The data types are many-many so more than one id
    # many to one
    data_type_id = Column(Integer, ForeignKey("data_types.id"), nullable=False)

    data_types = relationship("Data_Type", 
        secondary=sensor_datatype_association, backref="sensors")


class Data_Type(db.Model):
    __tablename__ = "data_types"
    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    unit = Column("unit", String, nullable=False)


class Site(db.Model):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True)
    name = Column("name", String, nullable=False)