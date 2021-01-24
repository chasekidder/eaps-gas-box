class Sensor():
    def __init__(self, id, type, protocol, address, measurements):
        self.ID = id
        self.TYPE = type
        self.PROTOCOL = protocol
        self.ADDRESS = address
        self.MEASUREMENTS = measurements
        

    def read_all(self):
        raise NotImplementedError

    def calibrate(self):
        raise NotImplementedError