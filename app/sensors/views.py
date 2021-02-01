from flask import Blueprint

from flask import render_template
from flask import request
from flask import redirect
from flask import flash

from app import utils
from app.ui.forms import AddSensorForm
from app.measurement.measure import celery, start_cycle

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
        name = form.name.data
        address = form.address.data
        data_type = float(form.data_type_id.data)
        #add_sensor(name, address, data_type)
        
        flash("Success! Sensor Added!", "alert-success")
        return redirect("/")

    elif request.method == 'POST' and not form.validate():
        flash("Required Field Not Completed!", "alert-warning")

    return render_template("sensor-add.html", form=form)


@sensor_routes.route("/test/")
def test():
    config = {
            "sample_frequency": 1,
            "duration": 0.25,
            "sensor_metadata": {
                0: "MPL3115A2",
                1: "TEROS12",
                2: "AWM3300V",
                3: "ABPxxx",
                4: "LOX02F",
                5: "GMP251",
            }
        }

    task = start_cycle.delay(config)
    async_result = celery.AsyncResult(id=task.task_id, app=celery)
    return redirect("/live/")
