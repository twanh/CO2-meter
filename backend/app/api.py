from flask import Blueprint, current_app, request
from flask import jsonify

from . import models

bp = Blueprint("api", __name__, url_prefix="/api/v1")


@bp.route("/sensors")
def get_all_sensors():
    res = current_app.session.query(models.Sensor).all()
    print(res)
    return jsonify({"sensors": [1, 2, 3]})


@bp.route("/sensors/add", methods=["POST"])  # type: ignore
def add_sensor():
    if request.method == "POST":
        data_uuid = request.form["uuid"]
        data_room_nr = request.form["room_number"]

        sensor = models.Sensor(uuid=data_uuid, room_number=data_room_nr)

        current_app.session.add(sensor)
        current_app.session.commit()
        return jsonify(sensor.toJSON())

    else:
        return "BAD REQUEST", 404
