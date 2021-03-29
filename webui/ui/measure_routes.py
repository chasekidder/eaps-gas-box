from flask import Blueprint

from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import send_from_directory
from flask import jsonify

from webui import utils
from webui.ui.forms import CycleConfigForm
import measure

from measure import task_queue, measurement_cycle



measure_routes = Blueprint("measure_routes", __name__)

@measure_routes.route("/config/", methods=["GET", "POST"])
def config():
    form = CycleConfigForm()

    if request.method == 'POST' and form.validate():
        config = {
            "sample_frequency": form.frequency.data,
            "duration": form.duration.data,
        }


        #task = measurement_cycle.delay()
        #async_result = task_queue.AsyncResult(id=task.task_id, app=task_queue)
        measure.setup()
        i = 0
        while (i < 1):
            measure.loop()
            i = i + 1
        measure.clean_up()

        
        flash("Success! Configuration sent to box. Measurements Starting...", "alert-success")
        return redirect("/live/")

    elif request.method == 'POST' and not form.validate():
        flash("Required Field Not Completed!", "alert-warning")

    return render_template("config.html", form=form)

@measure_routes.route("/data/")
def data():
    files = utils.get_files_in_dir("/")
    return render_template("data.html", file_list=files)

@measure_routes.route("/download/")
def download_root():
    return render_template("404.html"), 404

@measure_routes.route("/download/<string:file_name>/")
def download(file_name):
    return send_from_directory("/", filename=file_name)

@measure_routes.route("/api/")
def api():
    data = utils.get_live_data()
    return jsonify(data)