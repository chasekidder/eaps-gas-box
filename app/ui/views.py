from flask import Blueprint

from flask import render_template
from app.measurement.measure import celery

ui_routes = Blueprint("ui_routes", __name__)

@ui_routes.route('/')
def index():
    return render_template("index.html")

@ui_routes.route("/live/")
def live():
    return render_template("live.html")

