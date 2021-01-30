from flask import Blueprint

from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import send_from_directory
from flask import jsonify

from app import utils
from app.ui.forms import CycleConfigForm
import app.measurement.measure

db_routes = Blueprint("db_routes", __name__)

@db_routes.route("/start/", methods=["GET", "POST"])
def start():
    form = CycleConfigForm()

    if request.method == 'POST' and form.validate():
        freq = form.frequency
        duration = form.duration
        site_id = form.site_id

        config = {
            "sample_frequency": form.frequency,
            "duration": form.duration,
            "sensor_metadata": {}
        }

        task = measure.start_cycle.delay(config)
        async_result = celery.AsyncResult(id=task.task_id, app=celery)
        
        flash("Success! Configuration sent to box. Measurements Starting...", "alert-success")
        return redirect("/live/")

    elif request.method == 'POST' and not form.validate():
        flash("Required Field Not Completed!", "alert-warning")

    return render_template("config.html", form=form)

@db_routes.route("/data/")
def data():
    files = utils.get_files_in_dir("/")
    return render_template("data.html", file_list=files)

@db_routes.route("/download/")
def download_root():
    return render_template("404.html"), 404

@db_routes.route("/download/<string:file_name>/")
def download(file_name):
    return send_from_directory("/", filename=file_name)

@db_routes.route("/api/")
def api():
    data = utils.get_live_data()
    return jsonify(data)