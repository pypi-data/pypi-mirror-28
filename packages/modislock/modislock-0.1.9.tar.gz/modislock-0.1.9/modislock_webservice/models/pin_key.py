# coding: utf-8
from ._base import db
from ._marsh import ma
from sqlalchemy.sql import func

"""
@startuml
!define table(x) class x << (T, #FFAAAA) >>
!define primary_key(x) <u>x</u>

table(PinKey){
    primary_key(key) INT
    enabled BOOLEAN
    created_on TIMESTAMP
    user_id INT
}
@enduml
"""


class PinKey(db.Model):
    """
    PinCode table holds the protocol PIN. Is used for pin codes and references the user they are assigned to.
    """
    __tablename__ = 'pin_key'

    key = db.Column(db.Integer, primary_key=True, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=1)
    created_on = db.Column(db.TIMESTAMP, default=func.now(), nullable=False)
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "PinKey(key={self.key}, enabled={self.enabled}, created_on={self.created_on}," \
               " user_id={self.user_id})".format(self=self)


class PinKeySchema(ma.Schema):
    class Meta:
        model = PinKey
        dateformat = '%Y-%m-%d %H:%M:%S'
        fields = ('key', 'enabled', 'created_on', 'user_id')


__all__ = ['PinKey', 'PinKeySchema']
