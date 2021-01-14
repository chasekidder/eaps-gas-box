from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import send_from_directory
from flask import jsonify
from flask import make_response

from app import frontend, utils
from app.ui.forms import DataCollectionForm

@frontend.route('/')
def index():
    return render_template("index.html")

@frontend.route("/config/", methods=["GET", "POST"])
def config():
    form = DataCollectionForm()

    if request.method == 'POST' and form.validate():
        freq = form.frequency
        filen = form.file_name
        #TODO: Send this to python measurement program
        
        flash("Success! Configuration sent to box.", "alert-success")
        return redirect("/")

    elif request.method == 'POST' and not form.validate():
        flash("Required Field Not Completed!", "alert-warning")

    return render_template("config.html", form=form)

@frontend.route("/data/")
def data():
    files = utils.get_files_in_dir(frontend.config["DATA_FOLDER"])
    return render_template("data.html", file_list=files)

@frontend.route("/download/<string:file_name>")
def download(file_name):
    return send_from_directory(frontend.config["DATA_FOLDER"], filename=file_name)

@frontend.route("/live/")
def live():
    return render_template("live.html")

@frontend.route("/api/")
def api():
    data = utils.get_live_data()
    return jsonify(data)

@frontend.route("/test/")
def test():
    from app import data
    data.collect_data()
    return render_template("test.html")