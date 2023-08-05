# coding: utf-8
"""
    @startuml

    !define table(x) class x << (T, #FFAAAA) >>
    !define primary_key(x) <u>x</u>

    table(settings) {
        primary_key(id_settings) INT
        settings_name VARCHAR(45)
        units VARCHAR(45)
        settings_group_id_group INT
    }

    table(settings_group) {
        primary_key(id_group) INT
        name ENUM('WEB', 'READERS', 'MONITOR', 'RULES')
    }

    table(settings_values) {
        primary_key(id_values) INT
        value VARCHAR(45)
        settings_id_settings INT
    }

    SettingsGroup "1" *-- "many" Settings
    Settings "1" *-- "many" SettingsValues

    @enduml
"""

from ._base import db
from flask_marshmallow import Schema
from marshmallow import fields


class Settings(db.Model):

    __tablename__ = 'settings'

    id_settings = db.Column(db.Integer, primary_key=True, autoincrement=True)
    settings_name = db.Column(db.Unicode(45), unique=True)
    units = db.Column(db.Unicode(45), nullable=False)
    # Foreign keys
    settings_group_name = db.Column(db.Enum('WEB', 'READERS', 'MONITOR', 'RULES'), nullable=False)

    def __repr__(self):
        return "Settings(id_settings={self.id_settings}, settings_name={self.settings_name}, " \
               "units={self.units})".format(self=self)


# class SettingsGroup(db.Model):
#     __tablename__ = 'settings_group'
#
#     name = db.Column(db.Enum('WEB', 'READERS', 'MONITOR', 'RULES'), primary_key=True)


class SettingsValues(db.Model):
    __tablename__ = 'settings_values'

    id_values = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    value = db.Column(db.Unicode(45), nullable=False)

    settings_id_settings = db.Column(db.Integer, db.ForeignKey('settings.id_settings'), nullable=False)

    def __repr__(self):
        return "SettingsValues(id_values={self.id_values}, value={self.value}, " \
               "settings_id_settings={self.settings_id_settings})".format(self=self)


class SettingsSchema(Schema):
    id_settings = fields.Integer()
    settings_name = fields.String()
