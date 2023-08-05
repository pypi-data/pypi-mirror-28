# coding: utf-8
from ._base import db
from ._marsh import ma
from sqlalchemy.sql import func

"""
@startuml
!define table(x) class x << (T, #FFAAAA) >>
!define primary_key(x) <u>x</u>

table(RfidKey){
    primary_key(key) INT
    enabled BOOLEAN
    created_on TIMESTAMP
    user_id INT
}
@enduml
"""


class RfidKey(db.Model):
    """
   RFIDCode table holds the protocol for RFID tags. References back to user they are assigned to.
   """
    __tablename__ = 'rfid_key'

    key = db.Column(db.Unicode(16), primary_key=True, unique=True, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=1)
    created_on = db.Column(db.TIMESTAMP, default=func.now(), nullable=False)
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "RfidKey(key={self.key}, enabled={self.enabled}, created_on={self.created_on}," \
               " user_id={self.user_id})".format(self=self)


class RfidKeySchema(ma.Schema):
    class Meta:
        model = RfidKey
        dateformat = '%Y-%m-%d %H:%M:%S'
        fields = ('key', 'enabled', 'created_on', 'user_id')


__all__ = ['RfidKey', 'RfidKeySchema']
