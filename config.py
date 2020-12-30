from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))

class BaseConfiguration(object):
    DEBUG = False
    SECRET_KEY = "f62c0c78db951fcc952e6b534e82d35e16e95136c64f4f31"
    DATA_FOLDER = "/home/pi/eaps-gas-box/DATA/"

class DevConfiguration(BaseConfiguration):
    DEBUG = True

class TestConfiguration(BaseConfiguration):
    DEBUG = True

class ProdConfigurateion(BaseConfiguration):
    pass