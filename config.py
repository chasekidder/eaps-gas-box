import os

class BaseConfiguration():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    SECRET_KEY = "f62c0c78db951fcc952e6b534e82d35e16e95136c64f4f31"
    DATA_FOLDER = "/home/pi/eaps-gas-box/DATA/"
    DB_NAME = "appdata.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfiguration(BaseConfiguration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        BaseConfiguration.BASEDIR, BaseConfiguration.DB_NAME)

class TestConfiguration(BaseConfiguration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProdConfigurateion(BaseConfiguration):
    pass