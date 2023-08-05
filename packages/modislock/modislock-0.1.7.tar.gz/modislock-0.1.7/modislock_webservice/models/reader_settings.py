# coding: utf-8
from ._base import db
from sqlalchemy.sql import func

"""
@startuml
!define table(x) class x << (T, #FFAAAA) >>
!define primary_key(x) <u>x</u>

table(reader_settings){
    primary_key(id_reader) INT
    location_name VARCHAR(20)
    location_direction ENUM('NONE', 'EXIT', 'ENTER')
    associated_relay ENUM('RELAY1', 'RELAY2')
    settings_id_settings INT
}

table(reader_status){
    primary_key(id_status) INT
    status ENUM('DISCONNECTED', 'CONNECTED', 'ERROR')
    updated_on TIMESTAMP
    reader_id_reader INT
}
@enduml
"""


class ReaderSettings(db.Model):
    __tablename__ = 'reader_settings'

    id_reader = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.Unicode(20), nullable=False)
    location_direction = db.Column(db.Enum('NONE', 'EXIT', 'ENTRY'), nullable=False)
    settings_id_settings = db.Column(db.Integer, db.ForeignKey('settings.id_settings'), nullable=False)

    def __repr__(self):
        return 'ReaderSettings(id_reader={self.id_reader}, ' \
               'location_direction={self.location_direction},' \
               'settings_id_settings={self.settings_id_settings})'.format(self=self)


class ReaderStatus(db.Model):
    __tablename__ = 'reader_status'

    id_status = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('DISCONNECTED', 'CONNECTED', 'ERROR'), nullable=False)
    updated_on = db.Column(db.TIMESTAMP, default=func.now(), nullable=False)

    reader_id_reader = db.Column(db.Integer, db.ForeignKey('reader_settings.id_reader'), nullable=False)

    def __repr__(self):
        return "ReaderStatus(id_status={self.id_status}, status={self.status}, updated_on={self.updated_on}, " \
               "reader_id_reader={self.reader_id_reader})".format(self=self)


__all__ = ['ReaderSettings', 'ReaderStatus']
