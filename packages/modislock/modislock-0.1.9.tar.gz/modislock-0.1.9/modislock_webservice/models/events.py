# coding: utf-8
from datetime import datetime
from ._base import db
from ._marsh import ma
from sqlalchemy.sql import func

"""
@startuml
    !define table(x) class x << (T, #FFAAAA) >>
    !define primary_key(x) <u>x</u>

    table(Events){
        primary_key(id_event) INT
        event_time TIMESTAMP
        event_type ENUM(USER_CREATED, ACCESS, DENIED)
        user_id INT FK
        reader_settings_id_reader INT FK
    }
@enduml
"""


class Events(db.Model):
    __tablename__ = 'events'

    id_event = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    # TIMESTAMP Format on MySQL 1970-01-01 00:00:01
    event_time = db.Column(db.TIMESTAMP, default=func.now(), nullable=False)
    event_type = db.Column(db.Enum('USER_CREATED', 'ACCESS', 'DENIED'), nullable=False)
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reader_settings_id_reader = db.Column(db.Integer, db.ForeignKey('reader_settings.id_reader'),
                                          default=0,
                                          nullable=False)
    reader_settings = db.relationship('ReaderSettings')
    # mysql_engine='InnoDB'

    def __repr__(self):
        return "Events(id_event={self.id_event}, event_time={self.event_time}, event_type={self.event_type}, " \
               "user_id={self.user_id}, reader_settings_id_reader={self.reader_settings_id_reader})".format(self=self)


class EventsSchema(ma.Schema):
    class Meta:
        model = Events
        dateformat = '%Y-%m-%d %H:%M:%S'
        fields = ('event_time', 'event_type', 'user_id', 'reader_settings_id_reader')


__all__ = ['Events', 'EventsSchema']
