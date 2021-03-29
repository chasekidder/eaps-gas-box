from flask import Flask
from webui.ui.home_routes import home_routes
from webui.ui.measure_routes import measure_routes
#from app.database.views import db_routes
#from app.sensors.views import sensor_routes

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
app.register_blueprint(home_routes)
app.register_blueprint(measure_routes)
#app.register_blueprint(sensor_routes)


app.config.from_object('webui.config.DevConfiguration')

# Create database
#db = SQLAlchemy(app)

