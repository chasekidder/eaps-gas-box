from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.ui.views import ui_routes
from app.database.views import db_routes
from app.sensors.views import sensor_routes

import sys

__version__ = (1, 0, 0, "dev")

# Initialize the app
app = Flask(__name__, 
            instance_relative_config=True,
            static_folder="ui/static/",
            static_url_path="",
            template_folder="ui/templates/"
            )

# Register routes
app.register_blueprint(ui_routes)
app.register_blueprint(db_routes)
app.register_blueprint(sensor_routes)


# Load the config file based on if we're testing
if "pytest" in sys.modules:
    app.config.from_object("config.TestConfiguration")
    app.template_folder = "../ui/templates/"
    app.static_folder = "../ui/static/"

else:
    app.config.from_object('config.DevConfiguration')

# Create database
db = SQLAlchemy(app)

