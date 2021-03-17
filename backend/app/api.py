from flask import Blueprint, current_app, request
from flask import jsonify

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
    results = current_app.session.query(models.Sensor).filter(
        models.Sensor.uuid == uuid
    )

    if results.first() is None:
        return jsonify({"error": "not found", "sensor": {}}), 404 

    return jsonify({"sensor": results.first().toJSON(show_stats=True)})
