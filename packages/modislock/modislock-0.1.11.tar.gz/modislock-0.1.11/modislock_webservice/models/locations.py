# coding: utf-8
from datetime import datetime
from ._base import db


class Locations(db.Model):
    __tablename__ = 'locations'

    id_locations = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(45), unique=True)

    def __repr__(self):
        return "Locations(id_locations={self.id_locations}, name={self.name})".format(self=self)
