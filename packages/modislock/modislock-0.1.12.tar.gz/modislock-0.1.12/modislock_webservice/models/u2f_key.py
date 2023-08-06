# coding: utf-8
from ._base import db
from ._marsh import ma
from sqlalchemy.sql import func


"""
@startuml
!define table(x) class x << (T, #FFAAAA) >>
!define primary_key(x) <u>x</u>

table(U2fKey){
    primary_key(key)
    handle VARCHAR(32)
    bind_data
    compromised
    counter
    transports
    enabled
    created_on
    certificate_idcertificate
    user_id
    certificate
}
@enduml
"""


class U2fKey(db.Model):
    __tablename__ = 'u2f_key'

    key = db.Column(db.Integer, primary_key=True, nullable=False)
    handle = db.Column(db.Unicode(128), nullable=False, unique=True)
    public_key = db.Column(db.Unicode(128), nullable=False)
    counter = db.Column(db.Integer, nullable=False)
    transports = db.Column(db.Enum('BT', 'BLE', 'NFC', 'USB'))
    enabled = db.Column(db.Boolean, nullable=False, default=1)
    created_on = db.Column(db.TIMESTAMP, default=func.now(), nullable=False)
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "U2fKey(key={self.key}, handle={self.handle}, public_key={self.public_key}, " \
               "counter={self.counter}, transports={self.transports}, enabled={self.enabled}, " \
               "created_on={self.created_on}, user_id={self.user_id})".format(self=self)


class U2fKeySchema(ma.Schema):
    class Meta:
        model = U2fKey
        dateformat = '%Y-%m-%d %H:%M:%S'
        fields = ('key', 'handle', 'counter', 'transports', 'enabled', 'created_on', 'user_id')


__all__ = ['U2fKey', 'U2fKeySchema']
