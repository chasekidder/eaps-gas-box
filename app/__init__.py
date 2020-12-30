from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__version__ = (1, 0, 0, "dev")



# Initialize the app
app = Flask(__name__, 
            instance_relative_config=True,
            static_folder="static/",
            static_url_path=""
            )

# Load the views
from app import views

# Load the config file
app.config.from_object('config.DevConfiguration')

# Open the DB Connection
db = SQLAlchemy(app)
