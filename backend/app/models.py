import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base


class Sensor(Base):

    __tablename__ = "Sensors"

    # Defaults
    id = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime, default=datetime.datetime.now)
    updated_add = Column(DateTime, default=datetime.datetime.now)
    # Room specific stuff
    uuid = Column(String(255), unique=True)
    room_number = Column(Integer, unique=True)
    # Statistics
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    air_quality = Column(Float, nullable=True)
    # Extra
    notes = Column(String, nullable=True)

    def toJSON(self):
        return {
            "id": self.id,
            "created_on": self.created_on,
            "updated_add": self.updated_add,
            "uuid": self.uuid,
            "room_number": self.room_number,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "air_quality": self.air_quality,
            "notes": self.notes,
        }
