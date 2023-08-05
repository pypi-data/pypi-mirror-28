# coding: utf-8
from datetime import datetime
from ._base import db


class AppApiAccess(db.Model):

    __tablename__ = 'app_api_access'

    token = db.Column(db.Unicode(128), primary_key=True)
    expires = db.Column(db.DateTime())
    app_api_app_api_id = db.Column(db.Unicode(25), db.ForeignKey('app_api.app_api_id'), nullable=False)

    def __repr__(self):
        return 'AppApiAccess(token={self.token}, expires={self.expires})'.format(self=self)
