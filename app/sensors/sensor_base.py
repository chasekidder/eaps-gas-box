def try_io(call, tries=10):
        assert tries > 0
        error = None
        result = None

        while tries:
            try:
                result = call()
            except IOError as e:
                error = e
                tries -= 1
            else:
                break

        if not tries:
            raise error

        return result

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

    