from flask import Blueprint, current_app, json, request
from flask import jsonify, url_for
from celery.result import AsyncResult

from . import models

bp = Blueprint("api", __name__, url_prefix="/api/v1")


@bp.route("/sensors")
def get_all_sensors():
    res: list[models.Sensor] = current_app.session.query(models.Sensor).all()
    return jsonify({"sensors": [sensor.toJSON() for sensor in res]})


@bp.route("/sensors/add", methods=["POST"])  # type: ignore
def add_sensor():
    if request.method == "POST":
        data_uuid = request.form["uuid"]
        data_room_nr = request.form["room_number"]

        sensor = models.Sensor(uuid=data_uuid, room_number=data_room_nr)
        current_app.session.add(sensor)
        current_app.session.commit()
        return jsonify(sensor.toJSON(show_stats=True))

    else:
        return "BAD REQUEST", 404


@bp.route("/sensors/<string:uuid>", methods=["GET"])
def get_sensor_info(uuid: str):

    # TODO:
    # - Allow for getting the results from a certain date range

    results = current_app.session.query(models.Sensor).filter(
        models.Sensor.uuid == uuid
    )

    if results.first() is None:
        return jsonify({"error": "not found", "sensor": {}}), 404

    return jsonify({"sensor": results.first().toJSON(show_stats=True)})


@bp.route("/sensors/<string:uuid>/update", methods=["GET"])
def update_sensor(uuid):
    # Imoprting here to prevent circular imports
    from .tasks import update_sensor

    # Check that the sensor exists
    results = current_app.session.query(models.Sensor).filter(
        models.Sensor.uuid == uuid
    )

    if results.first() is None:
        return jsonify({"error": "sensor not found"}), 404

    task = update_sensor.delay(uuid)

    return jsonify({
        "task_id": task.id,
        "result_url": url_for('api.get_result', id=task.id)
    })


@bp.route("/results/<string:id>")
def get_result(id: str):
    from .tasks import update_sensor

    res = update_sensor.AsyncResult(id)

    if res.state == "SUCCESS":
        return jsonify(
            {"task_id": id, "task_status": res.state, "task_result": res.get()}
        )
    else:
        return jsonify({"task_id": id, "task_status": res.state})
