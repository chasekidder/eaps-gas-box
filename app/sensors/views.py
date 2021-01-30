from flask import Blueprint

from flask import render_template
from flask import request
from flask import redirect
from flask import flash

from app import utils
from app.ui.forms import AddSensorForm
from app.database.database import add_sensor

sensor_routes = Blueprint("sensor_routes", __name__)

@sensor_routes.route("/sensor/")
def sensor_root():
    return render_template("404.html"), 404

@sensor_routes.route("/sensor/<int:file_name>/")
def sensor_view(sensor_id:int):
    pass

@sensor_routes.route("/sensor/add/", methods=["GET", "POST"])
def sensor_add():
    form = AddSensorForm()

    if request.method == 'POST' and form.validate():
        name = form.name
        address = form.address
        data_type = form.data_type_id
        add_sensor(name, address, data_type)
        
        flash("Success! Sensor Added!", "alert-success")
        return redirect("/")

    elif request.method == 'POST' and not form.validate():
        flash("Required Field Not Completed!", "alert-warning")

    return render_template("config.html", form=form)
