from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.ui.views import ui_routes
from app.database.views import db_routes

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

# TEST ROUTE
@app.route("/test/")
def test():
    #from app import data
    from flask import render_template
    #data.collect_data()
    return render_template("test.html")


# Load the config file
app.config.from_object('config.DevConfiguration')

# Open the DB Connection
db = SQLAlchemy(app)
