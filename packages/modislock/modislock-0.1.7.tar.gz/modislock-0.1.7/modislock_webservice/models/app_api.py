# coding: utf-8


from ._base import db


class AppApi(db.Model):

    __tablename__ = 'app_api'

    app_api_id = db.Column(db.Unicode(25), primary_key=True)
    app_secret = db.Column(db.Unicode(128), nullable=False)
    app_api_access = db.relationship('AppApiAccess', cascade='all, delete-orphan')

    def __repr__(self):
        return "AppApi(app_api_id={self.app_api_id}, app_secret={self.app_secret})".format(self=self)
