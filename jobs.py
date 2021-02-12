import schedule
import json
import os

from sensor import Sensor


class UpdateRoomValues:

    def __init__(self, room_file: str, webdriver_path: str):

        self._room_file = room_file

        self._webdriver_path = webdriver_path
        self._rooms_data = []
        self._sensors = []

        self._parse_rooms_file()
        self._init_sensors()

    def start(self, interval: int):
        schedule.every(int(interval)).minutes.do(self._job)

    def _parse_rooms_file(self):
        if os.path.isfile(self._room_file):
            with open(self._room_file) as json_data:
                data = json.load(json_data)
                self._rooms_data = data['rooms']

    def _init_sensors(self, headless=True):
        for data in self._rooms_data:
            if 'uuid' in data and 'number' in data:
                sensor = Sensor(data['uuid'], self._webdriver_path, headless=headless, metadata={
                                "room_number": data['number']})
                self._sensors.append(sensor)

    def _job(self):
        print("Running job!")
        data = []
        for sensor in self._sensors:
            temp, hum, aq = sensor.update_now()
            data.append(
                {
                    'room_number': sensor.metadata['room_number'],
                    'uuid': sensor.uuid,
                    'temperature': temp,
                    'humidity': hum,
                    'air_quality': aq

                }
            )
            print(
                f"Room {sensor.metadata['room_number']}: temp: {temp}, humidity: {hum}, air quality: {aq}")
