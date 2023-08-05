# coding: utf-8
from datetime import datetime
from ._base import db


class Sensors(db.Model):
    __tablename__ = 'sensors'

    id_sensors = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(45), unique=True, nullable=False)
    units = db.Column(db.Unicode(45), nullable=False)
    locations_id_locations = db.Column(db.Integer, db.ForeignKey('locations.id_locations'), nullable=False)

    # Relationships
    readings = db.relationship('Readings', cascade='all, delete-orphan')

    def __repr__(self):
        return "Sensors(id_sensors={self.id_sensors}, name={self.name}, units={self.units}," \
               "locations_id_locations={self.locations_id_locations})".format(self=self)
