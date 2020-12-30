from flask import Flask

# Initialize the app
frontend = Flask(__name__, 
            instance_relative_config=True,
            static_folder="static/",
            static_url_path=""
            )

# Load the views
from frontend import views

# Load the config file
frontend.config.from_object('config.DevConfiguration')
