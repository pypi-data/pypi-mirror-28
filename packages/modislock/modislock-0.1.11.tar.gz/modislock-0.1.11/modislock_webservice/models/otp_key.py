# coding: utf-8
from ._base import db
from ._marsh import ma
from sqlalchemy.sql import func

"""
@startuml
!define table(x) class x << (T, #FFAAAA) >>
!define primary_key(x) <u>x</u>

table(OtpKey){
    primary_key(key) VARCHAR(16)
    private_identity VARCHAR(16)
    aeskey VARCHAR(32)
    enabled BOOLEAN
    counter INT(11)
    time INT
    created_on TIMESTAMP
    remote_server BOOLEAN
    user_id INT
}
@enduml
"""


class OtpKey(db.Model):
    __tablename__ = 'otp_key'

    key = db.Column(db.Unicode(16), primary_key=True, nullable=False, index=True)
    private_identity = db.Column(db.Unicode(16), nullable=False)
    aeskey = db.Column(db.Unicode(32), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=1)
    counter = db.Column(db.Integer, nullable=False, default=1)
    time = db.Column(db.Integer, nullable=False, default=1)
    created_on = db.Column(db.TIMESTAMP, default=func.now(), nullable=False)
    remote_server = db.Column(db.Boolean, default=0)
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    otp_cloud_service = db.relationship('OtpCloudService', cascade='all, delete-orphan')

    def __repr__(self):
        return "OtpKey(key={self.key}, private_identity={self.private_identity}, " \
               "aeskey={self.aeskey}, enabled={self.enabled}, counter={self.counter}, " \
               "time={self.time}, remote_server={self.remote_server}, created_on={self.created_on}, " \
               "user_id={self.user_id})".format(self=self)


class OtpCloudService(db.Model):
    __tablename__ = 'otp_cloud_service'
    cloud_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    yubico_user_name = db.Column(db.Unicode(45), nullable=True)
    yubico_secret_key = db.Column(db.Unicode(45), nullable=True)
    # Foreign keys
    otp_key_key = db.Column(db.Unicode(16), db.ForeignKey('otp_key.key'), nullable=False)

    def __repr__(self):
        return "OtpCloudService(cloud_id={self.cloud_id}, yubico_user_name={self.yubico_user_name}, " \
               "yubico_secret_key={self.yublico_secret_key}, otp_key_key={self.otp_key_key})".format(self=self)


class OtpKeySchema(ma.Schema):
    class Meta:
        model = OtpKey
        dateformat = '%Y-%m-%d %H:%M:%S'
        fields = ('key', 'private_identity', 'aeskey', 'enabled', 'created_on', 'remote_server', 'user_id')


__all__ = ['OtpKey', 'OtpCloudService', 'OtpKeySchema']
