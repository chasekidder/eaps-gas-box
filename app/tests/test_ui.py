import pytest

from app.ui.views import ui_routes
from app.database.views import db_routes

from flask import Flask

url_base = "http://localhost:8000"

@pytest.fixture(scope='module')
def test_client():
    # Initialize the app
    app = Flask(__name__, instance_relative_config=True, 
        template_folder="../ui/templates/", static_folder="../ui/static/")
    app.config.from_object('config.TestConfiguration')

    # Register routes
    app.register_blueprint(ui_routes)
    app.register_blueprint(db_routes)
    

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client  


class TestUIPages():
    def test_home_page(self, test_client):
        response = test_client.get("/")
        assert response.status_code == 200

    def test_config_page(self, test_client):
        response = test_client.get("/config/")
        assert response.status_code == 200

    def test_data_page(self, test_client):
        response = test_client.get("/data/")
        assert response.status_code == 200

    def test_download_page(self, test_client):
        response = test_client.get("/download/")
        assert response.status_code == 404
        #TODO: add a file link and test status code 200

    def test_live_page(self, test_client):
        response = test_client.get("/live/")
        assert response.status_code == 200

    def test_api_page(self, test_client):
        response = test_client.get("/api/")
        assert response.status_code == 200