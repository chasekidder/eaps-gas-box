from . import models


from datetime import datetime

# Create reference values
site = models.Site("Site1")
data_type = models.Data_Type("CO2 Concentration", "ppm")


# Create some sensors
command = models.Command("r", "w", "c")
sensor = models.Sensor("Sensor1", 5, "SDI-12", command, data_type)

# Create a data cycle
cycle = models.Cycle(datetime.now(), site, sensor)
measure = models.Measurement(datetime.now(), 12, cycle, sensor, data_type)

db.session.add(measure)
db.session.commit()
db.session.close()
