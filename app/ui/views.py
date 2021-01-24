from flask import Blueprint

from flask import render_template
from app.frontend import celery

ui_routes = Blueprint("ui_routes", __name__)

@ui_routes.route('/')
def index():
    return render_template("index.html")

@ui_routes.route("/live/")
def live():
    return render_template("live.html")

# TEST ROUTE
@ui_routes.route("/test/")
def test():
    from app.measurement import measure
    print("Starting cycle!")
    task = measure.start_cycle.delay()
    async_result = celery.AsyncResult(id=task.task_id, app=celery)
    async_result = async_result.get()

    return render_template("test.html")
