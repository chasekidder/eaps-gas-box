from flask import Blueprint

from flask import render_template
#from app.measurement.measure import celery

home_routes = Blueprint("home_routes", __name__)

@home_routes.route('/')
def index():
    return render_template("index.html")

@home_routes.route("/live/")
def live():
    return render_template("live.html")

