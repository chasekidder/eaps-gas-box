from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__version__ = (1, 0, 0, "dev")

# Initialize the app
frontend = Flask(__name__, 
            instance_relative_config=True,
            static_folder="ui/static/",
            static_url_path="",
            template_folder="ui/templates/"
            )

# Load the views
from app.ui import views

# Load the config file
frontend.config.from_object('config.DevConfiguration')

# Open the DB Connection
db = SQLAlchemy(frontend)