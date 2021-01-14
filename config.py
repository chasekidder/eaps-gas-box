from os.path import abspath, dirname, join

class BaseConfiguration():
    _cwd = dirname(abspath(__file__))
    DEBUG = False
    SECRET_KEY = "f62c0c78db951fcc952e6b534e82d35e16e95136c64f4f31"
    DATA_FOLDER = "/home/pi/eaps-gas-box/DATA/"
    DB_NAME = "appdata.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfiguration(BaseConfiguration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + BaseConfiguration.DB_NAME


class TestConfiguration(BaseConfiguration):
    DEBUG = True

class ProdConfigurateion(BaseConfiguration):
    pass