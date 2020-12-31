from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import send_from_directory
from flask import jsonify
from flask import make_response

from . import app
from . import utils
from .forms import DataCollectionForm

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/config/", methods=["GET", "POST"])
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

@app.route("/data/")
def data():
    files = utils.get_files_in_dir(app.config["DATA_FOLDER"])
    return render_template("data.html", file_list=files)

@app.route("/download/<string:file_name>")
def download(file_name):
    return send_from_directory(app.config["DATA_FOLDER"], filename=file_name)

@app.route("/live/")
def live():
    return render_template("live.html")

@app.route("/api/")
def api():
    data = utils.get_live_data()
    return jsonify(data)

@app.route("/test/")
def test():
    from app import data
    data.collect_data()
    return "Success"