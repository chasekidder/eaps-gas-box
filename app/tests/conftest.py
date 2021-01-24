import pytest

from app.ui.views import ui_routes
from app.database.views import db_routes

from app.frontend import app
from app.database.models import db


@pytest.fixture(scope='module')
def flask_instance():
    yield app


@pytest.fixture(scope='module')
def test_client(flask_instance):
    with flask_instance.test_client() as testing_client:
        with flask_instance.app_context():
            yield testing_client  


@pytest.fixture(scope='function')
def db_session():
    db.drop_all()
    db.create_all()
    yield db.session
    db.drop_all()
