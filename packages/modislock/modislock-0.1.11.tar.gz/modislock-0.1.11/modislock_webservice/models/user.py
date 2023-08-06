# coding: utf-8

from ._base import db
from ._marsh import ma
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security.utils import hash_password, verify_password

"""
@startuml
!define table(x) class x << (T, #FFAAAA) >>
!define primary_key(x) <u>x</u>

table(User){
    primary_key(id) INT
    first_name VARCHAR(50)
    last_name VARCHAR(50)
    email VARCHAR(50)
    password VARCHAR(128)
    is_admin BOOLEAN
}
@enduml
"""


class User(db.Model):
    """
    User table defines login information but is also referenced in all available protocols
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Unicode(50), nullable=False)
    last_name = db.Column(db.Unicode(50), nullable=False)
    email = db.Column(db.Unicode(50), unique=True)
    password = db.Column(db.Unicode(128))
    is_admin = db.Column(db.Boolean, nullable=False, default=0)

    # Relationships
    rules = db.relationship('Rules', cascade='all, delete-orphan')
    pin_key = db.relationship('PinKey', cascade='all, delete-orphan')
    rfid_key = db.relationship('RfidKey', cascade='all, delete-orphan')
    event = db.relationship('Events', cascade='all, delete-orphan')
    otp_key = db.relationship('OtpKey', cascade='all, delete-orphan')
    u2f_key = db.relationship('U2fKey', cascade='all, delete-orphan')

    def __repr__(self):
        return "User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, " \
               "password={self.password}, email={self.email}, is_admin={self.is_admin})".format(self=self)

    # def __setattr__(self, name, value):
    #     # Hash password when set it.
    #     if name == 'password':
    #         # TODO if password has been hashed, leave alone
    #         value = hash_password(value)
    #     super(User, self).__setattr__(name, value)

    def check_password(self, password):
        return verify_password(password, self.password)
    #
    # def get_security_payload(self):
    #     return {
    #         'id': self.id,
    #         'first_name': self.first_name,
    #         'last_name': self.last_name,
    #         'email': self.email
    #     }

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    @hybrid_property
    def roles(self):
        """Added as per https://github.com/mattupstate/flask-security/issues/188
        Does not have a roles table or reference
        :return:
        """
        return []

    @roles.setter
    def roles(self, role):
        pass


class UserSchema(ma.Schema):
    class Meta:
        model = User
        dateformat = '%Y-%m-%d %H:%M:%S'
        fields = ('id', 'first_name', 'last_name', 'email', 'is_admin', 'created_on')

    # id = fields.Integer()
    # first_name = fields.String()
    # last_name = fields.String()
    # email = fields.Email()
    # is_admin = fields.Boolean()
    # created_on = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    # event = fields.Nested(EventsSchema, only=['event_type', 'event_time', 'event_location'], many=True)
    # pincode = fields.Nested(PincodeSchema, only=['code', 'enabled', 'created_on', 'updated_on'], many=True)
    # rfidcode = fields.Nested(RfidcodeSchema, only=['code', 'enabled', 'created_on', 'updated_on'], many=True)
    # otpcode = fields.Nested(OtpcodeSchema, only=['public_identity', 'enabled', 'created_on', 'updated_on'], many=True)
    # u2fcode = fields.Nested(U2fcodeSchema, many=True)


__all__ = ['User', 'UserSchema']
