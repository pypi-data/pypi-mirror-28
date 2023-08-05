# coding: utf-8
from ._base import db
from sqlalchemy.sql import func


class Readings(db.Model):
    __tablename__ = 'readings'

    id_readings = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, default=func.now())
    value = db.Column(db.Unicode(10), nullable=False)
    sensors_id_sensors = db.Column(db.Integer, db.ForeignKey('sensors.id_sensors'), nullable=False)

    def __repr__(self):
        return "Readings(id_readings={self.id_readings}, timestamp={self.timestamp}, value={self.value}," \
               "sensors_id_sensors={self.sensors_id_sensors})".format(self=self)
