import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Sensor(Base):

    __tablename__ = "sensors"

    # Defaults
    id = Column(Integer, primary_key=True, index=True)
    created_add = Column(DateTime, default=datetime.datetime.now)
    updated_add = Column(DateTime, default=datetime.datetime.now)
    # Room specific stuff
    uuid = Column(String(255), unique=True)
    room_number = Column(Integer, unique=True)
    # Statistics
    temperatures = relationship("Temperature", backref="sensor")
    humidities = relationship("Humidity", backref="sensor")
    air_qualities = relationship("AirQuality", backref="sensor")

    # Extra
    notes = Column(String, nullable=True)

    def toJSON(self, show_stats=False):
        if not show_stats:
            return {
                "id": self.id,
                "created_add": self.created_add,
                "updated_add": self.updated_add,
                "uuid": self.uuid,
                "room_number": self.room_number,
                "notes": self.notes,
            }

        return {
            "id": self.id,
            "created_add": self.created_add,
            "updated_add": self.updated_add,
            "uuid": self.uuid,
            "room_number": self.room_number,
            "temperatures": [temp.toJSON() for temp in self.temperatures],
            "humidities": [hum.toJSON() for hum in self.humidities],
            "air_qualities": [aq.toJSON() for aq in self.air_qualities],
            "notes": self.notes,
        }

    def __str__(self):
        return f"Sensor with uuid: {self.uuid} in room#: {self.room_number}"


class Temperature(Base):

    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=True)
    created_add = Column(DateTime, default=datetime.datetime.now)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))

    def toJSON(self):
        return {
            "id": self.id,
            "value": self.value,
            "created_at": self.created_add,
            "sensor_id": self.sensor_id,
        }


class Humidity(Base):

    __tablename__ = "humidities"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=True)
    created_add = Column(DateTime, default=datetime.datetime.now)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))

    def toJSON(self):
        return {
            "id": self.id,
            "value": self.value,
            "created_at": self.created_add,
            "sensor_id": self.sensor_id,
        }


class AirQuality(Base):

    __tablename__ = "air_qualities"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=True)
    created_add = Column(DateTime, default=datetime.datetime.now)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))

    def toJSON(self):
        return {
            "id": self.id,
            "value": self.value,
            "created_at": self.created_add,
            "sensor_id": self.sensor_id,
        }
